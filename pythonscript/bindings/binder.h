#ifndef PYTHONSCRIPT_BINDER_H
#define PYTHONSCRIPT_BINDER_H

// Godot imports
#include "core/string_db.h"
#include "core/list.h"
// Micropython imports
#include "micropython/micropython.h"
// Pythonscript imports
#include "bindings/tools.h"


void init_bindings();


class BaseBinder {
protected:
    StringName _type_name;
    const mp_obj_type_t *_p_mp_type;

public:
    _FORCE_INLINE_ const char *get_type_str() const { return qstr_str(this->get_type_qstr()); }
    _FORCE_INLINE_ StringName get_type_name() const { return this->_type_name; }
    _FORCE_INLINE_ qstr get_type_qstr() const { return this->_p_mp_type->name; }
    _FORCE_INLINE_ const mp_obj_type_t *get_mp_type() const { return this->_p_mp_type; }

    virtual bool is_type(mp_obj_t pyobj) { return MP_OBJ_IS_TYPE(pyobj, this->_p_mp_type); }
    virtual mp_obj_t build_pyobj() const = 0;
    virtual Variant pyobj_to_variant(mp_obj_t pyobj) const = 0;
    virtual mp_obj_t variant_to_pyobj(const Variant &p_variant) const = 0;
};


class GodotBindingsModule : public Singleton<GodotBindingsModule> {
    friend Singleton<GodotBindingsModule>;

private:
    List<BaseBinder*> _binders;
    mp_obj_t _mp_module = mp_const_none;

protected:
    GodotBindingsModule();
    virtual ~GodotBindingsModule();

public:
    void build_binders();
    _FORCE_INLINE_ mp_obj_t get_mp_module() const { return this->_mp_module; };
    const BaseBinder *get_binder(const StringName &p_type) const;
    const BaseBinder *get_binder(const qstr type) const;

    mp_obj_t object_to_pyobj(const Object *p_obj) const;
    mp_obj_t variant_to_pyobj(const Variant &p_variant) const;
    Variant pyobj_to_variant(const mp_obj_t pyobj) const;
};


#endif  // PYTHONSCRIPT_BINDER_H
