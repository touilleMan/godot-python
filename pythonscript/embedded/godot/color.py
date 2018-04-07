from pythonscriptcffi import lib, ffi

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_color_alloc


class Color(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_COLOR

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_color_alloc(gdobj[0])

    def __init__(self, r=0, g=0, b=0, a=None):
        self._gd_ptr = godot_color_alloc()
        if a is None:
            lib.godot_color_new_rgb(self._gd_ptr, r, g, b)
        else:
            lib.godot_color_new_rgba(self._gd_ptr, r, g, b, a)

    def __repr__(self):
        # gdstr = lib.godot_color_as_string(self._gd_ptr)
        # color = ffi.string(lib.godot_string_wide_str(ffi.addressof(gdstr)))
        return "<%s(r=%s, g=%s, b=%s, a=%s)>" % (
            type(self).__name__, self.r, self.g, self.b, self.a
        )

    def __eq__(self, other):
        return isinstance(other, Color) and lib.godot_color_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, Color):
            return lib.godot_color_operator_less(self._gd_ptr, other._gd_ptr)

        return NotImplemented

    # Properties

    @property
    def r(self):
        return lib.godot_color_get_r(self._gd_ptr)

    @r.setter
    def r(self, val):
        lib.godot_color_set_r(self._gd_ptr, val)

    @property
    def r8(self):
        return int(lib.godot_color_get_r(self._gd_ptr) * 256)

    @r8.setter
    def r8(self, val):
        lib.godot_color_set_r(self._gd_ptr, val / 256)

    @property
    def g(self):
        return lib.godot_color_get_g(self._gd_ptr)

    @g.setter
    def g(self, val):
        lib.godot_color_set_g(self._gd_ptr, val)

    @property
    def g8(self):
        return int(lib.godot_color_get_g(self._gd_ptr) * 256)

    @g8.setter
    def g8(self, val):
        lib.godot_color_set_g(self._gd_ptr, val / 256)

    @property
    def b(self):
        return lib.godot_color_get_b(self._gd_ptr)

    @b.setter
    def b(self, val):
        lib.godot_color_set_b(self._gd_ptr, val)

    @property
    def b8(self):
        return int(lib.godot_color_get_b(self._gd_ptr) * 256)

    @b8.setter
    def b8(self, val):
        lib.godot_color_set_b(self._gd_ptr, val / 256)

    @property
    def a(self):
        return lib.godot_color_get_a(self._gd_ptr)

    @a.setter
    def a(self, val):
        lib.godot_color_set_a(self._gd_ptr, val)

    @property
    def a8(self):
        return int(lib.godot_color_get_a(self._gd_ptr) * 256)

    @a8.setter
    def a8(self, val):
        lib.godot_color_set_a(self._gd_ptr, val / 256)

    @property
    def h(self):
        return lib.godot_color_get_h(self._gd_ptr)

    @property
    def s(self):
        return lib.godot_color_get_s(self._gd_ptr)

    @property
    def v(self):
        return lib.godot_color_get_v(self._gd_ptr)

    # Methods

    def to_rgba32(self):
        return lib.godot_color_to_rgba32(self._gd_ptr)

    def to_argb32(self):
        return lib.godot_color_to_argb32(self._gd_ptr)

    def gray(self):
        return lib.godot_color_gray(self._gd_ptr)

    def inverted(self):
        gd_obj = lib.godot_color_inverted(self._gd_ptr)
        return Color.build_from_gdobj(gd_obj)

    def contrasted(self):
        gd_obj = lib.godot_color_contrasted(self._gd_ptr)
        return Color.build_from_gdobj(gd_obj)

    def linear_interpolate(self, b, t):
        gd_obj = lib.godot_color_linear_interpolate(self._gd_ptr, b._gd_ptr, t)
        return Color.build_from_gdobj(gd_obj)

    def blend(self, over):
        gd_obj = lib.godot_color_blend(self._gd_ptr, over._gd_ptr)
        return Color.build_from_gdobj(gd_obj)

    def to_html(self, with_alpha=True):
        gdstr = lib.godot_color_to_html(self._gd_ptr, with_alpha)
        return ffi.string(lib.godot_string_wide_str(ffi.addressof(gdstr)))
