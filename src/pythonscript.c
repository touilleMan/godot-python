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

    PYTHON_INTERPRETER_READY,

    CRASHED,  // Something went wrong :'(
} PythonscriptState;

static PythonscriptState state = STALLED;
static PyThreadState *gilstate = NULL;

// Global variables used by Cython modules to access the Godot API
DLL_EXPORT GDExtensionInterfaceGetProcAddress pythonscript_gdextension_get_proc_address = NULL;
DLL_EXPORT GDExtensionClassLibraryPtr pythonscript_gdextension_library = NULL;


// GDExtension interface uses GDStringName everywhere a name should be passed,
// however it is very cumbersome to create it !

static GDExtensionPtrConstructor gdstring_constructor = NULL;
static GDExtensionPtrDestructor gdstring_destructor = NULL;
static GDExtensionPtrConstructor gdstringname_from_gdstring_constructor = NULL;
static GDExtensionPtrDestructor gdstringname_destructor = NULL;
static GDExtensionInterfaceStringNewWithUtf8Chars gdstring_new_with_utf8_chars = NULL;

DLL_EXPORT void pythonscript_gdstringname_new(GDExtensionStringNamePtr ptr, const char *cstr) {
    // Method name must be passed as a StringName object... which itself has
    // to be built from a String object :(
    char as_gdstring[GD_STRING_MAX_SIZE];
    const GDExtensionConstTypePtr args[1] = {&as_gdstring};
    gdstring_new_with_utf8_chars(&as_gdstring, cstr);
    gdstringname_from_gdstring_constructor(ptr, args);
    gdstring_destructor(&as_gdstring);
}

DLL_EXPORT void pythonscript_gdstringname_delete(GDExtensionStringNamePtr ptr) {
    gdstringname_destructor(ptr);
}

#define GD_PRINT_ERROR(msg) { \
    { \
        GDExtensionInterfacePrintError fn = (GDExtensionInterfacePrintError)(void*)pythonscript_gdextension_get_proc_address("print_error"); \
        if (fn) { \
            fn(msg, __func__, __FILE__, __LINE__, false); \
        } else { \
            printf("ERROR: %s", msg); \
        } \
    } \
}

#define GD_PRINT_WARNING(msg) { \
    { \
        GDExtensionInterfacePrintWarning fn = (GDExtensionInterfacePrintWarning)(void*)pythonscript_gdextension_get_proc_address("print_warning"); \
        if (fn) { \
            fn(msg, __func__, __FILE__, __LINE__, false); \
        } else { \
            printf("WARNING: %s", msg); \
        } \
    } \
}

