#ifndef PYTHONSCRIPT_API_H
#define PYTHONSCRIPT_API_H

#include <gdnative_api_struct.gen.h>
#include "cffi_bindings/api_struct.h"

typedef void *cffi_handle;

extern godot_pluginscript_language_data *pybind_init();
extern void pybind_finish(godot_pluginscript_language_data *p_data);

extern godot_string pybind_get_template_source_code(godot_pluginscript_language_data *p_data, const godot_string *p_class_name, const godot_string *p_base_class_name);
extern godot_bool pybind_validate(godot_pluginscript_language_data *p_data, const godot_string *p_script, int *r_line_error, int *r_col_error, godot_string *r_test_error, const godot_string *p_path, godot_pool_string_array *r_functions);
extern int pybind_find_function(godot_pluginscript_language_data *p_data, const godot_string *p_function, const godot_string *p_code);
extern godot_string pybind_make_function(godot_pluginscript_language_data *p_data, const godot_string *p_class, const godot_string *p_name, const godot_pool_string_array *p_args);
extern godot_error pybind_complete_code(godot_pluginscript_language_data *p_data, const godot_string *p_code, const godot_string *p_base_path, godot_object *p_owner, godot_array *r_options, godot_bool *r_force, godot_string *r_call_hint);
extern void pybind_auto_indent_code(godot_pluginscript_language_data *p_data, godot_string *p_code, int p_from_line, int p_to_line);

extern void pybind_add_global_constant(godot_pluginscript_language_data *p_data, const godot_string *p_variable, const godot_variant *p_value);
extern godot_string pybind_debug_get_error(godot_pluginscript_language_data *p_data);
extern int pybind_debug_get_stack_level_count(godot_pluginscript_language_data *p_data);
extern int pybind_debug_get_stack_level_line(godot_pluginscript_language_data *p_data, int p_level);
extern godot_string pybind_debug_get_stack_level_function(godot_pluginscript_language_data *p_data, int p_level);
extern godot_string pybind_debug_get_stack_level_source(godot_pluginscript_language_data *p_data, int p_level);
extern void pybind_debug_get_stack_level_locals(godot_pluginscript_language_data *p_data, int p_level, godot_pool_string_array *p_locals, godot_array *p_values, int p_max_subitems, int p_max_depth);
extern void pybind_debug_get_stack_level_members(godot_pluginscript_language_data *p_data, int p_level, godot_pool_string_array *p_members, godot_array *p_values, int p_max_subitems, int p_max_depth);
extern void pybind_debug_get_globals(godot_pluginscript_language_data *p_data, godot_pool_string_array *p_locals, godot_array *p_values, int p_max_subitems, int p_max_depth);
extern godot_string pybind_debug_parse_stack_level_expression(godot_pluginscript_language_data *p_data, int p_level, const godot_string *p_expression, int p_max_subitems, int p_max_depth);

extern void pybind_profiling_start(godot_pluginscript_language_data *p_data);
extern void pybind_profiling_stop(godot_pluginscript_language_data *p_data);
extern int pybind_profiling_get_accumulated_data(godot_pluginscript_language_data *p_data, godot_pluginscript_profiling_data *r_info, int p_info_max);
extern int pybind_profiling_get_frame_data(godot_pluginscript_language_data *p_data, godot_pluginscript_profiling_data *r_info, int p_info_max);

extern void pybind_profiling_frame(godot_pluginscript_language_data *p_data);

extern godot_pluginscript_script_manifest pybind_script_init(godot_pluginscript_language_data *p_data, const godot_string *path, const godot_string *source, godot_error *r_error);
extern void pybind_script_finish(godot_pluginscript_script_data *handle);
extern void pybind_script_get_name(godot_pluginscript_script_data *handle, godot_string *r_name);
extern godot_bool pybind_script_is_tool(godot_pluginscript_script_data *handle);
extern godot_bool pybind_script_can_instance(godot_pluginscript_script_data *handle);

extern godot_pluginscript_instance_data *pybind_instance_init(godot_pluginscript_script_data *, godot_object *);
extern void pybind_instance_finish(godot_pluginscript_instance_data *);

extern godot_bool pybind_instance_set_prop(godot_pluginscript_instance_data *handle, const godot_string *p_name, const godot_variant *p_value);
extern godot_bool pybind_instance_get_prop(godot_pluginscript_instance_data *handle, const godot_string *p_name, godot_variant *r_ret);
extern void pybind_instance_notification(godot_pluginscript_instance_data *handle, int notification);
extern godot_variant pybind_instance_call_method(godot_pluginscript_instance_data *handle, const godot_string_name *p_method, const godot_variant **p_args, int p_argcount, godot_variant_call_error *r_error);

#endif // PYTHONSCRIPT_API_H
