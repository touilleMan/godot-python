{% macro get_method_bind_register_name(cls, method) -%}
__methbind__{{ cls["name"] }}__{{ method["name"] }}
{%- endmacro %}


{% macro render_method_bind_register(cls, method) %}
cdef godot_method_bind *{{ get_method_bind_register_name(cls, method) }} = gdapi.godot_method_bind_get_method("{{ cls['name'] }}", "{{ method['name'] }}")
{%- endmacro %}


{% macro render_method_signature(method) %}
{% if method["return_type"] == "godot_variant" %}
object
{%- else %}
{{ method["return_type"] }}
{%- endif %}
 {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
 {{ arg["type"] }} {{ arg["name"] }},
{%- endfor %}
)
{%- endmacro %}


{% macro render_method_return(method, retval="__ret") %}
{% if method["return_type"] == "void" %}
return
{% elif method["return_type"] == "godot_variant" %}
return gd_variant_to_pyobj({{ retval }})
{% elif method["return_type_is_binding"] %}
return {{ method["return_type"] }}.from_ptr({{ retval }})
{% else %}
return {{ retval }}
{% endif %}
{%- endmacro %}


{% macro render_method_cook_args(method, argsval="__args") %}
{% if (method["arguments"] | length )  == 0 %}
cdef const void **{{ argsval }} = NULL
{% else %}
cdef const void *{{ argsval }}[{{ method["arguments"] | length }}]
{% endif %}
{% for arg in method["arguments"] %}
{% set i = loop.index - 1 %}
{% if method["return_type_is_binding"] %}
{{ argsval }}[{{ i }}] = <void*>&{{ arg["name"] }}._ptr
{% elif method["return_type"] == "godot_variant" %}
cdef godot_variant __var_{{ arg["name"] }}
pyobj_to_gdvar(arg["name"], &__var_{{ arg["name"] }})
{{ argsval }}[{{ i }}] = <void*>&__var_{{ arg["name"] }}
{% else %}
{{ argsval }}[{{ i }}] = <void*>&{{ arg["name"] }}
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro render_method_call(cls, method, argsval="__args", retval="__ret") %}
{% if method["return_type"] != "void" %}
cdef {{ method["return_type"] }} {{ retval }}
{% endif %}
gdapi.godot_method_bind_ptrcall(
    {{ get_method_bind_register_name(cls, method) }},
    self._ptr,
    {{ argsval }},
{% if method["return_type"] == "void" %}
    NULL
{% else %}
    &{{ retval }}
{% endif %}
)
{%- endmacro %}


{% macro render_method(cls, method) %}
cpdef {{ render_method_signature(method) }}:
    {{ render_method_cook_args(method) | indent }}
    {{ render_method_call(cls, method) | indent }}
    {{ render_method_return(method) | indent }}
{% endmacro %}
