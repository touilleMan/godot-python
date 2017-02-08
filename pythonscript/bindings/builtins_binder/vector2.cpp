#include <stdio.h>

#include "bindings/tools.h"
#include "bindings/builtins_binder/tools.h"
#include "bindings/builtins_binder/atomic.h"
#include "bindings/builtins_binder/vector2.h"


mp_obj_t Vector2Binder::_generate_bind_locals_dict() {
    // Build micropython type object
    mp_obj_t locals_dict = mp_obj_new_dict(0);

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

    // float   angle_to ( Vector2 to )
    BIND_METHOD_1("angle_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector2 to = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float angle_to = variant->godot_vect2.angle_to(to);
        return RealBinder::get_singleton()->build_pyobj(angle_to);
    });

    // float   angle_to_point ( Vector2 to )
    BIND_METHOD_1("angle_to_point", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector2 to = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float angle_to_point = variant->godot_vect2.angle_to_point(to);
        return RealBinder::get_singleton()->build_pyobj(angle_to_point);
    });

    // Vector2 clamped ( float length )
    BIND_METHOD_1("clamped", [](mp_obj_t self, mp_obj_t pylength) -> mp_obj_t {
        float length = RETRIEVE_ARG(RealBinder::get_singleton(), pylength, "length");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 clamped = variant->godot_vect2.clamped(length);
        return Vector2Binder::get_singleton()->build_pyobj(clamped);
    });

    // Vector2 cubic_interpolate ( Vector2 b, Vector2 pre_a, Vector2 post_b, float t )
    BIND_METHOD_VAR("cubic_interpolate", [](size_t n, const mp_obj_t *args) -> mp_obj_t {
        Vector2 b = RETRIEVE_ARG(Vector2Binder::get_singleton(), args[1], "b");
        Vector2 pre_a = RETRIEVE_ARG(Vector2Binder::get_singleton(), args[2], "pre_a");
        Vector2 post_b = RETRIEVE_ARG(Vector2Binder::get_singleton(), args[3], "post_b");
        float t = RETRIEVE_ARG(RealBinder::get_singleton(), args[4], "t");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(args[0]));
        Vector2 cubic_interpolate = variant->godot_vect2.cubic_interpolate(b, pre_a, post_b, t);
        return Vector2Binder::get_singleton()->build_pyobj(cubic_interpolate);
    }, 5, 5);

    // float   distance_squared_to ( Vector2 to )
    BIND_METHOD_1("distance_squared_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector2 to = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float distance_squared_to = variant->godot_vect2.distance_squared_to(to);
        return RealBinder::get_singleton()->build_pyobj(distance_squared_to);
    });

    // float   distance_to ( Vector2 to )
    BIND_METHOD_1("distance_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector2 to = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float distance_to = variant->godot_vect2.distance_to(to);
        return RealBinder::get_singleton()->build_pyobj(distance_to);
    });

    // float   dot ( Vector2 with )
    BIND_METHOD_1("dot", [](mp_obj_t self, mp_obj_t pywith) -> mp_obj_t {
        Vector2 with = RETRIEVE_ARG(Vector2Binder::get_singleton(), pywith, "with");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float dot = variant->godot_vect2.dot(with);
        return RealBinder::get_singleton()->build_pyobj(dot);
    });

    // Vector2 floor ( )
    BIND_METHOD("floor", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 vec = variant->godot_vect2.floor();
        return Vector2Binder::get_singleton()->build_pyobj(vec);
    });

    // float   aspect ( )
    BIND_METHOD("aspect", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float aspect = variant->godot_vect2.aspect();
        return RealBinder::get_singleton()->build_pyobj(aspect);
    });

    // float   length ( )
    BIND_METHOD("length", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float length = variant->godot_vect2.length();
        return RealBinder::get_singleton()->build_pyobj(length);
    });

    // float   length_squared ( )
    BIND_METHOD("length_squared", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float length_squared = variant->godot_vect2.length_squared();
        return RealBinder::get_singleton()->build_pyobj(length_squared);
    });

    // Vector2 linear_interpolate ( Vector2 b, float t )
    BIND_METHOD_2("linear_interpolate", [](mp_obj_t self, mp_obj_t pyb, mp_obj_t pyt) -> mp_obj_t {
        Vector2 b = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyb, "b");
        float t = RETRIEVE_ARG(RealBinder::get_singleton(), pyt, "t");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 linear_interpolate = variant->godot_vect2.linear_interpolate(b, t);
        return Vector2Binder::get_singleton()->build_pyobj(linear_interpolate);
    });

    // Vector2 normalized ( )
    BIND_METHOD("normalized", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 vec = variant->godot_vect2.normalized();
        return Vector2Binder::get_singleton()->build_pyobj(vec);
    });

    // Vector2 reflect ( Vector2 vec )
    BIND_METHOD_1("reflect", [](mp_obj_t self, mp_obj_t pyvec) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 vec = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyvec, "vec");
        Vector2 reflect = variant->godot_vect2.reflect(vec);
        return Vector2Binder::get_singleton()->build_pyobj(reflect);
    });

    // Vector2 rotated ( float phi )
    BIND_METHOD_1("rotated", [](mp_obj_t self, mp_obj_t pyphi) -> mp_obj_t {
        float phi = RETRIEVE_ARG(RealBinder::get_singleton(), pyphi, "phi");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 rotated = variant->godot_vect2.rotated(phi);
        return Vector2Binder::get_singleton()->build_pyobj(rotated);
    });

    // Vector2 slide ( Vector2 vec )
    BIND_METHOD_1("slide", [](mp_obj_t self, mp_obj_t pyvec) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 vec = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyvec, "vec");
        Vector2 slide = variant->godot_vect2.slide(vec);
        return Vector2Binder::get_singleton()->build_pyobj(slide);
    });

    // Vector2 snapped ( Vector2 by )
    BIND_METHOD_1("snapped", [](mp_obj_t self, mp_obj_t pyby) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 by = RETRIEVE_ARG(Vector2Binder::get_singleton(), pyby, "by");
        Vector2 snapped = variant->godot_vect2.snapped(by);
        return Vector2Binder::get_singleton()->build_pyobj(snapped);
    });

    // Vector2 tangent ( )
    BIND_METHOD("tangent", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector2 vec = variant->godot_vect2.tangent();
        return Vector2Binder::get_singleton()->build_pyobj(vec);
    });

    BIND_PROPERTY_GETSET("height",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float height = variant->godot_vect2.height;
        return RealBinder::get_singleton()->build_pyobj(height);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect2.height = val;
        return mp_const_none;
    });
    BIND_PROPERTY_GETSET("width",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float width = variant->godot_vect2.width;
        return RealBinder::get_singleton()->build_pyobj(width);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect2.width = val;
        return mp_const_none;
    });
    BIND_PROPERTY_GETSET("x",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float x = variant->godot_vect2.x;
        return RealBinder::get_singleton()->build_pyobj(x);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect2.x = val;
        return mp_const_none;
    });
    BIND_PROPERTY_GETSET("y", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float y = variant->godot_vect2.y;
        return RealBinder::get_singleton()->build_pyobj(y);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector2Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect2.y = val;
        return mp_const_none;
    });

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


static mp_obj_t _binary_op_vector2(mp_uint_t op, mp_obj_t lhs_in, mp_obj_t rhs_in) {
    auto self = static_cast<Vector2Binder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(lhs_in));
    if (op == MP_BINARY_OP_EQUAL && mp_obj_get_type(rhs_in) == Vector2Binder::get_singleton()->get_mp_type()) {
        auto other = static_cast<Vector2Binder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(rhs_in));
        return mp_obj_new_bool(self->godot_vect2.x == other->godot_vect2.x &&
                               self->godot_vect2.y == other->godot_vect2.y);
    }
    // op not supported
    return MP_OBJ_NULL;
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
        _binary_op_vector2,                       // binary_op
        attr_with_locals_and_properties,          // attr
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
