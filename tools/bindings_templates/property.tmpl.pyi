{#
TODO: some properties has / in there name
TODO: some properties pass a parameter to the setter/getter
TODO: see PinJoint.params/bias for a good example
#}

{% macro render_property(prop) %}

@property
def {{ prop["name"].replace('/', '_') }}(self):
    return self.{{ prop["getter"] }}(
{%- if prop["index"] != -1 -%}
{{ prop["index"] }}
{%- endif -%}
    )

{% if prop["setter"] %}
@{{ prop["name"].replace('/', '_') }}.setter
def {{ prop["name"].replace('/', '_') }}(self, val):
    self.{{ prop["setter"] }}(
{%- if prop["index"] != -1 -%}
{{ prop["index"] }},
{%- endif -%}
        val)
{% endif %}

{% endmacro %}
