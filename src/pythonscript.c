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

#include <godot/gdextension_interface.h>
#include "_pythonscript_api.h"

#ifdef _WIN32
# define DLL_EXPORT __declspec(dllexport)
# define DLL_IMPORT __declspec(dllimport)
#else
# define DLL_EXPORT
# define DLL_IMPORT
#endif

// Just like any Godot builtin classes, GDString's size is defined in `extension_api.json`
// and is platform-dependant (e.g. 4 bytes on float_32, 8 on double_64).
// So in theory we should retrieve the value from the json file, convert it into a C
// header file and include it here.
// However this is cumbersome and we only need this once before the Python interpreter
// is initialized (after that we can use the Python binding), so instead we stick with
// the biggest possible value and accept we will lose a couple of bytes on the stack ;)
#define GD_STRING_MAX_SIZE 8
#define GD_STRING_NAME_MAX_SIZE 8

// Nobody ain't no time to include stdbool.h !
#define bool unsigned int;
#define true 1
#define false 0

typedef enum {
    STALLED,  // Intitial state
    ENTRYPOINT_CALLED,  // pythonscript_init called
    ENTRYPOINT_RETURNED,  // pythonscript_init returns

    PYTHON_INTERPRETER_INIT,
    PYTHONSCRIPT_MODULE_INIT,
    PYTHONSCRIPT_INTERNAL_INIT,

    // All set !
    READY,

    // Teardown
    PYTHONSCRIPT_MODULE_TEARDOWN,
    PYTHON_INTERPRETER_TEARDOWN,

    CRASHED,  // Something went wrong :'(
} PythonscriptState;

static PythonscriptState state = STALLED;
static PyThreadState *gilstate = NULL;

// Global variables used by Cython modules to access the Godot API
DLL_EXPORT const GDExtensionInterface *pythonscript_gdextension = NULL;
DLL_EXPORT GDExtensionClassLibraryPtr pythonscript_gdextension_library = NULL;


// GDExtension interface uses GDStringName everywhere a name should be passed,
// however it is very cumbersome to create it !

static GDExtensionPtrConstructor gdstring_constructor = NULL;
static GDExtensionPtrDestructor gdstring_destructor = NULL;
static GDExtensionPtrConstructor gdstringname_from_gdstring_constructor = NULL;
static GDExtensionPtrDestructor gdstringname_destructor = NULL;

DLL_EXPORT void pythonscript_gdstringname_new(GDExtensionStringNamePtr ptr, const char *cstr) {
    // Method name must be passed as a StringName object... which itself has
    // to be built from a String object :(
    char as_gdstring[GD_STRING_MAX_SIZE];
    const GDExtensionConstTypePtr args[1] = {&as_gdstring};
    pythonscript_gdextension->string_new_with_utf8_chars(&as_gdstring, cstr);
    gdstringname_from_gdstring_constructor(ptr, args);
    gdstring_destructor(&as_gdstring);
}

DLL_EXPORT void pythonscript_gdstringname_delete(GDExtensionStringNamePtr ptr) {
    gdstringname_destructor(ptr);
}

#define GD_PRINT(msg) { \
    printf("%s\n", msg); \
}

#define GD_PRINT_ERROR(msg) { \
    pythonscript_gdextension->print_error(msg, __func__, __FILE__, __LINE__, false); \
}

#define GD_PRINT_WARNING(msg) { \
    pythonscript_gdextension->print_warning(msg, __func__, __FILE__, __LINE__, false); \
}

static void _late_initialize() {
    if (state == PYTHONSCRIPT_INTERNAL_INIT) {
        _pythonscript_late_init();
        state = READY;
    }
}

