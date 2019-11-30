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
object {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
 {{ arg["name"] }},
{%- endfor %}
)
{%- endmacro %}


{% macro _render_method_return(method, retval="__ret") %}
{% if method["return_type"] == "void" %}
return
{% elif method["return_type"] == "godot_string" %}
try:
    return godot_string_to_pyobj(&{{ retval }})
finally:
    gdapi.godot_string_destroy(&{{ retval }})
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
{% if (method["arguments"] | length )  == 0 %}
cdef const void **{{ argsval }} = NULL
{% else %}
cdef const void *{{ argsval }}[{{ method["arguments"] | length }}]
{% endif %}
{% for arg in method["arguments"] %}
{% set i = loop.index - 1 %}
# {{ arg["type"] }} {{ arg["name"] }}
{% if arg["type_is_binding"] %}
{{ argsval }}[{{ i }}] = <void*>(&{{ arg["name"] }}._ptr)
{% elif arg["type"] == "godot_int" %}
cdef godot_int __var_{{ arg["name"] }} = {{ arg["name"] }}
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg["name"] }})
{% elif arg["type"] == "godot_float" %}
cdef godot_float __var_{{ arg["name"] }} = {{ arg["name"] }}
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg["name"] }})
{% elif arg["type"] == "godot_bool" %}
cdef godot_bool __var_{{ arg["name"] }} = {{ arg["name"] }}
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg["name"] }})
{% elif arg["type"] == "godot_string" %}
cdef godot_string __var_{{ arg["name"] }}
pyobj_to_godot_string({{ arg["name"] }}, &__var_{{ arg["name"] }})
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg["name"] }})
{% elif arg["type"] == "godot_vector2" %}
{{ argsval }}[{{ i }}] = <void*>(&(<Vector2>{{ arg["name"] }})._gd_data)
{% elif arg["type"] == "godot_array" %}
{{ argsval }}[{{ i }}] = <void*>(&(<Array>{{ arg["name"] }})._gd_data)
{% elif arg["type"] == "godot_dictionary" %}
{{ argsval }}[{{ i }}] = <void*>(&(<Dictionary>{{ arg["name"] }})._gd_data)
{% elif arg["type"] == "godot_variant" %}
cdef godot_variant __var_{{ arg["name"] }}
pyobj_to_godot_variant({{ arg["name"] }}, &__var_{{ arg["name"] }})
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg["name"] }})
{% else %}
{{ argsval }}[{{ i }}] = <void*>(&{{ arg["name"] }})
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_destroy_args(method) %}
{% for arg in method["arguments"] %}
{% set i = loop.index - 1 %}
{% if arg["type"] == "godot_variant" %}
gdapi.godot_variant_destroy(&__var_{{ arg["name"] }})
{% elif arg["type"] == "godot_string" %}
gdapi.godot_string_destroy(&__var_{{ arg["name"] }})
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_call(cls, method, argsval="__args", retval="__ret") %}
{% if method["return_type"] == "void" %}
{% set retval_as_arg = "NULL" %}
{% elif method["return_type_is_binding"] %}
cdef {{ method["return_type"] }} {{ retval }} = {{ method["return_type"] }}.__new__({{ method["return_type"] }})
{% set retval_as_arg = "{}._ptr".format(retval) %}
{% elif method["return_type"] == "godot_vector2" %}
cdef Vector2 {{ retval }} = Vector2.__new__(Vector2)
{% set retval_as_arg = "&{}._gd_data".format(retval) %}
{% elif method["return_type"] == "godot_array" %}
cdef Array {{ retval }} = Array.__new__(Array)
{% set retval_as_arg = "&{}._gd_data".format(retval) %}
{% elif method["return_type"] == "godot_dictionary" %}
cdef Dictionary {{ retval }} = Dictionary.__new__(Dictionary)
{% set retval_as_arg = "&{}._gd_data".format(retval) %}
{% else %}
cdef {{ method["return_type"] }} {{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
{% endif %}
if {{ get_method_bind_register_name(cls, method) }} == NULL:
    raise NotImplementedError
gdapi.godot_method_bind_ptrcall(
    {{ get_method_bind_register_name(cls, method) }},
    self._ptr,
    {{ argsval }},
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
