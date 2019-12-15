{% macro get_method_bind_register_name(cls, method) -%}
__methbind__{{ cls["name"] }}__{{ method["name"] }}
{%- endmacro %}


{% macro render_method_bind_register(cls, method) %}
cdef godot_method_bind *{{ get_method_bind_register_name(cls, method) }} = gdapi.godot_method_bind_get_method("{{ cls['bind_register_name'] }}", "{{ method['name'] }}")
{%- endmacro %}


{% macro render_method_c_signature(method) %}
{{ method["return_type"] }} {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
 {{ arg["type"] }} {{ arg["name"] }},
{%- endfor %}
)
{%- endmacro %}


{% macro render_method_signature(method) %}
{{ method["return_type_specs"]["binding_type"] }} {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
 {{ arg["type_specs"]["binding_type"] }} {{ arg["name"] }},
{%- endfor %}
)
{%- endmacro %}


{% macro _render_method_return(method, retval="__ret") %}
{% if method["return_type"] == "void" %}
return
{% elif method["return_type_specs"]["is_object"] %}
if {{ retval }}._gd_ptr == NULL:
    return None
else:
    return {{ retval }}
{% elif method["return_type"] == "godot_variant" %}
try:
    return godot_variant_to_pyobj(&{{ retval }})
finally:
    gdapi.godot_variant_destroy(&{{ retval }})
{% else %}
return {{ retval }}
{% endif %}
{%- endmacro %}


{% macro _render_method_cook_args(method, argsval="__args") %}
{% if (method["arguments"] | length )  != 0 %}
cdef const void *{{ argsval }}[{{ method["arguments"] | length }}]
{% endif %}
{% for arg in method["arguments"] %}
{% set i = loop.index - 1 %}
# {{ arg["type"] }} {{ arg["name"] }}
{% if arg["type_specs"]["is_object"] %}
{{ argsval }}[{{ i }}] = <void*>(&{{ arg["name"] }}._gd_ptr)
{% elif arg["type"] == "godot_variant" %}
cdef godot_variant __var_{{ arg["name"] }}
pyobj_to_godot_variant({{ arg["name"] }}, &__var_{{ arg["name"] }})
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg["name"] }})
{% elif arg["type_specs"]["is_builtin"] %}
{{ argsval }}[{{ i }}] = <void*>(&{{ arg["name"] }}._gd_data)
{% else %}
{{ argsval }}[{{ i }}] = &{{ arg["name"] }}
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_destroy_args(method) %}
{% for arg in method["arguments"] %}
{% set i = loop.index - 1 %}
{% if arg["type"] == "godot_variant" %}
gdapi.godot_variant_destroy(&__var_{{ arg["name"] }})
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_call(cls, method, argsval="__args", retval="__ret") %}
{% if method["return_type"] == "void" %}
{% set retval_as_arg = "NULL" %}
{% elif method["return_type_specs"]["is_object"] %}
{% set binding_type =  method["return_type_specs"]["binding_type"] %}
cdef {{ binding_type }} {{ retval }} = {{ binding_type }}.__new__({{ binding_type }})
{% set retval_as_arg = "&{}._gd_ptr".format(retval) %}
{% elif method["return_type"] == "godot_variant" %}
cdef godot_variant {{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
{% elif method["return_type_specs"]["is_builtin"] %}
{% set binding_type =  method["return_type_specs"]["binding_type"] %}
cdef {{ binding_type }} {{ retval }} = {{ binding_type }}.__new__({{ binding_type }})
{% set retval_as_arg = "&{}._gd_data".format(retval) %}
{% else %}
cdef {{ method["return_type"] }} {{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
{% endif %}
if {{ get_method_bind_register_name(cls, method) }} == NULL:
    raise NotImplementedError
gdapi.godot_method_bind_ptrcall(
    {{ get_method_bind_register_name(cls, method) }},
    self._gd_ptr,
{% if (method["arguments"] | length )  != 0 %}
    {{ argsval }},
{%else %}
    NULL,
{% endif %}
    {{ retval_as_arg }}
)
{%- endmacro %}


{% macro render_method(cls, method) %}
# {{ render_method_c_signature(method) }}
cpdef {{ render_method_signature(method) }}:
    {{ _render_method_cook_args(method) | indent }}
    {{ _render_method_call(cls, method) | indent }}
    {{ _render_method_destroy_args(method) | indent }}
    {{ _render_method_return(method) | indent }}
{% endmacro %}
