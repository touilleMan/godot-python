#include <cstring>

#include "micropython.h"
// Pythonscript imports
#include "bindings/binder.h"
#include "bindings/dynamic_binder.h"
#include "bindings/builtins_binder.h"
// Godot imports
#include "core/variant.h"
#include "core/object_type_db.h"


GodotBindingsModule::GodotBindingsModule() {
    // TODO: don't use micropython memory mangement for this
    this->_mp_module = mp_obj_new_module(qstr_from_str("godot.bindings"));
}


GodotBindingsModule::~GodotBindingsModule() {
    for(auto E=this->_binders.front(); E; E=E->next()) {
        memdelete(E->get());
    }
}


void GodotBindingsModule::build_binders() {
    MP_WRAP_CALL([this]() {
        List<StringName> types;

    #define STORE_BINDED_TYPE(binder) { \
            const mp_obj_type_t *type = binder->get_mp_type(); \
            mp_store_attr(this->_mp_module, type->name, MP_OBJ_FROM_PTR(type)); \
            this->_binders.push_back(binder); \
    }

        // First init and store builtins bindings
        NilBinder::init();
        STORE_BINDED_TYPE(NilBinder::get_singleton());
        BoolBinder::init();
        STORE_BINDED_TYPE(BoolBinder::get_singleton());
        IntBinder::init();
        STORE_BINDED_TYPE(IntBinder::get_singleton());
        RealBinder::init();
        STORE_BINDED_TYPE(RealBinder::get_singleton());
        StringBinder::init();
        STORE_BINDED_TYPE(StringBinder::get_singleton());
        Vector2Binder::init();
        STORE_BINDED_TYPE(Vector2Binder::get_singleton());

        // Retrieve and create all the modules for freeeeeeeee !
        ObjectTypeDB::get_type_list(&types);
        for(auto E=types.front(); E; E=E->next()) {
            // WARN_PRINTS("Start building " + String(E->get()));
            auto binder = memnew(DynamicBinder(E->get()));
            STORE_BINDED_TYPE(binder);
        }
    });
}


const BaseBinder *GodotBindingsModule::get_binder(const StringName &p_type) const {
    // TODO: optimize this
    for(auto E=this->_binders.front(); E; E=E->next()) {
        if (E->get()->get_type_name() == p_type) {
            return E->get();
        }
    }
    return NULL;
}


const BaseBinder *GodotBindingsModule::get_binder(const qstr type) const {
    // TODO: optimize this
    for(auto E=this->_binders.front(); E; E=E->next()) {
        if (E->get()->get_type_qstr() == type) {
            return E->get();
        }
    }
    return NULL;
}


// This should be called from a micropython context (with nlr_push set)
Variant GodotBindingsModule::pyobj_to_variant(const mp_obj_t pyobj) const {
    mp_obj_type_t *pyobj_type = mp_obj_get_type(pyobj);
    auto binder = this->get_binder(pyobj_type->name);
    if (binder != NULL) {
        return binder->pyobj_to_variant(pyobj);
    }
    // Not handled raise exception in python caller
    nlr_raise(mp_obj_new_exception_msg_varg(&mp_type_TypeError,
        "Can't convert %s to Godot's Variant", mp_obj_get_type_str(pyobj)));
}


mp_obj_t GodotBindingsModule::variant_to_pyobj(const Variant &p_variant) const {
    switch (p_variant.get_type()) {
    case Variant::Type::NIL:
        return mp_const_none;

    // atomic types
    case Variant::Type::BOOL:
        return BoolBinder::get_singleton()->variant_to_pyobj(p_variant);
    case Variant::Type::INT:
        return IntBinder::get_singleton()->variant_to_pyobj(p_variant);
    case Variant::Type::REAL:
        return RealBinder::get_singleton()->variant_to_pyobj(p_variant);
    case Variant::Type::STRING:
        return StringBinder::get_singleton()->variant_to_pyobj(p_variant);

    // math types
    case Variant::Type::VECTOR2:
        return Vector2Binder::get_singleton()->variant_to_pyobj(p_variant);
    case Variant::Type::RECT2:
        break;
    case Variant::Type::VECTOR3:
        break;
    case Variant::Type::MATRIX32:
        break;
    case Variant::Type::PLANE:
        break;
    case Variant::Type::QUAT:
        break;
    case Variant::Type::_AABB:
        break;
    case Variant::Type::MATRIX3:
        break;
    case Variant::Type::TRANSFORM:
        break;

    // misc types
    case Variant::Type::COLOR:
        break;
    case Variant::Type::IMAGE:
        break;
    case Variant::Type::NODE_PATH:
        break;
    case Variant::Type::_RID:
        break;
    case Variant::Type::OBJECT:
    {
        Object *obj = p_variant;
        if (obj != NULL) {
            auto binder = this->get_binder(obj->get_type_name());
            if (binder) {
                return binder->variant_to_pyobj(p_variant);
            }
        } else {
            return mp_const_none;
        }
    } break;
    case Variant::Type::INPUT_EVENT:
        break;
    case Variant::Type::DICTIONARY:
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
    case Variant::Type::STRING_ARRAY:
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
