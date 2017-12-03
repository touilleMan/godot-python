#include "Python.h"

#ifndef _WIN32
#include <dlfcn.h>
#endif
#include <wchar.h>

#include "pythonscript.h"
#include "cffi_bindings/api.h"

#include <gdnative_api_struct.gen.h>

// TODO: Anyway, this cause a segfault....
// static void _pythonscript_finish() {
// 	#ifdef BACKEND_CPYTHON
// 		// TODO: Do we need to deinit the interpreter ?
// 		Py_FinalizeEx();
// 	#endif
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


// To avoid having to go through cffi call if profiling is not on,
// we use those simple _hook_ functions as a proxy
// Note _profiling_started should idealy be stored in the p_data pointer,
// but this would be much more cumbersome (given p_data points on a python
// object). Anyway, there is only one instance of Pythonscript started so
// it doesn't really matter.

static bool _profiling_started = false;


static void _hook_profiling_start(godot_pluginscript_language_data *p_data) {
	_profiling_started = true;
	pybind_profiling_start(p_data);
}


static void _hook_profiling_stop(godot_pluginscript_language_data *p_data) {
	_profiling_started = true;
	pybind_profiling_stop(p_data);
}


static void _hook_profiling_frame(godot_pluginscript_language_data *p_data) {
	if (_profiling_started) {
		pybind_profiling_frame(p_data);
	}
}


void godot_gdnative_init(godot_gdnative_init_options *options) {
	GDNATIVE_API_INIT(options);

#ifdef BACKEND_CPYTHON
#ifndef _WIN32
	// Make sure the shared library has all it symbols loaded
	// (strange bug with libpython3.6 otherwise...)
	{
		const wchar_t *wpath = godot_string_unicode_str(options->active_library_path);
		char path[300];
		wcstombs(path, wpath, 300);
		dlopen(path, RTLD_NOW | RTLD_GLOBAL);
	}

	const char *err = dlerror();
	if (err) {
		godot_string msg;
		godot_string_new_data(&msg, err, -1);
		godot_print(&msg);
		godot_string_destroy(&msg);
		return;
	}
#endif

	// Retrieve path and set pythonhome
	{
		static wchar_t pythonhome[300];
		godot_string _pythonhome = godot_string_get_base_dir(options->active_library_path);
		wcsncpy(pythonhome, godot_string_unicode_str(&_pythonhome), 300);
		godot_string_destroy(&_pythonhome);
		Py_SetPythonHome(pythonhome);
	}
#endif

	desc.name = "Python";
	desc.type = "Python";
	desc.extension = "py";
	desc.recognized_extensions = PYTHONSCRIPT_RECOGNIZED_EXTENSIONS;
	desc.init = pybind_init;
	desc.finish = pybind_finish;
	desc.reserved_words = PYTHONSCRIPT_RESERVED_WORDS;
	desc.comment_delimiters = PYTHONSCRIPT_COMMENT_DELIMITERS;
	desc.string_delimiters = PYTHONSCRIPT_STRING_DELIMITERS;
	desc.has_named_classes = false;
	desc.get_template_source_code = pybind_get_template_source_code;

	desc.script_desc.init = pybind_script_init;
	desc.script_desc.finish = pybind_script_finish;

	desc.script_desc.instance_desc.init = pybind_instance_init;
	desc.script_desc.instance_desc.finish = pybind_instance_finish;
	desc.script_desc.instance_desc.set_prop = pybind_instance_set_prop;
	desc.script_desc.instance_desc.get_prop = pybind_instance_get_prop;
	desc.script_desc.instance_desc.call_method = pybind_instance_call_method;
	desc.script_desc.instance_desc.notification = pybind_instance_notification;
	desc.script_desc.instance_desc.refcount_incremented = NULL;
	desc.script_desc.instance_desc.refcount_decremented = NULL;

	if (options->in_editor) {

		desc.get_template_source_code = pybind_get_template_source_code;
		desc.validate = pybind_validate;
		desc.find_function = pybind_find_function;
		desc.make_function = pybind_make_function;
		desc.complete_code = pybind_complete_code;
		desc.auto_indent_code = pybind_auto_indent_code;

		desc.add_global_constant = pybind_add_global_constant;
		desc.debug_get_error = pybind_debug_get_error;
		desc.debug_get_stack_level_count = pybind_debug_get_stack_level_count;
		desc.debug_get_stack_level_line = pybind_debug_get_stack_level_line;
		desc.debug_get_stack_level_function = pybind_debug_get_stack_level_function;
		desc.debug_get_stack_level_source = pybind_debug_get_stack_level_source;
		desc.debug_get_stack_level_locals = pybind_debug_get_stack_level_locals;
		desc.debug_get_stack_level_members = pybind_debug_get_stack_level_members;
		desc.debug_get_globals = pybind_debug_get_globals;
		desc.debug_parse_stack_level_expression = pybind_debug_parse_stack_level_expression;

		desc.profiling_start = _hook_profiling_start;
		desc.profiling_stop = _hook_profiling_stop;
		desc.profiling_get_accumulated_data = pybind_profiling_get_accumulated_data;
		desc.profiling_get_frame_data = pybind_profiling_get_frame_data;
		desc.profiling_frame = _hook_profiling_frame;
	}
	godot_pluginscript_register_language(&desc);
}

void godot_gdnative_singleton() {
}

void godot_gdnative_terminate() {
}
