#include <dlfcn.h>
#include "pythonscript.h"
#include "Python.h"
#include "cffi_bindings/api.h"

// Language

static void _pythonscript_finish() {
	// TODO: Anyway, this cause a segfault....
// #ifdef BACKEND_CPYTHON
// 	// TODO: Do we need to deinit the interpreter ?
// 	Py_FinalizeEx();
// #endif
}

godot_bool _pythonscript_validate(const godot_string *p_script, int *r_line_error,
	                              int *r_col_error, godot_string *r_test_error,
	                              const godot_string *p_path, godot_string *r_functions) {
	return true;
}

// Instance

godot_method_rpc_mode _pythonscript_instance_get_rpc_mode(godot_pluginscript_instance_handle handle, const godot_string *p_method) {
	return GODOT_METHOD_RPC_MODE_DISABLED;
}

godot_method_rpc_mode _pythonscript_instance_get_rset_mode(godot_pluginscript_instance_handle handle, const godot_string *p_variable) {
	return GODOT_METHOD_RPC_MODE_DISABLED;
}

void _pythonscript_instance_refcount_incremented() {
}

bool _pythonscript_instance_refcount_decremented() {
	return true;
}


// Final stuff

static const char *PYTHONSCRIPT_RECOGNIZED_EXTENSIONS[] = {"py", "pyc", "pyo", "pyd", 0};
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
static const char *PYTHONSCRIPT_COMMENT_DELIMITERS[] = {"#", "\"\"\"\"\"\"", 0};
static const char *PYTHONSCRIPT_STRING_DELIMITERS[] = {"\" \"", "' '", 0};


static void *libpython = NULL;


godot_pluginscript_language_desc_t *godot_pluginscript_init(const godot_pluginscript_init_options *options) {
	// Must explicitly open libpython to load all of it symbols
	libpython = dlopen("libpython3.6m.so.1.0", RTLD_NOW | RTLD_GLOBAL);
	// TODO: Set PYTHONHOME according
	// const wchar_t *plugin_path = godot_string_unicode_str(->plugin_path);
    Py_SetPythonHome(L"/home/emmanuel/projects/godot-python/pythonscript/cpython/build");

	static godot_pluginscript_language_desc_t desc = {
		.name="Python",
		.type="Python",
		.extension="py",
		.recognized_extensions=PYTHONSCRIPT_RECOGNIZED_EXTENSIONS,
		.init=pybind_init,
		.finish=_pythonscript_finish,
		.reserved_words=PYTHONSCRIPT_RESERVED_WORDS,
		.comment_delimiters=PYTHONSCRIPT_COMMENT_DELIMITERS,
		.string_delimiters=PYTHONSCRIPT_STRING_DELIMITERS,
		.get_template_source_code=pybind_get_template_source_code,
		.validate=_pythonscript_validate,

		.script_desc={
			.init=pybind_script_init,
			.finish=pybind_script_finish,

			.instance_desc={
				.init=pybind_instance_init,
				.finish=pybind_instance_finish,
				.set_prop=pybind_instance_set_prop,
				.get_prop=pybind_instance_get_prop,
				.call_method=pybind_instance_call_method,
				.notification=pybind_instance_notification,
				.refcount_incremented=NULL,
				.refcount_decremented=NULL
			}
		}
	};
	return &desc;
}
