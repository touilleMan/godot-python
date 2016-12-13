#ifndef GODOT_TYPE_BINDER_H
#define GODOT_TYPE_BINDER_H


#include "micropython.h"
// Godot imports
#include "core/map.h"
#include "core/object.h"
#include "core/object_type_db.h"
#include "core/string_db.h"
// Pythonscript imports
#include "bindings/converter.h"


namespace pythonscript { namespace bindings {

// Mainly used to have a common class for all types binder in order to store
// them together in a map
class BaseGodotTypeBinder {
};


template<class T>
class GodotTypeBinder : public BaseGodotTypeBinder {

private:
    const StringName name;
    // const qstr qstr_name;  # TODO: useful ?
    // GodotTypeBinder *parent;  # TODO: useful ?
    Map<qstr, mp_obj_t> method_lookup;
    Map<qstr, PropertyInfo> property_lookup;

    // Type object of this godot type in python
    mp_obj_type_t mp_type;

    static mp_obj_t _wrap_godot_method(StringName p_name) {
        // TODO: micropython doesn't allow to store a name for native functions
        // TODO: don't use `m_new_obj` but good old' `malloc` to avoid useless
        // python gc work on those stay-forever functions
        auto p_method_bind = ObjectTypeDB::get_method(T::get_type_static(), p_name);
        // Godot doesn't count self as an argument so python has one more
        switch (p_method_bind->get_argument_count()) {
            case 0:
            {
                auto o = m_new_obj(mp_obj_fun_builtin_fixed_t);
                o->base.type = &mp_type_fun_builtin_1;
                if (p_method_bind->has_return()) {
                    o->fun._1 = [](mp_obj_t self_in) -> mp_obj_t {
                        auto self = static_cast<mp_instance_t *>(self_in);
                        Variant::CallError err;
                        p_method_bind->call(self->godot_obj, NULL, 0, err);
                        if (err.error != Variant::CallError::CALL_OK) {
                            // Throw exception
                            // TODO: improve error message...
                            nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "Tough shit dude..."));
                        }
                        return mp_const_none;
                    };
                } else {
                    o->fun._1 = [](mp_obj_t self_in) -> mp_obj_t {
                        auto self = static_cast<mp_instance_t *>(self_in);
                        Variant::CallError err;
                        auto ret = p_method_bind->call(self->godot_obj, NULL, 0, err);
                        if (err.error != Variant::CallError::CALL_OK) {
                            // Throw exception
                            // TODO: improve error message...
                            nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "Tough shit dude..."));
                        }
                        // TODO: optimize conversion using return_val
                        return variant_to_pyobj(ret);
                    };
                }
                return o;
            }
            case 1:
            {
                auto o = m_new_obj(mp_obj_fun_builtin_fixed_t);
                o->base.type = &mp_type_fun_builtin_2;
                o->fun._2 = [](mp_obj_t self_in, mp_obj_t arg1) -> mp_obj_t {
                    nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "Not implemented yet"));
                    return mp_const_none;
                };
                return o;
            }
            case 2:
            {
                auto o = m_new_obj(mp_obj_fun_builtin_fixed_t);
                o->base.type = &mp_type_fun_builtin_3;
                o->fun._3 = [](mp_obj_t self_in, mp_obj_t arg1, mp_obj_t arg2) -> mp_obj_t {
                    nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "Not implemented yet"));
                    return mp_const_none;
                };
                return o;
            }
            default:
            {
                auto o = m_new_obj(mp_obj_fun_builtin_var_t);
                o->base.type = &mp_type_fun_builtin_var;
                o->is_kw = false;
                o->n_args_min = p_method_bind->get_argument_count();
                o->n_args_max = p_method_bind->get_argument_count();
                o->fun.var = [](size_t n, const mp_obj_t *, mp_map_t *) -> mp_obj_t {
                    nlr_raise(mp_obj_new_exception_msg(&mp_type_RuntimeError, "Not implemented yet"));
                    return mp_const_none;
                };
                return o;
            }
        }
    }

    // mp_obj_t _make_new_from_python(const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) {
    //     mp_arg_check_num(n_args, n_kw, 0, 0, false);
    //     return this->make_new();
    // };

