#ifndef BINDER_H
#define BINDER_H

#include "micropython.h"
// Godot imports
#include "core/string_db.h"
#include "core/object_type_db.h"
#include "core/map.h"


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
	inline StringName get_type_name() const { return _type_name; }
	inline mp_obj_type_t get_mp_type() const { return _mp_type; }
	void get_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) const;

};


void godot_binding_module_init();
void godot_binding_module_destroy();


#endif  // BINDER_H
