{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_vector3_new(godot_vector3* r_dest, godot_real p_x, godot_real p_y, godot_real p_z)
godot_string godot_vector3_as_string(godot_vector3* p_self)
godot_int godot_vector3_min_axis(godot_vector3* p_self)
godot_int godot_vector3_max_axis(godot_vector3* p_self)
godot_real godot_vector3_length(godot_vector3* p_self)
godot_real godot_vector3_length_squared(godot_vector3* p_self)
godot_bool godot_vector3_is_normalized(godot_vector3* p_self)
godot_vector3 godot_vector3_normalized(godot_vector3* p_self)
godot_vector3 godot_vector3_inverse(godot_vector3* p_self)
godot_vector3 godot_vector3_snapped(godot_vector3* p_self, godot_vector3* p_by)
godot_vector3 godot_vector3_rotated(godot_vector3* p_self, godot_vector3* p_axis, godot_real p_phi)
godot_vector3 godot_vector3_linear_interpolate(godot_vector3* p_self, godot_vector3* p_b, godot_real p_t)
godot_vector3 godot_vector3_cubic_interpolate(godot_vector3* p_self, godot_vector3* p_b, godot_vector3* p_pre_a, godot_vector3* p_post_b, godot_real p_t)
godot_real godot_vector3_dot(godot_vector3* p_self, godot_vector3* p_b)
godot_vector3 godot_vector3_cross(godot_vector3* p_self, godot_vector3* p_b)
godot_basis godot_vector3_outer(godot_vector3* p_self, godot_vector3* p_b)
godot_basis godot_vector3_to_diagonal_matrix(godot_vector3* p_self)
godot_vector3 godot_vector3_abs(godot_vector3* p_self)
godot_vector3 godot_vector3_floor(godot_vector3* p_self)
godot_vector3 godot_vector3_ceil(godot_vector3* p_self)
godot_real godot_vector3_distance_to(godot_vector3* p_self, godot_vector3* p_b)
godot_real godot_vector3_distance_squared_to(godot_vector3* p_self, godot_vector3* p_b)
godot_real godot_vector3_angle_to(godot_vector3* p_self, godot_vector3* p_to)
godot_vector3 godot_vector3_slide(godot_vector3* p_self, godot_vector3* p_n)
godot_vector3 godot_vector3_bounce(godot_vector3* p_self, godot_vector3* p_n)
godot_vector3 godot_vector3_reflect(godot_vector3* p_self, godot_vector3* p_n)
godot_vector3 godot_vector3_operator_add(godot_vector3* p_self, godot_vector3* p_b)
godot_vector3 godot_vector3_operator_subtract(godot_vector3* p_self, godot_vector3* p_b)
godot_vector3 godot_vector3_operator_multiply_vector(godot_vector3* p_self, godot_vector3* p_b)
godot_vector3 godot_vector3_operator_multiply_scalar(godot_vector3* p_self, godot_real p_b)
godot_vector3 godot_vector3_operator_divide_vector(godot_vector3* p_self, godot_vector3* p_b)
godot_vector3 godot_vector3_operator_divide_scalar(godot_vector3* p_self, godot_real p_b)
godot_bool godot_vector3_operator_equal(godot_vector3* p_self, godot_vector3* p_b)
godot_bool godot_vector3_operator_less(godot_vector3* p_self, godot_vector3* p_b)
godot_vector3 godot_vector3_operator_neg(godot_vector3* p_self)
void godot_vector3_set_axis(godot_vector3* p_self, godot_vector3_axis p_axis, godot_real p_val)
godot_real godot_vector3_get_axis(godot_vector3* p_self, godot_vector3_axis p_axis)
// GDAPI: 1.1
// GDAPI: 1.2
godot_vector3 godot_vector3_move_toward(godot_vector3* p_self, godot_vector3* p_to, godot_real p_delta)
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
from godot._hazmat.gdnative_api_struct cimport godot_vector3_axis

import math


cdef inline Vector3_multiply_vector(Vector3 self, Vector3 b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi10.godot_vector3_operator_multiply_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector3_multiply_scalar(Vector3 self, godot_real b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi10.godot_vector3_operator_multiply_scalar(&self._gd_data, b)
    return ret

cdef inline Vector3_divide_vector(Vector3 self, Vector3 b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi10.godot_vector3_operator_divide_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector3_divide_scalar(Vector3 self, godot_real b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi10.godot_vector3_operator_divide_scalar(&self._gd_data, b)
    return ret

{% endblock -%}


@cython.final
cdef class Vector3:
{% block cdef_attributes %}
    cdef godot_vector3 _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real x=0.0, godot_real y=0.0, godot_real z=0.0):
        gdapi10.godot_vector3_new(&self._gd_data, x, y, z)

    def __repr__(self):
        return f"<Vector3(x={self.x}, y={self.y}, z={self.z})>"

    @property
    def x(self) -> godot_real:
        return gdapi10.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X)

    @x.setter
    def x(self, godot_real val) -> None:
        gdapi10.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X, val)

    @property
    def y(self) -> godot_real:
        return gdapi10.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y)

    @y.setter
    def y(self, godot_real val) -> None:
        gdapi10.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y, val)

    @property
    def z(self) -> godot_real:
        return gdapi10.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z)

    @z.setter
    def z(self, godot_real val) -> None:
        gdapi10.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z, val)

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method("__neg__", "godot_vector3", gdname="operator_neg") | indent }}

    def __pos__(Vector3 self):
        return self

    {{ render_method("__add__", "godot_vector3", args=[
        ("godot_vector3*", "other")
    ], gdname="operator_add") | indent }}
    {{ render_method("__sub__", "godot_vector3", args=[
        ("godot_vector3*", "other")
    ], gdname="operator_subtract") | indent }}

    def __mul__(Vector3 self, val):
        cdef Vector3 _val
        try:
            _val = <Vector3?>val
        except TypeError:
            return Vector3_multiply_scalar(self, val)
        else:
            return Vector3_multiply_vector(self, _val)

    def __truediv__(Vector3 self, val):
        cdef Vector3 _val
        try:
            _val = <Vector3?>val
        except TypeError:
            if val is 0:
                raise ZeroDivisionError()
            return Vector3_divide_scalar(self, val)
        else:
            if _val.x == 0 or _val.y == 0 or _val.z == 0:
                raise ZeroDivisionError()
            return Vector3_divide_vector(self, _val)

    {{ render_method(**gd_functions["min_axis"]) | indent }}
    {{ render_method(**gd_functions["max_axis"]) | indent }}
    {{ render_method(**gd_functions["length"]) | indent }}
    {{ render_method(**gd_functions["length_squared"]) | indent }}
    {{ render_method(**gd_functions["is_normalized"]) | indent }}
    {{ render_method(**gd_functions["normalized"]) | indent }}
    {{ render_method(**gd_functions["inverse"]) | indent }}
    {{ render_method(**gd_functions["snapped"]) | indent }}
    {{ render_method(**gd_functions["rotated"]) | indent }}
    {{ render_method(**gd_functions["linear_interpolate"]) | indent }}
    {{ render_method(**gd_functions["cubic_interpolate"]) | indent }}
    {{ render_method(**gd_functions["move_toward"]) | indent }}
    {{ render_method(**gd_functions["dot"]) | indent }}
    {{ render_method(**gd_functions["cross"]) | indent }}
    {{ render_method(**gd_functions["outer"]) | indent }}
    {{ render_method(**gd_functions["to_diagonal_matrix"]) | indent }}
    {{ render_method(**gd_functions["abs"]) | indent }}
    {{ render_method(**gd_functions["floor"]) | indent }}
    {{ render_method(**gd_functions["ceil"]) | indent }}
    {{ render_method(**gd_functions["distance_to"]) | indent }}
    {{ render_method(**gd_functions["distance_squared_to"]) | indent }}
    {{ render_method(**gd_functions["angle_to"]) | indent }}
    {{ render_method(**gd_functions["slide"]) | indent }}
    {{ render_method(**gd_functions["bounce"]) | indent }}
    {{ render_method(**gd_functions["reflect"]) | indent }}
{% endblock %}

{%- block python_consts %}
    AXIS_X = godot_vector3_axis.GODOT_VECTOR3_AXIS_X
    AXIS_Y = godot_vector3_axis.GODOT_VECTOR3_AXIS_Y
    AXIS_Z = godot_vector3_axis.GODOT_VECTOR3_AXIS_Z

    ZERO = Vector3(0, 0, 0)  # Zero vector.
    ONE = Vector3(1, 1, 1)  # One vector.
    INF = Vector3(math.inf, math.inf, math.inf)  # Infinite vector.
    LEFT = Vector3(-1, 0, 0)  # Left unit vector.
    RIGHT = Vector3(1, 0, 0)  # Right unit vector.
    UP = Vector3(0, 1, 0)  # Up unit vector.
    DOWN = Vector3(0, -1, 0)  # Down unit vector.
    FORWARD = Vector3(0, 0, -1)  # Forward unit vector.
    BACK = Vector3(0, 0, 1)  # Back unit vector.
{% endblock %}
