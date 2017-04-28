// Pythonscript imports
#include "py_language.h"
#include "py_script.h"
// Godot imports
#include "core/os/file_access.h"

/* EDITOR FUNCTIONS */

void PyLanguage::get_reserved_words(List<String> *p_words) const {
	static const char *_reserved_words[] = {
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

	const char **w = _reserved_words;

	while (*w) {

		p_words->push_back(*w);
		w++;
	}

	// TODO add get_public_functions/get_public_constants ?
	// for(int i=0;i<PyFunctions::FUNC_MAX;i++) {
	//     p_words->push_back(PyFunctions::get_func_name(PyFunctions::Function(i)));
	// }
}

void PyLanguage::get_comment_delimiters(List<String> *p_delimiters) const {
	p_delimiters->push_back("#");
	p_delimiters->push_back("\"\"\" \"\"\"");
}

void PyLanguage::get_string_delimiters(List<String> *p_delimiters) const {
	p_delimiters->push_back("\" \"");
	p_delimiters->push_back("' '");
}

Ref<Script> PyLanguage::get_template(const String &p_class_name, const String &p_base_class_name) const {
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

	return script;
}

bool PyLanguage::validate(const String &p_script, int &r_line_error, int &r_col_error, String &r_test_error, const String &p_path, List<String> *r_functions) const {
	return true;
}

Script *PyLanguage::create_script() const {
	return memnew(PyScript);
}

bool PyLanguage::has_named_classes() const {
	return false;
}

int PyLanguage::find_function(const String &p_function, const String &p_code) const {
	return -1;
}

String PyLanguage::make_function(const String &p_class, const String &p_name, const PoolStringArray &p_args) const {

	String s = "def " + p_name + "(";
	if (p_args.size()) {
		s += " ";
		for (int i = 0; i < p_args.size(); i++) {
			if (i > 0)
				s += ", ";
			s += p_args[i].get_slice(":", 0);
		}
		s += " ";
	}
	s += "):\n    pass # replace with function body\n";

	return s;
}

// Error PyLanguage::complete_code(const String& p_code, const String& p_base_path, Object*p_owner, List<String>* r_options, String &r_call_hint) {
//     // Completion is for the weaks
//     return OK;
// }

void PyLanguage::auto_indent_code(String &p_code, int p_from_line, int p_to_line) const {
	// TODO ??
}

void PyLanguage::add_global_constant(const StringName &p_variable, const Variant &p_value) {
}

/* LOADER FUNCTIONS */

void PyLanguage::get_recognized_extensions(List<String> *p_extensions) const {

	p_extensions->push_back("py");
}

void PyLanguage::get_public_functions(List<MethodInfo> *p_functions) const {
// TODO: Display builtins module ?
// Seems to be only used for documentation (doc_data.cpp)
#if 0
    for(int i=0;i<PyFunctions::FUNC_MAX;i++) {

        p_functions->push_back(PyFunctions::get_info(PyFunctions::Function(i)));
    }

    //not really "functions", but..
    {
        MethodInfo mi;
        mi.name="preload:Resource";
        mi.arguments.push_back(PropertyInfo(Variant::STRING,"path"));
        mi.return_val=PropertyInfo(Variant::OBJECT,"",PROPERTY_HINT_RESOURCE_TYPE,"Resource");
        p_functions->push_back(mi);
    }
    {
        MethodInfo mi;
        mi.name="yield:GDFunctionState";
        mi.arguments.push_back(PropertyInfo(Variant::OBJECT,"object"));
        mi.arguments.push_back(PropertyInfo(Variant::STRING,"signal"));
        mi.default_arguments.push_back(Variant::NIL);
        mi.default_arguments.push_back(Variant::STRING);
        p_functions->push_back(mi);
    }
    {
        MethodInfo mi;
        mi.name="assert";
        mi.arguments.push_back(PropertyInfo(Variant::BOOL,"condition"));
        p_functions->push_back(mi);
    }
#endif
}

void PyLanguage::get_public_constants(List<Pair<String, Variant> > *p_constants) const {
// TODO: Display builtins module ?
// Seems to be only used for documentation (doc_data.cpp)
#if 0
    Pair<String,Variant> pi;
    pi.first="PI";
    pi.second=Math_PI;
    p_constants->push_back(pi);
#endif
}

void PyLanguage::profiling_start() {
#ifdef DEBUG_ENABLED
// TODO
#endif
}

void PyLanguage::profiling_stop() {
#ifdef DEBUG_ENABLED
// TODO
#endif
}

int PyLanguage::profiling_get_accumulated_data(ProfilingInfo *p_info_arr, int p_info_max) {
	int current = 0;
#ifdef DEBUG_ENABLED
// TODO
#endif
	return current;
}

int PyLanguage::profiling_get_frame_data(ProfilingInfo *p_info_arr, int p_info_max) {
	int current = 0;
#ifdef DEBUG_ENABLED
// TODO
#endif
	return current;
}

void PyLanguage::frame() {
#ifdef DEBUG_ENABLED
// TODO
#endif
}
