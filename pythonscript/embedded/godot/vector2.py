from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_vector2_alloc


class Vector2(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_VECTOR2

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_vector2_alloc(gdobj[0])

    def __init__(self, x=0.0, y=0.0):
        self._gd_ptr = godot_vector2_alloc()
        lib.godot_vector2_new(self._gd_ptr, x, y)

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector2) and lib.godot_vector2_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __pos__(self):
        return self

    def __add__(self, val):
        if isinstance(val, Vector2):
            gd_obj = lib.godot_vector2_operator_add(self._gd_ptr, val._gd_ptr)
            return Vector2.build_from_gdobj(gd_obj)

        else:
            return NotImplemented

    def __sub__(self, val):
        if isinstance(val, Vector2):
            gd_obj = lib.godot_vector2_operator_subtract(self._gd_ptr, val._gd_ptr)
            return Vector2.build_from_gdobj(gd_obj)

        else:
            return NotImplemented

    def __mul__(self, val):
        if isinstance(val, Vector2):
            gd_obj = lib.godot_vector2_operator_multiply_vector(
                self._gd_ptr, val._gd_ptr
            )
        else:
            gd_obj = lib.godot_vector2_operator_multiply_scalar(self._gd_ptr, val)
        return Vector2.build_from_gdobj(gd_obj)

    def __truediv__(self, val):
        if isinstance(val, Vector2):
            if val.x == 0 or val.y == 0:
                raise ZeroDivisionError()

            gd_obj = lib.godot_vector2_operator_divide_vector(self._gd_ptr, val._gd_ptr)
        else:
            if val is 0:
                raise ZeroDivisionError()

            gd_obj = lib.godot_vector2_operator_divide_scalar(self._gd_ptr, val)
        return Vector2.build_from_gdobj(gd_obj)

    # Properties

    @property
    def x(self):
        return lib.godot_vector2_get_x(self._gd_ptr)

    @property
    def y(self):
        return lib.godot_vector2_get_y(self._gd_ptr)

    @x.setter
    def x(self, val):
        self._check_param_float("val", val)
        lib.godot_vector2_set_x(self._gd_ptr, val)

    @y.setter
    def y(self, val):
        self._check_param_float("val", val)
        lib.godot_vector2_set_y(self._gd_ptr, val)

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

    def abs(self):
        return Vector2.build_from_gdobj(lib.godot_vector2_abs(self._gd_ptr))

    def angle(self):
        return lib.godot_vector2_angle(self._gd_ptr)

    def angle_to(self, to):
        self._check_param_type("to", to, Vector2)
        return lib.godot_vector2_angle_to(self._gd_ptr, to._gd_ptr)

    def angle_to_point(self, to):
        self._check_param_type("to", to, Vector2)
        return lib.godot_vector2_angle_to_point(self._gd_ptr, to._gd_ptr)

    def clamped(self, length):
        self._check_param_float("length", length)
        gd_obj = lib.godot_vector2_clamped(self._gd_ptr, length)
        return Vector2.build_from_gdobj(gd_obj)

    def cubic_interpolate(self, b, pre_a, post_b, t):
        self._check_param_type("b", b, Vector2)
        self._check_param_type("pre_a", pre_a, Vector2)
        self._check_param_type("post_b", post_b, Vector2)
        self._check_param_float("t", t)
        gd_obj = lib.godot_vector2_cubic_interpolate(
            self._gd_ptr, b._gd_ptr, pre_a._gd_ptr, post_b._gd_ptr, t
        )
        return Vector2.build_from_gdobj(gd_obj)

    def distance_squared_to(self, to):
        self._check_param_type("to", to, Vector2)
        return lib.godot_vector2_distance_squared_to(self._gd_ptr, to._gd_ptr)

    def distance_to(self, to):
        self._check_param_type("to", to, Vector2)
        return lib.godot_vector2_distance_to(self._gd_ptr, to._gd_ptr)

    def dot(self, with_):
        self._check_param_type("with_", with_, Vector2)
        return lib.godot_vector2_dot(self._gd_ptr, with_._gd_ptr)

    def floor(self):
        gd_obj = lib.godot_vector2_floor(self._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)

    def floorf(self):
        gd_obj = lib.godot_vector2_floorf(self._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)

    def aspect(self):
        return lib.godot_vector2_aspect(self._gd_ptr)

    def length(self):
        return lib.godot_vector2_length(self._gd_ptr)

    def length_squared(self):
        return lib.godot_vector2_length_squared(self._gd_ptr)

    def linear_interpolate(self, b, t):
        self._check_param_type("b", b, Vector2)
        self._check_param_float("t", t)
        gd_obj = lib.godot_vector2_linear_interpolate(self._gd_ptr, b._gd_ptr, t)
        return Vector2.build_from_gdobj(gd_obj)

    def normalized(self):
        gd_obj = lib.godot_vector2_normalized(self._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)

    def reflect(self, vec):
        self._check_param_type("vec", vec, Vector2)
        gd_obj = lib.godot_vector2_reflect(self._gd_ptr, vec._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)

    def rotated(self, phi):
        self._check_param_float("phi", phi)
        gd_obj = lib.godot_vector2_rotated(self._gd_ptr, phi)
        return Vector2.build_from_gdobj(gd_obj)

    def slide(self, vec):
        self._check_param_type("vec", vec, Vector2)
        gd_obj = lib.godot_vector2_slide(self._gd_ptr, vec._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)

    def snapped(self, by):
        self._check_param_type("by", by, Vector2)
        gd_obj = lib.godot_vector2_snapped(self._gd_ptr, by._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)

    def tangent(self):
        gd_obj = lib.godot_vector2_tangent(self._gd_ptr)
        return Vector2.build_from_gdobj(gd_obj)
