{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}

{{ force_mark_rendered("godot_node_path_new_copy") }} {# NodePath is const, why does this exists in the first place ? #}

@cython.final
cdef class NodePath:
{% block cdef_attributes %}
    cdef godot_node_path _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, from_):
        {{ force_mark_rendered("godot_node_path_new") }}
        cdef godot_string gd_from
        try:
            gdapi10.godot_node_path_new(&self._gd_data, &(<GDString?>from_)._gd_data)
        except TypeError:
            if not isinstance(from_, str):
                raise TypeError("`from_` must be str or GDString")
            pyobj_to_godot_string(from_, &gd_from)
            gdapi10.godot_node_path_new(&self._gd_data, &gd_from)
            gdapi10.godot_string_destroy(&gd_from)

    def __dealloc__(NodePath self):
        {{ force_mark_rendered("godot_node_path_destroy") }}
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.godot_node_path_destroy(&self._gd_data)

    def __repr__(NodePath self):
        return f"<NodePath({self.as_string()})>"

    def __str__(NodePath self):
        return str(self.as_string())

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("destroy") | indent }}
    {{ render_method("as_string") | indent }}
    {{ render_method("is_absolute") | indent }}
    {{ render_method("get_name_count") | indent }}
    {{ render_method("get_name") | indent }}
    {{ render_method("get_subname_count") | indent }}
    {{ render_method("get_subname") | indent }}
    {{ render_method("get_concatenated_subnames") | indent }}
    {{ render_method("is_empty") | indent }}
    {{ render_method("get_as_property_path") | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock %}
