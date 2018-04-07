from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_vector3_alloc


class Vector3(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_VECTOR3

    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_vector3_alloc(gdobj[0])

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._gd_ptr = godot_vector3_alloc()
        lib.godot_vector3_new(self._gd_ptr, x, y, z)

    def __repr__(self):
        return "<%s(x=%s, y=%s, z=%s)>" % (type(self).__name__, self.x, self.y, self.z)

    def __eq__(self, other):
        return isinstance(other, Vector3) and lib.godot_vector3_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self

    def __add__(self, val):
        if isinstance(val, Vector3):
            gd_obj = lib.godot_vector3_operator_add(self._gd_ptr, val._gd_ptr)
            return Vector3.build_from_gdobj(gd_obj)

        else:
            return NotImplemented

    def __sub__(self, val):
        if isinstance(val, Vector3):
            gd_obj = lib.godot_vector3_operator_subtract(self._gd_ptr, val._gd_ptr)
            return Vector3.build_from_gdobj(gd_obj)

        else:
            return NotImplemented

    def __mul__(self, val):
        if isinstance(val, Vector3):
            gd_obj = lib.godot_vector3_operator_multiply_vector(
                self._gd_ptr, val._gd_ptr
            )
        else:
            gd_obj = lib.godot_vector3_operator_multiply_scalar(self._gd_ptr, val)
        return Vector3.build_from_gdobj(gd_obj)

    def __truediv__(self, val):
        if isinstance(val, Vector3):
            if val.x == 0 or val.y == 0 or val.z == 0:
                raise ZeroDivisionError()

            gd_obj = lib.godot_vector3_operator_divide_vector(self._gd_ptr, val._gd_ptr)
        else:
            if val is 0:
                raise ZeroDivisionError()

            gd_obj = lib.godot_vector3_operator_divide_scalar(self._gd_ptr, val)
        return Vector3.build_from_gdobj(gd_obj)

    # Properties

    @property
    def x(self):
        return lib.godot_vector3_get_axis(self._gd_ptr, self.AXIS_X)

    @property
    def y(self):
        return lib.godot_vector3_get_axis(self._gd_ptr, self.AXIS_Y)

    @property
    def z(self):
        return lib.godot_vector3_get_axis(self._gd_ptr, self.AXIS_Z)

    @x.setter
    def x(self, val):
        self._check_param_float("val", val)
        lib.godot_vector3_set_axis(self._gd_ptr, self.AXIS_X, val)

    @y.setter
    def y(self, val):
        self._check_param_float("val", val)
        lib.godot_vector3_set_axis(self._gd_ptr, self.AXIS_Y, val)

    @z.setter
    def z(self, val):
        self._check_param_float("val", val)
        lib.godot_vector3_set_axis(self._gd_ptr, self.AXIS_Z, val)

    # Methods

    def min_axis(self):
        return lib.godot_vector3_min_axis(self._gd_ptr)

    def max_axis(self):
        return lib.godot_vector3_max_axis(self._gd_ptr)

    def length(self):
        return lib.godot_vector3_length(self._gd_ptr)

    def length_squared(self):
        return lib.godot_vector3_length_squared(self._gd_ptr)

    def normalize(self):
        return lib.godot_vector3_normalize(self._gd_ptr)

    def normalized(self):
        gd_obj = lib.godot_vector3_normalized(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def inverse(self):
        gd_obj = lib.godot_vector3_inverse(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def zero(self):
        lib.godot_vector3_zero(self._gd_ptr)

    # TODO: not available yet in GDnative
    # def snap(self, by):
    #     self._check_param_float('by', by)
    #     lib.godot_vector3_snap(self._gd_ptr)

    def snapped(self, by):
        self._check_param_type("by", by, Vector3)
        gd_obj = lib.godot_vector3_snapped(self._gd_ptr, by._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def rotate(self, axis, phi):
        self._check_param_type("axis", axis, Vector3)
        self._check_param_float("phi", phi)
        lib.godot_vector3_rotate(self._gd_ptr, axis._gd_ptr, phi)

    def rotated(self, axis, phi):
        self._check_param_type("axis", axis, Vector3)
        self._check_param_float("phi", phi)
        gd_obj = lib.godot_vector3_rotated(self._gd_ptr, axis._gd_ptr, phi)
        return Vector3.build_from_gdobj(gd_obj)

    def linear_interpolate(self, b, t):
        self._check_param_type("b", b, Vector3)
        self._check_param_float("t", t)
        gd_obj = lib.godot_vector3_linear_interpolate(self._gd_ptr, b._gd_ptr, t)
        return Vector3.build_from_gdobj(gd_obj)

    def cubic_interpolate(self, b, pre_a, post_b, t):
        self._check_param_type("b", b, Vector3)
        self._check_param_type("pre_a", pre_a, Vector3)
        self._check_param_type("post_b", post_b, Vector3)
        self._check_param_float("t", t)
        gd_obj = lib.godot_vector3_cubic_interpolate(
            self._gd_ptr, b._gd_ptr, pre_a._gd_ptr, post_b._gd_ptr, t
        )
        return Vector3.build_from_gdobj(gd_obj)

    def cubic_interpolaten(self, b, pre_a, post_b, t):
        self._check_param_type("b", b, Vector3)
        self._check_param_type("pre_a", pre_a, Vector3)
        self._check_param_type("post_b", post_b, Vector3)
        self._check_param_float("t", t)
        gd_obj = lib.godot_vector3_cubic_interpolaten(
            self._gd_ptr, b._gd_ptr, pre_a._gd_ptr, post_b._gd_ptr, t
        )
        return Vector3.build_from_gdobj(gd_obj)

    def cross(self, b):
        self._check_param_type("b", b, Vector3)
        gd_obj = lib.godot_vector3_cross(self._gd_ptr, b._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def dot(self, b):
        self._check_param_type("b", b, Vector3)
        return lib.godot_vector3_dot(self._gd_ptr, b._gd_ptr)

    def outer(self, b):
        from godot.basis import Basis

        self._check_param_type("b", b, Vector3)
        gd_obj = lib.godot_vector3_outer(self._gd_ptr, b._gd_ptr)
        return Basis.build_from_gdobj(gd_obj)

    def to_diagonal_matrix(self):
        from godot.basis import Basis

        gd_obj = lib.godot_vector3_to_diagonal_matrix(self._gd_ptr)
        return Basis.build_from_gdobj(gd_obj)

    def abs(self):
        gd_obj = lib.godot_vector3_abs(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def floor(self):
        gd_obj = lib.godot_vector3_floor(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def ceil(self):
        gd_obj = lib.godot_vector3_ceil(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def distance_to(self, b):
        self._check_param_type("b", b, Vector3)
        return lib.godot_vector3_distance_to(self._gd_ptr, b._gd_ptr)

    def distance_squared_to(self, b):
        self._check_param_type("b", b, Vector3)
        return lib.godot_vector3_distance_squared_to(self._gd_ptr, b._gd_ptr)

    def angle_to(self, b):
        self._check_param_type("b", b, Vector3)
        return lib.godot_vector3_angle_to(self._gd_ptr, b._gd_ptr)

    def slide(self, vec):
        self._check_param_type("vec", vec, Vector3)
        gd_obj = lib.godot_vector3_slide(self._gd_ptr, vec._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def bounce(self, vec):
        self._check_param_type("vec", vec, Vector3)
        gd_obj = lib.godot_vector3_bounce(self._gd_ptr, vec._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def reflect(self, vec):
        self._check_param_type("vec", vec, Vector3)
        gd_obj = lib.godot_vector3_reflect(self._gd_ptr, vec._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)
