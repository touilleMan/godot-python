#include "Python.h"

#ifndef _WIN32
#include <dlfcn.h>
#endif
#include <wchar.h>

#include <Python.h>
#include <stdio.h>
#include <wchar.h>

#include <gdnative_api_struct.gen.h>

#include "_godot_api.h"


// TODO: Anyway, this cause a segfault....
// static void _pythonscript_finish() {
//  #ifdef BACKEND_CPYTHON
//      // TODO: Do we need to deinit the interpreter ?
//      Py_FinalizeEx();
//  #endif
// }

static godot_gdnative_core_api_struct pythonscript_gdapi;


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


// To avoid having to go through cffi call if profiling is not on,
// we use those simple _hook_ functions as a proxy
// Note _profiling_started should idealy be stored in the p_data pointer,
// but this would be much more cumbersome (given p_data points on a python
// object). Anyway, there is only one instance of Pythonscript started so
// it doesn't really matter.

static bool _profiling_started = false;


// static void _hook_profiling_start(godot_pluginscript_language_data *p_data) {
//  _profiling_started = true;
//  pythonscript_profiling_start(p_data);
// }


// static void _hook_profiling_stop(godot_pluginscript_language_data *p_data) {
//  _profiling_started = true;
//  pythonscript_profiling_stop(p_data);
// }


// static void _hook_profiling_frame(godot_pluginscript_language_data *p_data) {
//  if (_profiling_started) {
//      pythonscript_profiling_frame(p_data);
//  }
// }


const godot_gdnative_ext_pluginscript_api_struct *load_pluginscript_ext(const godot_gdnative_init_options *options) {
    for (int i = 0; i < options->api_struct->num_extensions; i++) {
        const godot_gdnative_api_struct *ext = options->api_struct->extensions[i];
        if (ext->type == GDNATIVE_EXT_PLUGINSCRIPT) {
            return (const godot_gdnative_ext_pluginscript_api_struct *)ext;
        }
    }
}


void godot_gdnative_init(godot_gdnative_init_options *options) {
    const godot_gdnative_core_api_struct *gdapi = options->api_struct;
    const godot_gdnative_ext_pluginscript_api_struct *pluginscriptapi = load_pluginscript_ext(options);
    if (!pluginscriptapi) {
        godot_string msg;
        gdapi->godot_string_new_with_wide_string(
            &msg, L"Cannot load Pythonscript: pluginscript extension not available", -1);
        gdapi->godot_print(&msg);
        gdapi->godot_string_destroy(&msg);
        return;
    }

#ifndef _WIN32
    // Make sure the shared library has all it symbols loaded
    // (strange bug with libpython3.6 otherwise...)
    {
        const wchar_t *wpath = gdapi->godot_string_wide_str(
            options->active_library_path
        );
        char path[300];
        wcstombs(path, wpath, 300);
        dlopen(path, RTLD_NOW | RTLD_GLOBAL);
    }

    const char *err = dlerror();
    if (err) {
        const size_t n = strlen(err);
        wchar_t werr[n];
        mbstowcs(werr, err, n);
        godot_string msg;
        gdapi->godot_string_new_with_wide_string(&msg, werr, -1);
        gdapi->godot_print(&msg);
        gdapi->godot_string_destroy(&msg);
        return;
    }
#endif

    // Initialize CPython interpreter

    // Retrieve path and set pythonhome
    {
        static wchar_t pythonhome[300];
        godot_string _pythonhome = gdapi->godot_string_get_base_dir(
            options->active_library_path
        );
        wcsncpy(pythonhome, gdapi->godot_string_wide_str(&_pythonhome), 300);
        gdapi->godot_string_destroy(&_pythonhome);
        Py_SetPythonHome(pythonhome);
    }
    // // Add current dir to PYTHONPATH
    // wchar_t *path = Py_GetPath();
    // int new_path_len = wcslen(path) + 3;
    // wchar_t new_path[new_path_len * sizeof(wchar_t)];
    // wcsncpy(new_path, L".:", new_path_len);
    // wcsncpy(new_path + 2, path, new_path_len - 2);
    // Py_SetPath(new_path);
    // printf("==>%ls\n", Py_GetPath());

    Py_SetProgramName(L"godot");
    // Initialize interpreter but skip initialization registration of signal handlers
    Py_InitializeEx(0);
    int ret = import__godot();
    if (ret != 0){
        godot_string msg;
        gdapi->godot_string_new_with_wide_string(
            &msg, L"Cannot load pythonscript module", -1
        );
        gdapi->godot_print(&msg);
        gdapi->godot_string_destroy(&msg);
        return;
    }
    pythonscript_register_gdapi(options);

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

    // desc.script_desc.init = pythonscript_script_init;
    // desc.script_desc.finish = pythonscript_script_finish;

    // desc.script_desc.instance_desc.init = pythonscript_instance_init;
    // desc.script_desc.instance_desc.finish = pythonscript_instance_finish;
    // desc.script_desc.instance_desc.set_prop = pythonscript_instance_set_prop;
    // desc.script_desc.instance_desc.get_prop = pythonscript_instance_get_prop;
    // desc.script_desc.instance_desc.call_method = pythonscript_instance_call_method;
    // desc.script_desc.instance_desc.notification = pythonscript_instance_notification;
    // desc.script_desc.instance_desc.refcount_incremented = NULL;
    // desc.script_desc.instance_desc.refcount_decremented = NULL;

    if (options->in_editor) {

        desc.get_template_source_code = pythonscript_get_template_source_code;
        desc.validate = pythonscript_validate;
        desc.find_function = pythonscript_find_function;
        // desc.make_function = pythonscript_make_function;
        desc.complete_code = pythonscript_complete_code;
        //  desc.auto_indent_code = pythonscript_auto_indent_code;

        //  desc.debug_get_error = pythonscript_debug_get_error;
        //  desc.debug_get_stack_level_count = pythonscript_debug_get_stack_level_count;
        //  desc.debug_get_stack_level_line = pythonscript_debug_get_stack_level_line;
        //  desc.debug_get_stack_level_function = pythonscript_debug_get_stack_level_function;
        //  desc.debug_get_stack_level_source = pythonscript_debug_get_stack_level_source;
        //  desc.debug_get_stack_level_locals = pythonscript_debug_get_stack_level_locals;
        //  desc.debug_get_stack_level_members = pythonscript_debug_get_stack_level_members;
        //  desc.debug_get_globals = pythonscript_debug_get_globals;
        //  desc.debug_parse_stack_level_expression = pythonscript_debug_parse_stack_level_expression;

        //  desc.profiling_start = _hook_profiling_start;
        //  desc.profiling_stop = _hook_profiling_stop;
        //  desc.profiling_get_accumulated_data = pythonscript_profiling_get_accumulated_data;
        //  desc.profiling_get_frame_data = pythonscript_profiling_get_frame_data;
        //  desc.profiling_frame = _hook_profiling_frame;
    }
    pluginscriptapi->godot_pluginscript_register_language(&desc);
}

void godot_gdnative_singleton() {
}

void godot_gdnative_terminate() {
    Py_Finalize();
}
