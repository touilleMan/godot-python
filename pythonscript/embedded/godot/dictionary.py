from pythonscriptcffi import lib, ffi

from .hazmat.base import BaseBuiltinWithGDObjOwnership
from .hazmat.allocator import godot_dictionary_alloc
from .hazmat.tools import pyobj_to_variant, variant_to_pyobj, godot_string_to_pyobj
from .array import Array


class Dictionary(BaseBuiltinWithGDObjOwnership):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_DICTIONARY

    @staticmethod
    def _copy_gdobj(gdobj):
        cpy_gdobj = godot_dictionary_alloc()
        lib.godot_dictionary_new_copy(cpy_gdobj, gdobj)
        return cpy_gdobj

    def __init__(self, items=None, **kwargs):
        if not items:
            self._gd_ptr = godot_dictionary_alloc()
            lib.godot_dictionary_new(self._gd_ptr)
        elif isinstance(items, Dictionary):
            self._gd_ptr = godot_dictionary_alloc()
            lib.godot_dictionary_new_copy(self._gd_ptr, items._gd_ptr)
        elif isinstance(items, dict):
            self._gd_ptr = godot_dictionary_alloc()
            lib.godot_dictionary_new(self._gd_ptr)
            for k, v in items.items():
                self[k] = v
        else:
            raise TypeError('Param `items` should be of type `dict` or `Dictionary`')
        for k, v in kwargs.items():
            self[k] = v

    def __repr__(self):
        return "<%s(%s)>" % (type(self).__name__, dict(self))

    def __eq__(self, other):
        # TODO? lib.godot_dictionary_operator_equal compares only the underlying
        # dict pool address instead of comparing each stored data.
        return isinstance(other, Dictionary) and lib.godot_dictionary_operator_equal(self._gd_ptr, other._gd_ptr)

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return lib.godot_dictionary_size(self._gd_ptr)

    def __contains__(self, value):
        pvar = pyobj_to_variant(value)
        return bool(lib.godot_dictionary_has(self._gd_ptr, pvar))

    def __iter__(self):
        return self.keys()

    def __getitem__(self, key):
        var = pyobj_to_variant(key)
        retvar = lib.godot_dictionary_get(self._gd_ptr, var)
        return variant_to_pyobj(ffi.addressof(retvar))

    def __setitem__(self, key, value):
        varkey = pyobj_to_variant(key)
        varvalue = pyobj_to_variant(value)
        lib.godot_dictionary_set(self._gd_ptr, varkey, varvalue)

    def __delitem__(self, key):
        var = pyobj_to_variant(key)
        lib.godot_dictionary_erase(self._gd_ptr, var)

    # Properties

    # Methods

    def copy(self):
        gd_ptr = godot_dictionary_alloc()
        lib.godot_dictionary_new_copy(gd_ptr, self._gd_ptr)
        return Dictionary.build_from_gdobj(gd_ptr, steal=True)

    def pop(self, *args):
        key, *default = args
        try:
            value = self[key]
        except KeyError:
            if default:
                return default[0]
            else:
                raise
        del self[key]
        return value

    def keys(self):
        gdarr = lib.godot_dictionary_keys(self._gd_ptr)
        return iter(Array.build_from_gdobj(gdarr))

    def values(self):
        gdarr = lib.godot_dictionary_values(self._gd_ptr)
        return iter(Array.build_from_gdobj(gdarr))

    def items(self):
        return ((k, self[k]) for k in self.keys())

    def empty(self):
        return bool(lib.godot_dictionary_empty(self._gd_ptr))

    def clear(self):
        lib.godot_dictionary_clear(self._gd_ptr)

    def has_all(self, keys):
        self._check_param_type('keys', keys, Array)
        return bool(lib.godot_dictionary_has_all(self._gd_ptr, keys._gd_ptr))

    def hash(self):
        return lib.godot_dictionary_hash(self._gd_ptr)

    def to_json(self):
        raw = lib.godot_dictionary_to_json(self._gd_ptr)
        return godot_string_to_pyobj(ffi.addressof(raw))
