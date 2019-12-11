# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_color, godot_bool, godot_int, godot_real, godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj


@cython.final
cdef class Color:

    def __init__(self, godot_real r=0, godot_real g=0, godot_real b=0, a=None):
        if a is None:
            gdapi.godot_color_new_rgb(&self._gd_data, r, g, b)
        else:
            gdapi.godot_color_new_rgba(&self._gd_data, r, g, b, a)

    @staticmethod
    cdef inline Color new_rgba(godot_real r, godot_real g, godot_real b, godot_real a):
        # Call to __new__ bypasses __init__ constructor
        cdef Color ret = Color.__new__(Color)
        gdapi.godot_color_new_rgba(&ret._gd_data, r, g, b, a)
        return ret

    @staticmethod
    cdef inline Color new_rgb(godot_real r, godot_real g, godot_real b):
        # Call to __new__ bypasses __init__ constructor
        cdef Color ret = Color.__new__(Color)
        gdapi.godot_color_new_rgb(&ret._gd_data, r, g, b)
        return ret

    @staticmethod
    cdef inline Color from_ptr(const godot_color *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})>"

    # Operators

    cdef inline bint operator_equal(self, Color b):
        cdef Color ret  = Color.__new__(Color)
        return gdapi.godot_color_operator_equal(&self._gd_data, &b._gd_data)

    cdef inline bint operator_less(self, Color b):
        cdef Color ret  = Color.__new__(Color)
        return gdapi.godot_color_operator_less(&self._gd_data, &b._gd_data)

    def __lt__(self, other):
        return Color.operator_less(self, other)

    def __eq__(self, other):
        try:
            return Color.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Color.operator_equal(self, other)
        except TypeError:
            return True

    # Properties

    # RGBA

    cdef inline godot_real get_r(self):
        return gdapi.godot_color_get_r(&self._gd_data)

    cdef inline void set_r(self, godot_real val):
        gdapi.godot_color_set_r(&self._gd_data, val)

    cdef inline godot_real get_g(self):
        return gdapi.godot_color_get_g(&self._gd_data)

    cdef inline void set_g(self, godot_real val):
        gdapi.godot_color_set_g(&self._gd_data, val)

    cdef inline godot_real get_b(self):
        return gdapi.godot_color_get_b(&self._gd_data)

    cdef inline void set_b(self, godot_real val):
        gdapi.godot_color_set_b(&self._gd_data, val)

    cdef inline godot_real get_a(self):
        return gdapi.godot_color_get_a(&self._gd_data)

    cdef inline void set_a(self, godot_real val):
        gdapi.godot_color_set_a(&self._gd_data, val)

    @property
    def r(self):
        return self.get_r()

    @r.setter
    def r(self, val):
        self.set_r(val)

    @property
    def g(self):
        return self.get_g()

    @g.setter
    def g(self, val):
        self.set_g(val)

    @property
    def b(self):
        return self.get_b()

    @b.setter
    def b(self, val):
        self.set_b(val)

    @property
    def a(self):
        return self.get_a()

    @a.setter
    def a(self, val):
        self.set_a(val)

    # RGBA8

    cdef inline uint8_t get_r8(self):
        return <uint8_t>(gdapi.godot_color_get_r(&self._gd_data) * 256)

    cdef inline void set_r8(self, uint8_t val):
        gdapi.godot_color_set_r(&self._gd_data, (<godot_real>val) / 256)

    cdef inline uint8_t get_g8(self):
        return <uint8_t>(gdapi.godot_color_get_g(&self._gd_data) * 256)

    cdef inline void set_g8(self, uint8_t val):
        gdapi.godot_color_set_g(&self._gd_data, (<godot_real>val) / 256)

    cdef inline uint8_t get_b8(self):
        return <uint8_t>(gdapi.godot_color_get_b(&self._gd_data) * 256)

    cdef inline void set_b8(self, uint8_t val):
        gdapi.godot_color_set_b(&self._gd_data, (<godot_real>val) / 256)

    cdef inline uint8_t get_a8(self):
        return <uint8_t>(gdapi.godot_color_get_a(&self._gd_data) * 256)

    cdef inline void set_a8(self, uint8_t val):
        gdapi.godot_color_set_a(&self._gd_data, (<godot_real>val) / 256)

    @property
    def r8(self):
        return self.get_r8()

    @r8.setter
    def r8(self, val):
        self.set_r8(val)

    @property
    def g8(self):
        return self.get_g8()

    @g8.setter
    def g8(self, val):
        self.set_g8(val)

    @property
    def b8(self):
        return self.get_b8()

    @b8.setter
    def b8(self, val):
        self.set_b8(val)

    @property
    def a8(self):
        return self.get_a8()

    @a8.setter
    def a8(self, val):
        self.set_a8(val)

    # HSV

    cdef inline godot_real get_h(self):
        return gdapi.godot_color_get_h(&self._gd_data)

    cdef inline godot_real get_s(self):
        return gdapi.godot_color_get_s(&self._gd_data)

    cdef inline godot_real get_v(self):
        return gdapi.godot_color_get_v(&self._gd_data)

    @property
    def h(self):
        return self.get_h()

    @property
    def s(self):
        return self.get_s()

    @property
    def v(self):
        return self.get_v()

    # Methods

    cpdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_color_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline godot_int to_rgba32(self):
        return gdapi.godot_color_to_rgba32(&self._gd_data)

    cpdef inline godot_int to_abgr32(self):
        return gdapi11.godot_color_to_abgr32(&self._gd_data)

    cpdef inline godot_int to_abgr64(self):
        return gdapi11.godot_color_to_abgr64(&self._gd_data)

    cpdef inline godot_int to_argb64(self):
        return gdapi11.godot_color_to_argb64(&self._gd_data)

    cpdef inline godot_int to_rgba64(self):
        return gdapi11.godot_color_to_rgba64(&self._gd_data)

    cpdef inline godot_int to_argb32(self):
        return gdapi.godot_color_to_argb32(&self._gd_data)

    cpdef inline godot_real gray(self):
        return gdapi.godot_color_gray(&self._gd_data)

    cpdef inline Color inverted(self):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi.godot_color_inverted(&self._gd_data)
        return ret

    cpdef inline Color contrasted(self):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi.godot_color_contrasted(&self._gd_data)
        return ret

    cpdef inline Color linear_interpolate(self, Color b, godot_real t):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi.godot_color_linear_interpolate(&self._gd_data, &b._gd_data, t)
        return ret

    cpdef inline Color blend(self, Color over):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi.godot_color_blend(&self._gd_data, &over._gd_data)
        return ret

    cpdef inline Color darkened(self, godot_real amount):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi11.godot_color_darkened(&self._gd_data, amount)
        return ret

    cpdef inline Color from_hsv(self, godot_real h, godot_real s, godot_real v, godot_real a=1):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi11.godot_color_from_hsv(&self._gd_data, h, s, v, a)
        return ret

    cpdef inline Color lightened(self, godot_real amount):
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = gdapi11.godot_color_lightened(&self._gd_data, amount)
        return ret

    cpdef inline str to_html(self, godot_bool with_alpha=True):
        cdef godot_string var_ret = gdapi.godot_color_to_html(&self._gd_data, with_alpha)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    # TODO: gdapi should expose those constants to us
    GRAY = Color.new_rgb(<godot_real>0.75, <godot_real>0.75, <godot_real>0.75)
    ALICEBLUE = Color.new_rgb(<godot_real>0.94, <godot_real>0.97, <godot_real>1)
    ANTIQUEWHITE = Color.new_rgb(<godot_real>0.98, <godot_real>0.92, <godot_real>0.84)
    AQUA = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>1)
    AQUAMARINE = Color.new_rgb(<godot_real>0.5, <godot_real>1, <godot_real>0.83)
    AZURE = Color.new_rgb(<godot_real>0.94, <godot_real>1, <godot_real>1)
    BEIGE = Color.new_rgb(<godot_real>0.96, <godot_real>0.96, <godot_real>0.86)
    BISQUE = Color.new_rgb(<godot_real>1, <godot_real>0.89, <godot_real>0.77)
    BLACK = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0)
    BLANCHEDALMOND = Color.new_rgb(<godot_real>1, <godot_real>0.92, <godot_real>0.8)
    BLUE = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>1)
    BLUEVIOLET = Color.new_rgb(<godot_real>0.54, <godot_real>0.17, <godot_real>0.89)
    BROWN = Color.new_rgb(<godot_real>0.65, <godot_real>0.16, <godot_real>0.16)
    BURLYWOOD = Color.new_rgb(<godot_real>0.87, <godot_real>0.72, <godot_real>0.53)
    CADETBLUE = Color.new_rgb(<godot_real>0.37, <godot_real>0.62, <godot_real>0.63)
    CHARTREUSE = Color.new_rgb(<godot_real>0.5, <godot_real>1, <godot_real>0)
    CHOCOLATE = Color.new_rgb(<godot_real>0.82, <godot_real>0.41, <godot_real>0.12)
    CORAL = Color.new_rgb(<godot_real>1, <godot_real>0.5, <godot_real>0.31)
    CORNFLOWER = Color.new_rgb(<godot_real>0.39, <godot_real>0.58, <godot_real>0.93)
    CORNSILK = Color.new_rgb(<godot_real>1, <godot_real>0.97, <godot_real>0.86)
    CRIMSON = Color.new_rgb(<godot_real>0.86, <godot_real>0.08, <godot_real>0.24)
    CYAN = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>1)
    DARKBLUE = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0.55)
    DARKCYAN = Color.new_rgb(<godot_real>0, <godot_real>0.55, <godot_real>0.55)
    DARKGOLDENROD = Color.new_rgb(<godot_real>0.72, <godot_real>0.53, <godot_real>0.04)
    DARKGRAY = Color.new_rgb(<godot_real>0.66, <godot_real>0.66, <godot_real>0.66)
    DARKGREEN = Color.new_rgb(<godot_real>0, <godot_real>0.39, <godot_real>0)
    DARKKHAKI = Color.new_rgb(<godot_real>0.74, <godot_real>0.72, <godot_real>0.42)
    DARKMAGENTA = Color.new_rgb(<godot_real>0.55, <godot_real>0, <godot_real>0.55)
    DARKOLIVEGREEN = Color.new_rgb(<godot_real>0.33, <godot_real>0.42, <godot_real>0.18)
    DARKORANGE = Color.new_rgb(<godot_real>1, <godot_real>0.55, <godot_real>0)
    DARKORCHID = Color.new_rgb(<godot_real>0.6, <godot_real>0.2, <godot_real>0.8)
    DARKRED = Color.new_rgb(<godot_real>0.55, <godot_real>0, <godot_real>0)
    DARKSALMON = Color.new_rgb(<godot_real>0.91, <godot_real>0.59, <godot_real>0.48)
    DARKSEAGREEN = Color.new_rgb(<godot_real>0.56, <godot_real>0.74, <godot_real>0.56)
    DARKSLATEBLUE = Color.new_rgb(<godot_real>0.28, <godot_real>0.24, <godot_real>0.55)
    DARKSLATEGRAY = Color.new_rgb(<godot_real>0.18, <godot_real>0.31, <godot_real>0.31)
    DARKTURQUOISE = Color.new_rgb(<godot_real>0, <godot_real>0.81, <godot_real>0.82)
    DARKVIOLET = Color.new_rgb(<godot_real>0.58, <godot_real>0, <godot_real>0.83)
    DEEPPINK = Color.new_rgb(<godot_real>1, <godot_real>0.08, <godot_real>0.58)
    DEEPSKYBLUE = Color.new_rgb(<godot_real>0, <godot_real>0.75, <godot_real>1)
    DIMGRAY = Color.new_rgb(<godot_real>0.41, <godot_real>0.41, <godot_real>0.41)
    DODGERBLUE = Color.new_rgb(<godot_real>0.12, <godot_real>0.56, <godot_real>1)
    FIREBRICK = Color.new_rgb(<godot_real>0.7, <godot_real>0.13, <godot_real>0.13)
    FLORALWHITE = Color.new_rgb(<godot_real>1, <godot_real>0.98, <godot_real>0.94)
    FORESTGREEN = Color.new_rgb(<godot_real>0.13, <godot_real>0.55, <godot_real>0.13)
    FUCHSIA = Color.new_rgb(<godot_real>1, <godot_real>0, <godot_real>1)
    GAINSBORO = Color.new_rgb(<godot_real>0.86, <godot_real>0.86, <godot_real>0.86)
    GHOSTWHITE = Color.new_rgb(<godot_real>0.97, <godot_real>0.97, <godot_real>1)
    GOLD = Color.new_rgb(<godot_real>1, <godot_real>0.84, <godot_real>0)
    GOLDENROD = Color.new_rgb(<godot_real>0.85, <godot_real>0.65, <godot_real>0.13)
    GREEN = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>0)
    GREENYELLOW = Color.new_rgb(<godot_real>0.68, <godot_real>1, <godot_real>0.18)
    HONEYDEW = Color.new_rgb(<godot_real>0.94, <godot_real>1, <godot_real>0.94)
    HOTPINK = Color.new_rgb(<godot_real>1, <godot_real>0.41, <godot_real>0.71)
    INDIANRED = Color.new_rgb(<godot_real>0.8, <godot_real>0.36, <godot_real>0.36)
    INDIGO = Color.new_rgb(<godot_real>0.29, <godot_real>0, <godot_real>0.51)
    IVORY = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>0.94)
    KHAKI = Color.new_rgb(<godot_real>0.94, <godot_real>0.9, <godot_real>0.55)
    LAVENDER = Color.new_rgb(<godot_real>0.9, <godot_real>0.9, <godot_real>0.98)
    LAVENDERBLUSH = Color.new_rgb(<godot_real>1, <godot_real>0.94, <godot_real>0.96)
    LAWNGREEN = Color.new_rgb(<godot_real>0.49, <godot_real>0.99, <godot_real>0)
    LEMONCHIFFON = Color.new_rgb(<godot_real>1, <godot_real>0.98, <godot_real>0.8)
    LIGHTBLUE = Color.new_rgb(<godot_real>0.68, <godot_real>0.85, <godot_real>0.9)
    LIGHTCORAL = Color.new_rgb(<godot_real>0.94, <godot_real>0.5, <godot_real>0.5)
    LIGHTCYAN = Color.new_rgb(<godot_real>0.88, <godot_real>1, <godot_real>1)
    LIGHTGOLDENROD = Color.new_rgb(<godot_real>0.98, <godot_real>0.98, <godot_real>0.82)
    LIGHTGRAY = Color.new_rgb(<godot_real>0.83, <godot_real>0.83, <godot_real>0.83)
    LIGHTGREEN = Color.new_rgb(<godot_real>0.56, <godot_real>0.93, <godot_real>0.56)
    LIGHTPINK = Color.new_rgb(<godot_real>1, <godot_real>0.71, <godot_real>0.76)
    LIGHTSALMON = Color.new_rgb(<godot_real>1, <godot_real>0.63, <godot_real>0.48)
    LIGHTSEAGREEN = Color.new_rgb(<godot_real>0.13, <godot_real>0.7, <godot_real>0.67)
    LIGHTSKYBLUE = Color.new_rgb(<godot_real>0.53, <godot_real>0.81, <godot_real>0.98)
    LIGHTSLATEGRAY = Color.new_rgb(<godot_real>0.47, <godot_real>0.53, <godot_real>0.6)
    LIGHTSTEELBLUE = Color.new_rgb(<godot_real>0.69, <godot_real>0.77, <godot_real>0.87)
    LIGHTYELLOW = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>0.88)
    LIME = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>0)
    LIMEGREEN = Color.new_rgb(<godot_real>0.2, <godot_real>0.8, <godot_real>0.2)
    LINEN = Color.new_rgb(<godot_real>0.98, <godot_real>0.94, <godot_real>0.9)
    MAGENTA = Color.new_rgb(<godot_real>1, <godot_real>0, <godot_real>1)
    MAROON = Color.new_rgb(<godot_real>0.69, <godot_real>0.19, <godot_real>0.38)
    MEDIUMAQUAMARINE = Color.new_rgb(<godot_real>0.4, <godot_real>0.8, <godot_real>0.67)
    MEDIUMBLUE = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0.8)
    MEDIUMORCHID = Color.new_rgb(<godot_real>0.73, <godot_real>0.33, <godot_real>0.83)
    MEDIUMPURPLE = Color.new_rgb(<godot_real>0.58, <godot_real>0.44, <godot_real>0.86)
    MEDIUMSEAGREEN = Color.new_rgb(<godot_real>0.24, <godot_real>0.7, <godot_real>0.44)
    MEDIUMSLATEBLUE = Color.new_rgb(<godot_real>0.48, <godot_real>0.41, <godot_real>0.93)
    MEDIUMSPRINGGREEN = Color.new_rgb(<godot_real>0, <godot_real>0.98, <godot_real>0.6)
    MEDIUMTURQUOISE = Color.new_rgb(<godot_real>0.28, <godot_real>0.82, <godot_real>0.8)
    MEDIUMVIOLETRED = Color.new_rgb(<godot_real>0.78, <godot_real>0.08, <godot_real>0.52)
    MIDNIGHTBLUE = Color.new_rgb(<godot_real>0.1, <godot_real>0.1, <godot_real>0.44)
    MINTCREAM = Color.new_rgb(<godot_real>0.96, <godot_real>1, <godot_real>0.98)
    MISTYROSE = Color.new_rgb(<godot_real>1, <godot_real>0.89, <godot_real>0.88)
    MOCCASIN = Color.new_rgb(<godot_real>1, <godot_real>0.89, <godot_real>0.71)
    NAVAJOWHITE = Color.new_rgb(<godot_real>1, <godot_real>0.87, <godot_real>0.68)
    NAVYBLUE = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0.5)
    OLDLACE = Color.new_rgb(<godot_real>0.99, <godot_real>0.96, <godot_real>0.9)
    OLIVE = Color.new_rgb(<godot_real>0.5, <godot_real>0.5, <godot_real>0)
    OLIVEDRAB = Color.new_rgb(<godot_real>0.42, <godot_real>0.56, <godot_real>0.14)
    ORANGE = Color.new_rgb(<godot_real>1, <godot_real>0.65, <godot_real>0)
    ORANGERED = Color.new_rgb(<godot_real>1, <godot_real>0.27, <godot_real>0)
    ORCHID = Color.new_rgb(<godot_real>0.85, <godot_real>0.44, <godot_real>0.84)
    PALEGOLDENROD = Color.new_rgb(<godot_real>0.93, <godot_real>0.91, <godot_real>0.67)
    PALEGREEN = Color.new_rgb(<godot_real>0.6, <godot_real>0.98, <godot_real>0.6)
    PALETURQUOISE = Color.new_rgb(<godot_real>0.69, <godot_real>0.93, <godot_real>0.93)
    PALEVIOLETRED = Color.new_rgb(<godot_real>0.86, <godot_real>0.44, <godot_real>0.58)
    PAPAYAWHIP = Color.new_rgb(<godot_real>1, <godot_real>0.94, <godot_real>0.84)
    PEACHPUFF = Color.new_rgb(<godot_real>1, <godot_real>0.85, <godot_real>0.73)
    PERU = Color.new_rgb(<godot_real>0.8, <godot_real>0.52, <godot_real>0.25)
    PINK = Color.new_rgb(<godot_real>1, <godot_real>0.75, <godot_real>0.8)
    PLUM = Color.new_rgb(<godot_real>0.87, <godot_real>0.63, <godot_real>0.87)
    POWDERBLUE = Color.new_rgb(<godot_real>0.69, <godot_real>0.88, <godot_real>0.9)
    PURPLE = Color.new_rgb(<godot_real>0.63, <godot_real>0.13, <godot_real>0.94)
    REBECCAPURPLE = Color.new_rgb(<godot_real>0.4, <godot_real>0.2, <godot_real>0.6)
    RED = Color.new_rgb(<godot_real>1, <godot_real>0, <godot_real>0)
    ROSYBROWN = Color.new_rgb(<godot_real>0.74, <godot_real>0.56, <godot_real>0.56)
    ROYALBLUE = Color.new_rgb(<godot_real>0.25, <godot_real>0.41, <godot_real>0.88)
    SADDLEBROWN = Color.new_rgb(<godot_real>0.55, <godot_real>0.27, <godot_real>0.07)
    SALMON = Color.new_rgb(<godot_real>0.98, <godot_real>0.5, <godot_real>0.45)
    SANDYBROWN = Color.new_rgb(<godot_real>0.96, <godot_real>0.64, <godot_real>0.38)
    SEAGREEN = Color.new_rgb(<godot_real>0.18, <godot_real>0.55, <godot_real>0.34)
    SEASHELL = Color.new_rgb(<godot_real>1, <godot_real>0.96, <godot_real>0.93)
    SIENNA = Color.new_rgb(<godot_real>0.63, <godot_real>0.32, <godot_real>0.18)
    SILVER = Color.new_rgb(<godot_real>0.75, <godot_real>0.75, <godot_real>0.75)
    SKYBLUE = Color.new_rgb(<godot_real>0.53, <godot_real>0.81, <godot_real>0.92)
    SLATEBLUE = Color.new_rgb(<godot_real>0.42, <godot_real>0.35, <godot_real>0.8)
    SLATEGRAY = Color.new_rgb(<godot_real>0.44, <godot_real>0.5, <godot_real>0.56)
    SNOW = Color.new_rgb(<godot_real>1, <godot_real>0.98, <godot_real>0.98)
    SPRINGGREEN = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>0.5)
    STEELBLUE = Color.new_rgb(<godot_real>0.27, <godot_real>0.51, <godot_real>0.71)
    TAN = Color.new_rgb(<godot_real>0.82, <godot_real>0.71, <godot_real>0.55)
    TEAL = Color.new_rgb(<godot_real>0, <godot_real>0.5, <godot_real>0.5)
    THISTLE = Color.new_rgb(<godot_real>0.85, <godot_real>0.75, <godot_real>0.85)
    TOMATO = Color.new_rgb(<godot_real>1, <godot_real>0.39, <godot_real>0.28)
    TURQUOISE = Color.new_rgb(<godot_real>0.25, <godot_real>0.88, <godot_real>0.82)
    VIOLET = Color.new_rgb(<godot_real>0.93, <godot_real>0.51, <godot_real>0.93)
    WEBGRAY = Color.new_rgb(<godot_real>0.5, <godot_real>0.5, <godot_real>0.5)
    WEBGREEN = Color.new_rgb(<godot_real>0, <godot_real>0.5, <godot_real>0)
    WEBMAROON = Color.new_rgb(<godot_real>0.5, <godot_real>0, <godot_real>0)
    WEBPURPLE = Color.new_rgb(<godot_real>0.5, <godot_real>0, <godot_real>0.5)
    WHEAT = Color.new_rgb(<godot_real>0.96, <godot_real>0.87, <godot_real>0.7)
    WHITE = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>1)
    WHITESMOKE = Color.new_rgb(<godot_real>0.96, <godot_real>0.96, <godot_real>0.96)
    YELLOW = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>0)
    YELLOWGREEN = Color.new_rgb(<godot_real>0.6, <godot_real>0.8, <godot_real>0.2)
