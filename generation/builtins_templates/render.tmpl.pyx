{#- `render_target` must be defined by calling context -#}
{% set get_target_method_spec = get_target_method_spec_factory(render_target) %}

{#- Define rendering macros -#}

{% macro render_method(method_name, py_name=None, default_args={}) %}
{% set spec = get_target_method_spec(method_name) %}
{% set args_without_self = spec.args[1:] %}
def {{ py_name or spec.py_name }}({{ spec.klass.cy_type }} self{%- if args_without_self -%},{%- endif -%}
{%- for arg in args_without_self %}
 {{ arg.cy_type }} {{ arg.name }}
{%-     if not arg.is_base_type and not arg.is_variant %}
 not None
{%-     endif -%}
,
{%- endfor -%}
) -> {{ spec.return_type.py_type }}:
{% for arg in args_without_self %}
{%     if arg.is_variant %}
    cdef godot_variant __var_{{ arg.name }}
    if not pyobj_to_godot_variant({{ arg.name }}, &__var_{{ arg.name }}):
{%         for initialized_arg in args_without_self %}
{%             if initialized_arg.name == arg.name %}
{%                 break %}
{%             endif %}
{%             if initialized_arg.is_variant %}
        gdapi10.godot_variant_destroy(&__var_{{ initialized_arg.name }})
{%             endif %}
{%         endfor %}
        raise TypeError(f"Cannot convert `{ {{ arg.name}} !r}` to Godot Variant")
{%     endif %}
{% endfor %}
{% if spec.return_type.is_variant %}
    cdef godot_variant __var_ret = (
{%- elif spec.return_type.is_builtin %}
    cdef {{ spec.return_type.cy_type }} __ret = {{ spec.return_type.cy_type }}.__new__({{ spec.return_type.cy_type }})
    __ret._gd_data = (
{%- elif spec.return_type.is_object %}
    cdef {{ spec.return_type.cy_type }} __ret = {{ spec.return_type.cy_type }}.__new__({{ spec.return_type.cy_type }})
    __ret._gd_ptr = (
{%- elif not spec.return_type.is_void %}
    cdef {{ spec.return_type.cy_type }} __ret = (
{%- else %}
    (
{%- endif %}
{{ spec.gdapi }}.{{ spec.c_name }}(&self._gd_data,
{%- for arg in args_without_self %}
{%- if arg.is_variant %}
 &__var_{{ arg.name }},
{%- elif arg.is_builtin %}
{%- if arg.is_ptr %}
 &{{ arg.name }}._gd_data,
{%- else %}
 {{ arg.name }}._gd_data,
{%- endif %}
{%- elif arg.is_object %}
 {{ arg.name }}._gd_ptr,
{%- else %}
 {{ arg.name }},
{%- endif %}
{% endfor %}
))
{% for arg in args_without_self %}
{% if arg.is_variant %}
    gdapi10.godot_variant_destroy(&__var_{{ arg.name }})
{% endif %}
{% endfor %}
{% if spec.return_type.is_variant %}
    cdef object __ret = godot_variant_to_pyobj(&__var_ret)
    gdapi10.godot_variant_destroy(&__var_ret)
    return __ret
{% elif not spec.return_type.is_void %}
    return __ret
{% endif %}
{% endmacro %}

{% macro render_operator_eq() %}
{% set spec = get_target_method_spec("operator_equal") %}
def __eq__({{ spec.klass.cy_type }} self, other):
    try:
        return {{ spec.gdapi }}.{{ spec.c_name }}(&self._gd_data, &(<{{ spec.klass.cy_type }}?>other)._gd_data)
    except TypeError:
        return False
{% endmacro %}

{% macro render_operator_ne() %}
{% set spec = get_target_method_spec("operator_equal") %}
def __ne__({{ spec.klass.cy_type }} self, other):
    try:
        return not {{ spec.gdapi }}.{{ spec.c_name }}(&self._gd_data, &(<{{ spec.klass.cy_type }}?>other)._gd_data)
    except TypeError:
        return True
{% endmacro %}

{% macro render_operator_lt() %}
{% set spec = get_target_method_spec("operator_less") %}
def __lt__({{ spec.klass.cy_type }} self, other):
    try:
        return {{ spec.gdapi }}.{{ spec.c_name }}(&self._gd_data, &(<{{ spec.klass.cy_type }}?>other)._gd_data)
    except TypeError:
        return False
{% endmacro %}

{% macro render_property(py_name, getter, setter=None) %}
@property
{{ render_method(getter, py_name=py_name) }}
{% if setter %}
@{{ py_name }}.setter
{{ render_method(setter, py_name=py_name) }}
{% endif %}
{% endmacro %}

{#- Overwrite blocks to be ignored -#}

{% block pxd_header %}{% endblock %}
{% block cdef_attributes %}{% endblock %}

{#- Now the template will be generated with the context -#}

{% extends render_target_to_template(render_target) %}
