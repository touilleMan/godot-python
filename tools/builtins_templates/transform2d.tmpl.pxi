{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_transform2d_new(godot_transform2d* r_dest, godot_real p_rot, godot_vector2* p_pos)
void godot_transform2d_new_axis_origin(godot_transform2d* r_dest, godot_vector2* p_x_axis, godot_vector2* p_y_axis, godot_vector2* p_origin)
godot_string godot_transform2d_as_string(godot_transform2d* p_self)
godot_transform2d godot_transform2d_inverse(godot_transform2d* p_self)
godot_transform2d godot_transform2d_affine_inverse(godot_transform2d* p_self)
godot_real godot_transform2d_get_rotation(godot_transform2d* p_self)
godot_vector2 godot_transform2d_get_origin(godot_transform2d* p_self)
godot_vector2 godot_transform2d_get_scale(godot_transform2d* p_self)
godot_transform2d godot_transform2d_orthonormalized(godot_transform2d* p_self)
godot_transform2d godot_transform2d_rotated(godot_transform2d* p_self, godot_real p_phi)
godot_transform2d godot_transform2d_scaled(godot_transform2d* p_self, godot_vector2* p_scale)
godot_transform2d godot_transform2d_translated(godot_transform2d* p_self, godot_vector2* p_offset)
godot_vector2 godot_transform2d_xform_vector2(godot_transform2d* p_self, godot_vector2* p_v)
godot_vector2 godot_transform2d_xform_inv_vector2(godot_transform2d* p_self, godot_vector2* p_v)
godot_vector2 godot_transform2d_basis_xform_vector2(godot_transform2d* p_self, godot_vector2* p_v)
godot_vector2 godot_transform2d_basis_xform_inv_vector2(godot_transform2d* p_self, godot_vector2* p_v)
godot_transform2d godot_transform2d_interpolate_with(godot_transform2d* p_self, godot_transform2d* p_m, godot_real p_c)
godot_bool godot_transform2d_operator_equal(godot_transform2d* p_self, godot_transform2d* p_b)
godot_transform2d godot_transform2d_operator_multiply(godot_transform2d* p_self, godot_transform2d* p_b)
void godot_transform2d_new_identity(godot_transform2d* r_dest)
godot_rect2 godot_transform2d_xform_rect2(godot_transform2d* p_self, godot_rect2* p_v)
godot_rect2 godot_transform2d_xform_inv_rect2(godot_transform2d* p_self, godot_rect2* p_v)
// GDAPI: 1.1
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Transform2D:
{% block cdef_attributes %}
    cdef godot_transform2d _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, x_axis=None, y_axis=None, origin=None):
        if x_axis is None and y_axis is None and origin is None:
            gdapi10.godot_transform2d_new_identity(&self._gd_data)
        else:
            gdapi10.godot_transform2d_new_axis_origin(
                &self._gd_data,
                &(<Vector2?>x_axis)._gd_data,
                &(<Vector2?>y_axis)._gd_data,
                &(<Vector2?>origin)._gd_data,
            )

    @staticmethod
    def from_rot_pos(godot_real rot, Vector2 pos not None):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        gdapi10.godot_transform2d_new(&ret._gd_data, rot, &pos._gd_data)
        return ret

    def __repr__(Transform2D self):
        return f"<Transform2D({self.as_string()})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("__mul__", "godot_transform2d", args=[
        ("godot_transform2d*", "other")
    ], gdname="operator_multiply") | indent }}

    # TODO: add axis properties once gdnative is updated
    {{ render_property("origin", "godot_vector2", "get_origin") | indent }}

    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["inverse"]) | indent }}
    {{ render_method(**gd_functions["affine_inverse"]) | indent }}
    {{ render_method(**gd_functions["get_rotation"]) | indent }}
    {{ render_method(**gd_functions["get_scale"]) | indent }}
    {{ render_method(**gd_functions["orthonormalized"]) | indent }}
    {{ render_method(**gd_functions["rotated"]) | indent }}
    {{ render_method(**gd_functions["scaled"]) | indent }}
    {{ render_method(**gd_functions["translated"]) | indent }}

    def xform(Transform2D self, v):
        cdef Vector2 ret_v2
        cdef Rect2 ret_r2
        try:
            ret_v2 = Vector2.__new__(Vector2)
            ret_v2._gd_data = gdapi10.godot_transform2d_xform_vector2(&self._gd_data, &(<Vector2?>v)._gd_data)
            return ret_v2
        except TypeError:
            pass
        try:
            ret_r2 = Rect2.__new__(Rect2)
            ret_r2._gd_data = gdapi10.godot_transform2d_xform_rect2(&self._gd_data, &(<Rect2?>v)._gd_data)
            return ret_r2
        except TypeError:
            raise TypeError("`v` must be Vector2 or Rect2")

    def xform_inv(Transform2D self, v):
        cdef Vector2 ret_v2
        cdef Rect2 ret_r2
        try:
            ret_v2 = Vector2.__new__(Vector2)
            ret_v2._gd_data = gdapi10.godot_transform2d_xform_inv_vector2(&self._gd_data, &(<Vector2?>v)._gd_data)
            return ret_v2
        except TypeError:
            pass
        try:
            ret_r2 = Rect2.__new__(Rect2)
            ret_r2._gd_data = gdapi10.godot_transform2d_xform_inv_rect2(&self._gd_data, &(<Rect2?>v)._gd_data)
            return ret_r2
        except TypeError:
            raise TypeError("`v` must be Vector2 or Rect2")

{% set basis_xform_specs = gd_functions["basis_xform_vector2"] | merge(pyname="basis_xform") %}
    {{ render_method(**basis_xform_specs) | indent }}
{% set basis_xform_inv_specs = gd_functions["basis_xform_inv_vector2"] | merge(pyname="basis_xform_inv") %}
    {{ render_method(**basis_xform_inv_specs) | indent }}
    {{ render_method(**gd_functions["interpolate_with"]) | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock %}
