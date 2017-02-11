#include <cstring>
#include <stdio.h>

// Godot imports
#include "core/math/vector3.h"
#include "core/math/plane.h"
// Pythonscript imports
#include "bindings/tools.h"
#include "bindings/builtins_binder/tools.h"
#include "bindings/builtins_binder/atomic.h"
#include "bindings/builtins_binder/plane.h"
#include "bindings/builtins_binder/vector3.h"


mp_obj_t PlaneBinder::_generate_bind_locals_dict() {
    // Build micropython type object
    mp_obj_t locals_dict = mp_obj_new_dict(0);

    // Vector3 center (  )
    BIND_METHOD("center", [](mp_obj_t self) -> mp_obj_t {
      auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
      auto ret = variant->godot_plane.center();
      return Vector3Binder::get_singleton()->build_pyobj(ret);
    });

    // float distance_to ( Vector3 to )
    BIND_METHOD_1("distance_to", [](mp_obj_t self, mp_obj_t pyto) -> mp_obj_t {
        auto to = RETRIEVE_ARG(Vector3Binder::get_singleton(), pyto, "to");
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        float ret = variant->godot_plane.distance_to(to);
        return RealBinder::get_singleton()->build_pyobj(ret);
    });

    // Vector3 get_any_point (  )
    BIND_METHOD("get_any_point", [](mp_obj_t self) -> mp_obj_t {
      auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
      auto ret = variant->godot_plane.get_any_point();
      return Vector3Binder::get_singleton()->build_pyobj(ret);
    });

    // bool has_point (Vector3, float)
    BIND_METHOD_VAR("has_point", [](size_t n, const mp_obj_t *args) -> mp_obj_t {
        if (n != 2 && n != 3) {
          char buff[64];
          snprintf(buff, sizeof(buff), "Plane.has_point expected 1 or 2 arguments but got %zu", n - 1);
          mp_raise_TypeError(buff);
        }
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(args[0]));
        auto point = RETRIEVE_ARG(Vector3Binder::get_singleton(), args[1], "point");
        float epsilon = 0.00001; // default value if not given
        if (n == 3) {
          epsilon = RETRIEVE_ARG(RealBinder::get_singleton(), args[n - 1], "epsilon");
        }
        auto ret = variant->godot_plane.has_point(point, epsilon);
        return BoolBinder::get_singleton()->build_pyobj(ret);
    }, 2, 3);

    // Vector3 intersect_3 ( Plane b, Plane c )
    BIND_METHOD_2("intersect_3", [](mp_obj_t self, mp_obj_t pyb, mp_obj_t pyc) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        auto b = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyb, "b");
        auto c = RETRIEVE_ARG(PlaneBinder::get_singleton(), pyc, "c");
        Vector3 ret;
        auto flag = variant->godot_plane.intersect_3(b, c, &ret);
        if (flag) {
          return MP_OBJ_NULL;
        } else {
          return Vector3Binder::get_singleton()->build_pyobj(ret);
        }
    });

    // Vector3 intersects_ray ( Vector3 from, Vector3 dir )
    BIND_METHOD_2("intersects_ray", [](mp_obj_t self, mp_obj_t py_from, mp_obj_t py_dir) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        auto from = RETRIEVE_ARG(Vector3Binder::get_singleton(), py_from, "from");
        auto dir = RETRIEVE_ARG(Vector3Binder::get_singleton(), py_dir, "dir");
        Vector3 ret;
        auto flag = variant->godot_plane.intersects_ray(from, dir, &ret);
        if (flag) {
          return MP_OBJ_NULL;
        } else {
          return Vector3Binder::get_singleton()->build_pyobj(ret);
        }
    });

    // Vector3 intersects_segment ( Vector3 begin, Vector3 end )
    BIND_METHOD_2("intersects_segment", [](mp_obj_t self, mp_obj_t py_begin, mp_obj_t py_end) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        auto begin = RETRIEVE_ARG(Vector3Binder::get_singleton(), py_begin, "begin");
        auto end = RETRIEVE_ARG(Vector3Binder::get_singleton(), py_end, "end");
        Vector3 ret;
        auto flag = variant->godot_plane.intersects_segment(begin, end, &ret);
        if (flag) {
          return MP_OBJ_NULL;
        } else {
          return Vector3Binder::get_singleton()->build_pyobj(ret);
        }
    });

    // bool is_point_over ( Vector3 point )
    BIND_METHOD_1("is_point_over", [](mp_obj_t self, mp_obj_t py_point) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        auto point = RETRIEVE_ARG(Vector3Binder::get_singleton(), py_point, "point");
        auto ret = variant->godot_plane.is_point_over(point);
        return BoolBinder::get_singleton()->build_pyobj(ret);
    });


    // Plane normalized (  )
    BIND_METHOD("normalized", [](mp_obj_t self) -> mp_obj_t {
      auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
      auto ret = variant->godot_plane.normalized();
      return PlaneBinder::get_singleton()->build_pyobj(ret);
    });

    // Vector3 project ( Vector3 point )
    BIND_METHOD_1("project", [](mp_obj_t self, mp_obj_t py_point) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        auto point = RETRIEVE_ARG(Vector3Binder::get_singleton(), py_point, "point");
        auto ret = variant->godot_plane.project(point);
        return Vector3Binder::get_singleton()->build_pyobj(ret);
    });


    BIND_PROPERTY_GETSET("x",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const auto x = variant->godot_plane.normal.x;
        return RealBinder::get_singleton()->build_pyobj(x);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const auto val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_plane.normal.x = val;
        return mp_const_none;
    });

    BIND_PROPERTY_GETSET("y",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const auto y = variant->godot_plane.normal.y;
        return RealBinder::get_singleton()->build_pyobj(y);
    },
        [](mp_obj_t self, mp_obj_t pyval) -> mp_obj_t {
        const auto val = RETRIEVE_ARG(RealBinder::get_singleton(), pyval, "val");
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_plane.normal.y = val;
        return mp_const_none;
    });

    BIND_PROPERTY_GETSET("z",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const auto z = variant->godot_plane.normal.z;
        return RealBinder::get_singleton()->build_pyobj(z);
    },
        [](mp_obj_t self, mp_obj_t pzval) -> mp_obj_t {
        const auto val = RETRIEVE_ARG(RealBinder::get_singleton(), pzval, "val");
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_plane.normal.z = val;
        return mp_const_none;
    });

    BIND_PROPERTY_GETSET("normal",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const auto normal = variant->godot_plane.normal;
        return Vector3Binder::get_singleton()->build_pyobj(normal);
    },
        [](mp_obj_t self, mp_obj_t pdval) -> mp_obj_t {
        const auto val = RETRIEVE_ARG(Vector3Binder::get_singleton(), pdval, "val");
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_plane.normal = val;
        return mp_const_none;
    });

    BIND_PROPERTY_GETSET("d",
        [](mp_obj_t self) -> mp_obj_t {
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        const auto d = variant->godot_plane.d;
        return RealBinder::get_singleton()->build_pyobj(d);
    },
        [](mp_obj_t self, mp_obj_t pdval) -> mp_obj_t {
        const auto val = RETRIEVE_ARG(RealBinder::get_singleton(), pdval, "val");
        auto variant = static_cast<PlaneBinder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(self));
        variant->godot_plane.d = val;
        return mp_const_none;
    });

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


