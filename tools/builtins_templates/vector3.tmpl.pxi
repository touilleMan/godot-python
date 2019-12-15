from godot.bindings cimport Resource
{% set py_type = "Vector3" %}

{% block pxd_header %}
{% endblock %}
{% block pyx_header %}
from godot._hazmat.gdnative_api_struct cimport godot_vector3_axis

import math


cdef inline Vector3_multiply_vector(Vector3 self, Vector3 b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi.godot_vector3_operator_multiply_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector3_multiply_scalar(Vector3 self, godot_real b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi.godot_vector3_operator_multiply_scalar(&self._gd_data, b)
    return ret

cdef inline Vector3_divide_vector(Vector3 self, Vector3 b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi.godot_vector3_operator_divide_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector3_divide_scalar(Vector3 self, godot_real b):
    cdef Vector3 ret  = Vector3.__new__(Vector3)
    ret._gd_data = gdapi.godot_vector3_operator_divide_scalar(&self._gd_data, b)
    return ret

{% endblock %}


@cython.final
cdef class Vector3:
{% block cdef_attributes %}
    cdef godot_rid _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real x=0.0, godot_real y=0.0, godot_real z=0.0):
        gdapi.godot_vector3_new(&self._gd_data, x, y, z)

    def __repr__(self):
        return f"<Vector3(x={self.x}, y={self.y}, z={self.z})>"

    @property
    def x(self):
        return gdapi.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X)

    @x.setter
    def x(self, godot_real val):
        gdapi.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X, val)

    @property
    def y(self):
        return gdapi.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y)

    @y.setter
    def y(self, godot_real val):
        gdapi.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y, val)

    @property
    def z(self):
        return gdapi.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z)

    @z.setter
    def z(self, godot_real val):
        gdapi.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z, val)

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method("__neg__", "godot_vector3", gdname="operator_neg") | indent }}

    def __pos__(self):
        return self

    {{ render_method("__add__", "godot_vector3", args=[
        ("godot_vector3", "other")
    ], gdname="operator_add") | indent }}
    {{ render_method("__sub__", "godot_vector3", args=[
        ("godot_vector3", "other")
    ], gdname="operator_subtract") | indent }}


    def __mul__(self, val):
        cdef Vector3 _val
        try:
            _val = <Vector3?>val
        except TypeError:
            return Vector3_multiply_scalar(self, val)
        else:
            return Vector3_multiply_vector(self, _val)

    def __truediv__(self, val):
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

    {{ render_method("min_axis", "godot_int") | indent }}
    {{ render_method("max_axis", "godot_int") | indent }}
    {{ render_method("length", "godot_real") | indent }}
    {{ render_method("length_squared", "godot_real") | indent }}
    {{ render_method("is_normalized", "godot_bool") | indent }}
    {{ render_method("normalized", "godot_vector3") | indent }}
    {{ render_method("inverse", "godot_vector3") | indent }}
    {{ render_method("snapped", "godot_vector3", args=[("godot_vector3", "by")]) | indent }}
    {{ render_method("rotated", "godot_vector3", args=[
        ("godot_vector3", "axis"),
        ("godot_real", "phi")
    ]) | indent }}
    {{ render_method("linear_interpolate", "godot_vector3", args=[
        ("godot_vector3", "b"),
        ("godot_real", "t")
    ]) | indent }}
    {{ render_method("cubic_interpolate", "godot_vector3", args=[
        ("godot_vector3", "b"),
        ("godot_vector3", "pre_a"),
        ("godot_vector3", "post_b"),
        ("godot_real", "t")
    ]) | indent }}
    {{ render_method("move_toward", "godot_vector3", args=[
        ("godot_vector3", "to"),
        ("godot_real", "delta")
    ]) | indent }}
    {{ render_method("dot", "godot_real", args=[("godot_vector3", "b")]) | indent }}
    {{ render_method("cross", "godot_vector3", args=[("godot_vector3", "b")]) | indent }}
    {{ render_method("outer", "godot_basis", args=[("godot_vector3", "b")]) | indent }}
    {{ render_method("to_diagonal_matrix", "godot_basis") | indent }}
    {{ render_method("abs", "godot_vector3") | indent }}
    {{ render_method("floor", "godot_vector3") | indent }}
    {{ render_method("ceil", "godot_vector3") | indent }}
    {{ render_method("distance_to", "godot_real", args=[("godot_vector3", "b")]) | indent }}
    {{ render_method("distance_squared_to", "godot_real", args=[("godot_vector3", "b")]) | indent }}
    {{ render_method("angle_to", "godot_real", args=[("godot_vector3", "to")]) | indent }}
    {{ render_method("slide", "godot_vector3", args=[("godot_vector3", "n")]) | indent }}
    {{ render_method("bounce", "godot_vector3", args=[("godot_vector3", "n")]) | indent }}
    {{ render_method("reflect", "godot_vector3", args=[("godot_vector3", "n")]) | indent }}
{% endblock %}

{% block python_consts %}
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
