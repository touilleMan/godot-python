#pragma once


#include "pythonscript.h"

#include "core/object.h"
#include "core/variant.h"


namespace bindings {
    // Dummy class to wrap Godot's Object* pointer from Python point of view
    struct GodotObject {
        ::Object *godot_obj;
        GodotObject(::Object *obj) : godot_obj(obj) {}
        GodotObject() {}
    };
    void init();
}
