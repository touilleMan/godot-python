{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_node_path_new(godot_node_path* r_dest, godot_string* p_from)
void godot_node_path_new_copy(godot_node_path* r_dest, godot_node_path* p_src)
void godot_node_path_destroy(godot_node_path* p_self)
godot_string godot_node_path_as_string(godot_node_path* p_self)
godot_bool godot_node_path_is_absolute(godot_node_path* p_self)
godot_int godot_node_path_get_name_count(godot_node_path* p_self)
godot_string godot_node_path_get_name(godot_node_path* p_self, godot_int p_idx)
godot_int godot_node_path_get_subname_count(godot_node_path* p_self)
godot_string godot_node_path_get_subname(godot_node_path* p_self, godot_int p_idx)
godot_string godot_node_path_get_concatenated_subnames(godot_node_path* p_self)
godot_bool godot_node_path_is_empty(godot_node_path* p_self)
godot_bool godot_node_path_operator_equal(godot_node_path* p_self, godot_node_path* p_b)
// GDAPI: 1.1
godot_node_path godot_node_path_get_as_property_path(godot_node_path* p_self)
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class NodePath:
{% block cdef_attributes %}
    cdef godot_node_path _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, from_):
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
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.godot_node_path_destroy(&self._gd_data)

    def __repr__(NodePath self):
        return f"<NodePath({self.as_string()})>"

    def __str__(NodePath self):
        return str(self.as_string())

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method(**gd_functions["destroy"]) | indent }}
    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["is_absolute"]) | indent }}
    {{ render_method(**gd_functions["get_name_count"]) | indent }}
    {{ render_method(**gd_functions["get_name"]) | indent }}
    {{ render_method(**gd_functions["get_subname_count"]) | indent }}
    {{ render_method(**gd_functions["get_subname"]) | indent }}
    {{ render_method(**gd_functions["get_concatenated_subnames"]) | indent }}
    {{ render_method(**gd_functions["is_empty"]) | indent }}
    {{ render_method(**gd_functions["get_as_property_path"]) | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock %}
