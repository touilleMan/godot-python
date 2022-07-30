/*
 * This file gets compiled as a shared library that act as the entry point
 * to the pythonscript plugin.
 * It should be loaded by Godot's GDExtension system (see the
 * `pythonscript.gdextension` file in the example/test projects).
 * As part of the loading, Godot will call the `pythonscript_init` function
 * very early, which will in turn register an initialization callback to be
 * called at the right time during Godot init. Once called, this callback
 * will initialize CPython interpreter then register Python as a new language
 * for Godot.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <godot/gdnative_interface.h>
#include "_pythonscript_api.h"

#ifdef _WIN32
# define DLL_EXPORT __declspec(dllexport)
# define DLL_IMPORT __declspec(dllimport)
#else
# define DLL_EXPORT
# define DLL_IMPORT
#endif

// TODO: Should be defined according to extension_api.json & target platform
#define GD_STRING_SIZE 8

// Nobody ain't no time to include stdbool.h !
#define true 1
#define false 0

typedef enum {
    STALLED,  // Intitial state
    ENTRYPOINT_CALLED,  // pythonscript_init called
    ENTRYPOINT_RETURNED,  // pythonscript_init returns
    PYTHON_INTERPRETER_INIT,
    PYTHONSCRIPT_MODULE_INIT,

    READY,

    PYTHONSCRIPT_MODULE_TEARDOWN,
    PYTHON_INTERPRETER_TEARDOWN,

    CRASHED,  // Something went wrong :'(
} PythonscriptState;

static PythonscriptState state = STALLED;
static PyThreadState *gilstate = NULL;
static GDNativeExtensionClassLibraryPtr gdextension = NULL;
static const GDNativeInterface *gdapi;


#define GD_PRINT(msg) { \
    printf("%s\n", msg); \
}

#define GD_PRINT_ERROR(msg) { \
    gdapi->print_error(msg, __func__, __FILE__, __LINE__); \
}

#define GD_PRINT_WARNING(msg) { \
    gdapi->print_warning(msg, __func__, __FILE__, __LINE__); \
}

static void _initialize(void *userdata, GDNativeInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (p_level != GDNATIVE_INITIALIZATION_CORE) {
        return;
    }

    if (state != ENTRYPOINT_RETURNED) {
        printf("Pythonscript: Invalid internal state (this should never happen !)\n");
        goto error;
    }

    // Initialize CPython interpreter
    state = PYTHON_INTERPRETER_INIT;

    PyStatus status;
    PyConfig config;
    PyConfig_InitIsolatedConfig(&config);
    config.configure_c_stdio = 1;

    // Set PYTHONHOME from .so path
    {
        // 0) Retrieve Godot methods
        GDNativePtrConstructor gdstring_constructor = gdapi->variant_get_ptr_constructor(GDNATIVE_VARIANT_TYPE_STRING, 0);
        if (gdstring_constructor == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retreive `String` constructor)");
            goto error;
        }
        GDNativePtrDestructor gdstring_destructor = gdapi->variant_get_ptr_destructor(GDNATIVE_VARIANT_TYPE_STRING);
        if (gdstring_destructor == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retreive `String` destructor)");
            goto error;
        }
        GDNativePtrBuiltInMethod gdstring_get_base_dir = gdapi->variant_get_ptr_builtin_method(GDNATIVE_VARIANT_TYPE_STRING, "get_base_dir", 3942272618);
        if (gdstring_get_base_dir == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retreive `String.get_base_dir` method)");
            goto error;
        }

        // 1) Retrieve library path
        char gd_library_path[GD_STRING_SIZE];
        gdstring_constructor(gd_library_path, NULL);
        gdapi->get_library_path(gdextension, gd_library_path);

        // 2) Retrieve base dir from library path
        char gd_basedir_path[GD_STRING_SIZE];
        gdstring_constructor(gd_basedir_path, NULL);
        gdstring_get_base_dir(gd_library_path, NULL, gd_basedir_path, 0);
        gdstring_destructor(gd_library_path);

        // 3) Convert base dir into regular c string
        GDNativeInt basedir_path_size = gdapi->string_to_utf8_chars(gd_basedir_path, NULL, 0);
        // Why not using variable length array here ? Glad you asked Timmy !
        // VLA are part of the C99 standard, but MSVC compiler is missing it :(
        // Because VLA were removed from the C11 standard, and the standards committee
        // decided it was no good, probably because you can't handle allocation errors
        // like we're about to do two lines down.
        char *basedir_path = gdapi->mem_alloc(basedir_path_size + 1);
        if (basedir_path == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (memory allocation failed)");
            goto error;
        }
        gdapi->string_to_utf8_chars(gd_basedir_path, basedir_path, basedir_path_size);
        basedir_path[basedir_path_size] = '\0';
        gdstring_destructor(gd_basedir_path);

        // 4) Configure pythonhome with base dir
        status = PyConfig_SetBytesString(
            &config,
            &config.home,
            basedir_path
        );
        gdapi->mem_free(basedir_path);
        if (PyStatus_Exception(status)) {
            GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
            GD_PRINT_ERROR(status.err_msg);
            goto error;
        }
    }

    // Set program name
    {
        status = PyConfig_SetBytesString(
            &config,
            &config.program_name,
            // TODO: retrieve real argv[0]
            "godot"
        );
        if (PyStatus_Exception(status)) {
            GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
            GD_PRINT_ERROR(status.err_msg);
            goto error;
        }
    }

    // argv and sys.path are going to be set by `_pythonscript_initialize`
    // This is much simpler this way given we will have acces to Godot API
    // through the nice Python bindings this way

    /* Read all configuration at once */
    status = PyConfig_Read(&config);
    if (PyStatus_Exception(status)) {
        GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
        GD_PRINT_ERROR(status.err_msg);
        goto error;
    }

    // TODO
    // Update sys.path with projet config
    // status = PyWideStringList_Append(&config.module_search_paths,
    //                                  L"/path/to/more/modules");
    // if (PyStatus_Exception(status)) {
    //     GD_PRINT_ERROR("Pythonscript: Cannot update sys.path");
    //     goto error;
    // }

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
        GD_PRINT_ERROR(status.err_msg);
        goto error;
    }

