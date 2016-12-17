#include "micropython.h"
// Godot imports
#include "core/variant.h"


mp_obj_t variant_to_pyobj(const Variant &p_variant);
Variant pyobj_to_variant(const mp_obj_t pyobj);
