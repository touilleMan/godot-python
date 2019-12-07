# cython: language_level=3

cimport cython

from godot._hazmat.gdnative_api_struct cimport godot_rid, godot_int


@cython.final
cdef class RID:
    cdef godot_rid _gd_data

    @staticmethod
    cdef inline RID new()

    @staticmethod
    cdef inline RID from_ptr(const godot_rid *_ptr)

    # Operators

    cdef inline bint operator_equal(self, RID b)
    cdef inline bint operator_less(self, RID b)

    # Methods

    cpdef inline godot_int get_id(self)
