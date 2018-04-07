from pythonscriptcffi import lib, ffi

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_transform2d_alloc
from godot.vector2 import Vector2
from godot.rect2 import Rect2


class Transform2D(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_TRANSFORM2D

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_transform2d_alloc(gdobj[0])

    def __init__(self, rot=0.0, pos=Vector2()):
        self._check_param_float("rot", rot)
        self._check_param_type("pos", pos, Vector2)
        self._gd_ptr = godot_transform2d_alloc()
        lib.godot_transform2d_new(self._gd_ptr, rot, pos._gd_ptr)

    @classmethod
    def built_from_axis_origin(
        cls, x_axis=Vector2(), y_axis=Vector2(), origin=Vector2()
    ):
        self._check_param_type("x_axis", x_axis, Vector2)
        self._check_param_type("y_axis", y_axis, Vector2)
        self._check_param_type("origin", origin, Vector2)
        ret = Transform2D()
        lib.godot_transform2d_new_with_axis_origin(
            self._gd_ptr, x_axis._gd_ptr, y_axis._gd_ptr, origin._gd_ptr
        )
        return ret

    def __eq__(self, other):
        return isinstance(other, Transform2D) and lib.godot_transform2d_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        gd_repr = lib.godot_transform2d_as_string(self._gd_ptr)
        raw_str = lib.godot_string_wide_str(ffi.addressof(gd_repr))
        return "<%s(%s)>" % (type(self).__name__, ffi.string(raw_str))

    def __mul__(self, other):
        if not isinstance(other, Transform2D):
            return NotImplemented

        raw = lib.godot_transform2d_operator_multiply(self._gd_ptr, other._gd_ptr)
        return Transform2D.build_from_gdobj(raw)

    # Properties

    # Methods

    def inverse(self):
        raw = lib.godot_transform2d_inverse(self._gd_ptr)
        return Transform2D.build_from_gdobj(raw)

    def affine_inverse(self):
        raw = lib.godot_transform2d_affine_inverse(self._gd_ptr)
        return Transform2D.build_from_gdobj(raw)

    def get_rotation(self):
        return lib.godot_transform2d_get_rotation(self._gd_ptr)

    def get_origin(self):
        raw = lib.godot_transform2d_get_origin(self._gd_ptr)
        return Vector2.build_from_gdobj(raw)

    def get_scale(self):
        raw = lib.godot_transform2d_get_scale(self._gd_ptr)
        return Vector2.build_from_gdobj(raw)

    def orthonormalized(self):
        raw = lib.godot_transform2d_orthonormalized(self._gd_ptr)
        return Transform2D.build_from_gdobj(raw)

    def rotated(self, phi):
        self._check_param_float("phi", phi)
        raw = lib.godot_transform2d_rotated(self._gd_ptr, phi)
        return Transform2D.build_from_gdobj(raw)

    def scaled(self, scale):
        self._check_param_type("scale", scale, Vector2)
        raw = lib.godot_transform2d_scaled(self._gd_ptr, scale._gd_ptr)
        return Transform2D.build_from_gdobj(raw)

    def translated(self, offset):
        self._check_param_type("offset", offset, Vector2)
        raw = lib.godot_transform2d_translated(self._gd_ptr, offset._gd_ptr)
        return Transform2D.build_from_gdobj(raw)

    def xform(self, v):
        if isinstance(v, Vector2):
            raw = lib.godot_transform2d_xform_vector2(self._gd_ptr, v._gd_ptr)
            return Vector2.build_from_gdobj(raw)

        elif isinstance(v, Rect2):
            raw = lib.godot_transform2d_xform_rect2(self._gd_ptr, v._gd_ptr)
            return Rect2.build_from_gdobj(raw)

        raise TypeError("Param `v` should be of type `Rect2` or `Vector2`")

    def xform_inv(self, v):
        if isinstance(v, Vector2):
            raw = lib.godot_transform2d_xform_inv_vector2(self._gd_ptr, v._gd_ptr)
            return Vector2.build_from_gdobj(raw)

        elif isinstance(v, Rect2):
            raw = lib.godot_transform2d_xform_inv_rect2(self._gd_ptr, v._gd_ptr)
            return Rect2.build_from_gdobj(raw)

        raise TypeError("Param `v` should be of type `Rect2` or `Vector2`")

    def basis_xform(self, v):
        self._check_param_type("v", v, Vector2)
        raw = lib.godot_transform2d_basis_xform_vector2(self._gd_ptr, v._gd_ptr)
        return Vector2.build_from_gdobj(raw)

    def basis_xform_inv(self, v):
        self._check_param_type("v", v, Vector2)
        raw = lib.godot_transform2d_basis_xform_inv_vector2(self._gd_ptr, v._gd_ptr)
        return Vector2.build_from_gdobj(raw)

    def interpolate_with(self, m, c):
        self._check_param_type("m", m, Transform2D)
        self._check_param_float("c", c)
        raw = lib.godot_transform2d_interpolate_with(self._gd_ptr, m._gd_ptr, c)
        return Transform2D.build_from_gdobj(raw)
