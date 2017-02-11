#include <stdio.h>

// Godot imports
#include "core/math/plane.h"
// Pythonscript imports
#include "bindings/tools.h"
#include "bindings/builtins_binder/tools.h"
#include "bindings/builtins_binder/atomic.h"
#include "bindings/builtins_binder/plane.h"


mp_obj_t PlaneBinder::_generate_bind_locals_dict() {
    // Build micropython type object
    mp_obj_t locals_dict = mp_obj_new_dict(0);

    /* // Plane abs ( ) */
    /* BIND_METHOD("abs", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane plane_abs = variant->godot_plane.abs(); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(plane_abs); */
    /* }); */

    /* // float   angle ( ) */
    /* BIND_METHOD("angle", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float angle = variant->godot_plane.angle(); */
    /*     return RealBinder::get_singleton()->build_pyobj(angle); */
    /* }); */

    /* // float   angle_to ( Plane to ) */
    /* BIND_METHOD_1("angle_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t { */
    /*     Plane to = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyto, "to"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float angle_to = variant->godot_plane.angle_to(to); */
    /*     return RealBinder::get_singleton()->build_pyobj(angle_to); */
    /* }); */

    /* // float   angle_to_point ( Plane to ) */
    /* BIND_METHOD_1("angle_to_point", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t { */
    /*     Plane to = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyto, "to"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float angle_to_point = variant->godot_plane.angle_to_point(to); */
    /*     return RealBinder::get_singleton()->build_pyobj(angle_to_point); */
    /* }); */

    /* // Plane clamped ( float length ) */
    /* BIND_METHOD_1("clamped", [](mp_obj_t self, mp_obj_t pylength) -> mp_obj_t { */
    /*     float length = RETRIEVE_ARG(RealBinder::get_singleton(), pylength, "length"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane clamped = variant->godot_plane.clamped(length); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(clamped); */
    /* }); */

    /* // Plane cubic_interpolate ( Plane b, Plane pre_a, Plane post_b, float t ) */
    /* BIND_METHOD_VAR("cubic_interpolate", [](size_t n, const mp_obj_t *args) -> mp_obj_t { */
    /*     Plane b = RETRIEVE_ARG(PlaneBinder::get_singleton(), args[1], "b"); */
    /*     Plane pre_a = RETRIEVE_ARG(PlaneBinder::get_singleton(), args[2], "pre_a"); */
    /*     Plane post_b = RETRIEVE_ARG(PlaneBinder::get_singleton(), args[3], "post_b"); */
    /*     float t = RETRIEVE_ARG(RealBinder::get_singleton(), args[4], "t"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(args[0])); */
    /*     Plane cubic_interpolate = variant->godot_plane.cubic_interpolate(b, pre_a, post_b, t); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(cubic_interpolate); */
    /* }, 5, 5); */

    /* // float   distance_squared_to ( Plane to ) */
    /* BIND_METHOD_1("distance_squared_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t { */
    /*     Plane to = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyto, "to"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float distance_squared_to = variant->godot_plane.distance_squared_to(to); */
    /*     return RealBinder::get_singleton()->build_pyobj(distance_squared_to); */
    /* }); */

    /* // float   distance_to ( Plane to ) */
    /* BIND_METHOD_1("distance_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t { */
    /*     Plane to = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyto, "to"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float distance_to = variant->godot_plane.distance_to(to); */
    /*     return RealBinder::get_singleton()->build_pyobj(distance_to); */
    /* }); */

    /* // float   dot ( Plane with ) */
    /* BIND_METHOD_1("dot", [](mp_obj_t self, mp_obj_t pywith) -> mp_obj_t { */
    /*     Plane with = RETRIEVE_ARG(PlaneBinder::get_singleton(), pywith, "with"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float dot = variant->godot_plane.dot(with); */
    /*     return RealBinder::get_singleton()->build_pyobj(dot); */
    /* }); */

    /* // Plane floor ( ) */
    /* BIND_METHOD("floor", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane vec = variant->godot_plane.floor(); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(vec); */
    /* }); */

    /* // float   aspect ( ) */
    /* BIND_METHOD("aspect", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float aspect = variant->godot_plane.aspect(); */
    /*     return RealBinder::get_singleton()->build_pyobj(aspect); */
    /* }); */

    /* // float   length ( ) */
    /* BIND_METHOD("length", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float length = variant->godot_plane.length(); */
    /*     return RealBinder::get_singleton()->build_pyobj(length); */
    /* }); */

    /* // float   length_squared ( ) */
    /* BIND_METHOD("length_squared", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     float length_squared = variant->godot_plane.length_squared(); */
    /*     return RealBinder::get_singleton()->build_pyobj(length_squared); */
    /* }); */

    /* // Plane linear_interpolate ( Plane b, float t ) */
    /* BIND_METHOD_2("linear_interpolate", [](mp_obj_t self, mp_obj_t pyb, mp_obj_t pyt) -> mp_obj_t { */
    /*     Plane b = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyb, "b"); */
    /*     float t = RETRIEVE_ARG(RealBinder::get_singleton(), pyt, "t"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane linear_interpolate = variant->godot_plane.linear_interpolate(b, t); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(linear_interpolate); */
    /* }); */

    /* // Plane normalized ( ) */
    /* BIND_METHOD("normalized", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane vec = variant->godot_plane.normalized(); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(vec); */
    /* }); */

    /* // Plane reflect ( Plane vec ) */
    /* BIND_METHOD_1("reflect", [](mp_obj_t self, mp_obj_t pyvec) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane vec = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyvec, "vec"); */
    /*     Plane reflect = variant->godot_plane.reflect(vec); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(reflect); */
    /* }); */

    /* // Plane rotated ( float phi ) */
    /* BIND_METHOD_1("rotated", [](mp_obj_t self, mp_obj_t pyphi) -> mp_obj_t { */
    /*     float phi = RETRIEVE_ARG(RealBinder::get_singleton(), pyphi, "phi"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane rotated = variant->godot_plane.rotated(phi); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(rotated); */
    /* }); */

    /* // Plane slide ( Plane vec ) */
    /* BIND_METHOD_1("slide", [](mp_obj_t self, mp_obj_t pyvec) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane vec = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyvec, "vec"); */
    /*     Plane slide = variant->godot_plane.slide(vec); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(slide); */
    /* }); */

    /* // Plane snapped ( Plane by ) */
    /* BIND_METHOD_1("snapped", [](mp_obj_t self, mp_obj_t pyby) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane by = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyby, "by"); */
    /*     Plane snapped = variant->godot_plane.snapped(by); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(snapped); */
    /* }); */

    /* // Plane tangent ( ) */
    /* BIND_METHOD("tangent", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     Plane vec = variant->godot_plane.tangent(); */
    /*     return PlaneBinder::get_singleton()->build_pyobj(vec); */
    /* }); */

    /* BIND_PROPERTY_GETSET("x", */
    /*     [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     const float x = variant->godot_plane.x; */
    /*     return RealBinder::get_singleton()->build_pyobj(x); */
    /* }, */
    /*     [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t { */
    /*     const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     variant->godot_plane.x = val; */
    /*     return mp_const_none; */
    /* }); */
    /* BIND_PROPERTY_GETSET("y", [](mp_obj_t self) -> mp_obj_t { */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     const float y = variant->godot_plane.y; */
    /*     return RealBinder::get_singleton()->build_pyobj(y); */
    /* }, */
    /*     [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t { */
    /*     const float val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val"); */
    /*     auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self)); */
    /*     variant->godot_plane.y = val; */
    /*     return mp_const_none; */
    /* }); */

    return locals_dict;
}


