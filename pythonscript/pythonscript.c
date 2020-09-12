/*
 * This file gets compiled as a shared library that act as the entry point
 * to the pythonscript plugin.
 * It should be loaded by Godot's GDNative system (see the `pythonscript.gdnlib`
 * file in the example/test projects).
 * As part of the loading, GDNative will call the `godot_gdnative_init`
 * function which will in turn initialize the CPython interpreter then register
 * Python as a new language using Godot's Pluginscript system.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifndef _WIN32
#include <dlfcn.h>
#endif
#include <wchar.h>

#include <gdnative_api_struct.gen.h>

#include "_godot_api.h"


static const char *PYTHONSCRIPT_RECOGNIZED_EXTENSIONS[] = { "py", "pyc", "pyo", "pyd", 0 };
static const char *PYTHONSCRIPT_RESERVED_WORDS[] = {
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
    0
};
static const char *PYTHONSCRIPT_COMMENT_DELIMITERS[] = { "#", "\"\"\"\"\"\"", 0 };
static const char *PYTHONSCRIPT_STRING_DELIMITERS[] = { "\" \"", "' '", 0 };
static godot_pluginscript_language_desc desc;
static PyThreadState *gilstate = NULL;


/*
 * Global variables exposing Godot API to the godot.hazmat cython module.
 * Hence we must initialized them before loading `_godot`/`godot` modules
 * (which both depend on `godot.hazmat`).
 */
#ifdef _WIN32
# define PYTHONSCRIPT_EXPORT __declspec(dllexport)
#else
# define PYTHONSCRIPT_EXPORT
#endif
PYTHONSCRIPT_EXPORT const godot_gdnative_core_api_struct *pythonscript_gdapi10 = NULL;
PYTHONSCRIPT_EXPORT const godot_gdnative_core_1_1_api_struct *pythonscript_gdapi11 = NULL;
PYTHONSCRIPT_EXPORT const godot_gdnative_core_1_2_api_struct *pythonscript_gdapi12 = NULL;
PYTHONSCRIPT_EXPORT const godot_gdnative_ext_nativescript_api_struct *pythonscript_gdapi_ext_nativescript = NULL;
PYTHONSCRIPT_EXPORT const godot_gdnative_ext_pluginscript_api_struct *pythonscript_gdapi_ext_pluginscript = NULL;
PYTHONSCRIPT_EXPORT const godot_gdnative_ext_android_api_struct *pythonscript_gdapi_ext_android = NULL;
PYTHONSCRIPT_EXPORT const godot_gdnative_ext_arvr_api_struct *pythonscript_gdapi_ext_arvr = NULL;


static void _register_gdapi(const godot_gdnative_init_options *options) {
    pythonscript_gdapi10 = (const godot_gdnative_core_api_struct *)options->api_struct;
    if (pythonscript_gdapi10->next) {
        pythonscript_gdapi11 = (const godot_gdnative_core_1_1_api_struct *)pythonscript_gdapi10->next;
        if (pythonscript_gdapi11->next) {
            pythonscript_gdapi12 = (const godot_gdnative_core_1_2_api_struct *)pythonscript_gdapi11->next;
        }
    }

    for (unsigned int i = 0; i < pythonscript_gdapi10->num_extensions; i++) {
        const godot_gdnative_api_struct *ext = pythonscript_gdapi10->extensions[i];
        switch (ext->type) {
            case GDNATIVE_EXT_NATIVESCRIPT:
                pythonscript_gdapi_ext_nativescript = (const godot_gdnative_ext_nativescript_api_struct *)ext;
                break;
            case GDNATIVE_EXT_PLUGINSCRIPT:
                pythonscript_gdapi_ext_pluginscript = (const godot_gdnative_ext_pluginscript_api_struct *)ext;
                break;
            case GDNATIVE_EXT_ANDROID:
                pythonscript_gdapi_ext_android = (const godot_gdnative_ext_android_api_struct *)ext;
                break;
            case GDNATIVE_EXT_ARVR:
                pythonscript_gdapi_ext_arvr = (const godot_gdnative_ext_arvr_api_struct *)ext;
                break;
            default:
                break;
        }
    }
}


GDN_EXPORT void godot_gdnative_init(godot_gdnative_init_options *options) {
    // Registering the api should be the very first thing to do !
    _register_gdapi(options);

    // Now those macros are usable

    #define GD_PRINT(c_msg) { \
        godot_string gd_msg; \
        pythonscript_gdapi10->godot_string_new_with_wide_string( \
            &gd_msg, c_msg, -1); \
        pythonscript_gdapi10->godot_print(&gd_msg); \
        pythonscript_gdapi10->godot_string_destroy(&gd_msg); \
    }

    #define GD_ERROR_PRINT(msg) { \
        pythonscript_gdapi10->godot_print_error(msg, __func__, __FILE__, __LINE__); \
    }

    // Check for mandatory plugins

    if (!pythonscript_gdapi10 || !pythonscript_gdapi11 || !pythonscript_gdapi12) {
        GD_ERROR_PRINT("Godot-Python requires GDNative API >= v1.2");
        return;
    }
    if (!pythonscript_gdapi_ext_pluginscript) {
        GD_ERROR_PRINT("Pluginscript extension not available");
        return;
    }

