# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_vector3, godot_vector3_axis, godot_int, godot_real
from godot.basis cimport Basis

import math


@cython.final
cdef class Vector3:

    def __init__(self, godot_real x=0.0, godot_real y=0.0, godot_real z=0.0):
        gdapi.godot_vector3_new(&self._gd_data, x, y, z)

    @staticmethod
    cdef Vector3 new(godot_real x=0.0, godot_real y=0.0, godot_real z=0.0):
        # Call to __new__ bypasses __init__ constructor
        cdef Vector3 ret = Vector3.__new__(Vector3)
        gdapi.godot_vector3_new(&ret._gd_data, x, y, z)
        return ret

    @staticmethod
    cdef Vector3 from_ptr(const godot_vector3 *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Vector3(x={self.x}, y={self.y}, z={self.z})>"

    # Operators

    cdef inline Vector3 operator_add(self, Vector3 b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_add(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector3 operator_subtract(self, Vector3 b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_subtract(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector3 operator_multiply_vector(self, Vector3 b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_multiply_vector(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector3 operator_multiply_scalar(self, godot_real b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_multiply_scalar(&self._gd_data, b)
        return ret

    cdef inline Vector3 operator_divide_vector(self, Vector3 b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_divide_vector(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector3 operator_divide_scalar(self, godot_real b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_divide_scalar(&self._gd_data, b)
        return ret

    cdef inline bint operator_equal(self, Vector3 b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        return gdapi.godot_vector3_operator_equal(&self._gd_data, &b._gd_data)

    cdef inline bint operator_less(self, Vector3 b):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        return gdapi.godot_vector3_operator_less(&self._gd_data, &b._gd_data)

    cdef inline Vector3 operator_neg(self):
        cdef Vector3 ret  = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_operator_neg(&self._gd_data)
        return ret

    def __lt__(self, other):
        cdef Vector3 _other = <Vector3?>other
        return self.operator_less(_other)

    def __eq__(self, other):
        cdef Vector3 _other = <Vector3?>other
        return self.operator_equal(_other)

    def __ne__(self, other):
        cdef Vector3 _other = <Vector3?>other
        return not self.operator_equal(_other)

    def __neg__(self):
        return self.operator_neg()

    def __pos__(self):
        return self

    def __add__(self, val):
        cdef Vector3 _val = <Vector3?>val
        return self.operator_add(_val)

    def __sub__(self, val):
        cdef Vector3 _val = <Vector3?>val
        return self.operator_subtract(_val)

    def __mul__(self, val):
        cdef Vector3 _val

        try:
            _val = <Vector3?>val

        except TypeError:
            return self.operator_multiply_scalar(val)

        else:
            return self.operator_multiply_vector(_val)

    def __truediv__(self, val):
        cdef Vector3 _val

        try:
            _val = <Vector3?>val

        except TypeError:
            if val is 0:
                raise ZeroDivisionError()

            return self.operator_divide_scalar(val)

        else:
            if _val.x == 0 or _val.y == 0:
                raise ZeroDivisionError()

            return self.operator_divide_vector(_val)

    # Properties

    cdef inline godot_real get_x(self):
        return gdapi.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X)

    cdef inline void set_x(self, godot_real val):
        gdapi.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_X, val)

    @property
    def x(self):
        return self.get_x()

    @x.setter
    def x(self, val):
        self.set_x(val)

    cdef inline godot_real get_y(self):
        return gdapi.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y)

    cdef inline void set_y(self, godot_real val):
        gdapi.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Y, val)

    @property
    def y(self):
        return self.get_y()

    @y.setter
    def y(self, val):
        self.set_y(val)

    cdef inline godot_real get_z(self):
        return gdapi.godot_vector3_get_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z)

    cdef inline void set_z(self, godot_real val):
        gdapi.godot_vector3_set_axis(&self._gd_data, godot_vector3_axis.GODOT_VECTOR3_AXIS_Z, val)

    @property
    def z(self):
        return self.get_z()

    @z.setter
    def z(self, val):
        self.set_z(val)

    # Methods

    cpdef godot_int min_axis(self):
        return gdapi.godot_vector3_min_axis(&self._gd_data)

    cpdef godot_int max_axis(self):
        return gdapi.godot_vector3_max_axis(&self._gd_data)

    cpdef godot_real length(self):
        return gdapi.godot_vector3_length(&self._gd_data)

    cpdef godot_real length_squared(self):
        return gdapi.godot_vector3_length_squared(&self._gd_data)

    cpdef bint is_normalized(self):
        return gdapi.godot_vector3_is_normalized(&self._gd_data)

    cpdef Vector3 normalized(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_normalized(&self._gd_data)
        return ret

    cpdef Vector3 inverse(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_inverse(&self._gd_data)
        return ret

    cpdef Vector3 snapped(self, Vector3 by):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_snapped(&self._gd_data, &by._gd_data)
        return ret

    cpdef Vector3 rotated(self, Vector3 axis, godot_real phi):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_rotated(&self._gd_data, &axis._gd_data, phi)
        return ret

    cpdef Vector3 linear_interpolate(self, Vector3 b, godot_real t):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_linear_interpolate(&self._gd_data, &b._gd_data, t)
        return ret

    cpdef Vector3 cubic_interpolate(self, Vector3 b, Vector3 pre_a, Vector3 post_b, godot_real t):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_cubic_interpolate(&self._gd_data, &b._gd_data, &pre_a._gd_data, &post_b._gd_data, t)
        return ret

    cpdef Vector3 move_toward(self, Vector3 to, godot_real delta):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi12.godot_vector3_move_toward(&self._gd_data, &to._gd_data, delta)
        return ret

    cpdef godot_real dot(self, Vector3 b):
        return gdapi.godot_vector3_dot(&self._gd_data, &b._gd_data)

    cpdef Vector3 cross(self, Vector3 b):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_cross(&self._gd_data, &b._gd_data)
        return ret

    cpdef Basis outer(self, Vector3 b):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_vector3_outer(&self._gd_data, &b._gd_data)
        return ret

    cpdef Basis to_diagonal_matrix(self):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_vector3_to_diagonal_matrix(&self._gd_data)
        return ret

    cpdef Vector3 abs(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_abs(&self._gd_data)
        return ret

    cpdef Vector3 floor(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_floor(&self._gd_data)
        return ret

    cpdef Vector3 ceil(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_ceil(&self._gd_data)
        return ret

    cpdef godot_real distance_to(self, Vector3 b):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        return gdapi.godot_vector3_distance_to(&self._gd_data, &b._gd_data)

    cpdef godot_real distance_squared_to(self, Vector3 b):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        return gdapi.godot_vector3_distance_squared_to(&self._gd_data, &b._gd_data)

    cpdef godot_real angle_to(self, Vector3 to):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        return gdapi.godot_vector3_angle_to(&self._gd_data, &to._gd_data)

    cpdef Vector3 slide(self, Vector3 n):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_slide(&self._gd_data, &n._gd_data)
        return ret

    cpdef Vector3 bounce(self, Vector3 n):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_bounce(&self._gd_data, &n._gd_data)
        return ret

    cpdef Vector3 reflect(self, Vector3 n):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_vector3_reflect(&self._gd_data, &n._gd_data)
        return ret

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