static void _print_plane(const mp_print_t *print, mp_obj_t o, mp_print_kind_t kind) {
    auto self = static_cast<PlaneBinder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(o));
    char buff[64];
    sprintf(buff, "<Plane(normal=Vector3(%f, %f, %f), d=%f)>",
            self->godot_plane.normal.x, self->godot_plane.normal.y,
            self->godot_plane.normal.z, self->godot_plane.d);
    mp_printf(print, buff);
}


static mp_obj_t _make_new_plane(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    auto obj = m_new_obj_with_finaliser(PlaneBinder::mp_godot_bind_t);
    obj->base.type = type;

    mp_arg_check_num(n_args, 0, 0, 4, false);
    if (n_args == 4) {
      float args[n_args];
      for (size_t i = 0; i < n_args; ++i) {
        const auto &n = all_args[i];
        if (MP_OBJ_IS_INT(n)) {
          args[i] = static_cast<float>(mp_obj_int_get_checked(n));
        } else if (mp_obj_is_float(n)) {
          args[i] = mp_obj_float_get(n);
        } else {
          mp_raise_TypeError("arguments must be of type int or float");
        }
      }
      obj->godot_plane = Plane(args[0], args[1], args[2], args[3]);
    }

    return MP_OBJ_FROM_PTR(obj);
}


static mp_obj_t _binary_op_plane(mp_uint_t op, mp_obj_t lhs_in, mp_obj_t rhs_in) {
    auto self = static_cast<PlaneBinder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(lhs_in));
    if (op == MP_BINARY_OP_EQUAL && MP_OBJ_IS_TYPE(rhs_in, PlaneBinder::get_singleton()->get_mp_type())) {
        auto other = static_cast<PlaneBinder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(rhs_in));
        return mp_obj_new_bool(self->godot_plane.normal == other->godot_plane.normal &&
                               self->godot_plane.d == other->godot_plane.d);
    }
    return MP_OBJ_NULL; // op not supported
}


static mp_obj_t _unary_op_plane(mp_uint_t op, mp_obj_t in) {
  auto self = static_cast<PlaneBinder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(in));
  switch (op) {
    case MP_UNARY_OP_NEGATIVE:
      return PlaneBinder::get_singleton()->build_pyobj(
          Plane(-self->godot_plane.normal.x, -self->godot_plane.normal.y,
                -self->godot_plane.normal.z, -self->godot_plane.d));
    case MP_UNARY_OP_POSITIVE:
      return MP_OBJ_FROM_PTR(self);
  }
  return MP_OBJ_NULL; // op not supported
}


PlaneBinder::PlaneBinder() {
    const char *name = "Plane";
    this->_type_name= StringName(name);
    auto locals_dict = PlaneBinder::_generate_bind_locals_dict();
    // TODO: build locals_dict here...
    this->_mp_type = {
        { &mp_type_type },                        // base
        qstr_from_str(name),                      // name
        _print_plane,                             // print
        _make_new_plane,                          // make_new
        0,                                        // call
        _unary_op_plane,                          // unary_op
        _binary_op_plane,                         // binary_op
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


mp_obj_t PlaneBinder::build_pyobj(const Plane &p_plane) const {
    auto pyobj = m_new_obj_with_finaliser(PlaneBinder::mp_godot_bind_t);
    pyobj->base.type = this->get_mp_type();
    pyobj->godot_plane = p_plane;
    return MP_OBJ_FROM_PTR(pyobj);
}


Variant PlaneBinder::pyobj_to_variant(mp_obj_t pyobj) const {
    auto obj = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(pyobj));
    return Variant(obj->godot_plane);
}
