#ifndef PYTHONSCRIPT_PLANE_H
#define PYTHONSCRIPT_PLANE_H

// Godot imports
#include "core/math/plane.h"
// Micropython imports
#include "micropython/micropython.h"
// Pythonscript imports
#include "bindings/dynamic_binder.h"
#include "bindings/tools.h"


class PlaneBinder : public Singleton<PlaneBinder>, public BaseBinder {
    friend Singleton<PlaneBinder>;

protected:
    PlaneBinder();
    mp_obj_t _generate_bind_locals_dict();
    mp_obj_type_t _mp_type;

public:
    typedef struct {
        mp_obj_base_t base;
        Plane godot_plane;
    } mp_godot_bind_t;

    _FORCE_INLINE_ mp_obj_t build_pyobj() const { auto p = Plane(); return this->build_pyobj(p); }
    mp_obj_t build_pyobj(const Plane &p_plane) const;
    Variant pyobj_to_variant(mp_obj_t pyobj) const;
    _FORCE_INLINE_ mp_obj_t variant_to_pyobj(const Variant &p_variant) const { return this->build_pyobj(p_variant); }

};


#endif // PYTHONSCRIPT_PLANE_H
