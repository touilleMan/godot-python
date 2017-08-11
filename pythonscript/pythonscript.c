#include "pythonscript.h"
#include "Python.h"
#include "cffi_bindings/api.h"
#include <dlfcn.h>

static void _pythonscript_finish() {
	// TODO: Anyway, this cause a segfault....
	// #ifdef BACKEND_CPYTHON
	// 	// TODO: Do we need to deinit the interpreter ?
	// 	Py_FinalizeEx();
	// #endif
}

godot_bool _pythonscript_validate(const godot_string *p_script, int *r_line_error,
		int *r_col_error, godot_string *r_test_error,
		const godot_string *p_path, godot_pool_string_array *r_functions) {
	return true;
}

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

static void *libpython = NULL;

godot_pluginscript_language_desc godot_pluginscript_init(const godot_pluginscript_init_options *options) {
	// Must explicitly open libpython to load all of it symbols
	libpython = dlopen("libpython3.6m.so.1.0", RTLD_NOW | RTLD_GLOBAL);
	// TODO: Set PYTHONHOME according
	// const wchar_t *plugin_path = godot_string_unicode_str(->plugin_path);
	Py_SetPythonHome(L"/home/emmanuel/projects/godot-python/pythonscript/cpython/build");

	godot_pluginscript_language_desc desc = {
		// .data = NULL,
		.name = "Python",
		.type = "Python",
		.extension = "py",
		.recognized_extensions = PYTHONSCRIPT_RECOGNIZED_EXTENSIONS,
		.init = pybind_init,
		.finish = pybind_finish,
		.reserved_words = PYTHONSCRIPT_RESERVED_WORDS,
		.comment_delimiters = PYTHONSCRIPT_COMMENT_DELIMITERS,
		.string_delimiters = PYTHONSCRIPT_STRING_DELIMITERS,
		.get_template_source_code = pybind_get_template_source_code,
		.validate = _pythonscript_validate,

		.script_desc = {
			.init = pybind_script_init,
			.finish = pybind_script_finish,

			.instance_desc = {
				.init = pybind_instance_init,
				.finish = pybind_instance_finish,
				.set_prop = pybind_instance_set_prop,
				.get_prop = pybind_instance_get_prop,
				.call_method = pybind_instance_call_method,
				.notification = pybind_instance_notification,
				.refcount_incremented = NULL,
				.refcount_decremented = NULL
			}
		}
	};
	if (options->debug) {

		desc.get_template_source_code = pybind_get_template_source_code;
		desc.validate = pybind_validate;
		desc.find_function = pybind_find_function;
		desc.make_function = pybind_make_function;
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

		desc.profiling_start = pybind_profiling_start;
		desc.profiling_stop = pybind_profiling_stop;
		desc.profiling_get_accumulated_data = pybind_profiling_get_accumulated_data;
		desc.profiling_get_frame_data = pybind_profiling_get_frame_data;

		desc.frame = pybind_frame;
	}

	return desc;
}
