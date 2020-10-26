{# TODO: Handle signals #}
{% macro render_class(cls) %}

class {{ cls.name }}({{ cls.base_class }}):
{% if not cls.base_class %}
    def free(self) -> None: ...
    def __init__(self): ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any): ...
    def call(self, name: str, *args) -> Any: ...

{% endif %}

{% if not cls.singleton and cls.instantiable %}

{% if cls.is_reference %}
    def __init__(self): ...
{% else %}
    @staticmethod
    def new() -> {{ cls.name }}: ...
{% endif %}

{% if cls.name == "Reference" %}
    @classmethod
    def new(cls) -> Reference: ...
{% endif %}

{% endif %}
{% if cls.constants | length %}
    # Constants
{% endif %}
{% for key, value in cls.constants.items() %}
    {{ key }}: int
{% endfor %}
{% if cls.enums | length %}
    # Enums
{% endif %}
{% for enum in cls.enums %}
    class {{ enum.name }}(IntFlag):
{% for key, value in enum.values.items() %}
        {{ key }}: int
{% endfor %}
{% endfor %}

{% if cls.methods | length %}
    # Methods
{% endif %}
{# TODO: Use typing for params&return #}
{% for method in cls.methods %}
{% if method.name != "free" %}
    def {{ method.name }}(self,
{%- for arg in method.arguments %}
{{ arg.name }}: {{ arg.type.py_type }}
{%- if arg.has_default_value %}
={{ arg.default_value }}
{%- endif %}
,
{%- endfor %}
) -> {{ method.return_type.py_type }}: ...
{% endif %}
{% endfor %}

{% if cls.properties | length %}
    # Properties
{% endif %}
{% for prop in cls.properties %}
    {{ prop.name }}: {{ prop.type.py_type }}
{% endfor %}

{% if not cls.constants and not cls.enums and not cls.methods and not cls.properties %}
    pass
{% endif %}

{% endmacro %}
