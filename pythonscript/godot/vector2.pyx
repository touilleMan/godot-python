# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_vector2, godot_real

import math


@cython.final
cdef class Vector2:

    def __init__(self, godot_real x=0.0, godot_real y=0.0):
        gdapi.godot_vector2_new(&self._gd_data, x, y)

    @staticmethod
    cdef inline Vector2 new(godot_real x=0.0, godot_real y=0.0):
        # Call to __new__ bypasses __init__ constructor
        cdef Vector2 ret = Vector2.__new__(Vector2)
        gdapi.godot_vector2_new(&ret._gd_data, x, y)
        return ret

    @staticmethod
    cdef inline Vector2 from_ptr(const godot_vector2 *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Vector2(x={self.x}, y={self.y})>"

    # Operators

    cdef inline Vector2 operator_add(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_add(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector2 operator_subtract(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_subtract(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector2 operator_multiply_vector(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_multiply_vector(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector2 operator_multiply_scalar(self, godot_real b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_multiply_scalar(&self._gd_data, b)
        return ret

    cdef inline Vector2 operator_divide_vector(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_divide_vector(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Vector2 operator_divide_scalar(self, godot_real b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_divide_scalar(&self._gd_data, b)
        return ret

    cdef inline bint operator_equal(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        return gdapi.godot_vector2_operator_equal(&self._gd_data, &b._gd_data)

    cdef inline bint operator_less(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        return gdapi.godot_vector2_operator_less(&self._gd_data, &b._gd_data)

    cdef inline Vector2 operator_neg(self):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_operator_neg(&self._gd_data)
        return ret

    def __lt__(self, Vector2 other not None):
        return Vector2.operator_less(self, other)

    def __eq__(self, other):
        cdef Vector2 _other
        try:
            _other = <Vector2?>other
        except TypeError:
            return False
        return Vector2.operator_equal(self, _other)

    def __ne__(self, other):
        cdef Vector2 _other
        try:
            _other = <Vector2?>other
        except TypeError:
            return True
        return not Vector2.operator_equal(self, _other)

    def __neg__(self):
        return Vector2.operator_neg(self, )

    def __pos__(self):
        return self

    def __add__(self, Vector2 val not None):
        return Vector2.operator_add(self, val)

    def __sub__(self, Vector2 val not None):
        return Vector2.operator_subtract(self, val)

    def __mul__(self, val):
        cdef Vector2 _val

        try:
            _val = <Vector2?>val

        except TypeError:
            return Vector2.operator_multiply_scalar(self, val)

        else:
            return Vector2.operator_multiply_vector(self, _val)

    def __truediv__(self, val):
        cdef Vector2 _val

        try:
            _val = <Vector2?>val

        except TypeError:
            if val is 0:
                raise ZeroDivisionError()

            return Vector2.operator_divide_scalar(self, val)

        else:
            if _val.x == 0 or _val.y == 0:
                raise ZeroDivisionError()

            return Vector2.operator_divide_vector(self, _val)

    # Properties

    cdef inline godot_real get_x(self):
        return gdapi.godot_vector2_get_x(&self._gd_data)

    cdef inline void set_x(self, godot_real val):
        gdapi.godot_vector2_set_x(&self._gd_data, val)

    cdef inline godot_real get_y(self):
        return gdapi.godot_vector2_get_y(&self._gd_data)

    cdef inline void set_y(self, godot_real val):
        gdapi.godot_vector2_set_y(&self._gd_data, val)

    @property
    def x(self):
        return self.get_x()

    @property
    def y(self):
        return self.get_y()

    @x.setter
    def x(self, val):
        self.set_x(val)

    @y.setter
    def y(self, val):
        self.set_y(val)

    @property
    def width(self):
        return self.get_x()

    @property
    def height(self):
        return self.get_y()

    @width.setter
    def width(self, val):
        self.set_x(val)

    @height.setter
    def height(self, val):
        self.set_y(val)

    # Methods

    cpdef inline Vector2 normalized(self):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_normalized(&self._gd_data)
        return ret

    cpdef inline godot_real length(self):
        return gdapi.godot_vector2_length(&self._gd_data)

    cpdef inline godot_real angle(self):
        return gdapi.godot_vector2_angle(&self._gd_data)

    cpdef inline godot_real length_squared(self):
        return gdapi.godot_vector2_length_squared(&self._gd_data)

    cpdef inline bint is_normalized(self):
        return gdapi.godot_vector2_is_normalized(&self._gd_data)

    cpdef inline godot_real distance_to(self, Vector2 to):
        return gdapi.godot_vector2_distance_to(&self._gd_data, &to._gd_data)

    cpdef inline godot_real distance_squared_to(self, Vector2 to):
        return gdapi.godot_vector2_distance_squared_to(&self._gd_data, &to._gd_data)

    cpdef inline godot_real angle_to(self, Vector2 to):
        return gdapi.godot_vector2_angle_to(&self._gd_data, &to._gd_data)

    cpdef inline godot_real angle_to_point(self, Vector2 to):
        return gdapi.godot_vector2_angle_to_point(&self._gd_data, &to._gd_data)

    cpdef inline Vector2 linear_interpolate(self, Vector2 b, godot_real t):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_linear_interpolate(&self._gd_data, &b._gd_data, t)
        return ret

    cpdef inline Vector2 cubic_interpolate(self, Vector2 b, Vector2 pre_a, Vector2 post_b, godot_real t):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_cubic_interpolate(
            &self._gd_data,
            &b._gd_data,
            &pre_a._gd_data,
            &post_b._gd_data,
            t
        )
        return ret

    cpdef inline Vector2 move_toward(self, Vector2 to, godot_real delta):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi12.godot_vector2_move_toward(&self._gd_data, &to._gd_data, delta)
        return ret

    cpdef inline Vector2 rotated(self, godot_real phi):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_rotated(&self._gd_data, phi)
        return ret

    cpdef inline Vector2 tangent(self):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_tangent(&self._gd_data)
        return ret

    cpdef inline Vector2 floor(self):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_floor(&self._gd_data)
        return ret

    cpdef inline Vector2 snapped(self, Vector2 by):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_snapped(&self._gd_data, &by._gd_data)
        return ret

    cpdef inline godot_real aspect(self):
        return gdapi.godot_vector2_aspect(&self._gd_data)

    cpdef inline godot_real dot(self, Vector2 with_):
        return gdapi.godot_vector2_dot(&self._gd_data, &with_._gd_data)

    cpdef inline Vector2 slide(self, Vector2 n):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_slide(&self._gd_data, &n._gd_data)
        return ret

    cpdef inline Vector2 bounce(self, Vector2 n):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_bounce(&self._gd_data, &n._gd_data)
        return ret

    cpdef inline Vector2 reflect(self, Vector2 n):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_reflect(&self._gd_data, &n._gd_data)
        return ret

    cpdef inline Vector2 abs(self):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_abs(&self._gd_data)
        return ret

    cpdef inline Vector2 clamped(self, godot_real length):
        cdef Vector2 ret  = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_vector2_clamped(&self._gd_data, length)
        return ret

    # TODO: gdapi should expose those constants to us

    AXIS_X = 0
    AXIS_Y = 0

    ZERO = Vector2(0, 0)
    ONE = Vector2(1, 1)
    INF = Vector2(math.inf, math.inf)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
