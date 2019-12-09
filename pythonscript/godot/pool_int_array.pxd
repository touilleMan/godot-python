# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport (
    godot_pool_int_array, godot_int,
    godot_pool_int_array_write_access,
    godot_pool_int_array_read_access,
)
from godot.array cimport Array

from contextlib import contextmanager


@cython.final
cdef class PoolIntArray:
    cdef godot_pool_int_array _gd_data

    @staticmethod
    cdef inline PoolIntArray new()

    @staticmethod
    cdef inline PoolIntArray new_with_array(Array other)

    @staticmethod
    cdef inline PoolIntArray from_ptr(const godot_pool_int_array *_ptr)

    # Operators

    cdef inline bint operator_equal(self, PoolIntArray other)
    cdef inline PoolIntArray operator_getslice(self, object slice_)
    cdef inline godot_int operator_getitem(self, godot_int index)
    cdef inline void operator_setitem(self, godot_int index, godot_int value)
    cdef inline void operator_delitem(self, godot_int index)

    # Methods

    cpdef inline PoolIntArray copy(self)
    cpdef inline void append(self, godot_int data)
    cdef inline void append_array(self, PoolIntArray array)
    cdef inline void insert(self, godot_int idx, godot_int data)
    cpdef inline void invert(self)
    cpdef inline void push_back(self, godot_int data)
    cdef inline void remove(self, godot_int idx)
    cpdef inline void resize(self, godot_int size)
    cpdef inline godot_int get(self, godot_int idx)
    cpdef inline void set(self, godot_int idx, godot_int data)
    cpdef inline godot_int size(self)

    # Raw access

    cpdef inline PoolIntArrayWriteAccess write_access(self)
    cpdef inline PoolIntArrayReadAccess read_access(self)


@cython.final
cdef class PoolIntArrayWriteAccess:
    cdef godot_pool_int_array_write_access *_gd_ptr

    cdef godot_int *access_ptr(self)
    cdef PoolIntArrayWriteAccess copy(self)
    cdef void operator_assign(self, PoolIntArrayWriteAccess other)


@cython.final
cdef class PoolIntArrayReadAccess:
    cdef godot_pool_int_array_read_access *_gd_ptr

    cdef const godot_int *access_ptr(self)
    cdef PoolIntArrayReadAccess copy(self)
    cdef void operator_assign(self, PoolIntArrayReadAccess other)