static void _early_initialize() {
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
        char method_name_as_gdstringname[GD_STRING_NAME_MAX_SIZE];
        pythonscript_gdstringname_new(&method_name_as_gdstringname, "get_base_dir");
        GDExtensionPtrBuiltInMethod gdstring_get_base_dir = pythonscript_gdextension->variant_get_ptr_builtin_method(
            GDEXTENSION_VARIANT_TYPE_STRING,
            &method_name_as_gdstringname,
            3942272618
        );
        pythonscript_gdstringname_delete(&method_name_as_gdstringname);
        if (gdstring_get_base_dir == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `String.get_base_dir` method)");
            goto error;
        }

        // 1) Retrieve library path
        char gd_library_path[GD_STRING_MAX_SIZE];
        gdstring_constructor(gd_library_path, NULL);
        pythonscript_gdextension->get_library_path(pythonscript_gdextension_library, gd_library_path);

        // 2) Retrieve base dir from library path
        char gd_basedir_path[GD_STRING_MAX_SIZE];
        gdstring_constructor(gd_basedir_path, NULL);
        gdstring_get_base_dir(gd_library_path, NULL, gd_basedir_path, 0);
        gdstring_destructor(gd_library_path);

        // 3) Convert base dir into regular c string
        GDExtensionInt basedir_path_size = pythonscript_gdextension->string_to_utf8_chars(gd_basedir_path, NULL, 0);
        // Why not using variable length array here ? Glad you asked Timmy !
        // VLA are part of the C99 standard, but MSVC compiler is missing it :(
        // Because VLA were removed from the C11 standard, and the standards committee
        // decided it was no good, probably because you can't handle allocation errors
        // like we're about to do two lines down.
        char *basedir_path = pythonscript_gdextension->mem_alloc(basedir_path_size + 1);
        if (basedir_path == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (memory allocation failed)");
            goto error;
        }
        pythonscript_gdextension->string_to_utf8_chars(gd_basedir_path, basedir_path, basedir_path_size);
        basedir_path[basedir_path_size] = '\0';
        gdstring_destructor(gd_basedir_path);

        // 4) Configure pythonhome with base dir
        status = PyConfig_SetBytesString(
            &config,
            &config.home,
            basedir_path
        );
        pythonscript_gdextension->mem_free(basedir_path);
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

    int ret = import__pythonscript();
    if (ret != 0) {
        GD_PRINT_ERROR("Pythonscript: Cannot load Python module `_pythonscript`");
        goto error;
    }

    state = PYTHONSCRIPT_INTERNAL_INIT;

    _pythonscript_early_init();

    PyConfig_Clear(&config);

    // Release the Kraken... er I mean the GIL !
    gilstate = PyEval_SaveThread();

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

static void _deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (p_level != GDEXTENSION_INITIALIZATION_SERVERS) {
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

static void _initialize(void *userdata, GDExtensionInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter

    // Language registration must be done at `GDEXTENSION_INITIALIZATION_SERVERS`
    // level which is too early to have have everything we need for (e.g. `OS` singleton).
    // So we have to do another init step at `GDEXTENSION_INITIALIZATION_SCENE` level.
    if (p_level == GDEXTENSION_INITIALIZATION_SERVERS) {
        _early_initialize();
    } else if (p_level == GDEXTENSION_INITIALIZATION_SCENE) {
        _late_initialize();
    }
}

DLL_EXPORT GDExtensionBool pythonscript_init(
    const GDExtensionInterface *p_interface,
    const GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
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
    // `pythonscript_gdextension` must be set as early as possible given it is never null-pointer
    // checked, especially in the Cython modules
    pythonscript_gdextension = p_interface;
    pythonscript_gdextension_library = p_library;

    // Load GDString/GDStringName contructor/destructor needed for pythonscript_gdstringname_new/delete helpers
    gdstring_constructor = pythonscript_gdextension->variant_get_ptr_constructor(GDEXTENSION_VARIANT_TYPE_STRING, 0);
    if (gdstring_constructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `String` constructor)");
        goto error;
    }
    gdstring_destructor = pythonscript_gdextension->variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING);
    if (gdstring_destructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `String` destructor)");
        goto error;
    }
    gdstringname_from_gdstring_constructor = pythonscript_gdextension->variant_get_ptr_constructor(GDEXTENSION_VARIANT_TYPE_STRING_NAME, 2);
    if (gdstringname_from_gdstring_constructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `StringName` constructor)");
        goto error;
    }
    gdstringname_destructor = pythonscript_gdextension->variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING_NAME);
    if (gdstringname_destructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `StringName` destructor)");
        goto error;
    }

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

    r_initialization->minimum_initialization_level  = GDEXTENSION_INITIALIZATION_SERVERS;
	r_initialization->userdata = NULL;
    r_initialization->initialize = _initialize;
    r_initialization->deinitialize = _deinitialize;

    state = ENTRYPOINT_RETURNED;
    return true;

error:
    state = CRASHED;
    return false;
}
