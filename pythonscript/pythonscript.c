#include "Python.h"

#include <dlfcn.h>
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

void godot_gdnative_init(godot_gdnative_init_options *options) {
	GDNATIVE_API_INIT(options);
	godot_string msg;
	godot_string_new_data(&msg, "Hello world from Pythonscript !", -1);
	godot_print(&msg);

#if 1

#ifdef BACKEND_CPYTHON

	// Make sure the shared library has all it symbols loaded
	// (strange bug with libpython3.6 otherwise...)
	const char *libpath = "/home/emmanuel/projects/godot_test_gdnative/pythonscript/libpython3.6m.so.1.0";
	void *lib = dlopen(libpath, RTLD_NOW | RTLD_GLOBAL);
	const char *err = dlerror();
	// dlopen(godot_string_c_str(options->active_library_path), RTLD_NOW | RTLD_GLOBAL);

	// Retrieve path and set pythonhome
	static wchar_t pythonhome[256];
	godot_string _pythonhome = godot_string_get_base_dir(options->active_library_path);
	wcsncpy(pythonhome, godot_string_unicode_str(&_pythonhome), 256);
	godot_string_destroy(&_pythonhome);
	Py_SetPythonHome(pythonhome);
#endif

	static godot_pluginscript_language_desc desc = {
		.name = "Python",
		.type = "Python",
		.extension = "py",
		.recognized_extensions = PYTHONSCRIPT_RECOGNIZED_EXTENSIONS,
		.init = pybind_init,
		.finish = pybind_finish,
		.reserved_words = PYTHONSCRIPT_RESERVED_WORDS,
		.comment_delimiters = PYTHONSCRIPT_COMMENT_DELIMITERS,
		.string_delimiters = PYTHONSCRIPT_STRING_DELIMITERS,
		.has_named_classes = false,
		.get_template_source_code = pybind_get_template_source_code,

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

		desc.profiling_start = pybind_profiling_start;
		desc.profiling_stop = pybind_profiling_stop;
		desc.profiling_get_accumulated_data = pybind_profiling_get_accumulated_data;
		desc.profiling_get_frame_data = pybind_profiling_get_frame_data;
		// TODO: avoid to go through cffi call if profiling is not on
		desc.profiling_frame = pybind_profiling_frame;
	}
#endif
	godot_pluginscript_register_language(&desc);
}

void godot_gdnative_terminate() {
}
