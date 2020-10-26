{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
from godot._hazmat.gdnative_api_struct cimport godot_vector3_axis

import math
from enum import IntEnum


cdef inline Vector3_multiply_vector(Vector3 self, Vector3 b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    {{ force_mark_rendered("godot_vector3_operator_multiply_vector") }}
    ret._gd_data = gdapi10.godot_vector3_operator_multiply_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector3_multiply_scalar(Vector3 self, godot_real b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    {{ force_mark_rendered("godot_vector3_operator_multiply_scalar") }}
    ret._gd_data = gdapi10.godot_vector3_operator_multiply_scalar(&self._gd_data, b)
    return ret

cdef inline Vector3_divide_vector(Vector3 self, Vector3 b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    {{ force_mark_rendered("godot_vector3_operator_divide_vector") }}
    ret._gd_data = gdapi10.godot_vector3_operator_divide_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector3_divide_scalar(Vector3 self, godot_real b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    {{ force_mark_rendered("godot_vector3_operator_divide_scalar") }}
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
        {{ force_mark_rendered("godot_vector3_new") }}
        gdapi10.godot_vector3_new(&self._gd_data, x, y, z)

    def __repr__(self):
        return f"<Vector3(x={self.x}, y={self.y}, z={self.z})>"

    @property
    def x(self) -> godot_real:
        {{ force_mark_rendered("godot_vector3_get_axis") }}
        return gdapi10.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X)

    @x.setter
    def x(self, godot_real val) -> None:
        {{ force_mark_rendered("godot_vector3_set_axis") }}
        gdapi10.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X, val)

    @property
    def y(self) -> godot_real:
        {{ force_mark_rendered("godot_vector3_get_axis") }}
        return gdapi10.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y)

    @y.setter
    def y(self, godot_real val) -> None:
        {{ force_mark_rendered("godot_vector3_set_axis") }}
        gdapi10.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y, val)

    @property
    def z(self) -> godot_real:
        {{ force_mark_rendered("godot_vector3_get_axis") }}
        return gdapi10.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z)

    @z.setter
    def z(self, godot_real val) -> None:
        {{ force_mark_rendered("godot_vector3_set_axis") }}
        gdapi10.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z, val)

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method("operator_neg", py_name="__neg__") | indent }}

    def __pos__(Vector3 self):
        return self

    {{ render_method("operator_add", py_name="__add__") | indent }}
    {{ render_method("operator_subtract", py_name="__sub__") | indent }}

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

    {{ render_method("as_string") | indent }}
    {{ render_method("min_axis") | indent }}
    {{ render_method("max_axis") | indent }}
    {{ render_method("length") | indent }}
    {{ render_method("length_squared") | indent }}
    {{ render_method("is_normalized") | indent }}
    {{ render_method("normalized") | indent }}
    {{ render_method("inverse") | indent }}
    {{ render_method("snapped") | indent }}
    {{ render_method("rotated") | indent }}
    {{ render_method("linear_interpolate") | indent }}
    {{ render_method("cubic_interpolate") | indent }}
    {{ render_method("move_toward") | indent }}
    {{ render_method("direction_to") | indent }}
    {{ render_method("dot") | indent }}
    {{ render_method("cross") | indent }}
    {{ render_method("outer") | indent }}
    {{ render_method("to_diagonal_matrix") | indent }}
    {{ render_method("abs") | indent }}
    {{ render_method("floor") | indent }}
    {{ render_method("ceil") | indent }}
    {{ render_method("distance_to") | indent }}
    {{ render_method("distance_squared_to") | indent }}
    {{ render_method("angle_to") | indent }}
    {{ render_method("slide") | indent }}
    {{ render_method("bounce") | indent }}
    {{ render_method("reflect") | indent }}
{% endblock %}

{%- block python_consts %}
    AXIS = IntEnum("AXIS", {
        "X": godot_vector3_axis.GODOT_VECTOR3_AXIS_X,
        "Y": godot_vector3_axis.GODOT_VECTOR3_AXIS_Y,
        "Z": godot_vector3_axis.GODOT_VECTOR3_AXIS_Z,
    })

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
