#include <iostream>
#include "pythonscript.h"


static void _pythonscript_init() {
	std::cout << "init pythonscript !\n";
}

static void _pythonscript_finish() {
	std::cout << "finish pythonscript !\n";
}

godot_error _pythonscript_execute_file(const godot_string *p_path) {
	// TODO ??
	return GODOT_OK;
}

godot_string _pythonscript_get_template_source_code(const godot_string *p_class_name, const godot_string *p_base_class_name) {
#if 0
	String _template = String() +
					   "from godot import exposed, export\n" +
					   "from godot.bindings import *\n" +
					   "\n\n" +
					   "@exposed\n" +
					   "class %CLS%(%BASE%):\n" +
					   "\n" +
					   "    # member variables here, example:\n" +
					   "    a = export(int)\n" +
					   "    b = export(str)\n" +
					   "\n" +
					   "    def _ready(self):\n" +
					   "        \"\"\"\n" +
					   "        Called every time the node is added to the scene.\n" +
					   "        Initialization here.\n" +
					   "        \"\"\"\n" +
					   "        pass\n";

	_template = _template.replace("%BASE%", p_base_class_name);
	if (p_class_name != "")
		_template = _template.replace("%CLS%", p_class_name);
	else
		_template = _template.replace("%CLS%", String("MyExportedCls"));

	Ref<PyScript> script;
	script.instance();
	script->set_source_code(_template);
#endif
	godot_string ret;
	// godot_string_new_unicode_data(&ret, "", 0);
	godot_string_new_data(&ret, "foo", 3);
	return ret;
}


godot_bool _pythonscript_validate(const godot_string *p_script, int *r_line_error, int *r_col_error, godot_string *r_test_error, const godot_string *p_path, godot_string *r_functions) {
	return true;
}


static const char *PYTHONSCRIPT_RECOGNIZED_EXTENSIONS[] = {"py", 0};
static const char *PYTHONSCRIPT_RESERVED_WORDS[] = {0};
static const char *PYTHONSCRIPT_COMMENT_DELIMITERS[] = {"#", "\"\"\"\"\"\"", 0};
static const char *PYTHONSCRIPT_STRING_DELIMITERS[] = {"\" \"", "' '", 0};

godot_pluginscript_script_handle _pythonscript_script_init() {
	return (godot_pluginscript_script_handle)NULL;
}

void _pythonscript_script_finish(godot_pluginscript_script_handle handle) {
	return;
}

godot_error _pythonscript_script_reload(godot_pluginscript_script_handle p_handle, godot_bool p_keep_state) {
	return GODOT_OK;
}

godot_bool _pythonscript_script_can_instance(godot_pluginscript_script_handle handle) {
	return true;
}

godot_pluginscript_language_desc_t *godot_pluginscript_init() {
	static godot_pluginscript_language_desc_t desc = {
		.name="Python",
		.type="Python",
		.extension="py",
		.recognized_extensions=PYTHONSCRIPT_RECOGNIZED_EXTENSIONS,
		.init=_pythonscript_init,
		.finish=_pythonscript_finish,
		.reserved_words=PYTHONSCRIPT_RESERVED_WORDS,
		.comment_delimiters=PYTHONSCRIPT_COMMENT_DELIMITERS,
		.string_delimiters=PYTHONSCRIPT_STRING_DELIMITERS,
		.execute_file=_pythonscript_execute_file,
		.get_template_source_code=_pythonscript_get_template_source_code,
		.validate=_pythonscript_validate,

		.script_desc={
			.init=_pythonscript_script_init,
			.finish=_pythonscript_script_finish,
			.reload=_pythonscript_script_reload,
			.can_instance=_pythonscript_script_can_instance
		}
	};
	return &desc;
}
