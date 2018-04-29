from pythonscriptcffi import lib, ffi

from godot.hazmat.base import BaseBuiltinWithGDObjOwnership
from godot.hazmat.allocator import godot_array_alloc
from godot.hazmat.tools import variant_to_pyobj, pyobj_to_variant
from godot.pool_arrays import (
    PoolColorArray,
    PoolVector3Array,
    PoolVector2Array,
    PoolStringArray,
    PoolIntArray,
    PoolByteArray,
    PoolRealArray,
)


class Array(BaseBuiltinWithGDObjOwnership):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_ARRAY

    @staticmethod
    def _copy_gdobj(gdobj):
        cpy_gdobj = godot_array_alloc(initialized=False)
        lib.godot_array_new_copy(cpy_gdobj, gdobj)
        return cpy_gdobj

    def __init__(self, items=()):
        if not items:
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new(self._gd_ptr)
        elif isinstance(items, Array):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_copy(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolColorArray):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_color_array(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolVector3Array):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_vector3_array(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolVector2Array):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_vector2_array(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolStringArray):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_string_array(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolRealArray):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_real_array(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolIntArray):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_int_array(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, PoolByteArray):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new_pool_byte_array(self._gd_ptr, items._gd_ptr)
        elif hasattr(items, "__iter__") and not isinstance(items, (str, bytes)):
            self._gd_ptr = godot_array_alloc(initialized=False)
            lib.godot_array_new(self._gd_ptr)
            for x in items:
                self.append(x)
        else:
            raise TypeError("Param `items` should be of type `Array` or `Pool*Array`")

    def __eq__(self, other):
        # TODO: should be able to optimize this...
        if isinstance(other, Array):
            return list(self) == list(other)

        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<%s(%s)>" % (type(self).__name__, list(self))

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        for c in range(len(self)):
            yield self[c]

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return Array(list(self)[idx])

        size = len(self)
        idx = size + idx if idx < 0 else idx
        if abs(idx) >= size:
            raise IndexError("list index out of range")

        gdvar = lib.godot_array_get(self._gd_ptr, idx)
        ret = variant_to_pyobj(ffi.addressof(gdvar))
        lib.godot_variant_destroy(ffi.addressof(gdvar))
        return ret

    def __setitem__(self, idx, value):
        size = len(self)
        idx = size + idx if idx < 0 else idx
        if abs(idx) >= size:
            raise IndexError("list index out of range")

        var = pyobj_to_variant(value)
        lib.godot_array_set(self._gd_ptr, idx, var)

    def __delitem__(self, idx):
        size = len(self)
        idx = size + idx if idx < 0 else idx
        if abs(idx) >= size:
            raise IndexError("list index out of range")

        lib.godot_array_remove(self._gd_ptr, idx)

    def __len__(self):
        return lib.godot_array_size(self._gd_ptr)

    def __iadd__(self, items):
        if isinstance(items, (str, bytes)):
            return NotImplemented

        for x in items:
            self.append(x)
        return self

    def __add__(self, items):
        if isinstance(items, (str, bytes)):
            return NotImplemented

        arr = Array()
        for x in self:
            arr.append(x)
        for x in items:
            arr.append(x)
        return arr

    # Properties

    # Methods

    def append(self, value):
        var = pyobj_to_variant(value)
        lib.godot_array_append(self._gd_ptr, var)

    def clear(self):
        lib.godot_array_clear(self._gd_ptr)

    def count(self, value):
        var = pyobj_to_variant(value)
        return lib.godot_array_count(self._gd_ptr, var)

    def empty(self):
        return bool(lib.godot_array_empty(self._gd_ptr))

    def erase(self, value):
        var = pyobj_to_variant(value)
        lib.godot_array_erase(self._gd_ptr, var)

    def front(self):
        gdvar = lib.godot_array_front(self._gd_ptr)
        ret = variant_to_pyobj(ffi.addressof(gdvar))
        lib.godot_variant_destroy(ffi.addressof(gdvar))
        return ret

    def back(self):
        gdvar = lib.godot_array_back(self._gd_ptr)
        ret = variant_to_pyobj(ffi.addressof(gdvar))
        lib.godot_variant_destroy(ffi.addressof(gdvar))
        return ret

    def find(self, what, from_):
        var = pyobj_to_variant(what)
        return lib.godot_array_find(self._gd_ptr, var, from_)

    def find_last(self, what):
        var = pyobj_to_variant(what)
        return lib.godot_array_find_last(self._gd_ptr, var)

    def has(self, value):
        var = pyobj_to_variant(value)
        return bool(lib.godot_array_has(self._gd_ptr, var))

    def hash(self):
        return lib.godot_array_hash(self._gd_ptr)

    def insert(self, pos, value):
        var = pyobj_to_variant(value)
        lib.godot_array_insert(self._gd_ptr, pos, var)

    def invert(self):
        lib.godot_array_invert(self._gd_ptr)

    def pop_back(self):
        gdvar = lib.godot_array_pop_back(self._gd_ptr)
        ret = variant_to_pyobj(ffi.addressof(gdvar))
        lib.godot_variant_destroy(ffi.addressof(gdvar))
        return ret

    def pop_front(self):
        gdvar = lib.godot_array_pop_front(self._gd_ptr)
        ret = variant_to_pyobj(ffi.addressof(gdvar))
        lib.godot_variant_destroy(ffi.addressof(gdvar))
        return ret

    def push_back(self, value):
        var = pyobj_to_variant(value)
        lib.godot_array_push_back(self._gd_ptr, var)

    def push_front(self, value):
        var = pyobj_to_variant(value)
        lib.godot_array_push_front(self._gd_ptr, var)

    def resize(self, size):
        lib.godot_array_resize(self._gd_ptr, size)

    def rfind(self, what, from_):
        var = pyobj_to_variant(what)
        return lib.godot_array_rfind(self._gd_ptr, var, from_)

    def sort(self):
        lib.godot_array_sort(self._gd_ptr)


# TODO
# def sort_custom(self, obj, func):
#     self._check_param_type('obj', obj, BaseObject)
#     self._check_param_type('func', func, str)
#     raw_func = pyobj_to_gdobj(func)
#     # TODO how to check sort hasn't failed ?
#     lib.godot_array_sort_custom(self._gd_ptr, obj._gd_ptr, raw_func)