// Initialize Python interpreter & godot
static void _initialize_python() {
    if (state != ENTRYPOINT_RETURNED) {
        printf("Pythonscript: Invalid internal state (this should never happen !)\n");
        goto error;
    }

    // Initialize CPython interpreter

    PyConfig config;
    PyConfig_InitIsolatedConfig(&config);
    config.configure_c_stdio = 1;

    // Set PYTHONHOME from .so path
    {
        // 0) Retrieve Godot methods
        char method_name_as_gdstringname[GD_STRING_NAME_MAX_SIZE];
        pythonscript_gdstringname_new(&method_name_as_gdstringname, "get_base_dir");
        GDExtensionPtrBuiltInMethod gdstring_get_base_dir;
        {
            GDExtensionInterfaceVariantGetPtrBuiltinMethod fn = (GDExtensionInterfaceVariantGetPtrBuiltinMethod)(void*)pythonscript_gdextension_get_proc_address("variant_get_ptr_builtin_method");
            gdstring_get_base_dir = fn(
                GDEXTENSION_VARIANT_TYPE_STRING,
                &method_name_as_gdstringname,
                3942272618
            );
        }
        pythonscript_gdstringname_delete(&method_name_as_gdstringname);
        if (gdstring_get_base_dir == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `String.get_base_dir` method)");
            goto error;
        }

        // 1) Retrieve library path
        char gd_library_path[GD_STRING_MAX_SIZE];
        {
            GDExtensionInterfaceGetLibraryPath fn = (GDExtensionInterfaceGetLibraryPath)(void*)pythonscript_gdextension_get_proc_address("get_library_path");
            fn(pythonscript_gdextension_library, gd_library_path);
        }

        // 2) Retrieve base dir from library path
        char gd_basedir_path[GD_STRING_MAX_SIZE];
        gdstring_constructor(gd_basedir_path, NULL);
        gdstring_get_base_dir(gd_library_path, NULL, gd_basedir_path, 0);
        gdstring_destructor(gd_library_path);

        // 3) Convert base dir into regular c string
        GDExtensionInt basedir_path_size;
        {
            GDExtensionInterfaceStringToUtf8Chars fn = (GDExtensionInterfaceStringToUtf8Chars)(void*)pythonscript_gdextension_get_proc_address("string_to_utf8_chars");
            basedir_path_size = fn(gd_basedir_path, NULL, 0);
        }
        // Why not using variable length array here ? Glad you asked Timmy !
        // VLA are part of the C99 standard, but MSVC compiler is missing it :(
        // Because VLA were removed from the C11 standard, and the standards committee
        // decided it was no good, probably because you can't handle allocation errors
        // like we're about to do two lines down.
        char *basedir_path;
        {
            GDExtensionInterfaceMemAlloc fn = (GDExtensionInterfaceMemAlloc)(void*)pythonscript_gdextension_get_proc_address("mem_alloc");
            basedir_path = fn(basedir_path_size + 1);
        }
        if (basedir_path == NULL) {
            GD_PRINT_ERROR("Pythonscript: Initialization error (memory allocation failed)");
            goto error;
        }
        {
            GDExtensionInterfaceStringToUtf8Chars fn = (GDExtensionInterfaceStringToUtf8Chars)(void*)pythonscript_gdextension_get_proc_address("string_to_utf8_chars");
            fn(gd_basedir_path, basedir_path, basedir_path_size);
        }
        basedir_path[basedir_path_size] = '\0';
        gdstring_destructor(gd_basedir_path);


        // 4) Configure pythonhome with base dir
        {
            PyStatus status = PyConfig_SetBytesString(
                &config,
                &config.home,
                basedir_path
            );
            {
                GDExtensionInterfaceMemFree fn = (GDExtensionInterfaceMemFree)(void*)pythonscript_gdextension_get_proc_address("mem_free");
                fn(basedir_path);
            }
            if (PyStatus_Exception(status)) {
                GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
                GD_PRINT_ERROR(status.err_msg);
                goto error;
            }
        }
    }

    // Set program name
    {
        PyStatus status = PyConfig_SetBytesString(
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

    // Read all configuration at once
    {
        PyStatus status = PyConfig_Read(&config);
        if (PyStatus_Exception(status)) {
            GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
            GD_PRINT_ERROR(status.err_msg);
            goto error;
        }
    }

    // TODO
    // Update sys.path with projet config
    // status = PyWideStringList_Append(&config.module_search_paths,
    //                                  L"/path/to/more/modules");
    // if (PyStatus_Exception(status)) {
    //     GD_PRINT_ERROR("Pythonscript: Cannot update sys.path");
    //     goto error;
    // }

    {
        PyStatus status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(status)) {
            GD_PRINT_ERROR("Pythonscript: Cannot initialize Python interpreter");
            GD_PRINT_ERROR(status.err_msg);
            goto error;
        }
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


    {
        int ret = import__pythonscript();
        if (ret != 0) {
            GD_PRINT_ERROR("Pythonscript: Cannot load Python module `_pythonscript`");
            goto post_init_error;
        }
    }


    PyConfig_Clear(&config);

    // Release the Kraken... er I mean the GIL !
    gilstate = PyEval_SaveThread();

    state = PYTHON_INTERPRETER_READY;
    return;

post_init_error:
    PyConfig_Clear(&config);
    {
        int ret = Py_FinalizeEx();
        if (ret != 0) {
            GD_PRINT_ERROR("Pythonscript: Cannot finalize Python interpreter");
        }
    }

error:
    state = CRASHED;
}

static void _deinitialize_python() {
    if (state != PYTHON_INTERPRETER_READY) {
        printf("Pythonscript: Invalid internal state (this should never happen !)\n");
        goto error;
    }

    // Re-acquire the gil in order to finalize properly
    PyEval_RestoreThread(gilstate);

    int ret = Py_FinalizeEx();
    if (ret != 0) {
        GD_PRINT_ERROR("Pythonscript: Cannot finalize Python interpreter");
    }

    state = STALLED;
    return;

error:
    state = CRASHED;
}

static void _initialize(void *userdata, GDExtensionInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (state == ENTRYPOINT_RETURNED && p_level == GDEXTENSION_INITIALIZATION_CORE) {
        _initialize_python();
    }
    if (state != CRASHED) {
        _pythonscript_initialize(p_level);
    }
}

static void _deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (state != CRASHED) {
        _pythonscript_deinitialize(p_level);
    }
    if (state == PYTHON_INTERPRETER_READY && p_level == GDEXTENSION_INITIALIZATION_CORE) {
        _deinitialize_python();
    }
}

