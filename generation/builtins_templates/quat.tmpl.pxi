{#
"""
// GDAPI: 1.0
void godot_quat_new(godot_quat* r_dest, godot_real p_x, godot_real p_y, godot_real p_z, godot_real p_w)
void godot_quat_new_with_axis_angle(godot_quat* r_dest, godot_vector3* p_axis, godot_real p_angle)
godot_real godot_quat_get_x(godot_quat* p_self)
void godot_quat_set_x(godot_quat* p_self, godot_real val)
godot_real godot_quat_get_y(godot_quat* p_self)
void godot_quat_set_y(godot_quat* p_self, godot_real val)
godot_real godot_quat_get_z(godot_quat* p_self)
void godot_quat_set_z(godot_quat* p_self, godot_real val)
godot_real godot_quat_get_w(godot_quat* p_self)
void godot_quat_set_w(godot_quat* p_self, godot_real val)
godot_string godot_quat_as_string(godot_quat* p_self)
godot_real godot_quat_length(godot_quat* p_self)
godot_real godot_quat_length_squared(godot_quat* p_self)
godot_quat godot_quat_normalized(godot_quat* p_self)
godot_bool godot_quat_is_normalized(godot_quat* p_self)
godot_quat godot_quat_inverse(godot_quat* p_self)
godot_real godot_quat_dot(godot_quat* p_self, godot_quat* p_b)
godot_vector3 godot_quat_xform(godot_quat* p_self, godot_vector3* p_v)
godot_quat godot_quat_slerp(godot_quat* p_self, godot_quat* p_b, godot_real p_t)
godot_quat godot_quat_slerpni(godot_quat* p_self, godot_quat* p_b, godot_real p_t)
godot_quat godot_quat_cubic_slerp(godot_quat* p_self, godot_quat* p_b, godot_quat* p_pre_a, godot_quat* p_post_b, godot_real p_t)
godot_quat godot_quat_operator_multiply(godot_quat* p_self, godot_real p_b)
godot_quat godot_quat_operator_add(godot_quat* p_self, godot_quat* p_b)
godot_quat godot_quat_operator_subtract(godot_quat* p_self, godot_quat* p_b)
godot_quat godot_quat_operator_divide(godot_quat* p_self, godot_real p_b)
godot_bool godot_quat_operator_equal(godot_quat* p_self, godot_quat* p_b)
godot_quat godot_quat_operator_neg(godot_quat* p_self)
// GDAPI: 1.1
void godot_quat_new_with_basis(godot_quat* r_dest, godot_basis* p_basis)
void godot_quat_new_with_euler(godot_quat* r_dest, godot_vector3* p_euler)
void godot_quat_set_axis_angle(godot_quat* p_self, godot_vector3* p_axis, godot_real p_angle)
// GDAPI: 1.2
"""
#}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Quat:
{% block cdef_attributes %}
    cdef godot_quat _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, x=0, y=0, z=0, w=0):
        gdapi10.godot_quat_new(&self._gd_data, x, y, z, w)

    @staticmethod
    def from_axis_angle(Vector3 axis not None, godot_real angle):
        # Call to __new__ bypasses __init__ constructor
        cdef Quat ret = Quat.__new__(Quat)
        gdapi10.godot_quat_new_with_axis_angle(&ret._gd_data, &axis._gd_data, angle)
        return ret

    @staticmethod
    def from_basis(Basis basis not None):
        # Call to __new__ bypasses __init__ constructor
        cdef Quat ret = Quat.__new__(Quat)
        gdapi11.godot_quat_new_with_basis(&ret._gd_data, &basis._gd_data)
        return ret

    @staticmethod
    def from_euler(Vector3 euler not None):
        # Call to __new__ bypasses __init__ constructor
        cdef Quat ret = Quat.__new__(Quat)
        gdapi11.godot_quat_new_with_euler(&ret._gd_data, &euler._gd_data)
        return ret

    def __repr__(Quat self):
        return f"<Quat(x={self.x}, y={self.y}, z={self.z}, w={self.w})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}

    {{ render_method("operator_neg", py_name="__neg__") | indent }}

    def __pos__(Quat self):
        return self

    {{ render_method("operator_add", py_name="__add__") | indent }}
    {{ render_method("operator_subtract", py_name="__sub__") | indent }}
    {{ render_method("operator_multiply", py_name="__mul__") | indent }}

    def __truediv__(Quat self, godot_real val):
        if val == 0:
            raise ZeroDivisionError
        cdef Quat ret  = Quat.__new__(Quat)
        ret._gd_data = gdapi10.godot_quat_operator_divide(&self._gd_data, val)
        return ret

    {{ render_property("x", getter="get_x", setter="set_x") | indent }}
    {{ render_property("y", getter="get_y", setter="set_y") | indent }}
    {{ render_property("z", getter="get_z", setter="set_z") | indent }}
    {{ render_property("w", getter="get_w", setter="set_w") | indent }}

    {{ render_method("as_string") | indent }}
    {{ render_method("length") | indent }}
    {{ render_method("length_squared") | indent }}
    {{ render_method("normalized") | indent }}
    {{ render_method("is_normalized") | indent }}
    {{ render_method("inverse") | indent }}
    {{ render_method("dot") | indent }}
    {{ render_method("xform") | indent }}
    {{ render_method("slerp") | indent }}
    {{ render_method("slerpni") | indent }}
    {{ render_method("cubic_slerp") | indent }}
    {{ render_method("set_axis_angle") | indent }}
{% endblock %}

{%- block python_consts %}
    IDENTITY = Quat(0, 0, 0, 1)
{% endblock %}
