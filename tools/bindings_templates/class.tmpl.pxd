{% from 'method.tmpl.pyx' import get_method_bind_register_name, render_method_signature %}

{% macro render_class_pxd(cls) %}

{% if not cls["singleton"] %}
cdef godot_class_constructor __{{ cls["name"] }}_constructor
{% endif %}

{% for method in cls["methods"] %}
cdef godot_method_bind *{{ get_method_bind_register_name(cls, method) }}
{% endfor %}

cdef class {{ cls["name"] }}({{ cls["base_class"] }}):
{% if not cls["base_class"] %}
    cdef godot_object *_gd_ptr
{% endif %}

    @staticmethod
    cdef {{ cls["name"] }} from_ptr(godot_object *_ptr, bint owner)

{% for method in cls["methods"] %}
    cpdef {{ render_method_signature(method) | indent }}
{% endfor %}

{% endmacro %}