DLL_EXPORT GDExtensionBool pythonscript_init(
    const GDExtensionInterfaceGetProcAddress p_get_proc_address,
    const GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
    if (state != STALLED) {
        printf("Pythonscript: Invalid internal state (this should never happen !)\n");
        goto error;
    }
    state = ENTRYPOINT_CALLED;

    if (p_get_proc_address == NULL || p_library == NULL || r_initialization == NULL) {
        printf("Pythonscript: Invalid init parameters provided by Godot (this should never happen !)\n");
        goto error;
    }
    // `pythonscript_gdextension_*` must be set as early as possible given it is never
    // null-pointer checked, especially in the Cython modules
    pythonscript_gdextension_get_proc_address = p_get_proc_address;
    pythonscript_gdextension_library = p_library;

    // Load GDString/GDStringName contructor/destructor needed for pythonscript_gdstringname_new/delete helpers

    GDExtensionInterfaceVariantGetPtrConstructor variant_get_ptr_constructor = (GDExtensionInterfaceVariantGetPtrConstructor)(void*)p_get_proc_address("variant_get_ptr_constructor");
    GDExtensionInterfaceVariantGetPtrDestructor variant_get_ptr_destructor = (GDExtensionInterfaceVariantGetPtrDestructor)(void*)p_get_proc_address("variant_get_ptr_destructor");

    gdstring_constructor = variant_get_ptr_constructor(GDEXTENSION_VARIANT_TYPE_STRING, 0);
    if (gdstring_constructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `String` constructor)");
        goto error;
    }

    gdstring_destructor = variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING);
    if (gdstring_destructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `String` destructor)");
        goto error;
    }

    gdstringname_from_gdstring_constructor = variant_get_ptr_constructor(GDEXTENSION_VARIANT_TYPE_STRING_NAME, 2);
    if (gdstringname_from_gdstring_constructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `StringName` constructor)");
        goto error;
    }

    gdstringname_destructor = variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING_NAME);
    if (gdstringname_destructor == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `StringName` destructor)");
        goto error;
    }

    gdstring_new_with_utf8_chars = (GDExtensionInterfaceStringNewWithUtf8Chars)p_get_proc_address("string_new_with_utf8_chars");
    if (gdstring_new_with_utf8_chars == NULL) {
        GD_PRINT_ERROR("Pythonscript: Initialization error (cannot retrieve `string_new_with_utf8_chars` destructor)");
        goto error;
    }

    // Check compatibility between the Godot version that has been used for building
    // (i.e. the bindings has been generated against) and the version currently executed.
    GDExtensionGodotVersion godot_version;
    {
        GDExtensionInterfaceGetGodotVersion get_godot_version = (GDExtensionInterfaceGetGodotVersion)p_get_proc_address("get_godot_version");
        get_godot_version(&godot_version);
    }
    if (godot_version.major != GODOT_VERSION_MAJOR || godot_version.minor < GODOT_VERSION_MINOR) {
        char buff[256];
        snprintf(
            buff,
            sizeof(buff),
            "Pythonscript: Incompatible Godot version (expected ~%d.%d, got %s)\n",
            GODOT_VERSION_MAJOR,
            GODOT_VERSION_MINOR,
            godot_version.string
        );
        GD_PRINT_ERROR(buff);
        goto error;
    }

    // Initialize as early as possible, this way we can have 3rd party plugins written
    // in Python/Cython that can do things at this level
    r_initialization->minimum_initialization_level  = GDEXTENSION_INITIALIZATION_CORE;
	r_initialization->userdata = NULL;
    r_initialization->initialize = _initialize;
    r_initialization->deinitialize = _deinitialize;

    state = ENTRYPOINT_RETURNED;
    return true;

error:
    state = CRASHED;
    return false;
}
