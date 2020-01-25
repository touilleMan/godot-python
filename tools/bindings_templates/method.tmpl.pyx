{% macro get_method_bind_register_name(cls, method) -%}
__methbind__{{ cls["name"] }}__{{ method["name"] }}
{%- endmacro %}


{% macro render_method_bind_register(cls, method) %}
cdef godot_method_bind *{{ get_method_bind_register_name(cls, method) }} = gdapi10.godot_method_bind_get_method("{{ cls['bind_register_name'] }}", "{{ method['name'] }}")
{%- endmacro %}


{% macro render_method_c_signature(method) %}
{{ method["return_type"] }} {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
 {{ arg["type"] }} {{ arg["name"] }},
{%- endfor %}
)
{%- endmacro %}


{% macro render_method_signature(method) %}
{{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
{%- if arg["type"] in ("godot_string", "godot_node_path") %}
 object {{ arg["name"] }}
{%- else %}
 {{ arg["type_specs"]["binding_type"] }} {{ arg["name"] }}
{%- if not arg["type_specs"]["is_base_type"] %}
  not None
{%- endif %}
{%- endif %}
{%- if arg["has_default_value"] %}
={{ arg["default_value"] }}
{%- endif %}
,
{%- endfor %}
)
{%- endmacro %}


{% macro _render_method_return(method, retval="__ret") %}
{% if method["return_type"] == "void" %}
return
{% elif method["return_type_specs"]["is_object"] %}
if {{ retval }} == NULL:
    return None
else:
    return Object.cast_from_ptr({{ retval }})
{% elif method["return_type"] == "godot_variant" %}
try:
    return godot_variant_to_pyobj(&{{ retval }})
finally:
    gdapi10.godot_variant_destroy(&{{ retval }})
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
{% if arg["type"] == "godot_string" %}
cdef GDString __gdstr_{{ arg["name"] }} = ensure_is_gdstring({{ arg["name"] }})
{{ argsval }}[{{ i }}] = <void*>(&__gdstr_{{ arg["name"] }}._gd_data)
{% elif arg["type"] == "godot_node_path" %}
cdef NodePath __nodepath_{{ arg["name"] }} = ensure_is_nodepath({{ arg["name"] }})
{{ argsval }}[{{ i }}] = <void*>(&__nodepath_{{ arg["name"] }}._gd_data)
{% elif arg["type_specs"]["is_object"] %}
{{ argsval }}[{{ i }}] = <void*>{{ arg["name"] }}._gd_ptr
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
gdapi10.godot_variant_destroy(&__var_{{ arg["name"] }})
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_call(cls, method, argsval="__args", retval="__ret") %}
{% if method["return_type"] == "void" %}
{% set retval_as_arg = "NULL" %}
{% elif method["return_type_specs"]["is_object"] %}
cdef godot_object *{{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
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
gdapi10.godot_method_bind_ptrcall(
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
def {{ render_method_signature(method) }}:
    {{ _render_method_cook_args(method) | indent }}
    {{ _render_method_call(cls, method) | indent }}
    {{ _render_method_destroy_args(method) | indent }}
    {{ _render_method_return(method) | indent }}
{% endmacro %}
