#include "micropython.h"
// Godot imports
#include "core/variant.h"


namespace pythonscript { namespace bindings {


Variant variant_to_pyobj(const mp_obj_t pyobj);
mp_obj_t pyobj_to_variant(const Variant &p_variant);


} }   // namespace
