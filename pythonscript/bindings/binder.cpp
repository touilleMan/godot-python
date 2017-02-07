#include <cstring>

#include "micropython.h"
// Pythonscript imports
#include "bindings/binder.h"
#include "bindings/dynamic_binder.h"
#include "bindings/builtins_binder/atomic.h"
#include "bindings/builtins_binder/vector2.h"
// Godot imports
#include "core/variant.h"
#include "core/class_db.h"
#include "core/global_constants.h"
#include "core/globals.h"


void init_bindings() {
    GodotBindingsModule::init();
    NilBinder::init();
    BoolBinder::init();
    IntBinder::init();
    RealBinder::init();
    StringBinder::init();
    Vector2Binder::init();
    // TODO: make this lazy ?
    GodotBindingsModule::get_singleton()->build_binders();
}


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

        #define STORE_BINDED_TYPE(binder) { \
                const mp_obj_type_t *type = binder->get_mp_type(); \
                mp_store_attr(this->_mp_module, type->name, MP_OBJ_FROM_PTR(type)); \
                this->_binders.push_back(binder); \
        }

        // Bind builtins bindings
        STORE_BINDED_TYPE(NilBinder::get_singleton());
        STORE_BINDED_TYPE(BoolBinder::get_singleton());
        STORE_BINDED_TYPE(IntBinder::get_singleton());
        STORE_BINDED_TYPE(RealBinder::get_singleton());
        STORE_BINDED_TYPE(StringBinder::get_singleton());
        STORE_BINDED_TYPE(Vector2Binder::get_singleton());
        // TODO: finish builtins

        // Dynamically bind modules registered through ClassDB
        List<StringName> classes;
        ClassDB::get_class_list(&classes);
        for(auto E=classes.front(); E; E=E->next()) {
            auto binder = memnew(DynamicBinder(E->get()));
            STORE_BINDED_TYPE(binder);
        }

        // Bind global singletons
        #define STORE_GLOBAL_SINGLETON(NAME, STORE_NAME) { \
            auto binder = static_cast<const DynamicBinder *>(this->get_binder("_"#NAME)); \
            Object *singleton = GlobalConfig::get_singleton()->get_singleton_object(#NAME); \
            if (!binder) { \
                WARN_PRINTS("Cannot retrieve binding `_" #NAME "`"); \
            } else if (!singleton) { \
                WARN_PRINTS("Cannot retrieve global singleton `" #STORE_NAME "`"); \
            } else { \
                mp_obj_t pyobj = binder->build_pyobj(singleton); \
                mp_store_attr(this->_mp_module, qstr_from_str(#STORE_NAME), MP_OBJ_FROM_PTR(pyobj)); \
            } \
        }
        STORE_GLOBAL_SINGLETON(AudioServer, AS);
        STORE_GLOBAL_SINGLETON(AudioServer, AudioServer);
        STORE_GLOBAL_SINGLETON(Geometry, Geometry);
        STORE_GLOBAL_SINGLETON(GlobalConfig, GlobalConfig);
        STORE_GLOBAL_SINGLETON(IP, IP);
        STORE_GLOBAL_SINGLETON(Input, Input);
        STORE_GLOBAL_SINGLETON(InputMap, InputMap);
        STORE_GLOBAL_SINGLETON(Marshalls, Marshalls);
        STORE_GLOBAL_SINGLETON(OS, OS);
        STORE_GLOBAL_SINGLETON(Engine, Engine);
        STORE_GLOBAL_SINGLETON(ClassDB, ClassDB);
        STORE_GLOBAL_SINGLETON(PhysicsServer, PS);
        STORE_GLOBAL_SINGLETON(Physics2DServer, PS2D);
        STORE_GLOBAL_SINGLETON(PathRemap, PathRemap);
        STORE_GLOBAL_SINGLETON(Performance, Performance);
        STORE_GLOBAL_SINGLETON(Physics2DServer, Physics2DServer);
        STORE_GLOBAL_SINGLETON(PhysicsServer, PhysicsServer);
        STORE_GLOBAL_SINGLETON(ResourceLoader, ResourceLoader);
        STORE_GLOBAL_SINGLETON(ResourceSaver, ResourceSaver);
        STORE_GLOBAL_SINGLETON(SpatialSoundServer, SS);
        STORE_GLOBAL_SINGLETON(SpatialSound2DServer, SS2D);
        STORE_GLOBAL_SINGLETON(SpatialSound2DServer, SpatialSound2DServer);
        STORE_GLOBAL_SINGLETON(SpatialSoundServer, SpatialSoundServer);
        STORE_GLOBAL_SINGLETON(TranslationServer, TS);
        STORE_GLOBAL_SINGLETON(TranslationServer, TranslationServer);
        STORE_GLOBAL_SINGLETON(VisualServer, VS);
        STORE_GLOBAL_SINGLETON(VisualServer, VisualServer);

        // Bind global constants
        auto int_binder = IntBinder::get_singleton();
        int count = GlobalConstants::get_global_constant_count();
        for (int i = 0; i < count; ++i) {
            qstr key = qstr_from_str(GlobalConstants::get_global_constant_name(i));
            int v = GlobalConstants::get_global_constant_value(i);
            mp_store_attr(this->_mp_module, key, int_binder->build_pyobj(v));
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
    case Variant::Type::TRANSFORM2D:
        break;
    case Variant::Type::PLANE:
        break;
    case Variant::Type::QUAT:
        break;
    case Variant::Type::RECT3:
        break;
    case Variant::Type::BASIS:
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
            auto binder = this->get_binder(obj->get_class_name());
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
    case Variant::Type::POOL_BYTE_ARRAY:
        break;
    case Variant::Type::POOL_INT_ARRAY:
        break;
    case Variant::Type::POOL_REAL_ARRAY:
        break;
    case Variant::Type::POOL_STRING_ARRAY:
        break;
    case Variant::Type::POOL_VECTOR2_ARRAY:
        break;
    case Variant::Type::POOL_VECTOR3_ARRAY:
        break;
    case Variant::Type::POOL_COLOR_ARRAY:
        break;

    default:
        ERR_EXPLAIN("Unknown Variant type `" + Variant::get_type_name(p_variant.get_type()) + "` (this should never happen !)");
        ERR_FAIL_V(mp_const_none);
    }
    ERR_EXPLAIN("Variant type `" + Variant::get_type_name(p_variant.get_type()) + "` not implemented yet");
    ERR_FAIL_V(mp_const_none);
}
