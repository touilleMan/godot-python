# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport (
    godot_pool_string_array,
    godot_int,
    godot_string,
    godot_pool_string_array_write_access,
    godot_pool_string_array_read_access,
)
from godot.array cimport Array

from contextlib import contextmanager


@cython.final
cdef class PoolStringArray:
    cdef godot_pool_string_array _gd_data

    @staticmethod
    cdef inline PoolStringArray new()

    @staticmethod
    cdef inline PoolStringArray new_with_array(Array other)

    @staticmethod
    cdef inline PoolStringArray from_ptr(const godot_pool_string_array *_ptr)

    # Operators

    cdef inline bint operator_equal(self, PoolStringArray other)
    cdef inline PoolStringArray operator_getslice(self, object slice_)
    cdef inline godot_int operator_getitem(self, godot_int index)
    cdef inline void operator_setitem(self, godot_int index, str value)
    cdef inline void operator_delitem(self, godot_int index)

    # Methods

    cpdef inline PoolStringArray copy(self)
    cpdef inline void append(self, str data)
    cdef inline void append_array(self, PoolStringArray array)
    cdef inline void insert(self, godot_int idx, str data)
    cpdef inline void invert(self)
    cpdef inline void push_back(self, str data)
    cdef inline void remove(self, godot_int idx)
    cpdef inline void resize(self, godot_int size)
    cpdef inline str get(self, godot_int idx)
    cpdef inline void set(self, godot_int idx, str data)
    cpdef inline godot_int size(self)

    # Raw access

    cpdef inline PoolStringArrayWriteAccess write_access(self)
    cpdef inline PoolStringArrayReadAccess read_access(self)


@cython.final
cdef class PoolStringArrayWriteAccess:
    cdef godot_pool_string_array_write_access *_gd_ptr

    cdef godot_string *access_ptr(self)
    cdef PoolStringArrayWriteAccess copy(self)
    cdef void operator_assign(self, PoolStringArrayWriteAccess other)


@cython.final
cdef class PoolStringArrayReadAccess:
    cdef godot_pool_string_array_read_access *_gd_ptr

    cdef const godot_string *access_ptr(self)
    cdef PoolStringArrayReadAccess copy(self)
    cdef void operator_assign(self, PoolStringArrayReadAccess other)
