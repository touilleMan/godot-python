{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_aabb_new(godot_aabb* r_dest, godot_vector3* p_pos, godot_vector3* p_size)
godot_vector3 godot_aabb_get_position(godot_aabb* p_self)
void godot_aabb_set_position(godot_aabb* p_self, godot_vector3* p_v)
godot_vector3 godot_aabb_get_size(godot_aabb* p_self)
void godot_aabb_set_size(godot_aabb* p_self, godot_vector3* p_v)
godot_string godot_aabb_as_string(godot_aabb* p_self)
godot_real godot_aabb_get_area(godot_aabb* p_self)
godot_bool godot_aabb_has_no_area(godot_aabb* p_self)
godot_bool godot_aabb_has_no_surface(godot_aabb* p_self)
godot_bool godot_aabb_intersects(godot_aabb* p_self, godot_aabb* p_with)
godot_bool godot_aabb_encloses(godot_aabb* p_self, godot_aabb* p_with)
godot_aabb godot_aabb_merge(godot_aabb* p_self, godot_aabb* p_with)
godot_aabb godot_aabb_intersection(godot_aabb* p_self, godot_aabb* p_with)
godot_bool godot_aabb_intersects_plane(godot_aabb* p_self, godot_plane* p_plane)
godot_bool godot_aabb_intersects_segment(godot_aabb* p_self, godot_vector3* p_from, godot_vector3* p_to)
godot_bool godot_aabb_has_point(godot_aabb* p_self, godot_vector3* p_point)
godot_vector3 godot_aabb_get_support(godot_aabb* p_self, godot_vector3* p_dir)
godot_vector3 godot_aabb_get_longest_axis(godot_aabb* p_self)
godot_int godot_aabb_get_longest_axis_index(godot_aabb* p_self)
godot_real godot_aabb_get_longest_axis_size(godot_aabb* p_self)
godot_vector3 godot_aabb_get_shortest_axis(godot_aabb* p_self)
godot_int godot_aabb_get_shortest_axis_index(godot_aabb* p_self)
godot_real godot_aabb_get_shortest_axis_size(godot_aabb* p_self)
godot_aabb godot_aabb_expand(godot_aabb* p_self, godot_vector3* p_to_point)
godot_aabb godot_aabb_grow(godot_aabb* p_self, godot_real p_by)
godot_vector3 godot_aabb_get_endpoint(godot_aabb* p_self, godot_int p_idx)
godot_bool godot_aabb_operator_equal(godot_aabb* p_self, godot_aabb* p_b)
// GDAPI: 1.1
// GDAPI: 1.2
""") -%}

{%- block pxd_header -%}
{%- endblock -%}
{%- block pyx_header -%}
{%- endblock -%}

@cython.final
cdef class AABB:
{% block cdef_attributes %}
    cdef godot_aabb _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, Vector3 pos not None=Vector3(), Vector3 size not None=Vector3()):
        gdapi10.godot_aabb_new(&self._gd_data, &pos._gd_data, &size._gd_data)

    def __repr__(self):
        return f"<AABB({self.as_string()})>"

    @property
    def position(AABB self) -> Vector3:
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi10.godot_aabb_get_position(&self._gd_data)
        return ret

    @position.setter
    def position(AABB self, Vector3 val not None) -> None:
        gdapi10.godot_aabb_set_position(&self._gd_data, &val._gd_data)

    @property
    def size(AABB self) -> Vector3:
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi10.godot_aabb_get_size(&self._gd_data)
        return ret

    @size.setter
    def size(AABB self, Vector3 val not None) -> None:
        gdapi10.godot_aabb_set_size(&self._gd_data, &val._gd_data)

    @property
    def end(AABB self) -> Vector3:
        cdef godot_vector3 position = gdapi10.godot_aabb_get_position(&self._gd_data)
        cdef godot_vector3 size = gdapi10.godot_aabb_get_size(&self._gd_data)
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi10.godot_vector3_operator_add(&position, &size)
        return ret

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["get_area"]) | indent }}
    {{ render_method(**gd_functions["has_no_area"]) | indent }}
    {{ render_method(**gd_functions["has_no_surface"]) | indent }}
    {{ render_method(**gd_functions["intersects"]) | indent }}
    {{ render_method(**gd_functions["encloses"]) | indent }}
    {{ render_method(**gd_functions["merge"]) | indent }}
    {{ render_method(**gd_functions["intersection"]) | indent }}
    {{ render_method(**gd_functions["intersects_plane"]) | indent }}
    {{ render_method(**gd_functions["intersects_segment"]) | indent }}
    {{ render_method(**gd_functions["has_point"]) | indent }}
    {{ render_method(**gd_functions["get_support"]) | indent }}
    {{ render_method(**gd_functions["get_longest_axis"]) | indent }}
    {{ render_method(**gd_functions["get_longest_axis_index"]) | indent }}
    {{ render_method(**gd_functions["get_longest_axis_size"]) | indent }}
    {{ render_method(**gd_functions["get_shortest_axis"]) | indent }}
    {{ render_method(**gd_functions["get_shortest_axis_index"]) | indent }}
    {{ render_method(**gd_functions["get_shortest_axis_size"]) | indent }}
    {{ render_method(**gd_functions["expand"]) | indent }}
    {{ render_method(**gd_functions["grow"]) | indent }}
    {{ render_method(**gd_functions["get_endpoint"]) | indent }}
{% endblock %}
