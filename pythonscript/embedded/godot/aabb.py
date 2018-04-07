from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_aabb_alloc
from godot.vector3 import Vector3


class AABB(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_AABB

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_aabb_alloc(gdobj[0])

    def __init__(self, position=Vector3(), size=Vector3()):
        self._check_param_type("position", position, Vector3)
        self._check_param_type("size", size, Vector3)
        self._gd_ptr = godot_aabb_alloc()
        lib.godot_aabb_new(self._gd_ptr, position._gd_ptr, size._gd_ptr)

    def __eq__(self, other):
        return isinstance(other, AABB) and lib.godot_aabb_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<%s(position=%s, size=%s)>" % (
            type(self).__name__, self.position, self.size
        )

    # Properties

    @property
    def position(self):
        return Vector3.build_from_gdobj(lib.godot_aabb_get_position(self._gd_ptr))

    @position.setter
    def position(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_aabb_set_position(self._gd_ptr, val._gd_ptr)

    @property
    def size(self):
        return Vector3.build_from_gdobj(lib.godot_aabb_get_size(self._gd_ptr))

    @size.setter
    def size(self, val):
        self._check_param_type("val", val, Vector3)
        lib.godot_aabb_set_size(self._gd_ptr, val._gd_ptr)

    # Methods

    def get_area(self):
        return lib.godot_aabb_get_area(self._gd_ptr)

    def has_no_area(self):
        return bool(lib.godot_aabb_has_no_area(self._gd_ptr))

    def has_no_surface(self):
        return bool(lib.godot_aabb_has_no_surface(self._gd_ptr))

    def intersects(self, with_):
        return bool(lib.godot_aabb_intersects(self._gd_ptr, with_._gd_ptr))

    def encloses(self, with_):
        return bool(lib.godot_aabb_encloses(self._gd_ptr, with_._gd_ptr))

    def merge(self, with_):
        raw = lib.godot_aabb_merge(self._gd_ptr, with_._gd_ptr)
        return AABB.build_from_gdobj(raw)

    def intersection(self, with_):
        raw = lib.godot_aabb_intersection(self._gd_ptr, with_._gd_ptr)
        return AABB.build_from_gdobj(raw)

    def intersects_plane(self, plane):
        return bool(lib.godot_aabb_intersects_plane(self._gd_ptr, plane._gd_ptr))

    def intersects_segment(self, from_, to):
        return bool(
            lib.godot_aabb_intersects_segment(self._gd_ptr, from_._gd_ptr, to._gd_ptr)
        )

    def has_point(self, point):
        return bool(lib.godot_aabb_has_point(self._gd_ptr, point._gd_ptr))

    def get_support(self, dir):
        raw = lib.godot_aabb_get_support(self._gd_ptr, dir._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_longest_axis(self):
        raw = lib.godot_aabb_get_longest_axis(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_longest_axis_index(self):
        return lib.godot_aabb_get_longest_axis_index(self._gd_ptr)

    def get_longest_axis_size(self):
        return lib.godot_aabb_get_longest_axis_size(self._gd_ptr)

    def get_shortest_axis(self):
        raw = lib.godot_aabb_get_shortest_axis(self._gd_ptr)
        return Vector3.build_from_gdobj(raw)

    def get_shortest_axis_index(self):
        return lib.godot_aabb_get_shortest_axis_index(self._gd_ptr)

    def get_shortest_axis_size(self):
        return lib.godot_aabb_get_shortest_axis_size(self._gd_ptr)

    def expand(self, to_point):
        raw = lib.godot_aabb_expand(self._gd_ptr, to_point._gd_ptr)
        return AABB.build_from_gdobj(raw)

    def grow(self, by):
        raw = lib.godot_aabb_grow(self._gd_ptr, by)
        return AABB.build_from_gdobj(raw)

    def get_endpoint(self, idx):
        raw = lib.godot_aabb_get_endpoint(self._gd_ptr, idx)
        return Vector3.build_from_gdobj(raw)