public:

    // Struture representing a single instance of this godot type in python
    typedef struct {
        mp_obj_base_t base;
        T *godot_obj;
    } mp_instance_t;

    GodotTypeBinder() : name(T::get_type_static()) {};

    inline mp_obj_type_t *get_mp_obj_type() { return &this->mp_type; };

    void init() {
        // Retrieve method&property from ObjectTypeDB and cook what can
        // be for faster runtime lookup
        // TODO: get inherited properties/methods as well ?
        List<PropertyInfo> properties;
        ObjectTypeDB::get_property_list(this->name, &properties, true);
        for(List<PropertyInfo>::Element *E=properties.front();E;E=E->next()) {
            const PropertyInfo info = E->get();
            this->property_lookup.insert(qstr_from_str(info.name.utf8().get_data()), info);
        }
        List<MethodInfo> methods;
        ObjectTypeDB::get_method_list(this->name, &methods, true);
        for(List<MethodInfo>::Element *E=methods.front();E;E=E->next()) {
            const MethodInfo info = E->get();
            const auto qstr_name = qstr_from_str(info.name.utf8().get_data());
            const auto mpo_method = this->_wrap_godot_method(info.name);
            this->method_lookup.insert(qstr_name, mpo_method);
        }

        // Build micropython type object
        // auto make_new = [this](const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) -> mp_obj_t {
        //     mp_arg_check_num(n_args, n_kw, 0, 0, false);
        //     return (void *)this->make_new();
        // };
        auto make_new2 = [this](const mp_obj_type_t *type, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) -> mp_obj_t { return mp_const_none; };

        auto attr = [this](mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
            return this->instance_attr_lookup(self_in, attr, dest);
        };

        const String s_name = String(this->name);
        // this->mp_type = {
        //     { &mp_type_type },
        //     .name = qstr_from_str(s_name.utf8().get_data()),
        //     .make_new = make_new,
        //     .attr = attr,
        //     .protocol = static_cast<void *>(this)
        // };
        this->mp_type.base.type = &mp_type_type;
        this->mp_type.name = qstr_from_str(s_name.utf8().get_data());
        this->mp_type.make_new = make_new2;
        this->mp_type.attr = attr;
        this->mp_type.protocol = static_cast<void *>(this);
    }

    inline mp_obj_t make_new() {
        return this->make_new(memnew(T));
    }

    mp_obj_t make_new(T *godot_obj) {
        mp_instance_t *obj = m_new_obj_with_finaliser(mp_instance_t);
        obj->base.type = &GodotTypeBinder::mp_type;
        obj->godot_obj = godot_obj;
        return MP_OBJ_FROM_PTR(obj);
    }

    void instance_attr_lookup(mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
        auto o = static_cast<mp_instance_t *>(self_in);
        // Try to retrieve the attr as a method
        auto E = this->method_lookup.find(attr);
        if (E != NULL) {
            // attr is a method
            if (dest[0] == MP_OBJ_NULL) {
                // do a load
                dest[0] = E->get();
                dest[1] = self_in;
            }
    #if 0
        } else {
            // TODO
            // We consider attr is a property
            if (dest[0] == MP_OBJ_NULL) {
                // do a load
                Variant r_value;
                if (ObjectTypeDB::get_property(o->godot_obj->ptr(), attr_name, r_value)) {
                    // attr was actually a property
                    // TODO:convert r_value to py object
                    dest[0] = mp_const_none;
                }
            } else if (dest[1] != MP_OBJ_NULL) {
                // do a store
                bool r_valid = false;
                // TODO: convert dest[1] to variant
                Variant value = Variant(true);
                if (ObjectTypeDB::set_property(o->godot_obj->ptr(), attr_name, value, r_valid) && r_valid) {
                    // attr was actually a property
                    dest[0] = MP_OBJ_NULL;
                }
            }
    #endif
        }
        // All other cases fail (i.e. don't modify `dest`)        
    }
};

void godot_binding_module_init();
void godot_binding_module_finish();

} }  // namespace

#endif  // GODOT_TYPE_BINDER_H
