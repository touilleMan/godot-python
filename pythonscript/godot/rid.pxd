# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_rid, godot_int


@cython.final
cdef class RID:
    cdef godot_rid _gd_data

    @staticmethod
    cdef RID new()

    @staticmethod
    cdef RID from_ptr(const godot_rid *_ptr)

    # Operators

    cdef inline bint operator_equal(self, RID b)
    cdef inline bint operator_less(self, RID b)

    # Methods

    cpdef inline godot_int get_id(self)
