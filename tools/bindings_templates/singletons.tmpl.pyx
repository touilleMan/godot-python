{% macro iter_singletons(classes) %}
{% for cls in classes %}
{% if cls["singleton"] %}
{{ caller(cls) }}
{% endif %}
{% endfor %}
{% endmacro %}

cdef void *ptr
{% call(cls) iter_singletons(classes) %}
ptr = gdapi10.godot_global_get_singleton("{{ cls['singleton_name'] }}")
if ptr:
    {{ cls["singleton_name"] }} = {{ cls["name"] }}.from_ptr(
        gdapi10.godot_global_get_singleton("{{ cls['singleton_name'] }}")
    )
{% endcall %}
