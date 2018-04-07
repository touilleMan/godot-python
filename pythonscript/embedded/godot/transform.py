from pythonscriptcffi import lib, ffi

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_transform_alloc
from godot.basis import Basis
from godot.vector3 import Vector3
from godot.aabb import AABB
from godot.plane import Plane


class Transform(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_TRANSFORM

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_transform_alloc(gdobj[0])

    def __init__(self, basis=Basis(), origin=Vector3()):
        self._check_param_type("basis", basis, Basis)
        self._check_param_type("origin", origin, Vector3)
        self._gd_ptr = godot_transform_alloc()
        lib.godot_transform_new(self._gd_ptr, basis._gd_ptr, origin._gd_ptr)

    @classmethod
    def built_from_axis_origin(
        cls, x_axis=Vector3(), y_axis=Vector3(), z_axis=Vector3(), origin=Vector3()
    ):
        self._check_param_type("x_axis", x_axis, Vector3)
        self._check_param_type("y_axis", y_axis, Vector3)
        self._check_param_type("z_axis", z_axis, Vector3)
        self._check_param_type("origin", origin, Vector3)
        ret = Transform()
        lib.godot_transform_new_with_axis_origin(
            self._gd_ptr, x_axis._gd_ptr, y_axis._gd_ptr, z._gd_ptr, origin._gd_ptr
        )
        return ret

    def __eq__(self, other):
        return isinstance(other, Transform) and lib.godot_transform_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        gd_repr = lib.godot_transform_as_string(self._gd_ptr)
        raw_str = lib.godot_string_wide_str(ffi.addressof(gd_repr))
        return "<%s(%s)>" % (type(self).__name__, ffi.string(raw_str))

    def __mul__(self, other):
        if not isinstance(other, Transform):
            return NotImplemented

        raw = lib.godot_transform_operator_multiply(self._gd_ptr, other._gd_ptr)
        return Transform.build_from_gdobj(raw)

    # Properties

    @property
    def basis(self):
        raw = lib.godot_transform_get_basis(self._gd_ptr)
        return Basis.build_from_gdobj(raw)

    @basis.setter
    def basis(self, val):
        self._check_param_type("val", val, Basis)
        lib.godot_transform_set_basis(self._gd_ptr, val._gd_ptr)

    @property
    def origin(self):
        raw = lib.godot_transform_get_origin(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    @origin.setter
    def origin(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_transform_set_origin(self._gd_ptr, val._gd_ptr)

    # Methods

    def inverse(self):
        raw = lib.godot_transform_inverse(self._gd_ptr)
        return Transform.build_from_gdobj(raw)

    def affine_inverse(self):
        raw = lib.godot_transform_affine_inverse(self._gd_ptr)
        return Transform.build_from_gdobj(raw)

    def orthonormalized(self):
        raw = lib.godot_transform_orthonormalized(self._gd_ptr)
        return Transform.build_from_gdobj(raw)

    def rotated(self, phi):
        self._check_param_float("phi", phi)
        raw = lib.godot_transform_rotated(self._gd_ptr, phi)
        return Transform.build_from_gdobj(raw)

    def scaled(self, scale):
        self._check_param_type("scale", scale, Vector3)
        raw = lib.godot_transform_scaled(self._gd_ptr, scale._gd_ptr)
        return Transform.build_from_gdobj(raw)

    def translated(self, offset):
        self._check_param_type("offset", offset, Vector3)
        raw = lib.godot_transform_translated(self._gd_ptr, offset._gd_ptr)
        return Transform.build_from_gdobj(raw)

    def looking_at(self, target, up):
        self._check_param_type("target", target, Vector3)
        self._check_param_type("up", up, Vector3)
        raw = lib.godot_transform_looking_at(self._gd_ptr, target._gd_ptr, up._gd_ptr)
        return Transform.build_from_gdobj(raw)

    def xform(self, v):
        if isinstance(v, Vector3):
            raw = lib.godot_transform_xform_vector3(self._gd_ptr, v._gd_ptr)
            return Vector3.build_from_gdobj(raw)

        elif isinstance(v, AABB):
            raw = lib.godot_transform_xform_aabb(self._gd_ptr, v._gd_ptr)
            return AABB.build_from_gdobj(raw)

        elif isinstance(v, Plane):
            raw = lib.godot_transform_xform_plane(self._gd_ptr, v._gd_ptr)
            return Plane.build_from_gdobj(raw)

        raise TypeError("Param `v` should be of type `Plane`, `AABB` or `Vector3`")

    def xform_inv(self, v):
        if isinstance(v, Vector3):
            raw = lib.godot_transform_xform_inv_vector3(self._gd_ptr, v._gd_ptr)
            return Vector3.build_from_gdobj(raw)

        elif isinstance(v, AABB):
            raw = lib.godot_transform_xform_inv_aabb(self._gd_ptr, v._gd_ptr)
            return AABB.build_from_gdobj(raw)

        elif isinstance(v, Plane):
            raw = lib.godot_transform_xform_inv_plane(self._gd_ptr, v._gd_ptr)
            return Plane.build_from_gdobj(raw)

        raise TypeError("Param `v` should be of type `Plane`, `AABB` or `Vector3`")
