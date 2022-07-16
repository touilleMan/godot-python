{% macro render_spec(spec) -%}

{% for c in spec.constructors %}
cdef GDNativePtrConstructor __{{ spec.name }}_constructor_{{ c.index }} = gdapi.variant_get_ptr_constructor(
    {{ spec.variant_type_name }}, {{ c.index }}
)
{% endfor %}
{% if spec.has_destructor %}
cdef GDNativePtrDestructor __{{ spec.name }}_destructor = gdapi.variant_get_ptr_destructor(
    {{ spec.variant_type_name }}
)
{% endif %}

@cython.final
cdef class {{ spec.name }}:
{# TODO: I guess only Nil has no size, so remove it and only use None ? #}
{% if spec.size %}
    cdef char _gd_data[{{ spec.size }}]

    # Constructors
    def __init__({{ spec.name }} self):
        __{{ spec.name }}_constructor_0(self._gd_data, NULL)

    @staticmethod
    cdef inline {{ spec.name }} new():
        # Call to __new__ bypasses __init__ constructor
        cdef {{ spec.name }} ret = {{ spec.name }}.__new__({{ spec.name }})
        __{{ spec.name }}_constructor_0(ret._gd_data, NULL)
        return ret
{% endif %}

{% if spec.has_destructor %}
    # Destructor
    def __dealloc__({{ spec.name }} self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        __{{ spec.name }}_destructor(self._gd_data)
{% else %}
    # Destructor not needed
{% endif %}

    def __repr__(self):
        # TODO: finish me...
        # gdapi.variant_stringify(&self._gd_data)
        return "<{{ spec.name }}>"

{% if spec.constants %}
    # Constants

{% endif %}
{% for c in spec.constants %}
    {{ c.name }} = {{ c.value }}
{% endfor %}

{% if spec.methods %}
    # Methods

{% endif %}
{% for m in spec.methods %}
    def {{ m.name }}(
        self,
{% for arg in m.arguments %}
        {{ arg.name }},
{% endfor %}
    ):
        # TODO
        # cdef GDNativePtrBuiltInMethod ptrmethod = pythonscript_gdapi.variant_get_ptr_builtin_method(
        #     {{ spec.variant_type_name }},
        #     "{{ m.original_name }}",
        #     {{ m.hash }}
        # )
        # if ptrmethod == NULL:
        #     raise RuntimeError("Cannot load method from Godot")

{% if m.arguments | length == 0 %}
# {%     if m.return_type %}
#         # TODO
#         # cdef {{ m.return_type.cython_name }} ret = {{ m.return_type.cython_name }}.__new__()
# {%         set retval_as_arg = "NULL" %}
# {%     else %}
# {%         set retval_as_arg = "NULL" %}
# {%     endif %}

#         with nogil:
#             ptrmethod(
#                 self._ptr,
#                 NULL, # args
#                 # return
#                 0, # args_count
#             )

        return
{% else %}
        raise NotImplemented
{% endif %}

{% endfor %}

{%- endmacro %}
