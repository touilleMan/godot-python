#ifndef PYTHONSCRIPT_VECTOR3_H
#define PYTHONSCRIPT_VECTOR3_H

// Godot imports
#include "core/math/vector3.h"
// Micropython imports
#include "micropython/micropython.h"
// Pythonscript imports
#include "bindings/dynamic_binder.h"
#include "bindings/tools.h"


class Vector3Binder : public Singleton<Vector3Binder>, public BaseBinder {
    friend Singleton<Vector3Binder>;

protected:
    Vector3Binder();
    mp_obj_t _generate_bind_locals_dict();
    mp_obj_type_t _mp_type;

public:
    typedef struct {
        mp_obj_base_t base;
        Vector3 godot_vect3;
    } mp_godot_bind_t;

    _FORCE_INLINE_ mp_obj_t build_pyobj() const { auto v = Vector3(); return this->build_pyobj(v); }
    mp_obj_t build_pyobj(const Vector3 &p_vect3) const;
    Variant pyobj_to_variant(mp_obj_t pyobj) const;
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const { return this->build_pyobj(p_variant); }

};


#endif // PYTHONSCRIPT_VECTOR3_H
