#include "bindings/tools.h"

static mp_obj_t _retrieve_attr(mp_obj_t self_in, qstr attr)
{
    // First use generic method lookup (basically copied from `mp_load_method_maybe`)
    mp_obj_type_t *type = mp_obj_get_type(self_in);
    mp_map_t *locals_map = &type->locals_dict->map;
    mp_map_elem_t *elem = mp_map_lookup(locals_map, MP_OBJ_NEW_QSTR(attr), MP_MAP_LOOKUP);
    return elem != NULL ? elem->value : MP_OBJ_NULL;
}

void attr_with_locals_and_properties(mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
    if (dest[0] == MP_OBJ_NULL) {
        // load attribute
        mp_obj_t val = _retrieve_attr(self_in, attr);
        if (val != MP_OBJ_NULL) {
            if (mp_obj_get_type(val) == &mp_type_property) {
                // Property should be retrieve by calling getter by hand
                mp_obj_t getter = mp_obj_property_get(val)[0];
                dest[0] = mp_call_function_1(getter, self_in);
                dest[1] = MP_OBJ_NULL;
            } else {
                // Classic attribute
                mp_obj_type_t *type = mp_obj_get_type(self_in);
                mp_convert_member_lookup(self_in, type, val, dest);
            }
        }
    } else if (dest[1] != MP_OBJ_NULL) {
        // store attribute, only property are accepted here
        mp_obj_t val = _retrieve_attr(self_in, attr);
        if (val != MP_OBJ_NULL && mp_obj_get_type(val) == &mp_type_property) {
            mp_obj_t setter = mp_obj_property_get(val)[1];
            mp_call_function_2(setter, self_in, dest[1]);
            dest[0] = MP_OBJ_NULL;
        }
    }
    // note that delete attribute is not supported
}
