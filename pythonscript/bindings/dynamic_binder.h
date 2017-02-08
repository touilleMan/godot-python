#ifndef DYNAMIC_BINDER_H
#define DYNAMIC_BINDER_H

// Godot imports
#include "core/string_db.h"
#include "core/class_db.h"
#include "core/map.h"
// Micropython imports
#include "micropython/micropython.h"
// Pythonscript imports
#include "bindings/binder.h"


class DynamicBinder : public BaseBinder {

private:
    // DynamicBinder *parent;  # TODO: useful ?
    Map<qstr, mp_obj_t> method_lookup;
    Map<qstr, StringName*> property_lookup;

    // Type object of this godot type in python
    mp_obj_type_t _mp_type;

public:

    // Struture representing a single instance of a godot object in python
    typedef struct {
        mp_obj_base_t base;
        Object *godot_obj;
        Variant godot_variant; // Keep a variant on the object here for memory
                               // management and easier convertion to Godot
    } mp_godot_bind_t;

	DynamicBinder(StringName type_name);
    ~DynamicBinder();

    virtual mp_obj_t build_pyobj() const;
    mp_obj_t build_pyobj(Object *obj) const;
    virtual Variant pyobj_to_variant(mp_obj_t pyobj) const;
    virtual mp_obj_t variant_to_pyobj(const Variant &p_variant) const;
};


#endif  // DYNAMIC_BINDER_H
