#ifndef BINDER_H
#define BINDER_H

#include "micropython.h"
// Godot imports
#include "core/string_db.h"
#include "core/object_type_db.h"
#include "core/map.h"


class DynamicBinder;


class GodotBindingsModule {
private:
    List<DynamicBinder*> _binders;
    mp_obj_t _mp_module;
    bool _initialized = false;
public:
    GodotBindingsModule();
    virtual ~GodotBindingsModule();

    void init();
    mp_obj_t get_mp_module() const { return this->_mp_module; };
    // TODO implements this
    // mp_obj_t variant_to_pyobj(const Variant &p_variant) const;
    // Variant pyobj_to_variant(const mp_obj_t pyobj) const;
};


// Struture representing a single instance of a godot object in python
typedef struct {
    mp_obj_base_t base;
    Object *godot_obj;
} mp_godot_bind_t;


class DynamicBinder {
private:
	const StringName _type_name;
    // const qstr qstr_name;  # TODO: useful ?
    // DynamicBinder *parent;  # TODO: useful ?
    Map<qstr, mp_obj_t> method_lookup;
    Map<qstr, PropertyInfo> property_lookup;

    // Type object of this godot type in python
    mp_obj_type_t _mp_type;
public:
	DynamicBinder(StringName type_name);
	inline StringName get_type_name() const { return this->_type_name; }
    inline const mp_obj_type_t *get_mp_type() const { return &this->_mp_type; }
	void get_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) const;

};


#endif  // BINDER_H
