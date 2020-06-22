{% from 'property.tmpl.pyi' import render_property %}
{% from 'method.tmpl.pyi' import render_method, get_method_bind_register_name %}


{% macro render_class_gdapi_ptrs_init(cls) %}
{% endmacro %}


{# TODO: Handle signals #}
{% macro render_class(cls) %}

class {{ cls["name"] }}({{ cls["base_class"] }}):
{% if not cls["base_class"] %}
    # free is virtual but this is not marked in api.json :'(
    def free(self): ...
    def __init__(self): ...
    def __repr__(self): ...
    def __eq__(self, other: {{ cls["name"] }}) -> bool: ...
    def __ne__(self, other: {{ cls["name"] }}) -> bool: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any): ...
    def call(self, name: str, *args) -> Any: ...

{% endif %}

{% if not cls["singleton"] and cls["instanciable"] %}

{% if cls["is_reference"] %}
    def __init__(self): ...
{% else %}
    @staticmethod
    def new() -> {{ cls["name"] }}: ...
{% endif %}

{% if cls["name"] == "Reference" %}
    @classmethod
    def new(cls): ...
{% endif %}

{% endif %}
    # Constants
{% for key, value in cls["constants"].items() %}
    {{ key }}: int
{% endfor %}

    # Methods
{# TODO: Use typing for params&return #}
{% for method in cls["methods"] %}
{% if method["name"] != "free" %}
    {{ render_method(cls, method) | indent }}
{% endif %}
{% endfor %}
    # Properties
{% for prop in cls["properties"] %}
    {{ render_property(prop) | indent }}
{% endfor %}

{% endmacro %}
