#include <stdio.h>

// Pythonscript
#include "bindings/tools.h"
#include "bindings/builtins_binder/tools.h"
#include "bindings/builtins_binder/atomic.h"
#include "bindings/builtins_binder/vector3.h"


mp_obj_t Vector3Binder::_generate_bind_locals_dict() {
    // Build micropython type object
    mp_obj_t locals_dict = mp_obj_new_dict(0);

    // Vector3 abs ( )
    BIND_METHOD("abs", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vect3_abs = variant->godot_vect3.abs();
        return Vector3Binder::get_singleton()->build_pyobj(vect3_abs);
    });


    // float   angle_to ( Vector3 to )
    BIND_METHOD_1("angle_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector3 to = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float angle_to = variant->godot_vect3.angle_to(to);
        return RealBinder::get_singleton()->build_pyobj(angle_to);
    });

    // Vector3 ceil ( )
    BIND_METHOD("ceil", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vect3_ceil = variant->godot_vect3.ceil();
        return Vector3Binder::get_singleton()->build_pyobj(vect3_ceil);
    });


    // Vector3 cross ( Vector3 b )
    BIND_METHOD_1("cross", [](mp_obj_t self, mp_obj_t pyb) -> mp_obj_t {
        Vector3 b = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyb, "b");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 clamped = variant->godot_vect3.cross(b);
        return Vector3Binder::get_singleton()->build_pyobj(clamped);
    });

    // Vector3 cubic_interpolate ( Vector3 b, Vector3 pre_a, Vector3 post_b, float t )
    BIND_METHOD_VAR("cubic_interpolate", [](size_t n, const mp_obj_t *args) -> mp_obj_t {
        Vector3 b = RETRIEVE_ARG(Vector3Binder::get_singleton(), args[1], "b");
        Vector3 pre_a = RETRIEVE_ARG(Vector3Binder::get_singleton(), args[2], "pre_a");
        Vector3 post_b = RETRIEVE_ARG(Vector3Binder::get_singleton(), args[3], "post_b");
        float t = RETRIEVE_ARG(RealBinder::get_singleton(), args[4], "t");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(args[0]));
        Vector3 cubic_interpolate = variant->godot_vect3.cubic_interpolate(b, pre_a, post_b, t);
        return Vector3Binder::get_singleton()->build_pyobj(cubic_interpolate);
    }, 5, 5);

    // float   distance_squared_to ( Vector3 to )
    BIND_METHOD_1("distance_squared_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector3 to = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float distance_squared_to = variant->godot_vect3.distance_squared_to(to);
        return RealBinder::get_singleton()->build_pyobj(distance_squared_to);
    });

    // float   distance_to ( Vector3 to )
    BIND_METHOD_1("distance_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        Vector3 to = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float distance_to = variant->godot_vect3.distance_to(to);
        return RealBinder::get_singleton()->build_pyobj(distance_to);
    });

    // float   dot ( Vector3 with )
    BIND_METHOD_1("dot", [](mp_obj_t self, mp_obj_t pywith) -> mp_obj_t {
        Vector3 with = RETRIEVE_ARG(Vector3Binder::get_singleton(), pywith, "with");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float dot = variant->godot_vect3.dot(with);
        return RealBinder::get_singleton()->build_pyobj(dot);
    });

    // Vector3 floor ( )
    BIND_METHOD("floor", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vec = variant->godot_vect3.floor();
        return Vector3Binder::get_singleton()->build_pyobj(vec);
    });

    // Vector3 inverse ( )
    BIND_METHOD("inverse", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vec = variant->godot_vect3.inverse();
        return Vector3Binder::get_singleton()->build_pyobj(vec);
    });

    // float   length ( )
    BIND_METHOD("length", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float length = variant->godot_vect3.length();
        return RealBinder::get_singleton()->build_pyobj(length);
    });

    // float   length_squared ( )
    BIND_METHOD("length_squared", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float length_squared = variant->godot_vect3.length_squared();
        return RealBinder::get_singleton()->build_pyobj(length_squared);
    });

    // Vector3 linear_interpolate ( Vector3 b, float t )
    BIND_METHOD_2("linear_interpolate", [](mp_obj_t self, mp_obj_t pyb, mp_obj_t pyt) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 b = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyb, "b");
        float t = RETRIEVE_ARG(RealBinder::get_singleton(), pyt, "t");
        Vector3 linear_interpolate = variant->godot_vect3.linear_interpolate(b, t);
        return Vector3Binder::get_singleton()->build_pyobj(linear_interpolate);
    });

    // Vector3 max_axis ( )
    BIND_METHOD("max_axis", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        int axis = variant->godot_vect3.max_axis();
        return IntBinder::get_singleton()->build_pyobj(axis);
    });

    // Vector3 min_axis ( )
    BIND_METHOD("min_axis", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        int axis = variant->godot_vect3.min_axis();
        return IntBinder::get_singleton()->build_pyobj(axis);
    });

    // Vector3 normalized ( )
    BIND_METHOD("normalized", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vec = variant->godot_vect3.normalized();
        return Vector3Binder::get_singleton()->build_pyobj(vec);
    });

    // Vector3 reflect ( Vector3 vec )
    BIND_METHOD_1("reflect", [](mp_obj_t self, mp_obj_t pyvec) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vec = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyvec, "vec");
        Vector3 reflect = variant->godot_vect3.reflect(vec);
        return Vector3Binder::get_singleton()->build_pyobj(reflect);
    });

    // Vector3 rotated ( Vector3 axis, float phi )
    BIND_METHOD_2("rotated", [](mp_obj_t self, mp_obj_t pyaxis, mp_obj_t pyphi) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 axis = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyaxis, "axis");
        float phi = RETRIEVE_ARG(RealBinder::get_singleton(), pyphi, "phi");
        Vector3 rotated = variant->godot_vect3.rotated(axis, phi);
        return Vector3Binder::get_singleton()->build_pyobj(rotated);
    });

    // Vector3 slide ( Vector3 vec )
    BIND_METHOD_1("slide", [](mp_obj_t self, mp_obj_t pyvec) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        Vector3 vec = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyvec, "vec");
        Vector3 slide = variant->godot_vect3.slide(vec);
        return Vector3Binder::get_singleton()->build_pyobj(slide);
    });

    // Vector3 snapped ( float by )
    BIND_METHOD_1("snapped", [](mp_obj_t self, mp_obj_t pyby) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float by = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyby, "by");
        Vector3 snapped = variant->godot_vect3.snapped(by);
        return Vector3Binder::get_singleton()->build_pyobj(snapped);
    });

    BIND_PROPERTY_GETSET("x",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float x = variant->godot_vect3.x;
        return RealBinder::get_singleton()->build_pyobj(x);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect3.x = val;
        return mp_const_none;
    });
    BIND_PROPERTY_GETSET("y", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float y = variant->godot_vect3.y;
        return RealBinder::get_singleton()->build_pyobj(y);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect3.y = val;
        return mp_const_none;
    });
    BIND_PROPERTY_GETSET("z", [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const float z = variant->godot_vect3.z;
        return RealBinder::get_singleton()->build_pyobj(z);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_vect3.z = val;
        return mp_const_none;
    });

    return locals_dict;
}


