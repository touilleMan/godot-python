#include "globals.h"

#include "py_script_language.h"


/* DEBUGGER FUNCTIONS */


String PyScriptLanguage::debug_get_error() const {
    return String("Nothing");
}


int PyScriptLanguage::debug_get_stack_level_count() const {
    return 1;
}


int PyScriptLanguage::debug_get_stack_level_line(int p_level) const {
    return 1;
}


String PyScriptLanguage::debug_get_stack_level_function(int p_level) const {
    return String("Nothing");
}


String PyScriptLanguage::debug_get_stack_level_source(int p_level) const {
    return String("Nothing");
}


void PyScriptLanguage::debug_get_stack_level_locals(int p_level, List<String> *p_locals, List<Variant> *p_values, int p_max_subitems, int p_max_depth) {

}


void PyScriptLanguage::debug_get_stack_level_members(int p_level, List<String> *p_members, List<Variant> *p_values, int p_max_subitems, int p_max_depth) {

}


void PyScriptLanguage::debug_get_globals(List<String> *p_locals, List<Variant> *p_values, int p_max_subitems, int p_max_depth) {

}


String PyScriptLanguage::debug_parse_stack_level_expression(int p_level, const String& p_expression, int p_max_subitems, int p_max_depth) {
    return String("Nothing");
}



void PyScriptLanguage::reload_all_scripts() {

}


void PyScriptLanguage::reload_tool_script(const Ref<Script>& p_script, bool p_soft_reload) {

}
