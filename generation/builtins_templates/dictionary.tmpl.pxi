{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}

{# We can't do const in Python #}
{{ force_mark_rendered("godot_dictionary_operator_index_const") }}

@cython.final
cdef class Dictionary:
{% block cdef_attributes %}
    cdef godot_dictionary _gd_data

    @staticmethod
    cdef inline Dictionary new()

    @staticmethod
    cdef inline Dictionary from_ptr(const godot_dictionary *_ptr)

    cdef inline operator_update(self, Dictionary items)
    cdef inline bint operator_equal(self, Dictionary other)
{% endblock %}

{% block python_defs %}
    def __init__(self, iterable=None):
        {{ force_mark_rendered("godot_dictionary_new") }}
        if not iterable:
            gdapi10.godot_dictionary_new(&self._gd_data)
        elif isinstance(iterable, Dictionary):
            self._gd_data = gdapi12.godot_dictionary_duplicate(&(<Dictionary>iterable)._gd_data, False)
        # TODO: handle Pool*Array
        elif isinstance(iterable, dict):
            gdapi10.godot_dictionary_new(&self._gd_data)
            for k, v in iterable.items():
                self[k] = v
        else:
            gdapi10.godot_dictionary_new(&self._gd_data)
            try:
                for k, v in iterable:
                    self[k] = v
            except ValueError as exc:
                raise ValueError("dictionary update sequence element has length 1; 2 is required")

    def __dealloc__(self):
        {{ force_mark_rendered("godot_dictionary_destroy") }}
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.godot_dictionary_destroy(&self._gd_data)

    @staticmethod
    cdef inline Dictionary new():
        # Call to __new__ bypasses __init__ constructor
        cdef Dictionary ret = Dictionary.__new__(Dictionary)
        gdapi10.godot_dictionary_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Dictionary from_ptr(const godot_dictionary *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Dictionary ret = Dictionary.__new__(Dictionary)
        # `godot_dictionary` is a cheap structure pointing on a refcounted hashmap
        # of variants. Unlike it name could let think, `godot_dictionary_new_copy`
        # only increment the refcount of the underlying structure.
        {{ force_mark_rendered("godot_dictionary_new_copy") }}
        gdapi10.godot_dictionary_new_copy(&ret._gd_data, _ptr)
        return ret

    def __repr__(self):
        repr_dict = {}
        for k, v in self.items():
            if isinstance(k, GDString):
                k = str(k)
            if isinstance(v, GDString):
                v = str(v)
            repr_dict[k] = v
        return f"<Dictionary({repr_dict})>"

    def __getitem__(self, object key):
        {{ force_mark_rendered("godot_dictionary_operator_index") }}
        cdef godot_variant var_key
        if not pyobj_to_godot_variant(key, &var_key):
            raise TypeError(f"Cannot convert `{key!r}` to Godot Variant")
        cdef godot_variant *p_var_ret = gdapi10.godot_dictionary_operator_index(&self._gd_data, &var_key)
        gdapi10.godot_variant_destroy(&var_key)
        if p_var_ret == NULL:
            raise KeyError(key)
        else:
            return godot_variant_to_pyobj(p_var_ret)

    {{ render_method("set", py_name="__setitem__") | indent }}

    def __delitem__(self, object key):
        {{ force_mark_rendered("godot_dictionary_erase_with_return") }}
        cdef godot_variant var_key
        if not pyobj_to_godot_variant(key, &var_key):
            raise TypeError(f"Cannot convert `{key!r}` to Godot Variant")
        cdef godot_bool ret = gdapi11.godot_dictionary_erase_with_return(&self._gd_data, &var_key)
        gdapi10.godot_variant_destroy(&var_key)
        if not ret:
            raise KeyError(key)

    def __iter__(self):
        {{ force_mark_rendered("godot_dictionary_next") }}
        cdef godot_variant *p_key = NULL
        # TODO: mid iteration mutation should throw exception ?
        while True:
            p_key = gdapi10.godot_dictionary_next(&self._gd_data, p_key)
            if p_key == NULL:
                return
            yield godot_variant_to_pyobj(p_key)

    def __copy__(self):
        return self.duplicate(False)

    def __deepcopy__(self):
        return self.duplicate(True)

    def get(self, object key, object default=None):
        {{ force_mark_rendered("godot_dictionary_get") }}
        {{ force_mark_rendered("godot_dictionary_get_with_default") }}
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef godot_variant var_ret
        cdef godot_variant var_default
        if default is not None:
            pyobj_to_godot_variant(default, &var_default)
            var_ret = gdapi11.godot_dictionary_get_with_default(&self._gd_data, &var_key, &var_default)
            gdapi10.godot_variant_destroy(&var_default)
        else:
            var_ret = gdapi10.godot_dictionary_get(&self._gd_data, &var_key)
        gdapi10.godot_variant_destroy(&var_key)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cdef inline operator_update(self, Dictionary items):
        cdef godot_variant *p_value
        cdef godot_variant *p_key = NULL
        while True:
            p_key = gdapi10.godot_dictionary_next(&items._gd_data, p_key)
            if p_key == NULL:
                break
            p_value = gdapi10.godot_dictionary_operator_index(&items._gd_data, p_key)
            gdapi10.godot_dictionary_set(&self._gd_data, p_key, p_value)
        return self

    def update(self, other):
        cdef object k
        cdef object v
        if isinstance(other, Dictionary):
            Dictionary.operator_update(self, other)
        elif isinstance(other, dict):
            for k, v in other.items():
                self[k] = v
        else:
            raise TypeError("other must be godot.Dictionary or dict")

    def items(self):
        cdef godot_variant *p_key = NULL
        cdef godot_variant *p_value
        # TODO: mid iteration mutation should throw exception ?
        while True:
            p_key = gdapi10.godot_dictionary_next(&self._gd_data, p_key)
            if p_key == NULL:
                return
            p_value = gdapi10.godot_dictionary_operator_index(&self._gd_data, p_key)
            yield godot_variant_to_pyobj(p_key), godot_variant_to_pyobj(p_value)

    cdef inline bint operator_equal(self, Dictionary other):
        if other is None:
            return False
        cdef godot_int size = self.size()
        if size != other.size():
            return False
        # TODO: gdnative should provide a function to do that
        return dict(self) == dict(other)

    def __eq__(self, other):
        {# see https://github.com/godotengine/godot/issues/27615 #}
        {{ force_mark_rendered("godot_dictionary_operator_equal") }}
        try:
            return Dictionary.operator_equal(self, <Dictionary?>other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Dictionary.operator_equal(self, <Dictionary?>other)
        except TypeError:
            return True

    {{ render_method("size", py_name="__len__") | indent }}
    {{ render_method("hash", py_name="__hash__") | indent }}
    {{ render_method("has", py_name="__contains__") | indent }}

    {{ render_method("duplicate") | indent }}
    {{ render_method("size") | indent }}
    {{ render_method("empty") | indent }}
    {{ render_method("clear") | indent }}
    {{ render_method("has") | indent }}
    {{ render_method("has_all") | indent }}
    {{ render_method("erase") | indent }}
    {{ render_method("hash") | indent }}
    {{ render_method("keys") | indent }}
    {{ render_method("values") | indent }}
    {{ render_method("to_json") | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock %}
