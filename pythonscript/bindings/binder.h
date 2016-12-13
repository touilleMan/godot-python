#ifndef BINDER_H
#define BINDER_H

#include "micropython.h"
// Godot imports
#include "core/object.h"
#include "core/map.h"


namespace pythonscript { namespace bindings {


// Mainly used to have a common class for all types binder in order to store
// them together in a map
class BaseGodotTypeBinder {
};


template<class T>
class GodotTypeBinder : public BaseGodotTypeBinder {

private:
    const StringName name;
    // const qstr qstr_name;  # TODO: useful ?
    // GodotTypeBinder *parent;  # TODO: useful ?
    Map<qstr, mp_obj_t> method_lookup;
    Map<qstr, PropertyInfo> property_lookup;

    // Type object of this godot type in python
    mp_obj_type_t mp_type;

    static mp_obj_t _wrap_godot_method(StringName p_name);

public:

    // Struture representing a single instance of this godot type in python
    typedef struct {
        mp_obj_base_t base;
        T *godot_obj;
    } mp_instance_t;

    GodotTypeBinder() : name(T::get_type_static()) {};

    void init();
    inline mp_obj_type_t *get_mp_obj_type() { return &this->mp_type; };
    mp_obj_t make_new();
    mp_obj_t make_new(T *godot_obj);
    void instance_attr_lookup(mp_obj_t self_in, qstr attr, mp_obj_t *dest);
};


void godot_binding_module_init();
void godot_binding_module_finish();


} }  // namespace

#endif  // BINDER_H
