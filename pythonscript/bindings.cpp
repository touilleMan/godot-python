#include "pythonscript.h"
#include "bindings.h"

#include "core/object.h"


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

    // Expose godot.bindings as a module
    auto sys = py::module::import("sys");
    sys.attr("modules")["godot.bindings"] = m;

    return m.ptr();
}

void init() {
	pybind11_init();
}

}
