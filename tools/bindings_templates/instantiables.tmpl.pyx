{%- macro iter_instanciables(data) -%}
{%- for item in data -%}
{%- if item["name"] != "GlobalConstants" -%}
{{ caller(item) }}
{%- endif -%}
{%- endfor -%}
{%- endmacro -%}


{%- call(item) iter_instanciables(data) -%}

{%- if not item["singleton"] %}
cdef godot_class_constructor __{{ item["name"] }}_constructor = NULL
{% endif -%}

cdef class {{ item["name"] }}({{ item["base_class"] }}):
{%- if not item["base_class"] %}
    cdef godot_object *_ptr
    cdef bint _ptr_owner
{%- endif %}

    def __init__(self):
{%- if item["singleton"] %}
        raise RuntimeError(f"{type(self)} is a singleton, cannot initialize it.")
{%- else %}
        self._ptr = __{{ item["name"] }}_constructor()
        if self._ptr is NULL:
            raise MemoryError
        self._ptr_owner = True
{%- endif %}

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self._ptr is not NULL and self._ptr_owner is True:
            godot_object_destroy(self._ptr)
            self._ptr = NULL

    @staticmethod
    cdef {{ item["name"] }} from_ptr(godot_object *_ptr, bint owner=False):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ item["name"] }} wrapper = {{ item["name"] }}.__new__()
        wrapper._ptr = _ptr
        wrapper._ptr_owner = owner
        return wrapper

    # Constants
{% for key, value in item["constants"].items() %}
    {{key}} = {{value}}
{%- endfor %}

    # Methods
{% for method in item["methods"] %}
    cpdef {{ method["return_type"] }} {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
        {{ arg["type"] }} {{ arg["name"] }},
{%- endfor %}
    ):
        pass
{% endfor %}
    # Properties
{% for prop in item["properties"] %}
{#
TODO: some properties has / in there name
TODO: some properties pass a parameter to the setter/getter
TODO: see PinJoint.params/bias for a good example
#}
    @property
    def {{ prop["name"].replace('/', '_') }}(self):
        return self.{{ prop["getter"] }}()

    @{{ prop["name"].replace('/', '_') }}.setter
    def {{ prop["name"].replace('/', '_') }}(self, val):
        self.{{ prop["getter"] }}(val)
{% endfor %}

{% endcall %}


cdef _init_constructors():
{%- call(item) iter_instanciables(data) %}
    global __{{ item["name"] }}_constructor
{%- endcall %}
{% call(item) iter_instanciables(data) %}
    __{{ item["name"] }}_constructor = godot_get_class_constructor("{{ item["name"] }}")
{%- endcall %}
