#ifndef PYTHONSCRIPT_API_H
#define PYTHONSCRIPT_API_H

#include "modules/gdnative/godot/gdnative.h"
#include "modules/pluginscript/pluginscript.h"
#include "cffi_bindings/api_struct.h"

typedef void *cffi_handle;

extern void pybind_init();
extern void pybind_get_template_source_code(const godot_string *class_name, const godot_string *base_class_name, godot_string *r_src);
extern void pybind_add_global_constant(const godot_string *p_variable, const godot_variant *p_value);

extern godot_string pybind_debug_get_error();
extern int pybind_debug_get_stack_level_count();
extern int pybind_debug_get_stack_level_line(int p_level);
extern godot_string pybind_debug_get_stack_level_function(int p_level);
extern godot_string pybind_debug_get_stack_level_source(int p_level);
extern void pybind_debug_get_stack_level_locals(int p_level, godot_pool_string_array *p_locals, godot_array *p_values, int p_max_subitems, int p_max_depth);
extern void pybind_debug_get_stack_level_members(int p_level, godot_pool_string_array *p_members, godot_array *p_values, int p_max_subitems, int p_max_depth);
extern void pybind_debug_get_globals(godot_pool_string_array *p_locals, godot_array *p_values, int p_max_subitems, int p_max_depth);
extern godot_string pybind_debug_parse_stack_level_expression(int p_level, const godot_string *p_expression, int p_max_subitems, int p_max_depth);

extern void pybind_profiling_start();
extern void pybind_profiling_stop();
extern int pybind_profiling_get_accumulated_data(godot_dictionary *p_info_arr, int p_info_max);
extern int pybind_profiling_get_frame_data(godot_dictionary *p_info_arr, int p_info_max);

extern void pybind_frame();

extern godot_pluginscript_script_manifest pybind_script_init(const godot_string *path, const godot_string *source, godot_error *r_error);
extern void pybind_script_finish(godot_pluginscript_script_handle handle);
extern void pybind_script_get_name(godot_pluginscript_script_handle handle, godot_string *r_name);
extern godot_bool pybind_script_is_tool(godot_pluginscript_script_handle handle);
extern godot_bool pybind_script_can_instance(godot_pluginscript_script_handle handle);

extern godot_pluginscript_instance_handle pybind_instance_init(godot_pluginscript_script_handle, godot_object *);
extern void pybind_instance_finish(godot_pluginscript_instance_handle);

extern godot_bool pybind_instance_set_prop(godot_pluginscript_instance_handle handle, const godot_string *p_name, const godot_variant *p_value);
extern godot_bool pybind_instance_get_prop(godot_pluginscript_instance_handle handle, const godot_string *p_name, godot_variant *r_ret);
extern void pybind_instance_notification(godot_pluginscript_instance_handle handle, int notification);
extern godot_variant pybind_instance_call_method(godot_pluginscript_instance_handle handle, const godot_string *p_method, const godot_variant **p_args, int p_argcount, godot_variant_call_error *r_error);

#endif // PYTHONSCRIPT_API_H
