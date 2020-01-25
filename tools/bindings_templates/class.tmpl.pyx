{% from 'property.tmpl.pyx' import render_property %}
{% from 'method.tmpl.pyx' import render_method, render_method_bind_register %}

{# TODO: Handle signals #}
{% macro render_class(cls) %}

{% if not cls["base_class"] %}
from cpython.object cimport PyObject_GenericGetAttr, PyObject_GenericSetAttr
{% endif %}

{% if not cls["singleton"] %}
cdef godot_class_constructor __{{ cls["name"] }}_constructor = gdapi10.godot_get_class_constructor("{{ cls['name'] }}")
{% endif %}

{% for method in cls["methods"] %}
{{ render_method_bind_register(cls, method) }}
{% endfor %}

cdef class {{ cls["name"] }}({{ cls["base_class"] }}):
{% if not cls["base_class"] %}
    # free is virtual but this is not marked in api.json :'(
    def free(self):
        gdapi10.godot_object_destroy(self._gd_ptr)

    def __init__(self):
        raise RuntimeError(f"Use `new()` method to instantiate Godot object.")

    def __repr__(self):
        return f"<{type(self).__name__} wrapper on 0x{<size_t>self._gd_ptr:x}>"

    @staticmethod
    cdef inline Object cast_from_variant(const godot_variant *p_gdvar):
        cdef godot_object *ptr = gdapi10.godot_variant_as_object(p_gdvar)
        cdef object obj = Object.from_ptr(ptr)
        return globals()[str(obj.get_class())]._from_ptr(<size_t>ptr)

    @staticmethod
    cdef inline Object cast_from_ptr(godot_object *ptr):
        cdef object obj = Object.from_ptr(ptr)
        return globals()[str(obj.get_class())]._from_ptr(<size_t>ptr)

    def __eq__(self, other):
        try:
            return self._gd_ptr == (<{{ cls["name"] }}>other)._gd_ptr
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return self._gd_ptr != (<{{ cls["name"] }}>other)._gd_ptr
        except TypeError:
            return True

    def __getattr__(self, name):
        cdef GDString gdname = GDString(name)
        cdef GDString gdnamefield = GDString("name")

        # If a script is attached to the object, we expose here it methods
        if not hasattr(type(self), '__exposed_python_class'):
            if self.has_method(name):

                def _call(*args):
                    print(f'CALLING _CALL {name!r} on {self!r}')
                    return {{ cls["name"] }}.callv(self, gdname, Array(args))

                return _call
                # from functools import partial
                # return partial(self.call, gdname)

            elif any(x for x in self.get_property_list() if x[gdnamefield] == gdname):
                # TODO: Godot currently lacks a `has_property` method
                return self.get(gdname)

        raise AttributeError(
            f"`{type(self).__name__}` object has no attribute `{name}`"
        )

    def __setattr__(self, name, value):
        cdef GDString gdname = GDString(name)
        cdef GDString gdnamefield = GDString("name")

        if hasattr(type(self), '__exposed_python_class'):
            PyObject_GenericSetAttr(self, name, value)
            return

        # Could retrieve the item inside the Godot class, try to look into
        # the attached script if it has one
        else:
            if any(x for x in self.get_property_list() if x[gdnamefield] == gdname):
                # TODO: Godot currently lacks a `has_property` method
                self.set(name, value)
                return

        raise AttributeError(
            f"`{type(self).__name__}` object has no attribute `{name}`"
        )

    def call(self, name, *args):
        return self.callv(name, Array(args))

{% endif %}

{% if not cls["singleton"] and cls["instanciable"] %}
    @staticmethod
    def new():
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__({{ cls["name"] }})
        wrapper._gd_ptr = __{{ cls["name"] }}_constructor()
        if wrapper._gd_ptr is NULL:
            raise MemoryError
{% if cls["is_reference"] %}
        cdef godot_bool __is_reference_ret
        gdapi10.godot_method_bind_ptrcall(
            __methbind__Reference__reference,
            wrapper._gd_ptr,
            NULL,
            &__is_reference_ret
        )
{% endif %}
        return wrapper

{% if cls["is_reference"] %}
    def __del__(self):
        cdef godot_bool __ret
        gdapi10.godot_method_bind_ptrcall(
            __methbind__Reference__unreference,
            self._gd_ptr,
            NULL,
            &__ret
        )
        if __ret:
            gdapi10.godot_object_destroy(self._gd_ptr)
{% endif %}
{% endif %}

    @staticmethod
    cdef {{ cls["name"] }} from_ptr(godot_object *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__({{ cls["name"] }})
        wrapper._gd_ptr = _ptr
{% if cls["is_reference"] %}
        cdef godot_bool __is_reference_ret
        gdapi10.godot_method_bind_ptrcall(
            __methbind__Reference__reference,
            wrapper._gd_ptr,
            NULL,
            &__is_reference_ret
        )
{% endif %}
        return wrapper

    @staticmethod
    def _from_ptr(ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__({{ cls["name"] }})
        # /!\ doing `<godot_object*>ptr` would return the address of
        # the PyObject instead of casting it value !
        wrapper._gd_ptr = <godot_object *><size_t>ptr
{% if cls["is_reference"] %}
        cdef godot_bool __is_reference_ret
        gdapi10.godot_method_bind_ptrcall(
            __methbind__Reference__reference,
            wrapper._gd_ptr,
            NULL,
            &__is_reference_ret
        )
{% endif %}
        return wrapper

    # Constants
{% for key, value in cls["constants"].items() %}
    {{ key }} = {{ value }}
{% endfor %}

    # Methods
{# TODO: Use typing for params&return #}
{% for method in cls["methods"] %}
{% if method["name"] != "free" %}
    {{ render_method(cls, method) | indent }}
{% endif %}
{% endfor %}
    # Properties
{% for prop in cls["properties"] %}
    {{ render_property(prop) | indent }}
{% endfor %}

{% endmacro %}
