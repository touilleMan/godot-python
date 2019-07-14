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


const godot_gdnative_ext_pluginscript_api_struct *load_pluginscript_ext(const godot_gdnative_init_options *options) {
    for (int i = 0; i < options->api_struct->num_extensions; i++) {
        const godot_gdnative_api_struct *ext = options->api_struct->extensions[i];
        if (ext->type == GDNATIVE_EXT_PLUGINSCRIPT) {
            return (const godot_gdnative_ext_pluginscript_api_struct *)ext;
        }
    }
    return NULL;
}


void godot_gdnative_init(godot_gdnative_init_options *options) {
    #define GD_PRINT(c_msg) { \
        godot_string gd_msg; \
        gdapi->godot_string_new_with_wide_string( \
            &gd_msg, c_msg, -1); \
        gdapi->godot_print(&gd_msg); \
        gdapi->godot_string_destroy(&gd_msg); \
    }

    #define GD_ERROR_PRINT(msg) { \
        gdapi->godot_print_error(msg, __func__, __FILE__, __LINE__); \
    }

    const godot_gdnative_core_api_struct *gdapi = options->api_struct;
    const godot_gdnative_ext_pluginscript_api_struct *pluginscriptapi = load_pluginscript_ext(options);
    if (!pluginscriptapi) {
        GD_ERROR_PRINT("Pluginscript extension not available");
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
        GD_ERROR_PRINT(err);
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
        printf("++>%ls\n", pythonhome);
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
    PyRun_SimpleString("import sys\nprint('////', sys.path)\n");
    PyRun_SimpleString("import site\nprint('~~~',  site.USER_SITE)\n");
    // PyRun_SimpleString("import _godot\nprint('~~~',  _godot)\n");
    int ret = import__godot();
    if (ret != 0){
        GD_ERROR_PRINT("Cannot load godot python module");
        return;
    }
    pythonscript_register_gdapi(options);
    pythonscript_print_banner();

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
    pluginscriptapi->godot_pluginscript_register_language(&desc);
}

void godot_gdnative_singleton() {
}

void godot_gdnative_terminate() {
    Py_Finalize();
}