//     // TODO: site.USER_SITE seems to point to an invalid location in ~/.local
//     // Add current dir to PYTHONPATH
//     wchar_t *path = Py_GetPath();
//     int new_path_len = wcslen(path) + 3;
//     wchar_t new_path[new_path_len * sizeof(wchar_t)];
//     wcsncpy(new_path, L".:", new_path_len);
//     wcsncpy(new_path + 2, path, new_path_len - 2);
//     Py_SetPath(new_path);
#if 0
    // Useful for debugging if `import__pythonscript` returns an error
    PyRun_SimpleString("import sys\nprint('PYTHON_PATH:', sys.path)\n");
#endif

    state = PYTHONSCRIPT_MODULE_INIT;

    // TODO: Dunno why, but print from Python code doesn't do anything (Godot patching stdout ?)
    int ret = import__pythonscript();
    if (ret != 0){
        GD_PRINT_ERROR("Pythonscript: Cannot load Python module `_pythonscript`");
        goto error;
    }
    _pythonscript_set_gdapi(gdapi);  // Must be right after `import__pythonscript`
    _pythonscript_initialize();

    state = READY;

    // Release the Kraken... er I mean the GIL !
    gilstate = PyEval_SaveThread();

    PyConfig_Clear(&config);
    return;

error:

    if (state > PYTHONSCRIPT_MODULE_INIT && state < PYTHONSCRIPT_MODULE_TEARDOWN) {
        _pythonscript_deinitialize();
    }

    if (state > PYTHON_INTERPRETER_INIT && state < PYTHON_INTERPRETER_TEARDOWN) {
        PyConfig_Clear(&config);
        int ret = Py_FinalizeEx();
        if (ret != 0) {
            GD_PRINT_ERROR("Pythonscript: Cannot finalize Python interpreter");
        }
    }

    state = CRASHED;
}

static void _deinitialize(void *userdata, GDNativeInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (p_level != GDNATIVE_INITIALIZATION_CORE) {
        return;
    }

    if (state > PYTHON_INTERPRETER_INIT && state < PYTHON_INTERPRETER_TEARDOWN) {

        // Re-acquire the gil in order to finalize properly
        PyEval_RestoreThread(gilstate);

        if (state > PYTHONSCRIPT_MODULE_INIT && state < PYTHONSCRIPT_MODULE_TEARDOWN) {
            _pythonscript_deinitialize();
        }

        int ret = Py_FinalizeEx();
        if (ret != 0) {
            GD_PRINT_ERROR("Pythonscript: Cannot finalize Python interpreter");
            state = CRASHED;
            return;
        }
    }

    state = STALLED;
}

DLL_EXPORT GDNativeBool pythonscript_init(
    const GDNativeInterface *p_interface,
    const GDNativeExtensionClassLibraryPtr p_library,
    GDNativeInitialization *r_initialization
) {
    printf("I am ALIIIIIVE!\n");
    if (state != STALLED) {
        printf("Pythonscript: Invalid internal state (this should never happen !)\n");
        goto error;
    }
    state = ENTRYPOINT_CALLED;

    (void) p_library;  // acknowledge unreferenced parameter
    if (p_interface == NULL || r_initialization == NULL) {
        printf("Pythonscript: Invalid init parameters provided by Godot (this should never happen !)\n");
        goto error;
    }
    gdapi = p_interface;
    gdextension = p_library;

    // Check compatibility between the Godot version that has been used for building
    // (i.e. the bindings has been generated against) and the version currently executed.
    if (p_interface->version_major != GODOT_VERSION_MAJOR) {
        // Don't use GD_PRINT_ERROR here given we don't even know if it is available !
        printf(
            "Pythonscript: Incompatible Godot version (expected ~%d.%d, got %d.%d.%d)\n",
            GODOT_VERSION_MAJOR,
            GODOT_VERSION_MINOR,
            p_interface->version_major,
            p_interface->version_minor,
            p_interface->version_patch
        );
        goto error;
    }
    if (p_interface->version_minor != GODOT_VERSION_MINOR) {
        char buff[256];
        snprintf(
            buff,
            sizeof(buff),
            "Pythonscript: extension is built for Godot ~%d.%d, but your are running %d.%d.%d. This may cause issues !\n",
            GODOT_VERSION_MAJOR,
            GODOT_VERSION_MINOR,
            p_interface->version_major,
            p_interface->version_minor,
            p_interface->version_patch
        );
        GD_PRINT_WARNING(buff);
    }

    // TODO: Or is it GDNATIVE_INITIALIZATION_SERVERS ?
    r_initialization->minimum_initialization_level  = GDNATIVE_INITIALIZATION_CORE;
	r_initialization->userdata = NULL;
    r_initialization->initialize = _initialize;
    r_initialization->deinitialize = _deinitialize;

    state = ENTRYPOINT_RETURNED;
    return true;

error:
    state = CRASHED;
    return false;
}
