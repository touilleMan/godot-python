{%- macro iter_singletons(data) -%}
{%- for item in data -%}
{%- if item["singleton"] and item["name"] != "GlobalConstants" -%}
{{ caller(item) }}
{%- endif -%}
{%- endfor -%}
{%- endmacro -%}

{%- call(item) iter_singletons(data) %}
cdef godot_object *__singleton__{{item["name"]}}
{%- endcall %}


cdef init_singletons():
{%- call(item) iter_singletons(data) %}
    global __singleton__{{item["name"]}}
{%- endcall %}
{% call(item) iter_singletons(data) %}
    __singleton__{{item["name"]}} = _{{ item["name"] }}.from_ptr(
    	godot_global_get_singleton("{{ item["name"] }}")
    )
{%- endcall -%}
