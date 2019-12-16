{#- `render_target` must be defined by calling context -#}
{% set py_type = render_target_to_py_type(render_target) %}
{% set gd_type = py_to_gd_type(py_type) %}

{#- Define rendering macros -#}

{% macro render_method(pyname, return_type=None, args=(), gdname=None, gdapi="") %}{% endmacro %}
{% macro render_operator_eq() %}{% endmacro %}
{% macro render_operator_ne() %}{% endmacro %}
{% macro render_operator_lt() %}{% endmacro %}

{#- Overwrite blocks to be ignored -#}

{% block pyx_header %}{% endblock %}
{% block python_defs %}{% endblock %}
{% block python_consts %}{% endblock %}

{#- Now the template will be generated with the context -#}

{% extends render_target_to_template(render_target) %}
