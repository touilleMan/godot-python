#include "pythonscript.h"
#include "static_bindings.h"

#include "core/object.h"
#include "core/variant.h"
#include "core/error_list.h"

#include "core/math/math_2d.h"


namespace bindings {


PYBIND11_PLUGIN(godot_bindings) {
    py::module m = py::module::import("godot.bindings");
    // py::module m("godot.bindings", "godot classes just for you ;-)");

    // TODO: improve bindings
    py::class_<String>(m, "String");
    py::class_<Rect2>(m, "Rect2");
    py::class_<Plane>(m, "Plane");
    py::class_<Rect3>(m, "Rect3");
    py::class_<Quat>(m, "Quat");
    py::class_<Basis>(m, "Basis");
    py::class_<Transform>(m, "Transform");
    py::class_<Transform2D>(m, "Transform2D");
    py::class_<Color>(m, "Color");
    py::class_<Image>(m, "Image");
    py::class_<NodePath>(m, "NodePath")
        .def(py::init<String>(), py::arg("from"))
        // Methods
        .def("get_name", &NodePath::get_name)
        .def("get_name_count", &NodePath::get_name_count)
        .def("get_property", &NodePath::get_property)
        .def("get_subname", &NodePath::get_subname)
        .def("get_subname_count", &NodePath::get_subname_count)
        .def("is_absolute", &NodePath::is_absolute)
        .def("is_empty", &NodePath::is_empty)
        // Properties
        // Constants
        ;

    py::class_<RefPtr>(m, "RefPtr");
    py::class_<RID>(m, "RID");
    py::class_<InputEvent>(m, "InputEvent");

    py::class_<PoolByteArray>(m, "PoolByteArray");
    // py::class_<RawArray>(m, "RawArray");
    py::class_<PoolIntArray>(m, "PoolIntArray");
    py::class_<PoolRealArray>(m, "PoolFloatArray");
    py::class_<PoolStringArray>(m, "PoolStringArray");
    py::class_<PoolVector2Array>(m, "PoolVector2Array");
    py::class_<PoolVector3Array>(m, "PoolVector3Array");
    py::class_<PoolColorArray>(m, "PoolColorArray");

    py::class_<Vector3>(m, "Vector3")
        .def(py::init<float, float, float>(), py::arg("x")=0.0, py::arg("y")=0.0, py::arg("z")=0.0)
        .def("__repr__", [](const Vector3 &v) -> std::string { return "<Vector3(x=" + std::to_string(v.x) + ", y=" + std::to_string(v.y) + ", z=" + std::to_string(v.z) + ")>"; })
        .def("__eq__", [](const Vector3 &v1, const Vector3 &v2) { return v1.x == v2.x && v1.y == v2.y && v1.z == v2.z; })
        // TODO: is __neq__ needed ?
        .def("__neg__", [](const Vector3 &v) -> Vector3 { return Vector3(-v.x, -v.y, -v.z); })
        .def("__pos__", [](const Vector3 &v) -> Vector3 { return v; })
        // Methods
        .def("abs", &Vector3::abs)
        .def("angle_to", &Vector3::angle_to)
        .def("ceil", &Vector3::ceil)
        .def("cross", &Vector3::cross)
        .def("cubic_interpolate", &Vector3::cubic_interpolate)
        .def("distance_squared_to", &Vector3::distance_squared_to)
        .def("distance_to", &Vector3::distance_to)
        .def("dot", &Vector3::dot)
        .def("floor", &Vector3::floor)
        .def("inverse", &Vector3::inverse)
        .def("length", &Vector3::length)
        .def("length_squared", &Vector3::length_squared)
        .def("linear_interpolate", &Vector3::linear_interpolate)
        .def("max_axis", &Vector3::max_axis)
        .def("min_axis", &Vector3::min_axis)
        .def("normalized", &Vector3::normalized)
        .def("reflect", &Vector3::reflect)
        .def("rotated", &Vector3::rotated)
        .def("slide", &Vector3::slide)
        .def("snapped", &Vector3::snapped)
        // Properties
        .def_readwrite("x", &Vector3::x)
        .def_readwrite("y", &Vector3::y)
        .def_readwrite("z", &Vector3::z)
        // Constants
        .def_property_readonly("AXIS_X", [](py::object self){return static_cast<int>(Vector3::AXIS_X);})
        .def_property_readonly("AXIS_Y", [](py::object self){return static_cast<int>(Vector3::AXIS_Y);})
        .def_property_readonly("AXIS_Z", [](py::object self){return static_cast<int>(Vector3::AXIS_Z);})
        ;

    py::class_<Vector2>(m, "Vector2")
        .def(py::init<float, float>(), py::arg("x")=0.0, py::arg("y")=0.0)
        .def("__repr__", [](const Vector2 &v) -> std::string { return "<Vector2(x=" + std::to_string(v.x) + ", y=" + std::to_string(v.y) + ")>"; })
        .def("__eq__", [](const Vector2 &v1, const Vector2 &v2) { return v1.x == v2.x && v1.y == v2.y; })
        // TODO: is __neq__ needed ?
        .def("__neg__", [](const Vector2 &v) -> Vector2 { return Vector2(-v.x, -v.y); })
        .def("__pos__", [](const Vector2 &v) -> Vector2 { return v; })
        // Methods
        .def("abs", &Vector2::abs)
        .def("angle", &Vector2::angle)
        .def("angle_to", &Vector2::angle_to)
        .def("angle_to_point", &Vector2::angle_to_point)
        .def("clamped", &Vector2::clamped)
        .def("cubic_interpolate", &Vector2::cubic_interpolate)
        .def("distance_squared_to", &Vector2::distance_squared_to)
        .def("distance_to", &Vector2::distance_to)
        .def("dot", &Vector2::dot)
        .def("floor", &Vector2::floor)
        .def("aspect", &Vector2::aspect)
        .def("length", &Vector2::length)
        .def("length_squared", &Vector2::length_squared)
        // Cannot directly bind to Vector2::linear_interpolate because there is two definitions of it
        .def("linear_interpolate", [](const Vector2 &a, const Vector2 &b, real_t t) -> Vector2 { return a.linear_interpolate(b, t); })
        .def("normalized", &Vector2::normalized)
        .def("reflect", &Vector2::reflect)
        .def("rotated", &Vector2::rotated)
        .def("slide", &Vector2::slide)
        .def("snapped", &Vector2::snapped)
        .def("tangent", &Vector2::tangent)
        // Properties
        .def_readwrite("height", &Vector2::height)
        .def_readwrite("width", &Vector2::width)
        .def_readwrite("x", &Vector2::x)
        .def_readwrite("y", &Vector2::y)
        // Constants
        ;

    return m.ptr();
}


void init() {
    pybind11_init();
}

}
