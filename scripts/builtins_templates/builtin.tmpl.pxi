{% macro render_spec(spec) -%}
@cython.final
cdef class {{ spec.name }}:

    def __init__(self, ):
        pass

    # Constants
{% for c in spec.constants %}
    {{ c.name }} = {{ c.value }}
{% endfor %}

{%- endmacro %}
