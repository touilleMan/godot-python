from pythonscriptcffi import lib, ffi

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_rect2_alloc
from godot.vector2 import Vector2


class Rect2(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_RECT2

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_rect2_alloc(gdobj[0])

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        self._gd_ptr = godot_rect2_alloc()
        lib.godot_rect2_new(self._gd_ptr, x, y, width, height)

    def __eq__(self, other):
        return isinstance(other, Rect2) and lib.godot_rect2_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        gd_repr = lib.godot_rect2_as_string(self._gd_ptr)
        raw_str = lib.godot_string_wide_str(ffi.addressof(gd_repr))
        return "<%s(%s)>" % (type(self).__name__, ffi.string(raw_str))

    # Properties

    @property
    def position(self):
        return Vector2.build_from_gdobj(lib.godot_rect2_get_position(self._gd_ptr))

    @property
    def size(self):
        return Vector2.build_from_gdobj(lib.godot_rect2_get_size(self._gd_ptr))

    @position.setter
    def position(self, val):
        self._check_param_type("val", val, Vector2)
        lib.godot_rect2_set_position(self._gd_ptr, val._gd_ptr)

    @size.setter
    def size(self, val):
        self._check_param_type("val", val, Vector2)
        lib.godot_rect2_set_size(self._gd_ptr, val._gd_ptr)

    # Methods

    def clip(self, b):
        self._check_param_type("b", b, Rect2)
        return Rect2.build_from_gdobj(lib.godot_rect2_clip(self._gd_ptr, b._gd_ptr))

    def encloses(self, b):
        self._check_param_type("b", b, Rect2)
        return bool(lib.godot_rect2_encloses(self._gd_ptr, b._gd_ptr))

    def expand(self, to):
        self._check_param_type("to", to, Vector2)
        return Rect2.build_from_gdobj(lib.godot_rect2_expand(self._gd_ptr, to._gd_ptr))

    def get_area(self):
        return lib.godot_rect2_get_area(self._gd_ptr)

    def grow(self, by):
        self._check_param_float("by", by)
        return Rect2.build_from_gdobj(lib.godot_rect2_grow(self._gd_ptr, by))

    def has_no_area(self):
        return bool(lib.godot_rect2_has_no_area(self._gd_ptr))

    def has_point(self, point):
        self._check_param_type("point", point, Vector2)
        return bool(lib.godot_rect2_has_point(self._gd_ptr, point._gd_ptr))

    def intersects(self, b):
        self._check_param_type("b", b, Rect2)
        return bool(lib.godot_rect2_intersects(self._gd_ptr, b._gd_ptr))

    def merge(self, b):
        self._check_param_type("b", b, Rect2)
        return Rect2.build_from_gdobj(lib.godot_rect2_merge(self._gd_ptr, b._gd_ptr))
