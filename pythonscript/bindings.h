#pragma once


#include "pythonscript.h"

#include "core/object.h"
#include "core/variant.h"


typedef PoolByteArray RawArray;
typedef PoolRealArray PoolFloatArray;


namespace bindings {
    // Dummy class to wrap Godot's Object* pointer from Python point of view
    struct GodotObject {
        ::Object *godot_obj;
        GodotObject(::Object *obj) : godot_obj(obj) {}
        GodotObject() {}
    };
    void init();

    // Defined in bindings.gen.cpp
    void __register_generated_bindings(py::module m);
}
