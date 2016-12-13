#include "micropython.h"
#include "micropython-wrap/detail/micropython.h"


STATIC const mp_obj_type_t socket_type = {
    { &mp_type_type },
    .name = MP_QSTR_socket,
    .make_new = socket_make_new,
    .protocol = &socket_stream_p,
    .locals_dict = (mp_obj_t)&socket_locals_dict,
};

// Godot binder metaclass

// Godot binder Node class

