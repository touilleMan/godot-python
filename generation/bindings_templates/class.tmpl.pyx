{% from 'method.tmpl.pyx' import render_method, get_method_bind_register_name %}


{% macro render_class_gdapi_ptrs_init(cls) %}

{% if not cls.singleton %}
global __{{ cls.name }}_constructor
__{{ cls.name }}_constructor = gdapi10.godot_get_class_constructor("{{ cls.name }}")
{% endif %}

{% for method in cls.methods %}
global {{ get_method_bind_register_name(cls, method) }}
{{ get_method_bind_register_name(cls, method) }} = gdapi10.godot_method_bind_get_method("{{ cls.bind_register_name }}", "{{ method.name }}")
{% endfor %}

{% endmacro %}


{# TODO: Handle signals #}
{% macro render_class(cls) %}

{% if not cls.base_class %}
from cpython.object cimport PyObject_GenericGetAttr, PyObject_GenericSetAttr
{% endif %}

{% if not cls.singleton %}
cdef godot_class_constructor __{{ cls.name }}_constructor = NULL
{% endif %}

{% for method in cls.methods %}
cdef godot_method_bind *{{ get_method_bind_register_name(cls, method) }} = NULL
{% endfor %}

cdef class {{ cls.name }}({{ cls.base_class }}):
{% if not cls.base_class %}
    # free is virtual but this is not marked in api.json :'(
    def free(self):
        with nogil:
            gdapi10.godot_object_destroy(self._gd_ptr)

    def __init__(self):
        raise RuntimeError(
            f"Use `new()` method to instantiate non-refcounted Godot object (and don't forget to free it !)"
        )

    def __repr__(self):
        return f"<{type(self).__name__} wrapper on 0x{<size_t>self._gd_ptr:x}>"

    @staticmethod
    cdef inline Object cast_from_variant(const godot_variant *p_gdvar):
        cdef godot_object *ptr = gdapi10.godot_variant_as_object(p_gdvar)
        # Retreive class
        cdef GDString classname = GDString.__new__(GDString)
        with nogil:
            gdapi10.godot_method_bind_ptrcall(
                __methbind__Object__get_class,
                ptr,
                NULL,
                &classname._gd_data
            )
        return globals()[str(classname)]._from_ptr(<size_t>ptr)

    @staticmethod
    cdef inline Object cast_from_ptr(godot_object *ptr):
        # Retreive class
        cdef GDString classname = GDString.__new__(GDString)
        with nogil:
            gdapi10.godot_method_bind_ptrcall(
                __methbind__Object__get_class,
                ptr,
                NULL,
                &classname._gd_data
            )
        return globals()[str(classname)]._from_ptr(<size_t>ptr)

    def __eq__(self, other):
        try:
            return self._gd_ptr == (<{{ cls.name }}>other)._gd_ptr
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return self._gd_ptr != (<{{ cls.name }}>other)._gd_ptr
        except TypeError:
            return True

    def __getattr__(self, name):
        cdef GDString gdname = GDString(name)
        cdef GDString gdnamefield = GDString("name")

        # If a script is attached to the object, we expose here it methods
        if not hasattr(type(self), '__exposed_python_class'):
            if self.has_method(name):

                def _call(*args):
                    return {{ cls.name }}.callv(self, gdname, Array(args))

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

{% if not cls.singleton and cls.instantiable %}

{% if cls.is_reference %}
    def __init__(self):
        if __{{ cls.name }}_constructor == NULL:
            raise NotImplementedError(__ERR_MSG_BINDING_NOT_AVAILABLE)
        cdef godot_bool __ret
        with nogil:
            self._gd_ptr = __{{ cls["name"] }}_constructor()

            if self._gd_ptr is NULL:
                raise MemoryError

            gdapi10.godot_method_bind_ptrcall(
                __methbind__Reference__init_ref,
                self._gd_ptr,
                NULL,
                &__ret
            )
{% else %}
    @staticmethod
    def new():
        if __{{ cls.name }}_constructor == NULL:
            raise NotImplementedError(__ERR_MSG_BINDING_NOT_AVAILABLE)
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls.name }} wrapper = {{ cls.name }}.__new__({{ cls.name }})
        with nogil:
            wrapper._gd_ptr = __{{ cls.name }}_constructor()
        if wrapper._gd_ptr is NULL:
            raise MemoryError
        return wrapper
{% endif %}

{% if cls.name == "Reference" %}
    @classmethod
    def new(cls):
        raise RuntimeError(f"Refcounted Godot object must be created with `{ cls.__name__ }()`")

    def __dealloc__(self):
        cdef godot_bool __ret
        if self._gd_ptr == NULL:
            return
        with nogil:
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
    cdef {{ cls.name }} from_ptr(godot_object *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls.name }} wrapper = {{ cls.name }}.__new__({{ cls.name }})
        wrapper._gd_ptr = _ptr
{% if cls.is_reference %}
        # Note we steal the reference from the caller given we
        # don't call `Reference.reference` here
{% endif %}
        return wrapper

{% if not cls.singleton and cls.instantiable %}
    @classmethod
    def _new(cls):
        cdef godot_object* ptr = __{{ cls.name }}_constructor()
        if ptr is NULL:
            raise MemoryError
        return <size_t>ptr
{% endif %}

    @staticmethod
    def _from_ptr(ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls.name }} wrapper = {{ cls.name }}.__new__({{ cls.name }})
        # /!\ doing `<godot_object*>ptr` would return the address of
        # the PyObject instead of casting it value !
        wrapper._gd_ptr = <godot_object *><size_t>ptr
{% if cls.is_reference %}
        # Note we steal the reference from the caller given we
        # don't call `Reference.reference` here
{% endif %}
        return wrapper

{% if cls.constants | length %}
    # Constants
{% endif %}
{% for key, value in cls.constants.items() %}
    {{ key }} = {{ value }}
{% endfor %}
{% if cls.enums | length %}
    # Enums
{% endif %}
{% for enum in cls.enums %}
    {{ enum.name }} = IntFlag("{{ enum.name }}", {
{% for key, value in enum.values.items() %}
    "{{ key }}": {{ value }},
{% endfor %}
    })
{% endfor %}

{% if cls.methods | length %}
    # Methods
{% endif %}
{# TODO: Use typing for params&return #}
{% for method in cls.methods %}
{% if method.name != "free" %}
    {{ render_method(cls, method) | indent }}
{% endif %}
{% endfor %}
{% if cls.properties | length %}
    # Properties
{% endif %}
{#
TODO: some properties has / in there name
TODO: some properties pass a parameter to the setter/getter
TODO: see PinJoint.params/bias for a good example
#}
{% for prop in cls.properties %}

    @property
    def {{ prop.name }}(self):
{% if prop.is_supported %}
        return self.{{ prop.getter }}({% if prop.index is not none %}{{ prop.index }}{% endif %})
{% else %}
        raise NotImplementedError("{{prop.unsupported_reason}}")
{% endif %}

{% if prop.setter %}
    @{{ prop.name }}.setter
    def {{ prop.name }}(self, val):
{% if prop.is_supported %}
        self.{{ prop.setter }}({% if prop.index is not none %}{{ prop.index }},{% endif %}val)
{% else %}
        raise NotImplementedError("{{prop.unsupported_reason}}")
{% endif %}
{% endif %}

{% endfor %}

{% endmacro %}
