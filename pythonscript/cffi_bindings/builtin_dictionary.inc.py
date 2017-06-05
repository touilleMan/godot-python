class Dictionary(BaseBuiltinWithGDObjOwnership):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_DICTIONARY

    def __init__(self, items=None):
        try:
            self._gd_ptr = ffi.new('godot_dictionary*')
            if not items:
                lib.godot_dictionary_new(self._gd_ptr)
            elif isinstance(items, Dictionary):
                self._gd_ptr[0] = lib.godot_dictionary_copy(items._gd_ptr)
                # copy
            elif isinstance(items, dict):
                lib.godot_dictionary_new(self._gd_ptr)
                for k, v in items.items():
                    self[k] = v
            else:
                raise TypeError('Param `items` should be of type `dict` or `Dictionary`')
        except:
            # Unset _gd_ptr anyway to avoid segfault in __del__
            self._gd_ptr = None
            raise

    def __del__(self):
        if self._gd_ptr:
            lib.godot_dictionary_destroy(self._gd_ptr)

    @staticmethod
    def _copy_gdobj(gdobj):
        return ffi.new('godot_dictionary*', lib.godot_dictionary_copy(gdobj))

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
        lib.godot_dictionary_erase(self._gd_ptr, var);

    # Properties

    # Methods

    def keys(self):
        gdarr = lib.godot_dictionary_keys(self._gd_ptr)
        return iter(godot_array_to_pyobj(ffi.addressof(gdarr)))

    def values(self):
        gdarr = lib.godot_dictionary_values(self._gd_ptr)
        return iter(godot_array_to_pyobj(ffi.addressof(gdarr)))

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
        raw = lib.godot_dictionary_to_json(self._gd_ptr);
        return godot_string_to_pyobj(ffi.addressof(raw))
