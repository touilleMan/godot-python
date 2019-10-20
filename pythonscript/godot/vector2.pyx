# cython: language_level=3

cimport cython

from godot_hazmat cimport gdapi, gdapi12
from godot_hazmat.gdnative_api_struct cimport godot_vector2, godot_real


@cython.final
cdef class Vector2:

    @staticmethod
    cdef Vector2 new(godot_real x=0.0, godot_real y=0.0):
        cdef Vector2 ret = Vector2.__new__()
        gdapi.godot_vector2_new(ret._c_vector2_ptr(), x, y)
        return ret

    def __cinit__(self, x=0.0, y=0.0):
        gdapi.godot_vector2_new(self._c_vector2_ptr(), x, y)

    cdef inline godot_vector2 *_c_vector2_ptr(Vector2 self):
        return &(<Vector2>self)._c_vector2

    def __repr__(self):
        return f"<Vector2(x={self.x}, y={self.y})>"

    # Operators

    cdef inline Vector2 operator_add(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_add(self._c_vector2_ptr(), b._c_vector2_ptr())
        return ret

    cdef inline Vector2 operator_subtract(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_subtract(self._c_vector2_ptr(), b._c_vector2_ptr())
        return ret

    cdef inline Vector2 operator_multiply_vector(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_multiply_vector(self._c_vector2_ptr(), b._c_vector2_ptr())
        return ret

    cdef inline Vector2 operator_multiply_scalar(self, godot_real b):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_multiply_scalar(self._c_vector2_ptr(), b)
        return ret

    cdef inline Vector2 operator_divide_vector(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_divide_vector(self._c_vector2_ptr(), b._c_vector2_ptr())
        return ret

    cdef inline Vector2 operator_divide_scalar(self, godot_real b):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_divide_scalar(self._c_vector2_ptr(), b)
        return ret

    cdef inline bint operator_equal(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__()
        return gdapi.godot_vector2_operator_equal(self._c_vector2_ptr(), b._c_vector2_ptr())

    cdef inline bint operator_less(self, Vector2 b):
        cdef Vector2 ret  = Vector2.__new__()
        return gdapi.godot_vector2_operator_less(self._c_vector2_ptr(), b._c_vector2_ptr())

    cdef inline Vector2 operator_neg(self):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_neg(self._c_vector2_ptr())
        return ret

    def __lt__(self, other):
        cdef Vector2 _other = <Vector2?>other
        return self.operator_less(_other)

    def __eq__(self, other):
        cdef Vector2 _other = <Vector2?>other
        return self.operator_equal(_other)

    def __ne__(self, other):
        cdef Vector2 _other = <Vector2?>other
        return not self.operator_equal(_other)

    def __neg__(self):
        return self.operator_neg()

    def __pos__(self):
        return self

    def __add__(self, val):
        cdef Vector2 _val = <Vector2?>val
        return self.operator_add(_val)

    def __sub__(self, val):
        cdef Vector2 _val = <Vector2?>val
        return self.operator_subtract(_val)

    def __mul__(self, val):
        cdef Vector2 _val

        try:
            _val = <Vector2?>val

        except TypeError:
            return self.operator_multiply_scalar(val)

        else:
            return self.operator_multiply_vector(_val)

    def __truediv__(self, val):
        cdef Vector2 _val

        try:
            _val = <Vector2?>val

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
        return gdapi.godot_vector2_get_x(self._c_vector2_ptr())

    cdef inline void set_x(self, godot_real val):
        gdapi.godot_vector2_set_x(self._c_vector2_ptr(), val)

    cdef inline godot_real get_y(self):
        return gdapi.godot_vector2_get_y(self._c_vector2_ptr())

    cdef inline void set_y(self, godot_real val):
        gdapi.godot_vector2_set_y(self._c_vector2_ptr(), val)

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

    cpdef Vector2 normalized(self):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_normalized(self._c_vector2_ptr())
        return ret

    cpdef godot_real length(self):
        return gdapi.godot_vector2_length(self._c_vector2_ptr())

    cpdef godot_real angle(self):
        return gdapi.godot_vector2_angle(self._c_vector2_ptr())

    cpdef godot_real length_squared(self):
        return gdapi.godot_vector2_length_squared(self._c_vector2_ptr())

    cpdef bint is_normalized(self):
        return gdapi.godot_vector2_is_normalized(self._c_vector2_ptr())

    cpdef godot_real distance_to(self, Vector2 to):
        return gdapi.godot_vector2_distance_to(self._c_vector2_ptr(), to._c_vector2_ptr())

    cpdef godot_real distance_squared_to(self, Vector2 to):
        return gdapi.godot_vector2_distance_squared_to(self._c_vector2_ptr(), to._c_vector2_ptr())

    cpdef godot_real angle_to(self, Vector2 to):
        return gdapi.godot_vector2_angle_to(self._c_vector2_ptr(), &to._c_vector2)

    cpdef godot_real angle_to_point(self, Vector2 to):
        return gdapi.godot_vector2_angle_to_point(self._c_vector2_ptr(), &to._c_vector2)

    cpdef Vector2 linear_interpolate(self, Vector2 b, godot_real t):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_linear_interpolate(self._c_vector2_ptr(), b._c_vector2_ptr(), t)
        return ret

    cpdef Vector2 cubic_interpolate(self, Vector2 b, Vector2 pre_a, Vector2 post_b, godot_real t):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_cubic_interpolate(
            self._c_vector2_ptr(),
            b._c_vector2_ptr(),
            pre_a._c_vector2_ptr(),
            post_b._c_vector2_ptr(),
            t
        )
        return ret

    cpdef Vector2 move_toward(self, Vector2 to, godot_real delta):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi12.godot_vector2_move_toward(self._c_vector2_ptr(), to._c_vector2_ptr(), delta)
        return ret

    cpdef Vector2 rotated(self, godot_real phi):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_rotated(self._c_vector2_ptr(), phi)
        return ret

    cpdef Vector2 tangent(self):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_tangent(self._c_vector2_ptr())
        return ret

    cpdef Vector2 floor(self):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_floor(self._c_vector2_ptr())
        return ret

    cpdef Vector2 snapped(self, Vector2 by):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_snapped(self._c_vector2_ptr(), by._c_vector2_ptr())
        return ret

    cpdef godot_real aspect(self):
        return gdapi.godot_vector2_aspect(self._c_vector2_ptr())

    cpdef godot_real dot(self, Vector2 with_):
        return gdapi.godot_vector2_dot(self._c_vector2_ptr(), with_._c_vector2_ptr())

    cpdef Vector2 slide(self, Vector2 n):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_slide(self._c_vector2_ptr(), n._c_vector2_ptr())
        return ret

    cpdef Vector2 bounce(self, Vector2 n):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_bounce(self._c_vector2_ptr(), n._c_vector2_ptr())
        return ret

    cpdef Vector2 reflect(self, Vector2 n):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_reflect(self._c_vector2_ptr(), n._c_vector2_ptr())
        return ret

    cpdef Vector2 abs(self):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_abs(self._c_vector2_ptr())
        return ret

    cpdef Vector2 clamped(self, godot_real length):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_clamped(self._c_vector2_ptr(), length)
        return ret
