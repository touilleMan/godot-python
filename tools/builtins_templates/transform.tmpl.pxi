{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_transform_new_with_axis_origin(godot_transform* r_dest, godot_vector3* p_x_axis, godot_vector3* p_y_axis, godot_vector3* p_z_axis, godot_vector3* p_origin)
void godot_transform_new(godot_transform* r_dest, godot_basis* p_basis, godot_vector3* p_origin)
godot_basis godot_transform_get_basis(godot_transform* p_self)
void godot_transform_set_basis(godot_transform* p_self, godot_basis* p_v)
godot_vector3 godot_transform_get_origin(godot_transform* p_self)
void godot_transform_set_origin(godot_transform* p_self, godot_vector3* p_v)
godot_string godot_transform_as_string(godot_transform* p_self)
godot_transform godot_transform_inverse(godot_transform* p_self)
godot_transform godot_transform_affine_inverse(godot_transform* p_self)
godot_transform godot_transform_orthonormalized(godot_transform* p_self)
godot_transform godot_transform_rotated(godot_transform* p_self, godot_vector3* p_axis, godot_real p_phi)
godot_transform godot_transform_scaled(godot_transform* p_self, godot_vector3* p_scale)
godot_transform godot_transform_translated(godot_transform* p_self, godot_vector3* p_ofs)
godot_transform godot_transform_looking_at(godot_transform* p_self, godot_vector3* p_target, godot_vector3* p_up)
godot_plane godot_transform_xform_plane(godot_transform* p_self, godot_plane* p_v)
godot_plane godot_transform_xform_inv_plane(godot_transform* p_self, godot_plane* p_v)
void godot_transform_new_identity(godot_transform* r_dest)
godot_bool godot_transform_operator_equal(godot_transform* p_self, godot_transform* p_b)
godot_transform godot_transform_operator_multiply(godot_transform* p_self, godot_transform* p_b)
godot_vector3 godot_transform_xform_vector3(godot_transform* p_self, godot_vector3* p_v)
godot_vector3 godot_transform_xform_inv_vector3(godot_transform* p_self, godot_vector3* p_v)
godot_aabb godot_transform_xform_aabb(godot_transform* p_self, godot_aabb* p_v)
godot_aabb godot_transform_xform_inv_aabb(godot_transform* p_self, godot_aabb* p_v)
// GDAPI: 1.1
void godot_transform_new_with_quat(godot_transform* r_dest, godot_quat* p_quat)
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Transform:
{% block cdef_attributes %}
    cdef godot_transform _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, x_axis=None, y_axis=None, z_axis=None, origin=None):
        if x_axis is None and y_axis is None and z_axis is None and origin is None:
            gdapi10.godot_transform_new_identity(&self._gd_data)
        else:
            gdapi10.godot_transform_new_with_axis_origin(
                &self._gd_data,
                &(<Vector3?>x_axis)._gd_data,
                &(<Vector3?>y_axis)._gd_data,
                &(<Vector3?>z_axis)._gd_data,
                &(<Vector3?>origin)._gd_data,
            )

    @staticmethod
    def from_basis_origin(Basis basis not None, Vector3 origin not None):
        cdef Transform ret = Transform.__new__(Transform)
        gdapi10.godot_transform_new(&ret._gd_data, &basis._gd_data, &origin._gd_data)
        return ret

    @staticmethod
    def from_quat(Quat quat not None):
        cdef Transform ret = Transform.__new__(Transform)
        gdapi11.godot_transform_new_with_quat(&ret._gd_data, &quat._gd_data)
        return ret

    def __repr__(Transform self):
        return f"<Transform({self.as_string()})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("__mul__", "godot_transform", args=[
        ("godot_transform*", "other")
    ], gdname="operator_multiply") | indent }}

    {{ render_property("basis", "godot_basis", "get_basis", "set_basis") | indent }}
    {{ render_property("origin", "godot_vector3", "get_origin", "set_origin") | indent }}

    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["inverse"]) | indent }}
    {{ render_method(**gd_functions["affine_inverse"]) | indent }}
    {{ render_method(**gd_functions["orthonormalized"]) | indent }}
    {{ render_method(**gd_functions["rotated"]) | indent }}
    {{ render_method(**gd_functions["scaled"]) | indent }}
    {{ render_method(**gd_functions["translated"]) | indent }}
    {{ render_method(**gd_functions["looking_at"]) | indent }}
    {{ render_method(**gd_functions["xform_plane"]) | indent }}
    {{ render_method(**gd_functions["xform_inv_plane"]) | indent }}
    {{ render_method(**gd_functions["xform_vector3"]) | indent }}
    {{ render_method(**gd_functions["xform_inv_vector3"]) | indent }}
    {{ render_method(**gd_functions["xform_aabb"]) | indent }}
    {{ render_method(**gd_functions["xform_inv_aabb"]) | indent }}
{% endblock %}

{%- block python_consts %}
    IDENTITY = Transform(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    FLIP_X = Transform(Vector3(-1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    FLIP_Y = Transform(Vector3(1, 0, 0), Vector3(0, -1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    FLIP_Z = Transform(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, -1), Vector3(0, 0, 0))
{% endblock %}
