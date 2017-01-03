#include <cstring>

#include "micropython.h"
// Pythonscript imports
#include "bindings/binder.h"
#include "bindings/dynamic_binder.h"
// Godot imports
#include "core/object_type_db.h"


GodotBindingsModule *GodotBindingsModule::_singleton = NULL;


void GodotBindingsModule::init() {
    if (_singleton == NULL) {
        _singleton = new GodotBindingsModule();
        // TODO: don't use micropython memory mangement for this
        _singleton->_mp_module = mp_obj_new_module(qstr_from_str("godot.bindings"));
        MP_WRAP_CALL(_singleton->_build_binders);
    }
}


void GodotBindingsModule::finish() {
    if (_singleton != NULL) {
        delete _singleton;
        _singleton = NULL;
    }
}


void GodotBindingsModule::_build_binders() {
    // Retrieve and create all the modules for freeeeeeeee !
    List<StringName> types;
    ObjectTypeDB::get_type_list(&types);
    for(auto E=types.front(); E; E=E->next()) {
        // WARN_PRINTS("Start building " + String(E->get()));
        auto binder = memnew(DynamicBinder(E->get()));
        const mp_obj_type_t *type = binder->get_mp_type();
        mp_store_attr(this->_mp_module, type->name, MP_OBJ_FROM_PTR(type));
        this->_binders.push_back(binder);
    }
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


GodotBindingsModule::~GodotBindingsModule() {
    for(auto E=this->_binders.front(); E; E=E->next()) {
        memdelete(E->get());
    }
}