static void _print_vector3(const mp_print_t *print, mp_obj_t o, mp_print_kind_t kind) {
    auto self = static_cast<Vector3Binder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(o));
    char buff[64];
    sprintf(buff, "<Vector3(x=%f, y=%f, z=%f)>", self->godot_vect3.x, self->godot_vect3.y, self->godot_vect3.z);
    mp_printf(print, buff);
}


static mp_obj_t _make_new_vector3(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    float x, y, z;

    mp_arg_check_num(n_args, 0, 0, 3, false);
    if (n_args == 3) {
        const mp_obj_t obj_z = all_args[2];
        if (MP_OBJ_IS_INT(obj_z)) {
            z = static_cast<float>(mp_obj_int_get_checked(obj_z));
        } else if (mp_obj_is_float(obj_z)) {
            z = mp_obj_float_get(obj_z);
        } else {
            mp_raise_TypeError("z must be a int or a float");
        }
    } else {
        z = 0.0;
    }
    if (n_args >= 2) {
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

    auto obj = m_new_obj_with_finaliser(Vector3Binder::mp_godot_bind_t);
    obj->base.type = type;
    obj->godot_vect3 = Vector3(x, y, z);
    return MP_OBJ_FROM_PTR(obj);
}


static mp_obj_t _binary_op_vector3(mp_uint_t op, mp_obj_t lhs_in, mp_obj_t rhs_in) {
    auto self = static_cast<Vector3Binder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(lhs_in));
    if (op == MP_BINARY_OP_EQUAL && mp_obj_get_type(rhs_in) == Vector3Binder::get_singleton()->get_mp_type()) {
        auto other = static_cast<Vector3Binder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(rhs_in));
        return mp_obj_new_bool(self->godot_vect3.x == other->godot_vect3.x &&
                               self->godot_vect3.y == other->godot_vect3.y &&
                               self->godot_vect3.z == other->godot_vect3.z);
    }
    // op not supported
    return MP_OBJ_NULL;
}


Vector3Binder::Vector3Binder() {
    const char *name = "Vector3";
    this->_type_name= StringName(name);
    auto locals_dict = Vector3Binder::_generate_bind_locals_dict();
    // TODO: build locals_dict here...
    this->_mp_type = {
        { &mp_type_type },                        // base
        qstr_from_str(name),                      // name
        _print_vector3,                           // print
        _make_new_vector3,                        // make_new
        0,                                        // call
        0,                                        // unary_op
        _binary_op_vector3,                       // binary_op
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


mp_obj_t Vector3Binder::build_pyobj(const Vector3 &p_vect3) const {
    auto pyobj = m_new_obj_with_finaliser(Vector3Binder::mp_godot_bind_t);
    pyobj->base.type = this->get_mp_type();
    pyobj->godot_vect3 = p_vect3;
    return MP_OBJ_FROM_PTR(pyobj);
}


Variant Vector3Binder::pyobj_to_variant(mp_obj_t pyobj) const {
    auto obj = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(pyobj));
    return Variant(obj->godot_vect3);
}
