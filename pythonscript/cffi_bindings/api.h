#ifndef PYTHONSCRIPT_API_H
#define PYTHONSCRIPT_API_H

#include "modules/gdnative/godot.h"
#include "pythonscript.h"
#include "cffi_bindings/api_struct.h"

typedef void *cffi_handle;

extern godot_bool pybind_init_sys_path_and_argv(const wchar_t *pythonpath, const wchar_t *res_path, const wchar_t *data_path);
extern void *pybind_load_exposed_class_per_module(const wchar_t *modname);
extern void py_instance_set_godot_obj(cffi_handle py_instance, godot_object *godot_obj);
extern cffi_handle instanciate_binding_from_godot_obj(cffi_handle py_cls, godot_object *godot_obj);
extern cffi_handle variants_to_pyobjs(void *args, int argcount);
extern cffi_handle variant_to_pyobj2(void *arg);
extern cffi_handle pyobj_to_variant2(cffi_handle arg);
extern godot_variant *call_with_variants(cffi_handle func, const godot_variant **args, int argcount);
extern void *pybind_instanciate_from_classname(const wchar_t *classname);
extern void *pybind_wrap_gdobj_with_class(void *cls_handle, void *owner);
extern void pybind_release_instance(void *handle);
extern void pybind_call_meth(void *handle, const wchar_t *methname, void **args, int argcount, void *ret, int *error);
extern godot_bool pybind_set_prop(void *handle, const wchar_t *propname, const godot_variant *value);
extern godot_bool pybind_get_prop(void *handle, const wchar_t *propname, godot_variant *ret);
extern godot_bool pybind_get_prop_type(void *handle, const wchar_t *propname, int *prop_type);
extern const godot_string *pybind_get_prop_list(void *handle);
extern godot_bool pybind_get_prop_default_value(void *handle, const wchar_t *propname, godot_variant *r_val);
extern godot_bool pybind_get_prop_info(void *handle, const wchar_t *propname, pybind_prop_info *r_prop_info);

#endif // PYTHONSCRIPT_API_H
