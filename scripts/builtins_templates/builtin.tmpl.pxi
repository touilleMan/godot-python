{% macro render_spec(spec) -%}
@cython.final
cdef class {{ spec.name }}:

    def __init__(self, ):
        pass

{% if spec.constants %}
    # Constants

{% endif %}
{% for c in spec.constants %}
    {{ c.name }} = {{ c.value }}
{% endfor %}

{%- endmacro %}
