#ifndef VECTOR2_H
#define VECTOR2_H

// Godot imports
#include "core/math/math_2d.h"
// Micropython imports
#include "micropython/micropython.h"
// Pythonscript imports
#include "bindings/dynamic_binder.h"
#include "bindings/tools.h"


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


#endif // VECTOR2_H
