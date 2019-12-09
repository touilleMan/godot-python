# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_array, godot_int, godot_string, godot_variant
from godot._hazmat.conversion cimport godot_variant_to_pyobj, pyobj_to_godot_variant, godot_string_to_pyobj


@cython.final
cdef class Dictionary:

    def __init__(self, iterable=None):
        if not iterable:
            gdapi.godot_dictionary_new(&self._gd_data)
        elif isinstance(iterable, Dictionary):
            gdapi.godot_dictionary_new_copy(&self._gd_data, &(<Dictionary>iterable)._gd_data)
        # TODO: handle Pool*Array
        elif isinstance(iterable, dict):
            gdapi.godot_dictionary_new(&self._gd_data)
            for k, v in iterable.items():
                self[k] = v
        else:
            try:
                for k, v in iterable:
                    self[k] = v
            except ValueError:
                raise ValueError("dictionary update sequence element #0 has length 1; 2 is required")

    def __dealloc__(self):
        gdapi.godot_dictionary_destroy(&self._gd_data)

    @staticmethod
    cdef inline Dictionary new():
        # Call to __new__ bypasses __init__ constructor
        cdef Dictionary ret = Dictionary.__new__(Dictionary)
        gdapi.godot_dictionary_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Dictionary from_ptr(const godot_dictionary *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Dictionary ret = Dictionary.__new__(Dictionary)
        # `godot_dictionary` is a cheap structure pointing on a refcounted vector
        # of variants. Unlike it name could let think, `godot_dictionary_new_copy`
        # only increment the refcount of the underlying structure.
        gdapi.godot_dictionary_new_copy(&ret._gd_data, _ptr)
        return ret

    def __repr__(self):
        return f"<{type(self).__name__}({dict(self)})>"

    # Operators

    def __getitem__(self, key):
        return self.operator_getitem(key)

    def __setitem__(self, object key, object value):
        self.operator_setitem(key, value)

    # TODO: support slice
    def __delitem__(self, object key):
        self.operator_delitem(key)

    def __len__(self):
        return self.size()

    def __iter__(self):
        cdef godot_variant *p_value
        cdef godot_variant *p_key = NULL
        # TODO: mid iteration mutation should throw exception ?
        while True:
            p_value = gdapi.godot_dictionary_next(&self._gd_data, p_key)
            if p_value == NULL:
                return
            yield godot_variant_to_pyobj(p_value)

    def __copy__(self):
        return self.duplicate(False)

    def __deepcopy__(self):
        return self.duplicate(True)

    def __hash__(self):
        return self.hash()

    def __eq__(self, Dictionary other):
        return self.operator_equal(other)

    def __ne__(self, object other):
        return not self.operator_equal(other)

    def __contains__(self, object key):
        return self.operator_contains(key)

    # TODO: support __iadd__ for other types than Dictionary ?
    def __iadd__(self, Dictionary items):
        cdef godot_variant *p_value
        cdef godot_variant *p_key = NULL
        while True:
            p_value = gdapi.godot_dictionary_next(&items._gd_data, p_key)
            if p_value == NULL:
                break
            gdapi.godot_dictionary_set(&self._gd_data, p_key, p_value)
        return self

    # TODO: support __add__ for other types than Dictionary ?
    def __add__(Dictionary self, Dictionary items):
        cdef Dictionary dictionary = Dictionary.new()
        cdef godot_variant *p_value
        cdef godot_variant *p_key = NULL
        while True:
            p_value = gdapi.godot_dictionary_next(&items._gd_data, p_key)
            if p_value == NULL:
                break
            gdapi.godot_dictionary_set(&dictionary._gd_data, p_key, p_value)
        p_key = NULL
        while True:
            p_value = gdapi.godot_dictionary_next(&self._gd_data, p_key)
            if p_value == NULL:
                break
            gdapi.godot_dictionary_set(&dictionary._gd_data, p_key, p_value)
        return dictionary

    cdef inline godot_bool operator_equal(self, Dictionary other):
        return gdapi.godot_dictionary_operator_equal(
            &self._gd_data, &other._gd_data
        )

    cdef inline godot_bool operator_contains(self, object key):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef godot_bool ret = gdapi.godot_dictionary_has(&self._gd_data, &var_key)
        gdapi.godot_variant_destroy(&var_key)
        return ret

    cdef inline object operator_getitem(self, object key):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef godot_variant *p_var_ret = gdapi.godot_dictionary_operator_index(&self._gd_data, &var_key)
        gdapi.godot_variant_destroy(&var_key)
        if p_var_ret == NULL:
            raise KeyError(key)
        else:
            return godot_variant_to_pyobj(p_var_ret)

    cdef inline void operator_setitem(self, object key, object value):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi.godot_dictionary_set(&self._gd_data, &var_key, &var_value)
        gdapi.godot_variant_destroy(&var_key)
        gdapi.godot_variant_destroy(&var_value)

    cdef inline void operator_delitem(self, object key):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef godot_bool ret = gdapi11.godot_dictionary_erase_with_return(&self._gd_data, &var_key)
        if not ret:
            raise KeyError(key)
        gdapi.godot_variant_destroy(&var_key)

    # Methods

    cpdef inline godot_int hash(self):
        return gdapi.godot_dictionary_hash(&self._gd_data)

    cpdef inline godot_int size(self):
        return gdapi.godot_dictionary_size(&self._gd_data)

    cpdef inline Dictionary duplicate(self, godot_bool deep):
        cdef Dictionary ret = Dictionary.__new__(Dictionary)
        ret._gd_data = gdapi12.godot_dictionary_duplicate(&self._gd_data, deep)
        return ret

    cpdef inline object get(self, object key, object default=None):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef godot_variant var_default
        if default is not None:
            pyobj_to_godot_variant(default, &var_default)
        else:
            gdapi.godot_variant_new_nil(&var_default)
        cdef godot_variant var_ret = gdapi11.godot_dictionary_get_with_default(&self._gd_data, &var_key, &var_default)
        gdapi.godot_variant_destroy(&var_key)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline void clear(self):
        gdapi.godot_dictionary_clear(&self._gd_data)

    cpdef inline godot_bool empty(self):
        return gdapi.godot_dictionary_empty(&self._gd_data)

    cpdef inline godot_bool has_all(self, Array keys):
        return gdapi.godot_dictionary_has_all(&self._gd_data, &keys._gd_data)

    cpdef inline void erase(self, object item):
        cdef godot_variant var_item
        pyobj_to_godot_variant(item, &var_item)
        gdapi.godot_dictionary_erase(&self._gd_data, &var_item)
        gdapi.godot_variant_destroy(&var_item)

    # TODO: would be better to turn this into an iterator
    cpdef inline list keys(self):
        cdef godot_array gd_keys = gdapi.godot_dictionary_keys(&self._gd_data)
        cdef int i
        cdef list ret = [
            godot_variant_to_pyobj(gdapi.godot_array_operator_index(&gd_keys, i))
            for i in range(gdapi.godot_array_size(&gd_keys))
        ]
        gdapi.godot_array_destroy(&gd_keys)
        return ret

    # TODO: would be better to turn this into an iterator
    cpdef inline list values(self):
        cdef godot_array gd_values = gdapi.godot_dictionary_values(&self._gd_data)
        cdef int i
        cdef list ret = [
            godot_variant_to_pyobj(gdapi.godot_array_operator_index(&gd_values, i))
            for i in range(gdapi.godot_array_size(&gd_values))
        ]
        gdapi.godot_array_destroy(&gd_values)
        return ret

    cpdef inline str to_json(self):
        cdef godot_string var_ret = gdapi.godot_dictionary_to_json(&self._gd_data)
        cdef object ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret
