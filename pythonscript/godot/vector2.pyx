# cython: language_level=3

cimport cython

from _godot cimport gdapi
from .gdnative_api_struct cimport godot_vector2, godot_real


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

    def __eq__(self, other):
        cdef Vector2 _other = <Vector2?>other
        return gdapi.godot_vector2_operator_equal(
            self._c_vector2_ptr(), _other._c_vector2_ptr()
        )

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        cdef ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_neg(self._c_vector2_ptr())
        return ret

    def __pos__(self):
        return self

    def __add__(self, val):
        cdef Vector2 _val = <Vector2?>val
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_add(
            (<Vector2>self)._c_vector2_ptr(), _val._c_vector2_ptr()
        )
        return ret

    def __sub__(self, val):
        cdef Vector2 _val = <Vector2?>val
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_operator_subtract(
            (<Vector2>self)._c_vector2_ptr(), _val._c_vector2_ptr())
        return ret

    def __mul__(self, val):
        cdef Vector2 _val
        cdef Vector2 ret

        try:
            _val = <Vector2?>val

        except TypeError:
            ret  = Vector2.__new__()
            ret._c_vector2 = gdapi.godot_vector2_operator_multiply_scalar(
                (<Vector2>self)._c_vector2_ptr(), val)
            return ret

        else:
            ret  = Vector2.__new__()
            ret._c_vector2 = gdapi.godot_vector2_operator_multiply_vector(
                (<Vector2>self)._c_vector2_ptr(), _val._c_vector2_ptr())
            return ret

    def __truediv__(self, val):
        cdef Vector2 _val
        cdef Vector2 ret

        try:
            _val = <Vector2?>val

        except TypeError:
            if val is 0:
                raise ZeroDivisionError()

            ret  = Vector2.__new__()
            ret._c_vector2 = gdapi.godot_vector2_operator_divide_scalar(
                (<Vector2>self)._c_vector2_ptr(), val)
            return ret

        else:
            if _val.x == 0 or _val.y == 0:
                raise ZeroDivisionError()

            ret  = Vector2.__new__()
            ret._c_vector2 = gdapi.godot_vector2_operator_divide_vector(
                (<Vector2>self)._c_vector2_ptr(), _val._c_vector2_ptr())
            return ret

    # Properties

    cdef godot_real get_x(self):
        return gdapi.godot_vector2_get_x(self._c_vector2_ptr())

    cdef void set_x(self, godot_real val):
        gdapi.godot_vector2_set_x(self._c_vector2_ptr(), val)

    cdef godot_real get_y(self):
        return gdapi.godot_vector2_get_y(self._c_vector2_ptr())

    cdef void set_y(self, godot_real val):
        gdapi.godot_vector2_set_y(self._c_vector2_ptr(), val)

    @property
    def x(self):
        return gdapi.godot_vector2_get_x(self._c_vector2_ptr())

    @property
    def y(self):
        return gdapi.godot_vector2_get_y(self._c_vector2_ptr())

    @x.setter
    def x(self, val):
        gdapi.godot_vector2_set_x(self._c_vector2_ptr(), val)

    @y.setter
    def y(self, val):
        gdapi.godot_vector2_set_y(self._c_vector2_ptr(), val)

    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y

    @width.setter
    def width(self, val):
        self.x = val

    @height.setter
    def height(self, val):
        self.y = val

    # Methods

    cpdef Vector2 abs(self):
        cdef Vector2 ret  = Vector2.__new__()
        ret._c_vector2 = gdapi.godot_vector2_abs(self._c_vector2_ptr())
        return ret

    cpdef godot_real angle(self):
        return gdapi.godot_vector2_angle(self._c_vector2_ptr())

    cpdef godot_real angle_to(self, Vector2 to):
        return gdapi.godot_vector2_angle_to(self._c_vector2_ptr(), &to._c_vector2)

    cpdef godot_real angle_to_point(self, Vector2 to):
        return gdapi.godot_vector2_angle_to_point(self._c_vector2_ptr(), &to._c_vector2)

    # def clamped(self, length):
    #     self._check_param_float("length", length)
    #     gd_obj = lib.godot_vector2_clamped(self._gd_ptr, length)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def cubic_interpolate(self, b, pre_a, post_b, t):
    #     self._check_param_type("b", b, Vector2)
    #     self._check_param_type("pre_a", pre_a, Vector2)
    #     self._check_param_type("post_b", post_b, Vector2)
    #     self._check_param_float("t", t)
    #     gd_obj = lib.godot_vector2_cubic_interpolate(
    #         self._gd_ptr, b._gd_ptr, pre_a._gd_ptr, post_b._gd_ptr, t
    #     )
    #     return Vector2.build_from_gdobj(gd_obj)

    # def distance_squared_to(self, to):
    #     self._check_param_type("to", to, Vector2)
    #     return lib.godot_vector2_distance_squared_to(self._gd_ptr, to._gd_ptr)

    # def distance_to(self, to):
    #     self._check_param_type("to", to, Vector2)
    #     return lib.godot_vector2_distance_to(self._gd_ptr, to._gd_ptr)

    # def dot(self, with_):
    #     self._check_param_type("with_", with_, Vector2)
    #     return lib.godot_vector2_dot(self._gd_ptr, with_._gd_ptr)

    # def floor(self):
    #     gd_obj = lib.godot_vector2_floor(self._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def floorf(self):
    #     gd_obj = lib.godot_vector2_floorf(self._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def aspect(self):
    #     return lib.godot_vector2_aspect(self._gd_ptr)

    # def length(self):
    #     return lib.godot_vector2_length(self._gd_ptr)

    # def length_squared(self):
    #     return lib.godot_vector2_length_squared(self._gd_ptr)

    # def linear_interpolate(self, b, t):
    #     self._check_param_type("b", b, Vector2)
    #     self._check_param_float("t", t)
    #     gd_obj = lib.godot_vector2_linear_interpolate(self._gd_ptr, b._gd_ptr, t)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def normalized(self):
    #     gd_obj = lib.godot_vector2_normalized(self._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def reflect(self, vec):
    #     self._check_param_type("vec", vec, Vector2)
    #     gd_obj = lib.godot_vector2_reflect(self._gd_ptr, vec._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def rotated(self, phi):
    #     self._check_param_float("phi", phi)
    #     gd_obj = lib.godot_vector2_rotated(self._gd_ptr, phi)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def slide(self, vec):
    #     self._check_param_type("vec", vec, Vector2)
    #     gd_obj = lib.godot_vector2_slide(self._gd_ptr, vec._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def snapped(self, by):
    #     self._check_param_type("by", by, Vector2)
    #     gd_obj = lib.godot_vector2_snapped(self._gd_ptr, by._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)

    # def tangent(self):
    #     gd_obj = lib.godot_vector2_tangent(self._gd_ptr)
    #     return Vector2.build_from_gdobj(gd_obj)
