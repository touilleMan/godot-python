from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_quat_alloc
from godot.vector3 import Vector3


class Quat(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_QUAT

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_quat_alloc(gdobj[0])

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self._gd_ptr = godot_quat_alloc()
        lib.godot_quat_new(self._gd_ptr, x, y, z, w)

    @classmethod
    def build_with_axis_angle(cls, axis, angle):
        cls._check_param_type("axis", axis, Vector3)
        gd_ptr = godot_quat_alloc()
        lib.godot_quat_new_with_axis_angle(gd_ptr, axis._gd_ptr, angle)
        return cls.build_from_gdobj(gd_ptr, steal=True)

    def __eq__(self, other):
        return isinstance(other, Quat) and lib.godot_quat_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_operator_neg(self._gd_ptr)
        return ret

    def __pos__(self):
        return self

    def __mul__(self, val):
        if not isinstance(val, (float, int)):
            return NotImplemented

        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_operator_multiply(self._gd_ptr, val)
        return ret

    def __add__(self, other):
        if not isinstance(other, Quat):
            return NotImplemented

        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_operator_add(self._gd_ptr, other._gd_ptr)
        return ret

    def __sub__(self, other):
        if not isinstance(other, Quat):
            return NotImplemented

        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_operator_subtract(self._gd_ptr, other._gd_ptr)
        return ret

    def __truediv__(self, val):
        if not isinstance(val, (float, int)):
            return NotImplemented

        if val is 0:
            raise ZeroDivisionError()

        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_operator_divide(self._gd_ptr, val)
        return ret

    def __repr__(self):
        return "<%s(x=%s, y=%s, z=%s, w=%s)>" % (
            type(self).__name__, self.x, self.y, self.z, self.w
        )

    @property
    def x(self):
        return lib.godot_quat_get_x(self._gd_ptr)

    @x.setter
    def x(self, val):
        return lib.godot_quat_set_x(self._gd_ptr, val)

    @property
    def y(self):
        return lib.godot_quat_get_y(self._gd_ptr)

    @y.setter
    def y(self, val):
        return lib.godot_quat_set_y(self._gd_ptr, val)

    @property
    def z(self):
        return lib.godot_quat_get_z(self._gd_ptr)

    @z.setter
    def z(self, val):
        return lib.godot_quat_set_z(self._gd_ptr, val)

    @property
    def w(self):
        return lib.godot_quat_get_w(self._gd_ptr)

    @w.setter
    def w(self, val):
        return lib.godot_quat_set_w(self._gd_ptr, val)

    def length(self):
        return lib.godot_quat_length(self._gd_ptr)

    def length_squared(self):
        return lib.godot_quat_length_squared(self._gd_ptr)

    def normalized(self):
        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_normalized(self._gd_ptr)
        return ret

    def is_normalized(self):
        return bool(lib.godot_quat_is_normalized(self._gd_ptr))

    def inverse(self):
        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_inverse(self._gd_ptr)
        return ret

    def dot(self, b):
        self._check_param_type("b", b, Quat)
        return lib.godot_quat_dot(self._gd_ptr, b._gd_ptr)

    def xform(self, v):
        self._check_param_type("v", v, Vector3)
        ret = Vector3()
        ret._gd_ptr[0] = lib.godot_quat_xform(self._gd_ptr, v._gd_ptr)
        return ret

    def slerp(self, b, t):
        self._check_param_type("b", b, Quat)
        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_slerp(self._gd_ptr, b._gd_ptr, t)
        return ret

    def slerpni(self, b, t):
        self._check_param_type("b", b, Quat)
        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_slerpni(self._gd_ptr, b._gd_ptr, t)
        return ret

    def cubic_slerp(self, b, pre_a, post_b, t):
        self._check_param_type("b", b, Quat)
        self._check_param_type("pre_a", pre_a, Quat)
        self._check_param_type("post_b", post_b, Quat)
        ret = Quat()
        ret._gd_ptr[0] = lib.godot_quat_cubic_slerp(
            self._gd_ptr, b._gd_ptr, pre_a._gd_ptr, post_b._gd_ptr, t
        )
        return ret
