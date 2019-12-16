{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_rect2_new_with_position_and_size(godot_rect2* r_dest, godot_vector2* p_pos, godot_vector2* p_size)
void godot_rect2_new(godot_rect2* r_dest, godot_real p_x, godot_real p_y, godot_real p_width, godot_real p_height)
godot_string godot_rect2_as_string(godot_rect2* p_self)
godot_real godot_rect2_get_area(godot_rect2* p_self)
godot_bool godot_rect2_intersects(godot_rect2* p_self, godot_rect2* p_b)
godot_bool godot_rect2_encloses(godot_rect2* p_self, godot_rect2* p_b)
godot_bool godot_rect2_has_no_area(godot_rect2* p_self)
godot_rect2 godot_rect2_clip(godot_rect2* p_self, godot_rect2* p_b)
godot_rect2 godot_rect2_merge(godot_rect2* p_self, godot_rect2* p_b)
godot_bool godot_rect2_has_point(godot_rect2* p_self, godot_vector2* p_point)
godot_rect2 godot_rect2_grow(godot_rect2* p_self, godot_real p_by)
godot_rect2 godot_rect2_expand(godot_rect2* p_self, godot_vector2* p_to)
godot_bool godot_rect2_operator_equal(godot_rect2* p_self, godot_rect2* p_b)
godot_vector2 godot_rect2_get_position(godot_rect2* p_self)
godot_vector2 godot_rect2_get_size(godot_rect2* p_self)
void godot_rect2_set_position(godot_rect2* p_self, godot_vector2* p_pos)
void godot_rect2_set_size(godot_rect2* p_self, godot_vector2* p_size)
// GDAPI: 1.1
godot_rect2 godot_rect2_grow_individual(godot_rect2* p_self, godot_real p_left, godot_real p_top, godot_real p_right, godot_real p_bottom)
godot_rect2 godot_rect2_grow_margin(godot_rect2* p_self, godot_int p_margin, godot_real p_by)
godot_rect2 godot_rect2_abs(godot_rect2* p_self)
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Rect2:
{% block cdef_attributes %}
    cdef godot_rect2 _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real x=0.0, godot_real y=0.0, godot_real width=0.0, godot_real height=0.0):
        gdapi10.godot_rect2_new(&self._gd_data, x, y, width, height)

    @staticmethod
    def from_pos_size(Vector2 position not None, Vector2 size not None):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        gdapi10.godot_rect2_new_with_position_and_size(&ret._gd_data, &position._gd_data, &size._gd_data)
        return ret

    def __repr__(Rect2 self):
        return f"<Rect2({self.as_string()})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_property("size", "godot_vector2", "get_size", "set_size") | indent }}
    {{ render_property("position", "godot_vector2", "get_position", "set_position") | indent }}

    @property
    def end(Rect2 self) -> Vector2:
        cdef godot_vector2 position = gdapi10.godot_rect2_get_position(&self._gd_data)
        cdef godot_vector2 size = gdapi10.godot_rect2_get_size(&self._gd_data)
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi10.godot_vector2_operator_add(&position, &size)
        return ret

    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["get_area"]) | indent }}
    {{ render_method(**gd_functions["intersects"]) | indent }}
    {{ render_method(**gd_functions["encloses"]) | indent }}
    {{ render_method(**gd_functions["has_no_area"]) | indent }}
    {{ render_method(**gd_functions["clip"]) | indent }}
    {{ render_method(**gd_functions["merge"]) | indent }}
    {{ render_method(**gd_functions["has_point"]) | indent }}
    {{ render_method(**gd_functions["grow"]) | indent }}
    {{ render_method(**gd_functions["grow_individual"]) | indent }}
    {{ render_method(**gd_functions["grow_margin"]) | indent }}
    {{ render_method(**gd_functions["abs"]) | indent }}
    {{ render_method(**gd_functions["expand"]) | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock %}
