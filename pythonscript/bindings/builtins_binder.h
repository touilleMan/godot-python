#ifndef BUILTINS_BINDER_H
#define BUILTINS_BINDER_H

#include "micropython.h"
// Godot imports

// Pythonscript imports
#include "bindings/dynamic_binder.h"
#include "bindings/tools.h"



class NilBinder : public Singleton<NilBinder>, public BaseBinder {
    friend Singleton<NilBinder>;

protected:
    NilBinder() {
        const char *name = "Nil";
        this->_type_name= StringName(name);
        this->_p_mp_type = &mp_type_NoneType;
    }

public:
    _FORCE_INLINE_ mp_obj_t build_pyobj() const { return mp_const_none; }
    Variant pyobj_to_variant(mp_obj_t pyobj) const { return Variant(); }
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const { return mp_const_none; }
};


class BoolBinder : public Singleton<BoolBinder>, public BaseBinder {
    friend Singleton<BoolBinder>;

protected:
    BoolBinder() {
        const char *name = "Bool";
        this->_type_name= StringName(name);
        this->_p_mp_type = &mp_type_bool;
    }

public:
    _FORCE_INLINE_ mp_obj_t build_pyobj() const { return mp_const_false; }
    _FORCE_INLINE_ mp_obj_t build_pyobj(bool v) const { return v ? mp_const_true : mp_const_false; }
    Variant pyobj_to_variant(mp_obj_t pyobj) const { return Variant(pyobj == mp_const_true); }
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const {
        bool val = p_variant;
        return val ? mp_const_true : mp_const_false;
    }
};


class IntBinder : public Singleton<IntBinder>, public BaseBinder {
    friend Singleton<IntBinder>;

protected:
    IntBinder() {
        const char *name = "Int";
        this->_type_name= StringName(name);
        this->_p_mp_type = &mp_type_int;
    }

public:
    _FORCE_INLINE_ bool is_type(mp_obj_t pyobj) { return MP_OBJ_IS_INT(pyobj); }
    _FORCE_INLINE_ mp_obj_t build_pyobj() const { return mp_obj_new_int(0); }
    _FORCE_INLINE_ mp_obj_t build_pyobj(int v) const { return mp_obj_new_int(v); }
    Variant pyobj_to_variant(mp_obj_t pyobj) const { return Variant(mp_obj_get_int(pyobj)); }
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const {
        int val = p_variant;
        return mp_obj_new_int(val);
    }
};


// TODO: make sure whether we should use float or double here...
class RealBinder : public Singleton<RealBinder>, public BaseBinder {
    friend Singleton<RealBinder>;

protected:
    RealBinder() {
        const char *name = "Real";
        this->_type_name= StringName(name);
        this->_p_mp_type = &mp_type_float;
    }

public:
    _FORCE_INLINE_ mp_obj_t build_pyobj() const { return mp_obj_new_float(0); }
    _FORCE_INLINE_ mp_obj_t build_pyobj(float v) const { return mp_obj_new_float(v); }
    Variant pyobj_to_variant(mp_obj_t pyobj) const {
        return Variant(mp_obj_get_float(pyobj));
    }
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const {
        double val = p_variant;
        return mp_obj_new_float(val);
    }
};


class StringBinder : public Singleton<StringBinder>, public BaseBinder {
    friend Singleton<StringBinder>;

protected:
    StringBinder() {
        const char *name = "String";
        this->_type_name= StringName(name);
        this->_p_mp_type = &mp_type_str;
    }

public:
    _FORCE_INLINE_ bool is_type(mp_obj_t pyobj) { return MP_OBJ_IS_STR(pyobj); }
    _FORCE_INLINE_ mp_obj_t build_pyobj() const { return this->build_pyobj(""); }
    _FORCE_INLINE_ mp_obj_t build_pyobj(const char *v) const {
        return mp_obj_new_str(v, strlen(v), false);
    }
    Variant pyobj_to_variant(mp_obj_t pyobj) const {
        return Variant(qstr_str(MP_OBJ_QSTR_VALUE(pyobj)));
    }
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const {
        const String val = p_variant;
        const char *raw_str = val.utf8().get_data();
        return mp_obj_new_str(raw_str, strlen(raw_str), false);
    }
};


class Vector2Binder : public Singleton<Vector2Binder>, public BaseBinder {
    friend Singleton<Vector2Binder>;

protected:
    Vector2Binder();
    mp_obj_t _generate_bind_locals_dict();
    mp_obj_type_t _mp_type;

public:
    typedef struct {
        mp_obj_base_t base;
        Vector2 godot_vect2;
    } mp_godot_bind_t;

    _FORCE_INLINE_ mp_obj_t build_pyobj() const { auto v = Vector2(); return this->build_pyobj(v); }
    mp_obj_t build_pyobj(const Vector2 &p_vect2) const;
    Variant pyobj_to_variant(mp_obj_t pyobj) const;
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const { return this->build_pyobj(p_variant); }

};


#endif // BUILTINS_BINDER_H
