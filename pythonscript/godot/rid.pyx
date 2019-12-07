# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_rid, godot_int


@cython.final
cdef class RID:

    def __init__(self):
        gdapi.godot_rid_new(&self._gd_data)

    @staticmethod
    cdef inline RID new():
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        gdapi.godot_rid_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline RID from_ptr(const godot_rid *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<RID(id={self.get_id()})>"

    # Operators

    cdef inline bint operator_equal(self, RID b):
        cdef RID ret  = RID.__new__(RID)
        return gdapi.godot_rid_operator_equal(&self._gd_data, &b._gd_data)

    cdef inline bint operator_less(self, RID b):
        cdef RID ret  = RID.__new__(RID)
        return gdapi.godot_rid_operator_less(&self._gd_data, &b._gd_data)

    def __lt__(self, other):
        cdef RID _other = <RID?>other
        return self.operator_less(_other)

    def __eq__(self, other):
        cdef RID _other = <RID?>other
        return self.operator_equal(_other)

    def __ne__(self, other):
        cdef RID _other = <RID?>other
        return not self.operator_equal(_other)

    # Methods

    cpdef inline godot_int get_id(self):
        return gdapi.godot_rid_get_id(&self._gd_data)
