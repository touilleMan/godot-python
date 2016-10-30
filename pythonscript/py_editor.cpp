#include "globals.h"
#include "os/file_access.h"

#include "py_script_language.h"
// #include "py_script.h"


/* EDITOR FUNCTIONS */


void PyScriptLanguage::get_reserved_words(List<String> *p_words) const  {
// TODO update me !
#if 0
    static const char *_reserved_words[]={
        // operators
        "and",
        "in",
        "not",
        "or",
        // types and values
        "false",
        "float",
        "int",
        "bool",
        "null",
        "PI",
        "self",
        "true",
        // functions
        "assert",
        "breakpoint",
        "class",
        "extends",
        "func",
        "preload",
        "setget",
        "signal",
        "tool",
        "yield",
        // var
        "const",
        "enum",
        "export",
        "onready",
        "static",
        "var",
        // control flow
        "break",
        "continue",
        "if",
        "elif",
        "else",
        "for",
        "pass",
        "return",
        "while",
        "remote",
        "sync",
        "master",
        "slave",
        0};


    const char **w=_reserved_words;


    while (*w) {

        p_words->push_back(*w);
        w++;
    }

    for(int i=0;i<PyFunctions::FUNC_MAX;i++) {
        p_words->push_back(PyFunctions::get_func_name(PyFunctions::Function(i)));
    }
#endif
}


void PyScriptLanguage::get_comment_delimiters(List<String> *p_delimiters) const {
    p_delimiters->push_back("#");
    p_delimiters->push_back("\"\"\" \"\"\"");
}


void PyScriptLanguage::get_string_delimiters(List<String> *p_delimiters) const {
    p_delimiters->push_back("\" \"");
    p_delimiters->push_back("' '");
}


Ref<Script> PyScriptLanguage::get_template(const String& p_class_name, const String& p_base_class_name) const {
// TODO update me !
    String _template = String()+
    "\nextends %BASE%\n\n"+
    "# member variables here, example:\n"+
    "# var a=2\n"+
    "# var b=\"textvar\"\n\n"+
    "func _ready():\n"+
    "\t# Called every time the node is added to the scene.\n"+
    "\t# Initialization here\n"+
    "\tpass\n"+
    "\n"+
    "\n";

    _template = _template.replace("%BASE%",p_base_class_name);

    // Ref<PyScript> script;
    // script.instance();
    // script->set_source_code(_template);
    Ref<Script> script;

    return script;

}


bool PyScriptLanguage::validate(const String& p_script, int &r_line_error,int &r_col_error,String& r_test_error, const String& p_path,List<String> *r_functions) const {
    return true;
}


Script *PyScriptLanguage::create_script() const {
    // return memnew(PyScript);
    return NULL;
}


bool PyScriptLanguage::has_named_classes() const {
    return false;
}


int PyScriptLanguage::find_function(const String& p_function,const String& p_code) const {
    return -1;
}


String PyScriptLanguage::make_function(const String& p_class,const String& p_name,const StringArray& p_args) const {

    String s="def "+p_name+"(";
    if (p_args.size()) {
        s+=" ";
        for(int i=0;i<p_args.size();i++) {
            if (i>0)
                s+=", ";
            s+=p_args[i].get_slice(":",0);
        }
        s+=" ";
    }
    s+="):\n    pass # replace with function body\n";

    return s;

}


// Error PyScriptLanguage::complete_code(const String& p_code, const String& p_base_path, Object*p_owner, List<String>* r_options, String &r_call_hint) {
//     // Completion is for the weaks
//     return OK;
// }


void PyScriptLanguage::auto_indent_code(String& p_code,int p_from_line,int p_to_line) const {
// TODO ??
}


void PyScriptLanguage::add_global_constant(const StringName& p_variable,const Variant& p_value) {

}


/* LOADER FUNCTIONS */


void PyScriptLanguage::get_recognized_extensions(List<String> *p_extensions) const {

    p_extensions->push_back("py");
}


void PyScriptLanguage::get_public_functions(List<MethodInfo> *p_functions) const {
// TODO: improve ?
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


void PyScriptLanguage::get_public_constants(List<Pair<String,Variant> > *p_constants) const {
// TODO: improve ?
    Pair<String,Variant> pi;
    pi.first="PI";
    pi.second=Math_PI;
    p_constants->push_back(pi);
}


void PyScriptLanguage::profiling_start() {
#ifdef DEBUG_ENABLED
    // TODO
#endif
}


void PyScriptLanguage::profiling_stop() {
#ifdef DEBUG_ENABLED
    // TODO
#endif
}


int PyScriptLanguage::profiling_get_accumulated_data(ProfilingInfo *p_info_arr,int p_info_max) {
    int current=0;
#ifdef DEBUG_ENABLED
    // TODO
#endif
    return current;
}


int PyScriptLanguage::profiling_get_frame_data(ProfilingInfo *p_info_arr,int p_info_max) {
    int current=0;
#ifdef DEBUG_ENABLED
    // TODO
#endif
    return current;
}


void PyScriptLanguage::frame() {
#ifdef DEBUG_ENABLED
    // TODO
#endif
}
