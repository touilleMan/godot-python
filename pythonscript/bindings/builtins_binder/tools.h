#ifndef BUILTINS_TOOLS_H
#define BUILTINS_TOOLS_H

#include "micropython.h"
// Godot imports

// Pythonscript imports
#include "bindings/dynamic_binder.h"
#include "bindings/tools.h"

#define BIND_PROPERTY_GET(NAME, GETTER) {\
    auto o = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    o->base.type = &mp_type_fun_builtin_1; \
    o->fun._1 = GETTER; \
    mp_obj_t property = mp_call_function_1(MP_OBJ_FROM_PTR(&mp_type_property), o); \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, property); \
}


#define BIND_PROPERTY_GETSET(NAME, GETTER, SETTER) {\
    auto g = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    g->base.type = &mp_type_fun_builtin_1; \
    g->fun._1 = GETTER; \
    auto s = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    s->base.type = &mp_type_fun_builtin_2; \
    s->fun._2 = SETTER; \
    mp_obj_t property = mp_call_function_2(MP_OBJ_FROM_PTR(&mp_type_property), g, s); \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, property); \
}


#define BIND_METHOD(NAME, CB) {\
    auto o = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    o->base.type = &mp_type_fun_builtin_1; \
    o->fun._1 = CB; \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, o); \
}


#define BIND_METHOD_1(NAME, CB) {\
    auto o = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    o->base.type = &mp_type_fun_builtin_2; \
    o->fun._2 = CB; \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, o); \
}


#define BIND_METHOD_2(NAME, CB) {\
    auto o = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    o->base.type = &mp_type_fun_builtin_3; \
    o->fun._3 = CB; \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, o); \
}


#define BIND_METHOD_VAR(NAME, CB, ARG_MIN, ARG_MAX) {\
    auto o = m_new_obj(mp_obj_fun_builtin_var_t); \
    o->base.type = &mp_type_fun_builtin_var; \
    o->is_kw = false; \
    o->n_args_min = ARG_MIN; \
    o->n_args_max = ARG_MAX; \
    o->fun.var = CB; \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, o); \
}


static Variant RETRIEVE_ARG(BaseBinder *type_binder, mp_obj_t var, const char *var_name) {
    if (!type_binder->is_type(var)) {
        char buff[64];
        snprintf(buff, sizeof(buff), "%s type must be %s", var_name, type_binder->get_type_str());
        mp_raise_TypeError(buff);
    }
    return type_binder->pyobj_to_variant(var);
}


#endif // BUILTINS_TOOLS_H
