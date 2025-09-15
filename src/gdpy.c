/*
 * This file gets compiled as a shared library that act as the entry point
 * to the Godot-Python plugin.
 * It should be loaded by Godot's GDExtension system (see the
 * `gdpy.gdextension` file in the example/test projects).
 * As part of the loading, Godot will call the `gdpy_init` function
 * very early, which will in turn register an initialization callback to be
 * called at the right time during Godot init. Once called, this callback
 * will initialize CPython interpreter then register Python as a new language
 * for Godot.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <godot/gdextension_interface.h>

#ifdef _WIN32
# define DLL_EXPORT __declspec(dllexport)
# define DLL_IMPORT __declspec(dllimport)
#else
# define DLL_EXPORT __attribute__((visibility("default")))
# define DLL_IMPORT __attribute__((visibility("default")))
#endif

#ifdef __linux__
#include <dlfcn.h>  // Contains dlopen, RTLD_LAZY & RTLD_GLOBAL
#endif

// Just like any Godot builtin classes, Godot `String`&`StringName`'s size is defined in
// `extension_api.json` and is platform-dependant (e.g. 4 bytes on float_32, 8 on double_64).
// So in theory we should retrieve the value from the json file, convert it into a C
// header file and include it here.
// However this is cumbersome and we only need this once before the Python interpreter
// is initialized (after that we can use the Python bindings), so instead we stick with
// the biggest possible value and accept we will lose a couple of bytes on the stack ;)
#define GD_STRING_MAX_SIZE 8
#define GD_STRING_NAME_MAX_SIZE 8

// Nobody ain't no time to include stdbool.h !
#define bool unsigned int;
#define true 1
#define false 0

typedef enum {
    STALLED,  // Intitial state

    ENTRYPOINT_CALLED,  // gdpy_init called
    ENTRYPOINT_RETURNED,  // gdpy_init returns

    PYTHON_INTERPRETER_READY,

    CRASHED,  // Something went wrong :'(
} GdpyState;

static GdpyState state = STALLED;
static PyThreadState *gilstate = NULL;
// Callbacks originally defined in `godot._lang`, we load them rigth after CPython
// initialization, then use them in each subsequent Godot (de)initialization step.
static void (*gdpy_initialize)(int p_level);
static void (*gdpy_deinitialize)(int p_level);

// Global variables used by Cython modules to access the Godot API, and defined
// in `gdpy_gdptr_ptrs.c` (which is compiled together with this file).
void init_gdpy_gdextension();
DLL_IMPORT extern GDExtensionInterfaceGetProcAddress gdpy_gdptr_get_proc_address;
DLL_IMPORT extern GDExtensionClassLibraryPtr gdpy_gdptr_library;

#define GD_PRINT_ERROR(msg) { \
    { \
        GDExtensionInterfacePrintError fn = (GDExtensionInterfacePrintError)(void*)gdpy_gdptr_get_proc_address("print_error"); \
        if (fn) { \
            fn(msg, __func__, __FILE__, __LINE__, false); \
        } else { \
            printf("ERROR: %s", msg); \
        } \
    } \
}

#define GD_PRINT_WARNING(msg) { \
    { \
        GDExtensionInterfacePrintWarning fn = (GDExtensionInterfacePrintWarning)(void*)gdpy_gdptr_get_proc_address("print_warning"); \
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
        printf("Godot-Python: Invalid internal state (this should never happen !)\n");
        goto error;
    }

    // Load GDString & GDStringName contructors/destructors (needed above)

    GDExtensionInterfaceVariantGetPtrConstructor variant_get_ptr_constructor = (GDExtensionInterfaceVariantGetPtrConstructor)(void*)gdpy_gdptr_get_proc_address("variant_get_ptr_constructor");
    GDExtensionInterfaceVariantGetPtrDestructor variant_get_ptr_destructor = (GDExtensionInterfaceVariantGetPtrDestructor)(void*)gdpy_gdptr_get_proc_address("variant_get_ptr_destructor");

    GDExtensionPtrConstructor gd_string_constructor = variant_get_ptr_constructor(GDEXTENSION_VARIANT_TYPE_STRING, 0);
    if (gd_string_constructor == NULL) {
        GD_PRINT_ERROR("Godot-Python: Initialization error (cannot retrieve `String` constructor)");
        goto error;
    }

    GDExtensionPtrDestructor gd_string_destructor = variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING);
    if (gd_string_destructor == NULL) {
        GD_PRINT_ERROR("Godot-Python: Initialization error (cannot retrieve `String` destructor)");
        goto error;
    }

    GDExtensionPtrDestructor gd_string_name_destructor = variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING_NAME);
    if (gd_string_name_destructor == NULL) {
        GD_PRINT_ERROR("Godot-Python: Initialization error (cannot retrieve `StringName` destructor)");
        goto error;
    }

    GDExtensionInterfaceStringNameNewWithUtf8Chars gd_string_name_new_with_utf8_chars_with_utf8_chars = (GDExtensionInterfaceStringNameNewWithUtf8Chars)gdpy_gdptr_get_proc_address("string_name_new_with_utf8_chars");
    if (gd_string_name_new_with_utf8_chars_with_utf8_chars == NULL) {
        GD_PRINT_ERROR("Godot-Python: Initialization error (cannot retrieve `string_name_new_with_utf8_chars`)");
        goto error;
    }

    // Initialize CPython interpreter

    PyConfig config;
    PyConfig_InitIsolatedConfig(&config);
    config.configure_c_stdio = 1;

    // Set PYTHONHOME from .so path
    {
        // 0) Retrieve Godot methods
        char method_name_as_gd_string_name[GD_STRING_NAME_MAX_SIZE];
        gd_string_name_new_with_utf8_chars_with_utf8_chars(&method_name_as_gd_string_name, "get_base_dir");
        GDExtensionPtrBuiltInMethod gdstring_get_base_dir;
        {
            GDExtensionInterfaceVariantGetPtrBuiltinMethod fn = (GDExtensionInterfaceVariantGetPtrBuiltinMethod)(void*)gdpy_gdptr_get_proc_address("variant_get_ptr_builtin_method");
            gdstring_get_base_dir = fn(
                GDEXTENSION_VARIANT_TYPE_STRING,
                &method_name_as_gd_string_name,
                3942272618
            );
        }
        gd_string_name_destructor(&method_name_as_gd_string_name);
        if (gdstring_get_base_dir == NULL) {
            GD_PRINT_ERROR("Godot-Python: Initialization error (cannot retrieve `String.get_base_dir` method)");
            goto error;
        }

        // 1) Retrieve library path
        char gd_library_path[GD_STRING_MAX_SIZE];
        {
            GDExtensionInterfaceGetLibraryPath fn = (GDExtensionInterfaceGetLibraryPath)(void*)gdpy_gdptr_get_proc_address("get_library_path");
            fn(gdpy_gdptr_library, gd_library_path);
        }

        // 2) Retrieve base dir from library path
        char gd_basedir_path[GD_STRING_MAX_SIZE];
        gd_string_constructor(gd_basedir_path, NULL);
        gdstring_get_base_dir(gd_library_path, NULL, gd_basedir_path, 0);
        gd_string_destructor(gd_library_path);

        // 3) Convert base dir into regular c string
        GDExtensionInt basedir_path_size;
        {
            GDExtensionInterfaceStringToUtf8Chars fn = (GDExtensionInterfaceStringToUtf8Chars)(void*)gdpy_gdptr_get_proc_address("string_to_utf8_chars");
            basedir_path_size = fn(gd_basedir_path, NULL, 0);
        }
        // Why not using variable length array here ? Glad you asked Timmy !
        // VLA are part of the C99 standard, but MSVC compiler is missing it :(
        // Because VLA were removed from the C11 standard, and the standards committee
        // decided it was no good, probably because you can't handle allocation errors
        // like we're about to do two lines down.
        char *basedir_path;
        {
            GDExtensionInterfaceMemAlloc fn = (GDExtensionInterfaceMemAlloc)(void*)gdpy_gdptr_get_proc_address("mem_alloc");
            basedir_path = fn(basedir_path_size + 1);
        }
        if (basedir_path == NULL) {
            GD_PRINT_ERROR("Godot-Python: Initialization error (memory allocation failed)");
            goto error;
        }
        {
            GDExtensionInterfaceStringToUtf8Chars fn = (GDExtensionInterfaceStringToUtf8Chars)(void*)gdpy_gdptr_get_proc_address("string_to_utf8_chars");
            fn(gd_basedir_path, basedir_path, basedir_path_size);
        }
        basedir_path[basedir_path_size] = '\0';
        gd_string_destructor(gd_basedir_path);


        // 4) Configure pythonhome with base dir
        {
            PyStatus status = PyConfig_SetBytesString(
                &config,
                &config.home,
                basedir_path
            );
            {
                GDExtensionInterfaceMemFree fn = (GDExtensionInterfaceMemFree)(void*)gdpy_gdptr_get_proc_address("mem_free");
                fn(basedir_path);
            }
            if (PyStatus_Exception(status)) {
                GD_PRINT_ERROR("Godot-Python: Cannot initialize Python interpreter");
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
            GD_PRINT_ERROR("Godot-Python: Cannot initialize Python interpreter");
            GD_PRINT_ERROR(status.err_msg);
            goto error;
        }
    }

    // argv and sys.path are going to be set by `gdpy_initialize`
    // This is much simpler this way given we will have acces to Godot API
    // through the nice Python bindings this way

    // Read all configuration at once
    {
        PyStatus status = PyConfig_Read(&config);
        if (PyStatus_Exception(status)) {
            GD_PRINT_ERROR("Godot-Python: Cannot initialize Python interpreter");
            GD_PRINT_ERROR(status.err_msg);
            goto error;
        }
    }

    // TODO
    // Update sys.path with projet config
    // status = PyWideStringList_Append(&config.module_search_paths,
    //                                  L"/path/to/more/modules");
    // if (PyStatus_Exception(status)) {
    //     GD_PRINT_ERROR("Godot-Python: Cannot update sys.path");
    //     goto error;
    // }

    // When embedding Python, the symbols from `libpython3.so` are not made available.
    //
    // This is an issue when loading native modules (typically error message
    // `undefined symbol: PyExc_SystemError`) since they use those symbols while
    // not explicitly being linked to `libpython3.so`.
    //
    // So the solution is to force those symbols with an explicit RTLD_GLOBAL dlopen.
    //
    // See: https://stackoverflow.com/a/50489814
    #ifdef __linux__
    void*const libpython_handle = dlopen("libpython3.so", RTLD_LAZY | RTLD_GLOBAL);
    if (!libpython_handle) {
        GD_PRINT_ERROR("Godot-Python: Cannot dlopen libpython3.so");
        goto error;
    }
    #endif

    {
        PyStatus status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(status)) {
            GD_PRINT_ERROR("Godot-Python: Cannot initialize Python interpreter");
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
    // Useful for debugging if `import__gdpy` returns an error
    PyRun_SimpleString("import sys\nprint('PYTHON_PATH:', sys.path)\n");
#endif

    // Now get back `gdpy_(de)initialize` callbacks from `godot._lang` module,
    // they will be then used in each subsequent Godot (de)initialization step.
    {

        // Basically we do in C the equivalent of:
        // ```python
        // import godot._lang
        // gdpy_initialize = godot._lang.gdpy_initialize_function_ptr
        // gdpy_deinitialize = godot._lang.gdpy_deinitialize_function_ptr
        // ```

        // 1. Do `import godot._lang`

        PyObject* py_godot_lang_module;
        {
            PyObject* py_module_name = PyUnicode_FromString("godot._lang");
            if (py_module_name == NULL) {
                PyErr_Print();
                goto post_init_error;
            }

            py_godot_lang_module = PyImport_Import(py_module_name);
            Py_DECREF(py_module_name);
        }

        if (py_godot_lang_module == NULL) {
            PyErr_Print();
            goto post_init_error;
        }

        // 2. Do `gdpy_initialize = godot._lang.gdpy_initialize_function_ptr`

        {
            PyObject* py_gdpy_initialize_function_ptr = PyObject_GetAttrString(py_godot_lang_module, "gdpy_initialize_function_ptr");
            if (py_gdpy_initialize_function_ptr == NULL) {
                PyErr_Print();
                goto post_init_error;
            }
            gdpy_initialize = PyLong_AsVoidPtr(py_gdpy_initialize_function_ptr);
            Py_DECREF(py_gdpy_initialize_function_ptr);
        }

        // 3. Do `gdpy_deinitialize = godot._lang.gdpy_deinitialize_function_ptr`

        {
            PyObject* py_gdpy_deinitialize_function_ptr = PyObject_GetAttrString(py_godot_lang_module, "gdpy_deinitialize_function_ptr");
            if (py_gdpy_deinitialize_function_ptr == NULL) {
                PyErr_Print();
                goto post_init_error;
            }
            gdpy_deinitialize = PyLong_AsVoidPtr(py_gdpy_deinitialize_function_ptr);
            Py_DECREF(py_gdpy_deinitialize_function_ptr);
        }

        // 4. `godot._lang` module no longer needed

        Py_DECREF(py_godot_lang_module);

        if (gdpy_initialize == NULL || gdpy_deinitialize == NULL) {
            GD_PRINT_ERROR("Godot-Python: Cannot retrieve `gdpy_(de)initialize` function pointers");
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
            GD_PRINT_ERROR("Godot-Python: Cannot finalize Python interpreter");
        }
    }

error:
    state = CRASHED;
}

static void _deinitialize_python() {
    if (state != PYTHON_INTERPRETER_READY) {
        printf("Godot-Python: Invalid internal state (this should never happen !)\n");
        goto error;
    }

    // Re-acquire the gil in order to finalize properly
    PyEval_RestoreThread(gilstate);

    int ret = Py_FinalizeEx();
    if (ret != 0) {
        GD_PRINT_ERROR("Godot-Python: Cannot finalize Python interpreter");
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
    if (state != CRASHED && gdpy_initialize != NULL) {
        gdpy_initialize(p_level);
    }
}

static void _deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
    (void) userdata;  // acknowledge unreferenced parameter
    if (state != CRASHED && gdpy_deinitialize != NULL) {
        gdpy_deinitialize(p_level);
    }
    if (state == PYTHON_INTERPRETER_READY && p_level == GDEXTENSION_INITIALIZATION_CORE) {
        _deinitialize_python();
    }
}

// Entry point called by Godot
DLL_EXPORT GDExtensionBool gdpy_init(
    const GDExtensionInterfaceGetProcAddress p_get_proc_address,
    const GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
    if (state != STALLED) {
        printf("Godot-Python: Invalid internal state (this should never happen !)\n");
        goto error;
    }
    state = ENTRYPOINT_CALLED;

    if (p_get_proc_address == NULL || p_library == NULL || r_initialization == NULL) {
        printf("Godot-Python: Invalid init parameters provided by Godot (this should never happen !)\n");
        goto error;
    }

    // `gdpy_gdptr_*` must be set as early as possible given it is never
    // null-pointer checked, especially in the Cython modules.
    // Note we start by setting only `get_proc_address`&`library` since it is the
    // minimum we need to check Godot compatibility, and only after that we proceed
    // with the rest of the pointers.
    gdpy_gdptr_get_proc_address = p_get_proc_address;
    gdpy_gdptr_library = p_library;

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
            "Godot-Python: Incompatible Godot version (expected ~%d.%d, got %s)\n",
            GODOT_VERSION_MAJOR,
            GODOT_VERSION_MINOR,
            godot_version.string
        );
        GD_PRINT_ERROR(buff);
        goto error;
    }

    // Initialize the rest of the `gdpy_gdptr_*` pointers
    init_gdpy_gdextension();

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
