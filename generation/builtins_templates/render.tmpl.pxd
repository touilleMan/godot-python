{#- `render_target` must be defined by calling context -#}
{% set get_target_method_spec = get_target_method_spec_factory(render_target) %}

{#- Define rendering macros -#}

{% macro render_method(method_name, py_name=None, default_args={}) %}{% endmacro %}
{% macro render_property(py_name, getter, setter=None) %}{% endmacro %}
{% macro render_operator_eq() %}{% endmacro %}
{% macro render_operator_ne() %}{% endmacro %}
{% macro render_operator_lt() %}{% endmacro %}

{#- Overwrite blocks to be ignored -#}

{% block pyx_header %}{% endblock %}
{% block python_defs %}{% endblock %}
{% block python_consts %}{% endblock %}

{#- Now the template will be generated with the context -#}

{% extends render_target_to_template(render_target) %}
