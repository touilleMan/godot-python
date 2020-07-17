{#- `render_target` must be defined by calling context -#}
{% set py_type = render_target_to_py_type(render_target) %}
{% set gd_type = py_to_gd_type(py_type) %}

{#- Define rendering macros -#}

{% macro render_method(pyname, return_type=None, args=(), gdname=None, gdapi="10") %}
{% set gdname = gdname or pyname %}
{% set return_type = cook_return_type(return_type) %}
{% set args = cook_args(args) %}
def {{ pyname }}(self{%- if args -%},{%- endif -%}
{%- for arg in args %}
 {{ arg["name"] }}: {{ arg["py_type"] }}
{%- if not arg["is_base_type"] and arg["gd_type"] != "godot_variant" %}
 not None
{%- endif -%}
,
{%- endfor -%}
) -> {{ return_type["signature_type"] }}: ...
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

{% macro render_property(pyname, type, gdname_getter, gdname_setter=None) %}
{{ pyname }}: {{ type }}
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
