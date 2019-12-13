# cython: language_level=3

cimport cython
from libc.stdint cimport uintptr_t

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport (
    GODOT_OK,
    godot_error,
    godot_pool_int_array,
    godot_int,
    godot_pool_int_array_write_access,
    godot_pool_int_array_read_access,
)
from godot.array cimport Array

from contextlib import contextmanager


@cython.final
cdef class PoolIntArray:

    def __init__(self, other=None):
        cdef PoolIntArray other_as_pool_int_array
        cdef Array other_as_array
        cdef godot_int item
        cdef int i
        if other is None:
            gdapi.godot_pool_int_array_new(&self._gd_data)
        else:
            try:
                other_as_pool_int_array = <PoolIntArray?>other
                gdapi.godot_pool_int_array_new_copy(&self._gd_data, &other_as_pool_int_array._gd_data)
            except TypeError:
                try:
                    other_as_array = <Array?>other
                    gdapi.godot_pool_int_array_new_with_array(&self._gd_data, &other_as_array._gd_data)
                except TypeError:
                    gdapi.godot_pool_int_array_new(&self._gd_data)
                    PoolIntArray.resize(self, len(other))
                    with PoolIntArray.raw_access(self) as ptr:
                        for i, item in enumerate(other):
                            ptr[i] = item

    def __dealloc__(self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi.godot_pool_int_array_destroy(&self._gd_data)

    @staticmethod
    cdef inline PoolIntArray new():
        # Call to __new__ bypasses __init__ constructor
        cdef PoolIntArray ret = PoolIntArray.__new__(PoolIntArray)
        gdapi.godot_pool_int_array_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline PoolIntArray new_with_array(Array other):
        # Call to __new__ bypasses __init__ constructor
        cdef PoolIntArray ret = PoolIntArray.__new__(PoolIntArray)
        gdapi.godot_pool_int_array_new_with_array(&ret._gd_data, &other._gd_data)
        return ret

    @staticmethod
    cdef inline PoolIntArray from_ptr(const godot_pool_int_array *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef PoolIntArray ret = PoolIntArray.__new__(PoolIntArray)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<{type(self).__name__}([{', '.join(repr(x) for x in self)}])>"

    # Operators

    def __getitem__(self, index):
        cdef godot_int size = self.size()
        cdef godot_int start
        cdef godot_int stop
        cdef godot_int step
        if isinstance(index, slice):
            step = index.step if index.step is not None else 1
            if step == 0:
                raise ValueError("range() arg 3 must not be zero")
            elif step > 0:
                start = index.start if index.start is not None else 0
                stop = index.stop if index.stop is not None else size
            else:
                start = index.start if index.start is not None else size
                stop = index.stop if index.stop is not None else -size - 1
            return self.operator_getslice(
                start,
                stop,
                step,
            )
        else:
            size = self.size()
            if index < 0:
                index = index + size
            if index < 0 or index >= size:
                raise IndexError("list index out of range")
            return gdapi.godot_pool_int_array_get(&self._gd_data, index)

    cdef inline PoolIntArray operator_getslice(self, godot_int start, godot_int stop, godot_int step):
        cdef PoolIntArray ret = PoolIntArray.new()
        cdef godot_int size = self.size()

        if start > size - 1:
            start = size - 1
        elif start < 0:
            start += size
            if start < 0:
                start = 0

        if stop > size:
            stop = size
        elif stop < -size:
            stop = -1
        elif stop < 0:
            stop += size

        if step > 0:
            if start >= stop:
                return ret
            items = 1 + (stop - start - 1) // step
            if items <= 0:
                return ret
        else:
            if start <= stop:
                return ret
            items = 1 + (stop - start + 1) // step
            if items <= 0:
                return ret

        ret.resize(items)
        cdef godot_pool_int_array_read_access *src_access = gdapi.godot_pool_int_array_read(
            &self._gd_data
        )
        cdef godot_pool_int_array_write_access *dst_access = gdapi.godot_pool_int_array_write(
            &ret._gd_data
        )
        cdef const godot_int *src_ptr = gdapi.godot_pool_int_array_read_access_ptr(src_access)
        cdef godot_int *dst_ptr = gdapi.godot_pool_int_array_write_access_ptr(dst_access)
        cdef godot_int i
        for i in range(items):
            dst_ptr[i] = src_ptr[i * step + start]
        gdapi.godot_pool_int_array_read_access_destroy(src_access)
        gdapi.godot_pool_int_array_write_access_destroy(dst_access)

        return ret

    # TODO: support slice
    def __setitem__(self, index, value):
        cdef godot_int size
        if isinstance(index, slice):
            raise NotImplemented
        else:
            size = self.size()
            if index < 0:
                index += size
            if index < 0 or index >= size:
                raise IndexError("list index out of range")
            gdapi.godot_pool_int_array_set(&self._gd_data, index, value)

    # TODO: support slice
    def __delitem__(self, index):
        cdef godot_int size
        if isinstance(index, slice):
            raise NotImplemented
        else:
            size = self.size()
            if index < 0:
                index += size
            if index < 0 or index >= size:
                raise IndexError("list index out of range")
            gdapi.godot_pool_int_array_remove(&self._gd_data, index)

    def __len__(self):
        return self.size()

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        cdef int i
        for i in range(self.size()):
            yield gdapi.godot_pool_int_array_get(&self._gd_data, i)

    def __copy__(self):
        return self.copy()

    def __eq__(self, other):
        try:
            return PoolIntArray.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not PoolIntArray.operator_equal(self, other)
        except TypeError:
            return True

    def __iadd__(self, PoolIntArray items not None):
        self.append_array(items)
        return self

    def __add__(self, PoolIntArray items not None):
        cdef PoolIntArray ret = PoolIntArray.copy(self)
        ret.append_array(items)
        return ret

    cdef inline bint operator_equal(self, PoolIntArray other):
        # TODO `godot_array_operator_equal` is missing in gdapi, submit a PR ?
        cdef godot_int size = self.size()
        if size != other.size():
            return False
        cdef int i
        for i in range(size):
            if (
                gdapi.godot_pool_int_array_get(&self._gd_data, i) !=
                gdapi.godot_pool_int_array_get(&other._gd_data, i)
            ):
                return False
        return True

    # Methods

    cpdef inline PoolIntArray copy(self):
        # Call to __new__ bypasses __init__ constructor
        cdef PoolIntArray ret = PoolIntArray.__new__(PoolIntArray)
        gdapi.godot_pool_int_array_new_copy(&ret._gd_data, &self._gd_data)
        return ret

    cpdef inline void append(self, godot_int data):
        gdapi.godot_pool_int_array_append(&self._gd_data, data)

    cdef inline void append_array(self, PoolIntArray array):
        gdapi.godot_pool_int_array_append_array(&self._gd_data, &array._gd_data)

    cpdef inline void invert(self):
        gdapi.godot_pool_int_array_invert(&self._gd_data)

    cpdef inline void push_back(self, godot_int data):
        gdapi.godot_pool_int_array_push_back(&self._gd_data, data)

    cpdef inline void resize(self, godot_int size):
        gdapi.godot_pool_int_array_resize(&self._gd_data, size)

    cdef inline godot_int size(self):
        return gdapi.godot_pool_int_array_size(&self._gd_data)

    # Raw access

    @contextmanager
    def raw_access(self):
        cdef godot_pool_int_array_write_access *access = gdapi.godot_pool_int_array_write(
            &self._gd_data
        )
        cdef PoolIntArrayWriteAccess pyaccess = PoolIntArrayWriteAccess.__new__(PoolIntArrayWriteAccess)
        pyaccess._gd_ptr = gdapi.godot_pool_int_array_write_access_ptr(access)
        try:
            yield pyaccess

        finally:
            gdapi.godot_pool_int_array_write_access_destroy(access)


@cython.final
cdef class PoolIntArrayWriteAccess:

    def get_address(self):
        return <uintptr_t>self._gd_ptr

    def __getitem__(self, int idx):
        return self._gd_ptr[idx]

    def __setitem__(self, int idx, godot_int val):
        self._gd_ptr[idx] = val
