#include "pythonscript.h"
#include "bindings.h"

#include "core/object.h"
#include "core/math/math_2d.h"


namespace bindings {

class Object {
public:

    ::Object *godot_obj;
    ::Variant godot_variant;

    void set_godot_obj(GodotObject *obj) {
        this->godot_obj = obj->godot_obj;
        this->godot_variant = ::Variant(obj->godot_obj);
    }

    explicit Object(::Object *obj) {
        this->godot_obj = obj;
    }

    Object() {
        // TODO: Handle constructor's parameters ?
        this->godot_obj = ClassDB::instance("Object");
    }

    inline int get_instance_ID() {
        static MethodBind *mb = ClassDB::get_method("Object", "get_instance_ID");
        int ret;
        mb->ptrcall(this->godot_obj, nullptr, &ret);
        return ret;
    }

    inline bool is_class() {
        static MethodBind *mb = ClassDB::get_method("Object", "is_class");
        bool ret;
        mb->ptrcall(this->godot_obj, nullptr, &ret);
        return ret;
    }
};
PYBIND11_PLUGIN(godot_bindings) {
    py::module m("godot.bindings", "godot classes just for you ;-)");

    py::class_<GodotObject>(m, "_GodotObject")
        .def(py::init<>());

    py::class_<Object>(m, "Object")
        .def(py::init<>())
        .def("__set_godot_obj", &Object::set_godot_obj)
        .def("get_instance_ID", &Object::get_instance_ID)
        .def("is_class", &Object::is_class);


    py::class_<Vector2>(m, "Vector2")
        .def(py::init<float, float>(), py::arg("x")=0.0, py::arg("y")=0.0)
        .def("__repr__", [](const Vector2 &v) -> std::string { return "<Vector2(x=" + std::to_string(v.x) + ", y=" + std::to_string(v.y) + ")>"; })
        .def("__eq__", [](const Vector2 &v1, const Vector2 &v2) { return v1.x == v2.x && v1.y == v2.y; })
        // TODO: is __neq__ needed ?
        .def("__neg__", [](const Vector2 &v) -> Vector2 { return Vector2(-v.x, -v.y); })
        .def("__pos__", [](const Vector2 &v) -> Vector2 { return v; })
        // Vector2 abs ( )
        .def("abs", &Vector2::abs)
        // float   angle ( )
        .def("angle", &Vector2::angle)
        // float   angle_to ( Vector2 to )
        .def("angle_to", &Vector2::angle_to)
        // float   angle_to_point ( Vector2 to )
        .def("angle_to_point", &Vector2::angle_to_point)
        // Vector2 clamped ( float length )
        .def("clamped", &Vector2::clamped)
        // Vector2 cubic_interpolate ( Vector2 b, Vector2 pre_a, Vector2 post_b, float t )
        .def("cubic_interpolate", &Vector2::cubic_interpolate)
        // float   distance_squared_to ( Vector2 to )
        .def("distance_squared_to", &Vector2::distance_squared_to)
        // float   distance_to ( Vector2 to )
        .def("distance_to", &Vector2::distance_to)
        // float   dot ( Vector2 with )
        .def("dot", &Vector2::dot)
        // Vector2 floor ( )
        .def("floor", &Vector2::floor)
        // float   aspect ( )
        .def("aspect", &Vector2::aspect)
        // float   length ( )
        .def("length", &Vector2::length)
        // float   length_squared ( )
        .def("length_squared", &Vector2::length_squared)
        // Vector2 linear_interpolate ( Vector2 b, float t )
        // Cannot directly bind to Vector2::linear_interpolate because there is two definitions of it
        .def("linear_interpolate", [](const Vector2 &a, const Vector2 &b, real_t t) -> Vector2 { return a.linear_interpolate(b, t); })
        // Vector2 normalized ( )
        .def("normalized", &Vector2::normalized)
        // Vector2 reflect ( Vector2 vec )
        .def("reflect", &Vector2::reflect)
        // Vector2 rotated ( float phi )
        .def("rotated", &Vector2::rotated)
        // Vector2 slide ( Vector2 vec )
        .def("slide", &Vector2::slide)
        // Vector2 snapped ( Vector2 by )
        .def("snapped", &Vector2::snapped)
        // Vector2 tangent ( )
        .def("tangent", &Vector2::tangent)
        .def_readwrite("height", &Vector2::height)
        .def_readwrite("width", &Vector2::width)
        .def_readwrite("x", &Vector2::x)
        .def_readwrite("y", &Vector2::y);

    // Expose godot.bindings as a module
    auto sys = py::module::import("sys");
    sys.attr("modules")["godot.bindings"] = m;

    return m.ptr();
}

void init() {
    pybind11_init();
}

}