#ifndef _WIN32
    // Make sure the shared library has all it symbols loaded
    // (strange bug with libpython3.x.so otherwise...)
    {
        const wchar_t *wpath = pythonscript_gdapi10->godot_string_wide_str(
            options->active_library_path
        );
        char path[300];
        wcstombs(path, wpath, 300);
        dlopen(path, RTLD_NOW | RTLD_GLOBAL);
    }

    const char *err = dlerror();
    if (err) {
        GD_ERROR_PRINT(err);
        return;
    }
#endif

    // Initialize CPython interpreter

    // Retrieve path and set pythonhome
    {
        static wchar_t pythonhome[300];
        godot_string _pythonhome = pythonscript_gdapi10->godot_string_get_base_dir(
            options->active_library_path
        );
        wcsncpy(pythonhome, pythonscript_gdapi10->godot_string_wide_str(&_pythonhome), 300);
        pythonscript_gdapi10->godot_string_destroy(&_pythonhome);
        Py_SetPythonHome(pythonhome);
    }
    // TODO: site.USER_SITE seems to point to an invalid location in ~/.local
    // // Add current dir to PYTHONPATH
    // wchar_t *path = Py_GetPath();
    // int new_path_len = wcslen(path) + 3;
    // wchar_t new_path[new_path_len * sizeof(wchar_t)];
    // wcsncpy(new_path, L".:", new_path_len);
    // wcsncpy(new_path + 2, path, new_path_len - 2);
    // Py_SetPath(new_path);
    // PyRun_SimpleString("import sys\nprint('PYTHON_PATH:', sys.path)\n");

    Py_SetProgramName(L"godot");
    // Initialize interpreter but skip initialization registration of signal handlers
    Py_InitializeEx(0);
    // PyEval_InitThreads acquires the GIL, so we must release it later.
    // Since python3.7 PyEval_InitThreads is automatically called by Py_InitializeEx, but it's better to leave it here
    // to be explicit. Calling it again does nothing.
    PyEval_InitThreads();
    int ret = import__godot();
    if (ret != 0){
        GD_ERROR_PRINT("Cannot load godot python module");
        return;
    }

    desc.name = "Python";
    desc.type = "Python";
    desc.extension = "py";
    desc.recognized_extensions = PYTHONSCRIPT_RECOGNIZED_EXTENSIONS;
    desc.init = pythonscript_init;
    desc.finish = pythonscript_finish;
    desc.reserved_words = PYTHONSCRIPT_RESERVED_WORDS;
    desc.comment_delimiters = PYTHONSCRIPT_COMMENT_DELIMITERS;
    desc.string_delimiters = PYTHONSCRIPT_STRING_DELIMITERS;
    desc.has_named_classes = false;
    desc.add_global_constant = pythonscript_add_global_constant;

    desc.script_desc.init = pythonscript_script_init;
    desc.script_desc.finish = pythonscript_script_finish;

    desc.script_desc.instance_desc.init = pythonscript_instance_init;
    desc.script_desc.instance_desc.finish = pythonscript_instance_finish;
    desc.script_desc.instance_desc.set_prop = pythonscript_instance_set_prop;
    desc.script_desc.instance_desc.get_prop = pythonscript_instance_get_prop;
    desc.script_desc.instance_desc.call_method = pythonscript_instance_call_method;
    desc.script_desc.instance_desc.notification = pythonscript_instance_notification;
    desc.script_desc.instance_desc.refcount_incremented = NULL;
    desc.script_desc.instance_desc.refcount_decremented = NULL;

    if (options->in_editor) {

        desc.get_template_source_code = pythonscript_get_template_source_code;
        desc.validate = pythonscript_validate;
        desc.find_function = pythonscript_find_function;
        desc.make_function = pythonscript_make_function;
        desc.complete_code = pythonscript_complete_code;
        desc.auto_indent_code = pythonscript_auto_indent_code;

        desc.debug_get_error = pythonscript_debug_get_error;
        desc.debug_get_stack_level_count = pythonscript_debug_get_stack_level_count;
        desc.debug_get_stack_level_line = pythonscript_debug_get_stack_level_line;
        desc.debug_get_stack_level_function = pythonscript_debug_get_stack_level_function;
        desc.debug_get_stack_level_source = pythonscript_debug_get_stack_level_source;
        desc.debug_get_stack_level_locals = pythonscript_debug_get_stack_level_locals;
        desc.debug_get_stack_level_members = pythonscript_debug_get_stack_level_members;
        desc.debug_get_globals = pythonscript_debug_get_globals;
        desc.debug_parse_stack_level_expression = pythonscript_debug_parse_stack_level_expression;

        desc.profiling_start = pythonscript_profiling_start;
        desc.profiling_stop = pythonscript_profiling_stop;
        desc.profiling_get_accumulated_data = pythonscript_profiling_get_accumulated_data;
        desc.profiling_get_frame_data = pythonscript_profiling_get_frame_data;
        desc.profiling_frame = pythonscript_profiling_frame;
    }
    pythonscript_gdapi_ext_pluginscript->godot_pluginscript_register_language(&desc);

    // Release the Kraken... er I mean the GIL !
    gilstate = PyEval_SaveThread();
}


GDN_EXPORT void godot_gdnative_singleton() {
}


GDN_EXPORT void godot_gdnative_terminate() {
    // Re-acquire the gil in order to finalize properly
    PyEval_RestoreThread(gilstate);

    int ret = Py_FinalizeEx();
    if (ret != 0) {
        GD_ERROR_PRINT("Cannot finalize python interpreter");
    }
}
