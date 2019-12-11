# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_rid, godot_int
from godot.bindings cimport Resource


@cython.final
cdef class RID:

    def __init__(self, Resource from_=None):
        if from_ is not None:
            gdapi.godot_rid_new_with_resource(
                &self._gd_data,
                from_._gd_ptr
            )
        else:
            gdapi.godot_rid_new(&self._gd_data)

    @staticmethod
    cdef inline RID new():
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        gdapi.godot_rid_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline RID new_with_resource(Resource resource):
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        gdapi.godot_rid_new_with_resource(&ret._gd_data, resource._gd_ptr)
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
        return RID.operator_less(self, _other)

    def __eq__(self, other):
        try:
            return RID.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not RID.operator_equal(self, other)
        except TypeError:
            return True

    # Methods

    cpdef inline godot_int get_id(self):
        return gdapi.godot_rid_get_id(&self._gd_data)
