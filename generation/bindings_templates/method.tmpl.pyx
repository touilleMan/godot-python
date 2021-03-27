{% macro get_method_bind_register_name(cls, method) -%}
__methbind__{{ cls.name }}__{{ method.name }}
{%- endmacro %}


{% macro render_method_c_signature(method) %}
{{ method.return_type.c_type }} {{ method.name }}(self,
{%- for arg in method.arguments %}
 {{ arg.type.c_type }} {{ arg.name }},
{%- endfor %}
)
{%- endmacro %}


{% macro render_method_signature(method) %}
{{ method.name }}(self,
{%- for arg in method.arguments %}
{%- if arg.type.c_type in ("godot_string", "godot_node_path") %}
 object {{ arg.name }}
{%- else %}
 {{ arg.type.cy_type }} {{ arg.name }}
{#- `not None` is only for Python arguments so no need for base type #}
{#-  if default value is NULL, None should be allowed #}
{%- if not arg.type.is_base_type and not (arg.has_default_value and arg.default_value == "None") %}
  not None
{%- endif %}
{%- endif %}
{%- if arg.has_default_value %}
={{ arg.default_value }}
{%- endif %}
,
{%- endfor %}
)
{%- endmacro %}


{% macro _render_method_return(method, retval="__ret") %}
{% if method.return_type.c_type == "void" %}
return
{% elif method.return_type.is_object %}
if {{ retval }} == NULL:
    return None
else:
    return Object.cast_from_ptr({{ retval }})
{% elif method.return_type.c_type == "godot_variant" %}
try:
    return godot_variant_to_pyobj(&{{ retval }})
finally:
    with nogil:
        gdapi10.godot_variant_destroy(&{{ retval }})
{% elif method.return_type.is_enum %}
return {{ method.return_type.py_type }}({{ retval }})
{% else %}
return {{ retval }}
{% endif %}
{%- endmacro %}


{% macro _render_method_cook_args(method, argsval="__args") %}
{% if (method.arguments | length )  != 0 %}
cdef const void *{{ argsval }}[{{ method.arguments | length }}]
{% endif %}
{% for arg in method.arguments %}
{% set i = loop.index - 1 %}
# {{ arg.type.c_type }} {{ arg.name }}
{% if arg.type.c_type == "godot_string" %}
cdef GDString __gdstr_{{ arg.name }} = ensure_is_gdstring({{ arg.name }})
{{ argsval }}[{{ i }}] = <void*>(&__gdstr_{{ arg.name }}._gd_data)
{% elif arg.type.c_type == "godot_node_path" %}
cdef NodePath __nodepath_{{ arg.name }} = ensure_is_nodepath({{ arg.name }})
{{ argsval }}[{{ i }}] = <void*>(&__nodepath_{{ arg.name }}._gd_data)
{% elif arg.type.is_object %}
{%- if arg.has_default_value and arg.default_value == "None" %}
{{ argsval }}[{{ i }}] = <void*>{{ arg.name }}._gd_ptr if {{ arg.name }} is not None else NULL
{%- else %}
{{ argsval }}[{{ i }}] = <void*>{{ arg.name }}._gd_ptr
{%- endif %}
{% elif arg.type.c_type == "godot_variant" %}
cdef godot_variant __var_{{ arg.name }}
pyobj_to_godot_variant({{ arg.name }}, &__var_{{ arg.name }})
{{ argsval }}[{{ i }}] = <void*>(&__var_{{ arg.name }})
{% elif arg.type.is_builtin %}
{{ argsval }}[{{ i }}] = <void*>(&{{ arg.name }}._gd_data)
{% elif arg.type.c_type == "godot_real" %}
# ptrcall does not work with single precision floats, so we must convert to a double
cdef double {{ arg.name }}_d = <double>{{ arg.name }};
{{ argsval }}[{{ i }}] = &{{ arg.name }}_d
{% else %}
{{ argsval }}[{{ i }}] = &{{ arg.name }}
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_destroy_args(method) %}
{% for arg in method.arguments %}
{% set i = loop.index - 1 %}
{% if arg.type.c_type == "godot_variant" %}
with nogil:
    gdapi10.godot_variant_destroy(&__var_{{ arg.name }})
{% endif %}
{% endfor %}
{%- endmacro %}


{% macro _render_method_call(cls, method, argsval="__args", retval="__ret") %}
{% if method.return_type.c_type == "void" %}
{% set retval_as_arg = "NULL" %}
{% elif method.return_type.is_object %}
# It's important to initialize this pointer to null given
# in case of Reference, Godot will try to decrease the
# refcount if the pointer is valid !
# (see https://github.com/godotengine/godot/issues/35609)
cdef godot_object *{{ retval }} = NULL
{% set retval_as_arg = "&{}".format(retval) %}
{% elif method.return_type.c_type == "godot_variant" %}
cdef godot_variant {{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
{% elif method.return_type.is_builtin %}
{% set cy_type =  method.return_type.cy_type %}
cdef {{ cy_type }} {{ retval }} = {{ cy_type }}.__new__({{ cy_type }})
{% set retval_as_arg = "&{}._gd_data".format(retval) %}
{% elif method.return_type.c_type == "godot_real" %}
# ptrcall does not work with single precision floats, so we must convert to a double
cdef double {{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
{% else %}
cdef {{ method.return_type.c_type }} {{ retval }}
{% set retval_as_arg = "&{}".format(retval) %}
{% endif %}
if {{ get_method_bind_register_name(cls, method) }} == NULL:
    raise NotImplementedError(__ERR_MSG_BINDING_NOT_AVAILABLE)
with nogil:
    gdapi10.godot_method_bind_ptrcall(
        {{ get_method_bind_register_name(cls, method) }},
        self._gd_ptr,
    {% if (method.arguments | length )  != 0 %}
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
{% if method.is_virtual %}
    cdef Array args = Array()
{%   for arg in method.arguments %}
    args.append({{ arg.name }})
{%   endfor %}
    return Object.callv(self, "{{ method.name }}", args)
{% else %}
{%   if method.is_supported %}
    {{ _render_method_cook_args(method) | indent }}
    {{ _render_method_call(cls, method) | indent }}
    {{ _render_method_destroy_args(method) | indent }}
    {{ _render_method_return(method) | indent }}
{%   else %}
    raise NotImplementedError("{{method.unsupported_reason}}")
{%   endif %}
{% endif %}
{% endmacro %}
