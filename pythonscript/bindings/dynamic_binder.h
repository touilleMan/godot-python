#ifndef BINDER_H
#define BINDER_H

#include "micropython.h"
// Godot imports
#include "core/string_db.h"
#include "core/object_type_db.h"
#include "core/map.h"


class DynamicBinder;

// TODO: Currently Godot OS::singleton is destroyed too soon so
// ~GodotBindingsModule cause segfault when releasing memory...
// (see https://github.com/godotengine/godot/issues/1083)
class GodotBindingsModule {
private:
    List<DynamicBinder*> _binders;
    mp_obj_t _mp_module = mp_const_none;
    bool _initialized = false;
    static GodotBindingsModule _singleton;

    GodotBindingsModule() {};
public:
    _FORCE_INLINE_ static GodotBindingsModule *get_singleton() { return &_singleton; };
    virtual ~GodotBindingsModule();

    void init();
    void pre_init();
    _FORCE_INLINE_ mp_obj_t get_mp_module() const { return this->_mp_module; };
    const DynamicBinder *get_binder(const StringName &p_type) const;
    const DynamicBinder *get_binder(const qstr type) const;
    // TODO implements this
    // mp_obj_t variant_to_pyobj(const Variant &p_variant) const;
    // Variant pyobj_to_variant(const mp_obj_t pyobj) const;
};


// Struture representing a single instance of a godot object in python
typedef struct {
    mp_obj_base_t base;
    Object *godot_obj;
    Variant godot_variant; // Keep a variant on the object here for memory
                           // management and easier convertion to Godot
} mp_godot_bind_t;


class DynamicBinder {
private:
	const StringName _type_name;
    qstr _type_qstr;
    // DynamicBinder *parent;  # TODO: useful ?
    Map<qstr, mp_obj_t> method_lookup;
    Map<qstr, PropertyInfo> property_lookup;

    // Type object of this godot type in python
    mp_obj_type_t _mp_type;
public:
	DynamicBinder(StringName type_name);
    _FORCE_INLINE_ StringName get_type_name() const { return this->_type_name; }
    _FORCE_INLINE_ qstr get_type_qstr() const { return this->_type_qstr; }
    _FORCE_INLINE_ const mp_obj_type_t *get_mp_type() const { return &this->_mp_type; }
    void get_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) const;
    mp_obj_t build_mpo_wrapper(Object *obj) const;

};


#endif  // BINDER_H
