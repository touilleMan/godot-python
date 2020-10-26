{#- `render_target` must be defined by calling context -#}
{% set get_target_method_spec = get_target_method_spec_factory(render_target) %}

{#- Define rendering macros -#}

{% macro render_method(method_name, py_name=None, default_args={}) %}
{% set spec = get_target_method_spec(method_name) %}
def {{ py_name or spec.py_name }}(self{%- if spec.args -%},{%- endif -%}
{%- for arg in spec.args %}
 {{ arg.name }}: {{ arg.type.py_type }}
,
{%- endfor -%}
) -> {{ spec.return_type.py_type }}: ...
{% endmacro %}

{% macro render_operator_eq() %}
def __eq__(self, other) -> bool: ...
{% endmacro %}

{% macro render_operator_ne() %}
def __ne__(self, other) -> bool: ...
{% endmacro %}

{% macro render_operator_lt() %}
def __lt__(self, other) -> bool: ...
{% endmacro %}

{% macro render_property(py_name, getter, setter=None) %}
{{ pyname }}: {{ getter.return_type.py_type }}
{% endmacro %}

{#- Overwrite blocks to be ignored -#}

{% block python_defs %}
	pass
{% endblock %}
{% block pxd_header %}{% endblock %}
{% block pyx_header %}{% endblock %}
{% block python_consts %}{% endblock %}
{% block cdef_attributes %}{% endblock %}

{#- Now the template will be generated with the context -#}

{% extends render_target_to_template(render_target) %}
