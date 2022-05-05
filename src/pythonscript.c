/*
 * This file gets compiled as a shared library that act as the entry point
 * to the pythonscript plugin.
 * It should be loaded by Godot's GDNative system (see the `pythonscript.gdextension`
 * file in the example/test projects).
 * As part of the loading, Godot will call the `pythonscript_init`
 * function which will in turn initialize the CPython interpreter then register
 * Python as a new language using Godot's Pluginscript system.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "_pythonscript_api.h"
#include <godot/gdnative_interface.h>

#ifdef __GNUC__
# define GDN_EXPORT __attribute__((visibility("default")))
#elif defined(_WIN32)
# define GDN_EXPORT __declspec(dllexport)
#else
# define GDN_EXPORT
#endif

// TODO: Should be defined according to extension_api.json & target platform
#define GD_STRING_SIZE 8

// Nobody ain't no time to include stdbool.h !
#define true 1
#define false 0

static int python_initialized = false;
static PyThreadState *gilstate = NULL;
static const GDNativeInterface *gdapi = NULL;
static GDNativeExtensionClassLibraryPtr gdextension = NULL;

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

    // Initialize CPython interpreter

    PyStatus status;

    PyConfig config;
    PyConfig_InitIsolatedConfig(&config);
    python_initialized = true;

    // Set PYTHONHOME from .so path
    {
        // 0) Retreive Godot methods
        GDNativePtrDestructor gdstring_destructor = gdapi->variant_get_ptr_destructor(GDNATIVE_VARIANT_TYPE_STRING);
        if (gdstring_destructor == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retreive `String` destructor)");
            goto error;
        }
        GDNativePtrBuiltInMethod gdstring_get_base_dir = gdapi->variant_get_ptr_builtin_method(GDNATIVE_VARIANT_TYPE_STRING, "get_base_dir", 171192875);
        if (gdstring_get_base_dir == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retreive `String.get_base_dir` method)");
            goto error;
        }

        // 1) Retrieve library path
        char gd_library_path[GD_STRING_SIZE];
        gdapi->get_library_path(gdextension, gd_library_path);

        GDNativeInt library_path_size = gdapi->string_to_utf8_chars(gd_library_path, NULL, 0);
        char library_path[library_path_size + 1];
        gdapi->string_to_utf8_chars(gd_library_path, library_path, library_path_size);
        library_path[library_path_size] = '\0';

        // 2) Retrieve base dir from library path
        char gd_basedir_path[GD_STRING_SIZE];
        gdstring_get_base_dir(gd_library_path, NULL, gd_basedir_path, 0);

        // 3) Convert base dir into regular c string
        GDNativeInt basedir_path_size = gdapi->string_to_utf8_chars(gd_basedir_path, NULL, 0);
        char basedir_path[basedir_path_size + 1];
        gdapi->string_to_utf8_chars(gd_basedir_path, basedir_path, basedir_path_size);
        basedir_path[basedir_path_size] = '\0';

        // 3) Cleanup temporary gdstrings
        gdstring_destructor(gd_basedir_path);
        gdstring_destructor(gd_library_path);

        // 4) Configure pythonhome with base dir
        status = PyConfig_SetBytesString(
            &config,
            &config.home,
            basedir_path
        );
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
            // TODO: retreive real argv[0]
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

    int ret = import__pythonscript();
    if (ret != 0){
        GD_PRINT_ERROR("Pythonscript: Cannot load Python module `_pythonscript`");
        goto error;
    }
    _pythonscript_initialize();

    // Release the Kraken... er I mean the GIL !
    gilstate = PyEval_SaveThread();

    PyConfig_Clear(&config);
    return;

error:
    if (python_initialized) {
        PyConfig_Clear(&config);
        int ret = Py_FinalizeEx();
        python_initialized = false;
    }
}

static void _deinitialize(void *userdata, GDNativeInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (p_level != GDNATIVE_INITIALIZATION_CORE) {
        return;
    }

    if (!python_initialized) {
        return;
    }

    // Re-acquire the gil in order to finalize properly
    PyEval_RestoreThread(gilstate);

    _pythonscript_deinitialize();

    int ret = Py_FinalizeEx();
    if (ret != 0) {
        GD_PRINT_ERROR("Pythonscript: Cannot finalize Python interpreter");
    }
    python_initialized = false;
}

GDNativeBool GDN_EXPORT pythonscript_init(
    const GDNativeInterface *p_interface,
    const GDNativeExtensionClassLibraryPtr p_library,
    GDNativeInitialization *r_initialization
) {
    (void) p_library;  // acknowledge unreferenced parameter
    if (p_interface == NULL || r_initialization == NULL) {
        printf("Pythonscript: Invalid init parameters provided by Godot (this should never happen !)\n");
        return false;
    }
    gdapi = p_interface;
    gdextension = p_library;

    // Check compatibility between the Godot version that has been used for building
    // (i.e. the bindings has been generated against) and the version currently executed.
    if (p_interface->version_major != GODOT_VERSION_MAJOR) {
        printf(
            "Pythonscript: Incompatible Godot version (expected ~%d.%d, got %d.%d.%d)\n",
            GODOT_VERSION_MAJOR,
            GODOT_VERSION_MINOR,
            p_interface->version_major,
            p_interface->version_minor,
            p_interface->version_patch
        );
        return false;
    }
    if (p_interface->version_minor != GODOT_VERSION_MINOR) {
        printf(
            "Pythonscript: extension is built for Godot ~%d.%d, but your are running %d.%d.%d. This may cause issues !\n",
            GODOT_VERSION_MAJOR,
            GODOT_VERSION_MINOR,
            p_interface->version_major,
            p_interface->version_minor,
            p_interface->version_patch
        );
        return false;
    }

    // TODO: Or is it GDNATIVE_INITIALIZATION_SERVERS ?
    r_initialization->minimum_initialization_level  = GDNATIVE_INITIALIZATION_CORE;
	r_initialization->userdata = NULL;
    r_initialization->initialize = _initialize;
    r_initialization->deinitialize = _deinitialize;

    return true;
}
