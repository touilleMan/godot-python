{% macro render_method(method) -%}

def {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
    {{ arg["name"] }},
{%- endfor %}
):
    pass

{%- endmacro -%}
