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
    godot_pool_string_array,
    godot_string,
    godot_int,
    godot_pool_string_array_write_access,
    godot_pool_string_array_read_access,
)
from godot._hazmat.conversion cimport pyobj_to_godot_string, godot_string_to_pyobj
from godot.array cimport Array

from contextlib import contextmanager


@cython.final
cdef class PoolStringArray:

    def __init__(self, other=None):
        cdef PoolStringArray other_as_pool_string_array
        cdef Array other_as_array
        if not other:
            gdapi.godot_pool_string_array_new(&self._gd_data)
        try:
            other_as_pool_string_array = <PoolStringArray?>other
            gdapi.godot_pool_string_array_new_copy(&self._gd_data, &other_as_pool_string_array._gd_data)
        except TypeError:
            pass
        try:
            other_as_array = <Array?>other
            gdapi.godot_pool_string_array_new_with_array(&self._gd_data, &other_as_array._gd_data)
        except TypeError:
            pass
        raise ValueError("`other` must be `Array` or `PoolStringArray`")

    def __dealloc__(self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi.godot_pool_string_array_destroy(&self._gd_data)

    @staticmethod
    cdef inline PoolStringArray new():
        # Call to __new__ bypasses __init__ constructor
        cdef PoolStringArray ret = PoolStringArray.__new__(PoolStringArray)
        gdapi.godot_pool_string_array_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline PoolStringArray new_with_array(Array other):
        # Call to __new__ bypasses __init__ constructor
        cdef PoolStringArray ret = PoolStringArray.__new__(PoolStringArray)
        gdapi.godot_pool_string_array_new_with_array(&ret._gd_data, &other._gd_data)
        return ret

    @staticmethod
    cdef inline PoolStringArray from_ptr(const godot_pool_string_array *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef PoolStringArray ret = PoolStringArray.__new__(PoolStringArray)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<{type(self).__name__}([{', '.join(repr(x) for x in self)}])>"

    # Operators

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.operator_getslice(index)
        else:
            return self.operator_getitem(index)

    # TODO: support slice
    def __setitem__(self, godot_int index, object value):
        self.operator_setitem(index, value)

    # TODO: support slice
    def __delitem__(self, godot_int index):
        self.operator_delitem(index)

    def __len__(self):
        return self.size()

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        cdef int i
        for i in range(self.size()):
            yield self.get(i)

    def __copy__(self):
        return self.copy()

    def __eq__(self, PoolStringArray other):
        return self.operator_equal(other)

    def __ne__(self, other):
        return not self.operator_equal(other)

    def __iadd__(self, PoolStringArray items):
        self.append_array(items)
        return self

    def __add__(self, PoolStringArray items):
        cdef PoolStringArray ret = PoolStringArray.new_copy(self)
        ret.append_array(items)
        return ret

    cdef inline bint operator_equal(self, PoolStringArray other):
        # TODO: `godot_array_operator_equal` is missing in gdapi, submit a PR ?
        cdef godot_int size = self.size()
        if size != other.size():
            return False
        # TODO: optimize by using read access
        cdef int i
        for i in range(size):
            if self.get(i) != other.get(i):
                return False
        return True

    cdef inline PoolStringArray operator_getslice(self, object slice_):
        cdef PoolStringArray ret = PoolStringArray.new()
        # TODO: optimize with `godot_array_resize` ?
        cdef int i
        for i in range(slice_.start, slice_.end, slice_.step or 1):
            ret.append(self.operator_getitem(i))
        return ret

    cdef inline godot_int operator_getitem(self, godot_int index):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        return self.get(index)

    cdef inline void operator_setitem(self, godot_int index, str value):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        self.set(index, value)

    cdef inline void operator_delitem(self, godot_int index):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        self.remove(index)

    # Methods

    cpdef inline PoolStringArray copy(self):
        # Call to __new__ bypasses __init__ constructor
        cdef PoolStringArray ret = PoolStringArray.__new__(PoolStringArray)
        gdapi.godot_pool_string_array_new_copy(&ret._gd_data, &self._gd_data)
        return ret

    cpdef inline void append(self, str data):
        cdef godot_string gdstr
        pyobj_to_godot_string(data, &gdstr)
        gdapi.godot_pool_string_array_append(&self._gd_data, &gdstr)
        gdapi.godot_string_destroy(&gdstr)

    cdef inline void append_array(self, PoolStringArray array):
        gdapi.godot_pool_string_array_append_array(&self._gd_data, &array._gd_data)

    cdef inline void insert(self, godot_int idx, str data):
        cdef godot_string gdstr
        pyobj_to_godot_string(data, &gdstr)
        cdef godot_error ret = gdapi.godot_pool_string_array_insert(&self._gd_data, idx, &gdstr)
        gdapi.godot_string_destroy(&gdstr)
        # TODO...
        if ret != GODOT_OK:
            raise IndexError(f"Got error {ret}")

    cpdef inline void invert(self):
        gdapi.godot_pool_string_array_invert(&self._gd_data)

    cpdef inline void push_back(self, str data):
        cdef godot_string gdstr
        pyobj_to_godot_string(data, &gdstr)
        gdapi.godot_pool_string_array_push_back(&self._gd_data, &gdstr)
        gdapi.godot_string_destroy(&gdstr)

    cdef inline void remove(self, godot_int idx):
        gdapi.godot_pool_string_array_remove(&self._gd_data, idx)

    cpdef inline void resize(self, godot_int size):
        gdapi.godot_pool_string_array_resize(&self._gd_data, size)

    cpdef inline str get(self, godot_int idx):
        cdef godot_string gdstr = gdapi.godot_pool_string_array_get(&self._gd_data, idx)
        cdef object ret = godot_string_to_pyobj(&gdstr)
        gdapi.godot_string_destroy(&gdstr)
        return ret

    cpdef inline void set(self, godot_int idx, str data):
        cdef godot_string gdstr
        pyobj_to_godot_string(data, &gdstr)
        gdapi.godot_pool_string_array_set(&self._gd_data, idx, &gdstr)
        gdapi.godot_string_destroy(&gdstr)

    cpdef inline godot_int size(self):
        return gdapi.godot_pool_string_array_size(&self._gd_data)

    # Raw access

    cpdef inline PoolStringArrayWriteAccess write_access(self):
        return PoolStringArrayWriteAccess(self)

    cpdef inline PoolStringArrayReadAccess read_access(self):
        return PoolStringArrayReadAccess(self)

    @contextmanager
    def raw_access(self):
        cdef godot_pool_string_array_write_access *access = gdapi.godot_pool_string_array_write(
            &self._gd_data
        )
        try:
            yield <uintptr_t>gdapi.godot_pool_string_array_write_access_ptr(access)

        finally:
            gdapi.godot_pool_string_array_write_access_destroy(access)


@cython.final
cdef class PoolStringArrayWriteAccess:

    def __cinit__(self, PoolStringArray array):
        self._gd_ptr = gdapi.godot_pool_string_array_write(&array._gd_data)

    def __dealloc__(self):
        gdapi.godot_pool_string_array_write_access_destroy(self._gd_ptr)

    cdef godot_string *access_ptr(self):
        return gdapi.godot_pool_string_array_write_access_ptr(self._gd_ptr)

    cdef PoolStringArrayWriteAccess copy(self):
        cdef PoolStringArrayWriteAccess ret = PoolStringArrayWriteAccess.__new__(PoolStringArrayWriteAccess)
        ret._gd_ptr = gdapi.godot_pool_string_array_write_access_copy(self._gd_ptr)
        return ret

    cdef void operator_assign(self, PoolStringArrayWriteAccess other):
        gdapi.godot_pool_string_array_write_access_operator_assign(self._gd_ptr, other._gd_ptr)


@cython.final
cdef class PoolStringArrayReadAccess:

    def __cinit__(self, PoolStringArray array):
        self._gd_ptr = gdapi.godot_pool_string_array_read(&array._gd_data)

    def __dealloc__(self):
        gdapi.godot_pool_string_array_read_access_destroy(self._gd_ptr)

    cdef const godot_string *access_ptr(self):
        return gdapi.godot_pool_string_array_read_access_ptr(self._gd_ptr)

    cdef PoolStringArrayReadAccess copy(self):
        cdef PoolStringArrayReadAccess ret = PoolStringArrayReadAccess.__new__(PoolStringArrayReadAccess)
        ret._gd_ptr = gdapi.godot_pool_string_array_read_access_copy(self._gd_ptr)
        return ret

    cdef void operator_assign(self, PoolStringArrayReadAccess other):
        gdapi.godot_pool_string_array_read_access_operator_assign(self._gd_ptr, other._gd_ptr)
