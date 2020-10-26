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
            {{ force_mark_rendered("godot_transform_new_identity") }}
            gdapi10.godot_transform_new_identity(&self._gd_data)
        else:
            {{ force_mark_rendered("godot_transform_new_with_axis_origin") }}
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
        {{ force_mark_rendered("godot_transform_new") }}
        gdapi10.godot_transform_new(&ret._gd_data, &basis._gd_data, &origin._gd_data)
        return ret

    @staticmethod
    def from_quat(Quat quat not None):
        cdef Transform ret = Transform.__new__(Transform)
        {{ force_mark_rendered("godot_transform_new_with_quat") }}
        gdapi11.godot_transform_new_with_quat(&ret._gd_data, &quat._gd_data)
        return ret

    def __repr__(Transform self):
        return f"<Transform({self.as_string()})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("operator_multiply", py_name="__mul__") | indent }}

    {{ render_property("basis", getter="get_basis", setter="set_basis") | indent }}
    {{ render_property("origin", getter="get_origin", setter="set_origin") | indent }}

    {{ render_method("as_string") | indent }}
    {{ render_method("inverse") | indent }}
    {{ render_method("affine_inverse") | indent }}
    {{ render_method("orthonormalized") | indent }}
    {{ render_method("rotated") | indent }}
    {{ render_method("scaled") | indent }}
    {{ render_method("translated") | indent }}
    {{ render_method("looking_at") | indent }}
    {{ render_method("xform_plane") | indent }}
    {{ render_method("xform_inv_plane") | indent }}
    {{ render_method("xform_vector3") | indent }}
    {{ render_method("xform_inv_vector3") | indent }}
    {{ render_method("xform_aabb") | indent }}
    {{ render_method("xform_inv_aabb") | indent }}
{% endblock %}

{%- block python_consts %}
    IDENTITY = Transform(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    FLIP_X = Transform(Vector3(-1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    FLIP_Y = Transform(Vector3(1, 0, 0), Vector3(0, -1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))
    FLIP_Z = Transform(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, -1), Vector3(0, 0, 0))
{% endblock %}
