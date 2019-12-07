# cython: language_level=3

cimport cython

from godot._hazmat.gdnative_api_struct cimport (
    godot_dictionary,
    godot_bool,
    godot_int,
)
from godot.array cimport Array


@cython.final
cdef class Dictionary:
    cdef godot_dictionary _gd_data

    @staticmethod
    cdef inline Dictionary new()

    @staticmethod
    cdef inline Dictionary from_ptr(const godot_dictionary *_ptr)

    # Operators

    cdef inline godot_bool operator_equal(self, Dictionary other)
    cdef inline godot_bool operator_contains(self, object key)
    cdef inline object operator_getitem(self, object key)
    cdef inline void operator_setitem(self, object key, object value)
    cdef inline void operator_delitem(self, object key)

    # Methods

    cpdef inline godot_int hash(self)
    cpdef inline godot_int size(self)
    cpdef inline Dictionary duplicate(self, godot_bool deep)
    cpdef inline object get(self, object key, object default=*)
    cpdef inline void clear(self)
    cpdef inline godot_bool empty(self)
    cpdef inline godot_bool has_all(self, Array keys)
    cpdef inline void erase(self, object item)
    cpdef inline list keys(self)
    cpdef inline list values(self)
    cpdef inline str to_json(self)
