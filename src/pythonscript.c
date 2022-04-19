/*
 * This file gets compiled as a shared library that act as the entry point
 * to the pythonscript plugin.
 * It should be loaded by Godot's GDNative system (see the `pythonscript.gdextension`
 * file in the example/test projects).
 * As part of the loading, Godot will call the `pythonscript_init`
 * function which will in turn initialize the CPython interpreter then register
 * Python as a new language using Godot's Pluginscript system.
 */

#include "_pythonscript_api.h"
#include <godot/gdnative_interface.h>
#include <python.h>

// #define PY_SSIZE_T_CLEAN
// #ifdef _DEBUG
//   // On Windows with _DEBUG defined, python.h (pyconfig.h actually) specify it
//   // should be linked with python39_d.lib, however the we only have python39.lib
//   #undef _DEBUG
//   #include <python.h>
//   // Also include python.h
//   #include "_pythonscript_api.h"
//   #define _DEBUG
// #else
//   #include <python.h>
// #endif

#ifdef __GNUC__
# define GDN_EXPORT __attribute__((visibility("default")))
#elif defined(_WIN32)
# define GDN_EXPORT __declspec(dllexport)
#else
# define GDN_EXPORT
#endif

// Nobody ain't no time to include stdbool.h !
#define true 1
#define false 0

static PyThreadState *gilstate = NULL;
static const GDNativeInterface *gdapi = NULL;

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

    // TODO
    // // Retrieve path and set pythonhome
    // {
    //     static wchar_t pythonhome[300];
    //     godot_string _pythonhome = pythonscript_gdapi10->godot_string_get_base_dir(
    //         options->active_library_path
    //     );
    //     wcsncpy(pythonhome, pythonscript_gdapi10->godot_string_wide_str(&_pythonhome), 300);
    //     pythonscript_gdapi10->godot_string_destroy(&_pythonhome);
    //     Py_SetPythonHome(pythonhome);
    // }

    // TODO: site.USER_SITE seems to point to an invalid location in ~/.local
    // // Add current dir to PYTHONPATH
    // wchar_t *path = Py_GetPath();
    // int new_path_len = wcslen(path) + 3;
    // wchar_t new_path[new_path_len * sizeof(wchar_t)];
    // wcsncpy(new_path, L".:", new_path_len);
    // wcsncpy(new_path + 2, path, new_path_len - 2);
    // Py_SetPath(new_path);
    // PyRun_SimpleString("import sys\nprint('PYTHON_PATH:', sys.path)\n");

    // TODO: retreive real argv[0]
    Py_SetProgramName(L"godot");
    // Initialize interpreter but skip initialization registration of signal handlers
    Py_InitializeEx(0);


    int ret = import__pythonscript();
    if (ret != 0){
        GD_PRINT_ERROR("Pythonscript: Cannot load Python module `_pythonscript`");
        return;
    }
    _pythonscript_initialize();

    // Release the Kraken... er I mean the GIL !
    gilstate = PyEval_SaveThread();
}

static void _deinitialize(void *userdata, GDNativeInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    printf("=============== _deinitialize %d\n", p_level);
    if (p_level != GDNATIVE_INITIALIZATION_CORE) {
        printf("=============== _deinitialize skipped %d\n", p_level);
        return;
    }
    // Re-acquire the gil in order to finalize properly
    PyEval_RestoreThread(gilstate);

    _pythonscript_deinitialize();

    int ret = Py_FinalizeEx();
    if (ret != 0) {
        GD_PRINT_ERROR("Pythonscript: Cannot finalize Python interpreter");
    }
    printf("=============== _deinitialize done %d\n", p_level);
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
