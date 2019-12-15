{% from 'property.tmpl.pyx' import render_property %}
{% from 'method.tmpl.pyx' import render_method, render_method_bind_register %}

{# TODO: Handle signals #}
{% macro render_class(cls) %}

{% if not cls["singleton"] %}
cdef godot_class_constructor __{{ cls["name"] }}_constructor = gdapi.godot_get_class_constructor("{{ cls['name'] }}")
{% endif %}

{% for method in cls["methods"] %}
{{ render_method_bind_register(cls, method) }}
{% endfor %}

cdef class {{ cls["name"] }}({{ cls["base_class"] }}):
{% if not cls["base_class"] %}
    # free is virtual but this is not marked in api.json :'(
    cpdef void free(self):
        gdapi.godot_object_destroy(self._gd_ptr)

    def __init__(self):
        raise RuntimeError(f"Use `new()` method to instantiate Godot object.")
{% endif %}

{% if not cls["singleton"] and cls["instanciable"] %}
    @staticmethod
    def new():
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__({{ cls["name"] }})
        wrapper._gd_ptr = __{{ cls["name"] }}_constructor()
        if wrapper._gd_ptr is NULL:
            raise MemoryError
        return wrapper
{% endif %}

    @staticmethod
    cdef {{ cls["name"] }} from_ptr(godot_object *_ptr, bint owner):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__({{ cls["name"] }})
        wrapper._gd_ptr = _ptr
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
