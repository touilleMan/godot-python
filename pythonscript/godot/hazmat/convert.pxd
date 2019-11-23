# cython: c_string_type=unicode, c_string_encoding=utf8

from libc.stddef cimport wchar_t
from godot.hazmat._gdapi cimport pythonscript_gdapi as gdapi
from godot.hazmat.gdnative_api_struct cimport (
    godot_string,
)


cdef inline object godot_string_to_pyobj(const godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    return <char*>gdapi.godot_string_wide_str(p_gdstr)


cdef inline godot_string pyobj_to_godot_string(object pystr):
    # TODO: unicode&windows support is most likely broken...
    cdef godot_string gdstr;
    gdapi.godot_string_new_with_wide_string(
        &gdstr, <wchar_t*><char*>pystr, len(pystr)
    )
    return gdstr
