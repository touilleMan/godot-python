#ifndef BINDER_H
#define BINDER_H

#include "micropython.h"
// Godot imports
#include "core/string_db.h"
#include "core/list.h"


class BaseBinder {
public:
    virtual StringName get_type_name() const = 0;
    virtual qstr get_type_qstr() const = 0;
    virtual const mp_obj_type_t *get_mp_type() const = 0;
    virtual void get_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) const = 0;
    virtual mp_obj_t build_mpo_wrapper(Object *obj) const = 0;
};


// TODO: Currently Godot OS::singleton is destroyed too soon so
// ~GodotBindingsModule cause segfault when releasing memory...
// (see https://github.com/godotengine/godot/issues/1083)
class GodotBindingsModule {
private:
    List<BaseBinder*> _binders;
    mp_obj_t _mp_module = mp_const_none;
    bool _initialized = false;
    static GodotBindingsModule *_singleton;

    GodotBindingsModule() {};
    void _build_binders();

public:
    _FORCE_INLINE_ static GodotBindingsModule *get_singleton() { return _singleton; };
    void static init();
    void static finish();
    virtual ~GodotBindingsModule();

    void boostrap();
    _FORCE_INLINE_ mp_obj_t get_mp_module() const { return this->_mp_module; };
    const BaseBinder *get_binder(const StringName &p_type) const;
    const BaseBinder *get_binder(const qstr type) const;
    // TODO implements this
    // mp_obj_t variant_to_pyobj(const Variant &p_variant) const;
    // Variant pyobj_to_variant(const mp_obj_t pyobj) const;
};


#endif  // BINDER_H