static mp_obj_t _unary_op_plane(mp_uint_t op, mp_obj_t in) {
  auto self = static_cast<PlaneBinder::mp_godot_bind_t*>(MP_OBJ_TO_PTR(in));
  switch (op) {
    case MP_UNARY_OP_NEGATIVE:
      return PlaneBinder::get_singleton()->build_pyobj(
          Plane(-self->godot_plane.normal.x + 0.0,
                -self->godot_plane.normal.y + 0.0,
                -self->godot_plane.normal.z + 0.0,
                -self->godot_plane.d + 0.0));
    case MP_UNARY_OP_POSITIVE:
      return MP_OBJ_FROM_PTR(self);
  }
  return MP_OBJ_NULL; // op not supported
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


static mp_obj_t _make_new_plane(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    auto obj = m_new_obj_with_finaliser(PlaneBinder::mp_godot_bind_t);
    obj->base.type = type;

    mp_arg_check_num(n_args, 0, 0, 4, false);
    if (n_args == 4) {
      float godot_args[4];
      for (size_t i = 0; i < n_args; ++i) {
        const auto &n = all_args[i];
        if (MP_OBJ_IS_INT(n)) {
          godot_args[i] = static_cast<float>(mp_obj_int_get_checked(n));
        } else if (mp_obj_is_float(n)) {
          godot_args[i] = mp_obj_float_get(n);
        } else {
          mp_raise_TypeError("arguments must be of type int or float");
        }
      }
      obj->godot_plane = Plane(godot_args[0], godot_args[1], godot_args[2], godot_args[3]);
    } else if (n_args == 3) {
      Vector3Binder::mp_godot_bind_t * godot_args[3];
      for (size_t i = 0; i < n_args; ++i) {
        const auto &n = all_args[i];
        if (MP_OBJ_IS_TYPE(n, Vector3Binder::get_singleton()->get_mp_type())) {
          godot_args[i] = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(n));;
        } else {
          mp_raise_TypeError("arguments must be of type Vector3");
        }
      }
      obj->godot_plane = Plane(godot_args[0]->godot_vect3,
                               godot_args[1]->godot_vect3,
                               godot_args[2]->godot_vect3);
    } else if (n_args == 2) {
      Vector3Binder::mp_godot_bind_t * godot_args0;
      float godot_args1;
      if (MP_OBJ_IS_TYPE(all_args[0], Vector3Binder::get_singleton()->get_mp_type())) {
        godot_args0 = static_cast<Vector3Binder::mp_godot_bind_t *>(MP_OBJ_TO_PTR(all_args[0]));
      } else {
        mp_raise_TypeError("argument 0 must be of type Vector3");
      }
      if (mp_obj_is_float(all_args[1])) {
        godot_args1 = mp_obj_float_get(all_args[1]);
      } else if (MP_OBJ_IS_INT(all_args[1])) {
        godot_args1 = static_cast<float>(mp_obj_int_get_checked(all_args[1]));
      } else {
        mp_raise_TypeError("argument 1 must be of type int or float");
      }
      obj->godot_plane = Plane(godot_args0->godot_vect3, godot_args1);
    } else if (n_args == 0) {
      obj->godot_plane = Plane();
    } else {
      char buff[64];
      snprintf(buff, sizeof(buff), "Plane constructor expected 0, 2, 3 or 4 arguments but got %zu", n_args);
      mp_raise_TypeError(buff);
    }

    return MP_OBJ_FROM_PTR(obj);
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
