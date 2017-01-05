#include <stdio.h>

#include "bindings/builtins_binder.h"


#define BIND_METHOD(NAME, CB) {\
    auto o = m_new_obj(mp_obj_fun_builtin_fixed_t); \
    o->base.type = &mp_type_fun_builtin_1; \
    o->fun._1 = CB; \
    auto n = MP_OBJ_NEW_QSTR(qstr_from_str(NAME)); \
    mp_obj_dict_store(locals_dict, n, o); \
}


mp_obj_t Vector2Binder::_generate_bind_locals_dict() {
    // Build micropython type object
    mp_obj_t locals_dict = mp_obj_new_dict(0);

#if 0
    // Vector2 Vector2 ( float x, float y )
    BIND_METHOD("__init__", [](mp_obj_t self, mp_obj_t x, mp_obj_t y) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        auto bindings = GodotBindingsModule::get_singleton();
        variant->godot_vect2.x = bindings->pyobj_to_variant(x);
        variant->godot_vect2.y = bindings->pyobj_to_variant(y);
        return mp_const_none;
    });
#endif
    // Vector2 abs ( )
    BIND_METHOD("abs", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 vect2_abs = variant->godot_vect2.abs();
        return Vector2Binder::get_singleton()->build_pyobj(vect2_abs);
    });

    // float   angle ( )
    BIND_METHOD("angle", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float angle = variant->godot_vect2.angle();
        return RealBinder::get_singleton()->build_pyobj(angle);
    });
    // auto o = m_new_obj(mp_obj_fun_builtin_fixed_t);
    // o->base.type = &mp_type_fun_builtin_1;
    // o->fun._1 = [](mp_obj_t self) -> mp_obj_t {
    //     auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
    //     auto ret = variant->godot_vect2.abs();
    //     return this->build_pyobj(ret);
    // }
    // auto n = MP_OBJ_NEW_QSTR(qstr_from_str("abs"))
    // mp_obj_dict_store(locals_dict, n, o);

    // float   angle_to ( Vector2 to )
    // float   angle_to_point ( Vector2 to )
    // Vector2 clamped ( float length )
    // Vector2 cubic_interpolate ( Vector2 b, Vector2 pre_a, Vector2 post_b, float t )
    // float   distance_squared_to ( Vector2 to )
    // float   distance_to ( Vector2 to )
    // float   dot ( Vector2 with )
    // Vector2 floor ( )
    // Vector2 floorf ( )
    // float   get_aspect ( )
    // float   length ( )
    // float   length_squared ( )
    // Vector2 linear_interpolate ( Vector2 b, float t )
    // Vector2 normalized ( )
    // Vector2 reflect ( Vector2 vec )
    // Vector2 rotated ( float phi )
    // Vector2 slide ( Vector2 vec )
    // Vector2 snapped ( Vector2 by )
    // Vector2 tangent ( )

    return locals_dict;
}


static void _print_vector2(const mp_print_t *print, mp_obj_t o, mp_print_kind_t kind) {
    auto self = static_cast<Vector2Binder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(o));
    char buff[64];
    sprintf(buff, "<Vector2(x=%f, y=%f)>", self->godot_vect2.x, self->godot_vect2.y);
    mp_printf(print, buff);
}


static mp_obj_t _make_new_vector2(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    float x, y;

    mp_arg_check_num(n_args, 0, 0, 2, false);
    if (n_args == 2) {
        const mp_obj_t obj_y = all_args[1];
        if (MP_OBJ_IS_INT(obj_y)) {
            y = static_cast<float>(mp_obj_int_get_checked(obj_y));
        } else if (mp_obj_is_float(obj_y)) {
            y = mp_obj_float_get(obj_y);
        } else {
            mp_raise_TypeError("y must be a int or a float");
        }
    } else {
        y = 0.0;
    }
    if (n_args >= 1) {
        const mp_obj_t obj_x = all_args[0];
        if (MP_OBJ_IS_INT(obj_x)) {
            x = static_cast<float>(mp_obj_int_get_checked(obj_x));
        } else if (mp_obj_is_float(obj_x)) {
            x = mp_obj_float_get(obj_x);
        } else {
            mp_raise_TypeError("x must be a int or a float");
        }
    } else {
        x = 0.0;
    }

    auto obj = m_new_obj_with_finaliser(Vector2Binder::mp_godot_bind_t);
    obj->base.type = type;
    obj->godot_vect2 = Vector2(x, y);
    return MP_OBJ_FROM_PTR(obj);
}


Vector2Binder::Vector2Binder() {
    const char *name = "Vector2";
    this->_type_name= StringName(name);
    auto locals_dict = Vector2Binder::_generate_bind_locals_dict();
    // TODO: build locals_dict here...
    this->_mp_type = {
        { &mp_type_type },                        // base
        qstr_from_str(name),                      // name
        _print_vector2,                           // print
        _make_new_vector2,                        // make_new
        0,                                        // call
        0,                                        // unary_op
        0,                                        // binary_op
        0,                                        // attr
        0,                                        // subscr
        0,                                        // getiter
        0,                                        // iternext
        {0},                                      // buffer_p
        0,                                        // protocol
        0,                                        // bases_tuple
        static_cast<mp_obj_dict_t *>(MP_OBJ_TO_PTR(locals_dict))    // locals_dict
    };
    this->_p_mp_type = &this->_mp_type;
}


mp_obj_t Vector2Binder::build_pyobj(const Vector2 &p_vect2) const {
    auto pyobj = m_new_obj_with_finaliser(Vector2Binder::mp_godot_bind_t);
    pyobj->base.type = this->get_mp_type();
    pyobj->godot_vect2 = p_vect2;
    return MP_OBJ_FROM_PTR(pyobj);
}


Variant Vector2Binder::pyobj_to_variant(mp_obj_t pyobj) const {
    auto obj = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(pyobj));
    return Variant(obj->godot_vect2);
}
