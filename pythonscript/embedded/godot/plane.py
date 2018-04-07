from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_plane_alloc

from godot.vector3 import Vector3


class Plane(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_PLANE

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_plane_alloc(gdobj[0])

    @classmethod
    def build_from_vectors(cls, v1=Vector3(), v2=Vector3(), v3=Vector3()):
        cls._check_param_type("v1", v1, Vector3)
        cls._check_param_type("v2", v2, Vector3)
        cls._check_param_type("v3", v3, Vector3)
        gd_ptr = godot_plane_alloc()
        lib.godot_plane_new_with_vectors(gd_ptr, v1._gd_ptr, v2._gd_ptr, v3._gd_ptr)
        return cls.build_from_gdobj(gd_ptr, steal=True)

    @classmethod
    def build_from_reals(cls, a=0, b=0, c=0, d=0):
        cls._check_param_float("a", a)
        cls._check_param_float("b", b)
        cls._check_param_float("c", c)
        cls._check_param_float("d", d)
        gd_ptr = godot_plane_alloc()
        lib.godot_plane_new_with_reals(gd_ptr, a, b, c, d)
        return cls.build_from_gdobj(gd_ptr, steal=True)

    def __init__(self, normal=Vector3(), d=0.0):
        self._check_param_type("normal", normal, Vector3)
        self._check_param_float("d", d)
        self._gd_ptr = godot_plane_alloc()
        lib.godot_plane_new_with_normal(self._gd_ptr, normal._gd_ptr, d)

    def __eq__(self, other):
        return isinstance(other, Plane) and lib.godot_plane_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<%s(normal=%s, d=%s)>" % (type(self).__name__, self.normal, self.d)

    # Properties

    @property
    def d(self):
        return lib.godot_plane_get_d(self._gd_ptr)

    @d.setter
    def d(self, val):
        self._check_param_float("val", val)
        lib.godot_plane_set_d(self._gd_ptr, val)

    @property
    def normal(self):
        return Vector3.build_from_gdobj(lib.godot_plane_get_normal(self._gd_ptr))

    @normal.setter
    def normal(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_plane_set_normal(self._gd_ptr, val._gd_ptr)

    # Methods

    def normalized(self):
        raw = lib.godot_plane_normalized(self._gd_ptr)
        return Plane.build_from_gdobj(raw)

    def center(self):
        raw = lib.godot_plane_center(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_any_point(self):
        raw = lib.godot_plane_get_any_point(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def is_point_over(self, point):
        self._check_param_type("point", point, Vector3)
        return bool(lib.godot_plane_is_point_over(self._gd_ptr, point._gd_ptr))

    def distance_to(self, point):
        self._check_param_type("point", point, Vector3)
        return lib.godot_plane_distance_to(self._gd_ptr, point._gd_ptr)

    def has_point(self, point, epsilon):
        self._check_param_type("point", point, Vector3)
        self._check_param_float("epsilon", epsilon)
        return bool(lib.godot_plane_has_point(self._gd_ptr, point._gd_ptr, epsilon))

    def project(self, point):
        self._check_param_type("point", point, Vector3)
        raw = lib.godot_plane_project(self._gd_ptr, point._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def intersect_3(self, b, c):
        self._check_param_type("b", b, Plane)
        self._check_param_type("c", c, Plane)
        ret = Vector3()
        if not lib.godot_plane_intersect_3(
            self._gd_ptr, ret._gd_ptr, b._gd_ptr, c._gd_ptr
        ):
            return None

        return ret

    def intersects_ray(self, from_, dir):
        self._check_param_type("from_", from_, Vector3)
        self._check_param_type("dir", dir, Vector3)
        ret = Vector3()
        if not lib.godot_plane_intersects_ray(
            self._gd_ptr, ret._gd_ptr, from_._gd_ptr, dir._gd_ptr
        ):
            return None

        return ret

    def intersects_segment(self, begin, end):
        self._check_param_type("begin", begin, Vector3)
        self._check_param_type("end", end, Vector3)
        ret = Vector3()
        if not lib.godot_plane_intersects_segment(
            self._gd_ptr, ret._gd_ptr, begin._gd_ptr, end._gd_ptr
        ):
            return None

        return ret
