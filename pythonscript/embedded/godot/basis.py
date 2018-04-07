from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_basis_alloc
from godot.hazmat.allocator import godot_vector3_alloc
from godot.vector3 import Vector3
from godot.quat import Quat


class Basis(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_BASIS

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_basis_alloc(gdobj[0])

    @classmethod
    def build_from_rows(cls, row0, row1, row2):
        cls._check_param_type("row0", row0, Vector3)
        cls._check_param_type("row1", row1, Vector3)
        cls._check_param_type("row2", row2, Vector3)
        gd_ptr = godot_basis_alloc()
        lib.godot_basis_new_with_rows(gd_ptr, row0._gd_ptr, row1._gd_ptr, row2._gd_ptr)
        return cls.build_from_gdobj(gd_ptr, steal=True)

    @classmethod
    def build_from_euler(cls, euler):
        gd_ptr = godot_basis_alloc()
        if isinstance(euler, Vector3):
            lib.godot_basis_new_with_euler(gd_ptr, euler._gd_ptr)
        elif isinstance(euler, Quat):
            lib.godot_basis_new_with_euler_quat(gd_ptr, euler._gd_ptr)
        else:
            raise TypeError("Param `euler` should be of type `%s`" % (Vector3, Quat))

        return cls.build_from_gdobj(gd_ptr, steal=True)

    @classmethod
    def build_from_axis_and_angle(cls, axis, phi):
        cls._check_param_type("axis", axis, Vector3)
        cls._check_param_float("phi", phi)
        gd_ptr = godot_basis_alloc()
        lib.godot_basis_new_with_axis_and_angle(gd_ptr, axis._gd_ptr, phi)
        return cls.build_from_gdobj(gd_ptr, steal=True)

    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    def __init__(self):  # TODO: allow rows as param ?
        self._gd_ptr = godot_basis_alloc()
        x = godot_vector3_alloc()
        lib.godot_vector3_new(x, 1, 0, 0)
        y = godot_vector3_alloc()
        lib.godot_vector3_new(y, 0, 1, 0)
        z = godot_vector3_alloc()
        lib.godot_vector3_new(z, 0, 0, 1)
        lib.godot_basis_new_with_rows(self._gd_ptr, x, y, z)

    def __repr__(self):
        return "<{n}(({v.x.x}, {v.x.y}, {v.x.z}), ({v.y.x}, {v.y.y}, {v.y.z}), ({v.z.x}, {v.z.y}, {v.z.z}))>".format(
            n=type(self).__name__, v=self
        )

    def __eq__(self, other):
        return isinstance(other, Basis) and lib.godot_basis_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self

    def __add__(self, val):
        if isinstance(val, Basis):
            gd_obj = lib.godot_basis_operator_add(self._gd_ptr, val._gd_ptr)
            return Basis.build_from_gdobj(gd_obj)

        else:
            return NotImplemented

    def __sub__(self, val):
        if isinstance(val, Basis):
            gd_obj = lib.godot_basis_operator_subtract(self._gd_ptr, val._gd_ptr)
            return Basis.build_from_gdobj(gd_obj)

        else:
            return NotImplemented

    def __mul__(self, val):
        if isinstance(val, Basis):
            gd_obj = lib.godot_basis_operator_multiply_basis(self._gd_ptr, val._gd_ptr)
        else:
            gd_obj = lib.godot_basis_operator_multiply_scalar(self._gd_ptr, val)
        return Basis.build_from_gdobj(gd_obj)

    def __truediv__(self, val):
        if isinstance(val, Basis):
            gd_obj = lib.godot_basis_operator_divide_basis(self._gd_ptr, val._gd_ptr)
        else:
            gd_obj = lib.godot_basis_operator_divide_scalar(self._gd_ptr, val)
        return Basis.build_from_gdobj(gd_obj)

    # Properties

    @property
    def x(self):
        return Vector3.build_from_gdobj(
            lib.godot_basis_get_axis(self._gd_ptr, self.AXIS_X)
        )

    @property
    def y(self):
        return Vector3.build_from_gdobj(
            lib.godot_basis_get_axis(self._gd_ptr, self.AXIS_Y)
        )

    @property
    def z(self):
        return Vector3.build_from_gdobj(
            lib.godot_basis_get_axis(self._gd_ptr, self.AXIS_Z)
        )

    @x.setter
    def x(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_basis_set_axis(self._gd_ptr, self.AXIS_X, val._gd_ptr)

    @y.setter
    def y(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_basis_set_axis(self._gd_ptr, self.AXIS_Y, val._gd_ptr)

    @z.setter
    def z(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_basis_set_axis(self._gd_ptr, self.AXIS_Z, val._gd_ptr)

    # Methods

    def determinant(self):
        return lib.godot_basis_determinant(self._gd_ptr)

    def get_euler(self):
        gd_obj = lib.godot_basis_get_euler(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def get_orthogonal_index(self):
        return lib.godot_basis_get_orthogonal_index(self._gd_ptr)

    def get_scale(self):
        gd_obj = lib.godot_basis_get_scale(self._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def inverse(self):
        gd_obj = lib.godot_basis_inverse(self._gd_ptr)
        return Basis.build_from_gdobj(gd_obj)

    def orthonormalized(self):
        gd_obj = lib.godot_basis_orthonormalized(self._gd_ptr)
        return Basis.build_from_gdobj(gd_obj)

    def rotated(self, axis, phi):
        self._check_param_type("axis", axis, Vector3)
        gd_obj = lib.godot_basis_rotated(self._gd_ptr, axis._gd_ptr, phi)
        return Basis.build_from_gdobj(gd_obj)

    def scaled(self, scale):
        self._check_param_type("scale", scale, Vector3)
        gd_obj = lib.godot_basis_scaled(self._gd_ptr, scale._gd_ptr)
        return Basis.build_from_gdobj(gd_obj)

    def tdotx(self, with_):
        self._check_param_type("with_", with_, Vector3)
        return lib.godot_basis_tdotx(self._gd_ptr, with_._gd_ptr)

    def tdoty(self, with_):
        self._check_param_type("with_", with_, Vector3)
        return lib.godot_basis_tdoty(self._gd_ptr, with_._gd_ptr)

    def tdotz(self, with_):
        self._check_param_type("with_", with_, Vector3)
        return lib.godot_basis_tdotz(self._gd_ptr, with_._gd_ptr)

    def transposed(self):
        gd_obj = lib.godot_basis_transposed(self._gd_ptr)
        return Basis.build_from_gdobj(gd_obj)

    def xform(self, vect):
        self._check_param_type("vect", vect, Vector3)
        gd_obj = lib.godot_basis_xform(self._gd_ptr, vect._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)

    def xform_inv(self, vect):
        self._check_param_type("vect", vect, Vector3)
        gd_obj = lib.godot_basis_xform_inv(self._gd_ptr, vect._gd_ptr)
        return Vector3.build_from_gdobj(gd_obj)
