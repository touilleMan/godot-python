{% macro render_gdapi(spec) -%}

{% for c in spec.constructors %}
cdef GDNativePtrConstructor __{{ spec.name }}_constructor_{{ c.index }} = gdapi.variant_get_ptr_constructor(
    {{ spec.variant_type_name }}, {{ c.index }}
)
{% endfor %}
{% if spec.has_destructor %}
cdef GDNativePtrDestructor __{{ spec.name }}_destructor = gdapi.variant_get_ptr_destructor(
    {{ spec.variant_type_name }}
)
{% endif %}

{%- endmacro %}
