{% macro get_method_bind_register_name(cls, method) -%}
{%- endmacro %}


{% macro render_method_c_signature(method) %}
{%- endmacro %}


{% macro render_method_signature(method) %}
{{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
{%- if arg["type"] in ("godot_string", "godot_node_path") %}
{{ arg["name"] }}: Any
{%- else %}
{{ arg["name"] }}: {{ arg["type_specs"]["binding_type"] }}
{%- endif %}
{%- if arg["has_default_value"] %}
={{ arg["default_value"] }}
{%- endif %}
,
{%- endfor %}
)
{%- endmacro %}


{% macro _render_method_return(method, retval="__ret") %}
{%- endmacro %}


{% macro _render_method_cook_args(method, argsval="__args") %}
{%- endmacro %}


{% macro _render_method_destroy_args(method) %}
{%- endmacro %}


{% macro _render_method_call(cls, method, argsval="__args", retval="__ret") %}
{%- endmacro %}


{% macro render_method(cls, method) %}
# {{ render_method_c_signature(method) }}
def {{ render_method_signature(method) }} -> {{ method["return_type"] }}: ...
{% endmacro %}
