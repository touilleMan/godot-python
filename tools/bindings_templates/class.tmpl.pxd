{% from 'method.tmpl.pyx' import get_method_bind_register_name, render_method_signature %}

{% macro render_class_pxd(cls) %}

cdef class {{ cls.name }}({{ cls.base_class }}):
{% if not cls.base_class %}
    cdef godot_object *_gd_ptr

    @staticmethod
    cdef inline Object cast_from_variant(const godot_variant *p_gdvar)

    @staticmethod
    cdef inline Object cast_from_ptr(godot_object *ptr)

{% endif %}
    @staticmethod
    cdef {{ cls.name }} from_ptr(godot_object *_ptr)

{% endmacro %}
