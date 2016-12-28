#include "micropython.h"
// Godot imports
#include "core/variant.h"
// Pythonscript imports
#include "bindings/converter.h"
#include "bindings/dynamic_binder.h"


// This should be called from a micropython context (with nlr_push set)
Variant pyobj_to_variant(const mp_obj_t pyobj) {
    if (MP_OBJ_IS_INT(pyobj)) {
        return Variant(mp_obj_get_int(pyobj));
    } else if (MP_OBJ_IS_STR(pyobj)) {
        return Variant(qstr_str(MP_OBJ_QSTR_VALUE(pyobj)));
    } else if (mp_obj_is_float(pyobj)) {
        // TODO: use float for smaller numbers ?
        return Variant(mp_obj_get_float(pyobj));
    } else if (MP_OBJ_IS_OBJ(pyobj)) {
        // TODO: optimize this by using inheritance in binders
        mp_obj_type_t *pyobj_type = mp_obj_get_type(pyobj);
        auto binder = GodotBindingsModule::get_singleton()->get_binder(pyobj_type->name);
        if (binder != NULL) {
            auto p_obj = static_cast<mp_godot_bind_t *>(MP_OBJ_TO_PTR(pyobj));
            return p_obj->godot_variant;
        }
    }
    // Not handled raise exception in python caller
    nlr_raise(mp_obj_new_exception_msg_varg(&mp_type_TypeError,
        "Can't convert %s to Godot's Variant", mp_obj_get_type_str(pyobj)));
}


mp_obj_t variant_to_pyobj(const Variant &p_variant) {
    switch (p_variant.get_type()) {
    case Variant::Type::NIL:
        return mp_const_none;

    // atomic types
    case Variant::Type::BOOL: {
        const bool val = p_variant;
        return val ? mp_const_true : mp_const_false;
    }
    case Variant::Type::INT: {
        const int val = p_variant;
        return mp_obj_new_int(val);
    }
    case Variant::Type::REAL: {
        const double val = p_variant;
        return mp_obj_new_float(val);
    }
    case Variant::Type::STRING: {
        const String val = p_variant;
        const char *raw_str = val.utf8().get_data();
        return MP_OBJ_NEW_QSTR(qstr_from_str(raw_str));
    }
    // math types

    case Variant::Type::VECTOR2:        // 5
        break;
    case Variant::Type::RECT2:
        break;
    case Variant::Type::VECTOR3:
        break;
    case Variant::Type::MATRIX32:
        break;
    case Variant::Type::PLANE:
        break;
    case Variant::Type::QUAT:           // 10
        break;
    case Variant::Type::_AABB: //sorry naming convention fail :( not like it's used often
        break;
    case Variant::Type::MATRIX3:
        break;
    case Variant::Type::TRANSFORM:
        break;

    // misc types
    case Variant::Type::COLOR:
        break;
    case Variant::Type::IMAGE:          // 15
        break;
    case Variant::Type::NODE_PATH:
        break;
    case Variant::Type::_RID:
        break;
    case Variant::Type::OBJECT:
    {
        Object *obj = p_variant;
        auto binder = GodotBindingsModule::get_singleton()->get_binder(obj->get_type_name());
        if (binder) {
            return binder->build_mpo_wrapper(obj);
        }
    } break;
    case Variant::Type::INPUT_EVENT:
        break;
    case Variant::Type::DICTIONARY:     // 20
        break;
    case Variant::Type::ARRAY:
        break;

    // arrays
    case Variant::Type::RAW_ARRAY:
        break;
    case Variant::Type::INT_ARRAY:
        break;
    case Variant::Type::REAL_ARRAY:
        break;
    case Variant::Type::STRING_ARRAY:   // 25
        break;
    case Variant::Type::VECTOR2_ARRAY:
        break;
    case Variant::Type::VECTOR3_ARRAY:
        break;
    case Variant::Type::COLOR_ARRAY:
        break;
    default:
        ERR_EXPLAIN("Unknown Variant type `" + Variant::get_type_name(p_variant.get_type()) + "` (this should never happen !)");
        ERR_FAIL_V(mp_const_none);
    }
    ERR_EXPLAIN("Variant type `" + Variant::get_type_name(p_variant.get_type()) + "` not implemented yet");
    ERR_FAIL_V(mp_const_none);
}
