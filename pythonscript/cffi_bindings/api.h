#ifndef PYTHONSCRIPT_API_H
#define PYTHONSCRIPT_API_H

#include "modules/gdnative/godot.h"
#include "pythonscript.h"
#include "cffi_bindings/api_struct.h"

typedef void *cffi_handle;

extern godot_bool pybind_init_sys_path_and_argv(const wchar_t *pythonpath, const wchar_t *res_path, const wchar_t *data_path);
extern cffi_handle pybind_load_exposed_class_per_module(const wchar_t *modname);
extern cffi_handle pybind_instanciate_from_classname(const wchar_t *classname);
extern cffi_handle pybind_wrap_gdobj_with_class(cffi_handle cls_handle, void *gdobj);
extern void pybind_release_instance(cffi_handle handle);
extern void pybind_call_meth(cffi_handle handle, const wchar_t *methname, void **args, int argcount, void *ret, int *error);
extern godot_bool pybind_set_prop(cffi_handle handle, const wchar_t *propname, const godot_variant *value);
extern godot_bool pybind_get_prop(cffi_handle handle, const wchar_t *propname, godot_variant *ret);
extern godot_bool pybind_get_prop_type(cffi_handle handle, const wchar_t *propname, int *prop_type);
extern const godot_string *pybind_get_prop_list(cffi_handle handle);
extern godot_bool pybind_get_prop_default_value(cffi_handle handle, const wchar_t *propname, godot_variant *r_val);
extern godot_bool pybind_get_prop_info(cffi_handle handle, const wchar_t *propname, pybind_prop_info *r_prop_info);
extern void pybind_notification(cffi_handle handle, int notification);

#endif // PYTHONSCRIPT_API_H
