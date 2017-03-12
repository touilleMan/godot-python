// Pythonscript imports
#include "py_language.h"


/* DEBUGGER FUNCTIONS */


String PyLanguage::debug_get_error() const {
    return String("Nothing");
}


int PyLanguage::debug_get_stack_level_count() const {
    return 1;
}


int PyLanguage::debug_get_stack_level_line(int p_level) const {
    return 1;
}


String PyLanguage::debug_get_stack_level_function(int p_level) const {
    return String("Nothing");
}


String PyLanguage::debug_get_stack_level_source(int p_level) const {
    return String("Nothing");
}


void PyLanguage::debug_get_stack_level_locals(int p_level, List<String> *p_locals, List<Variant> *p_values, int p_max_subitems, int p_max_depth) {

}


void PyLanguage::debug_get_stack_level_members(int p_level, List<String> *p_members, List<Variant> *p_values, int p_max_subitems, int p_max_depth) {

}


void PyLanguage::debug_get_globals(List<String> *p_locals, List<Variant> *p_values, int p_max_subitems, int p_max_depth) {

}


String PyLanguage::debug_parse_stack_level_expression(int p_level, const String& p_expression, int p_max_subitems, int p_max_depth) {
    return String("Nothing");
}



void PyLanguage::reload_all_scripts() {

}


void PyLanguage::reload_tool_script(const Ref<Script>& p_script, bool p_soft_reload) {

}
