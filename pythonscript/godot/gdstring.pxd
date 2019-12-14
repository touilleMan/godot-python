# cython: language_level=3

cimport cython

from godot._hazmat.gdnative_api_struct cimport godot_string


@cython.final
cdef class GDString:
    cdef godot_string _gd_data

    @staticmethod
    cdef inline GDString new()
    @staticmethod
    cdef inline GDString new_with_pystr(str pystr)
    @staticmethod
    cdef inline GDString from_ptr(const godot_string *_ptr)
