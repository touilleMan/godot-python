{%- for cls in classes -%}

{%- if not cls["singleton"] %}
cdef godot_class_constructor __{{ cls["name"] }}_constructor = NULL
{% endif -%}

cdef class {{ cls["name"] }}({{ cls["base_class"] }}):
{%- if not cls["base_class"] %}
    cdef godot_object *_ptr
    cdef bint _ptr_owner

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self._ptr is not NULL and self._ptr_owner is True:
            godot_object_destroy(self._ptr)
            self._ptr = NULL
{%- endif %}

    def __init__(self):
{%- if cls["singleton"] %}
        raise RuntimeError(f"{type(self)} is a singleton, cannot initialize it.")
{%- else %}
        self._ptr = __{{ cls["name"] }}_constructor()
        if self._ptr is NULL:
            raise MemoryError
        self._ptr_owner = True
{%- endif %}

    @staticmethod
    cdef {{ cls["name"] }} from_ptr(godot_object *_ptr, bint owner=False):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__()
        wrapper._ptr = _ptr
        wrapper._ptr_owner = owner
        return wrapper

    # Constants
{% for key, value in cls["constants"].items() %}
    {{key}} = {{value}}
{%- endfor %}

    # Methods
{# TODO: Use typing for params&return #}
{% for method in cls["methods"] %}
    def {{ method["name"] }}(self,
{%- for arg in method["arguments"] %}
        {{ arg["name"] }},
{%- endfor %}
    ):
        pass
{% endfor %}
    # Properties
{% for prop in cls["properties"] %}
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

{% endfor %}


cdef _init_constructors():
{%- for cls in classes %}
{%- if not cls["singleton"] %}
    global __{{ cls["name"] }}_constructor
{%- endif %}
{%- endfor %}
{%- for cls in classes %}
{%- if not cls["singleton"] %}
    __{{ cls["name"] }}_constructor = godot_get_class_constructor("{{ cls['name'] }}")
{%- endif %}
{%- endfor %}
