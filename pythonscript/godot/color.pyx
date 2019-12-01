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
    cdef Color new_rgba(godot_real r, godot_real g, godot_real b, godot_real a):
        # Call to __new__ bypasses __init__ constructor
        cdef Color ret = Color.__new__(Color)
        gdapi.godot_color_new_rgba(&ret._gd_data, r, g, b, a)
        return ret

    @staticmethod
    cdef Color new_rgb(godot_real r, godot_real g, godot_real b):
        # Call to __new__ bypasses __init__ constructor
        cdef Color ret = Color.__new__(Color)
        gdapi.godot_color_new_rgb(&ret._gd_data, r, g, b)
        return ret

    @staticmethod
    cdef Color from_ptr(const godot_color *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Color ret = Color.__new__(Color)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Color({self.as_string()})>"

    # Operators

    cdef inline bint operator_equal(self, Color b):
        cdef Color ret  = Color.__new__(Color)
        return gdapi.godot_color_operator_equal(&self._gd_data, &b._gd_data)

    cdef inline bint operator_less(self, Color b):
        cdef Color ret  = Color.__new__(Color)
        return gdapi.godot_color_operator_less(&self._gd_data, &b._gd_data)

    def __lt__(self, other):
        cdef Color _other = <Color?>other
        return self.operator_less(_other)

    def __eq__(self, other):
        cdef Color _other = <Color?>other
        return self.operator_equal(_other)

    def __ne__(self, other):
        cdef Color _other = <Color?>other
        return not self.operator_equal(_other)

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
        return (<uint8_t>gdapi.godot_color_get_r(&self._gd_data) * 256)

    cdef inline void set_r8(self, uint8_t val):
        gdapi.godot_color_set_r(&self._gd_data, (<godot_real>val) / 256)

    cdef inline uint8_t get_g8(self):
        return (<uint8_t>gdapi.godot_color_get_g(&self._gd_data) * 256)

    cdef inline void set_g8(self, uint8_t val):
        gdapi.godot_color_set_g(&self._gd_data, (<godot_real>val) / 256)

    cdef inline uint8_t get_b8(self):
        return (<uint8_t>gdapi.godot_color_get_b(&self._gd_data) * 256)

    cdef inline void set_b8(self, uint8_t val):
        gdapi.godot_color_set_b(&self._gd_data, (<godot_real>val) / 256)

    cdef inline uint8_t get_a8(self):
        return (<uint8_t>gdapi.godot_color_get_a(&self._gd_data) * 256)

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
    gray = Color.new_rgb(0.75, 0.75, 0.75)
    aliceblue = Color.new_rgb(0.94, 0.97, 1)
    antiquewhite = Color.new_rgb(0.98, 0.92, 0.84)
    aqua = Color.new_rgb(0, 1, 1)
    aquamarine = Color.new_rgb(0.5, 1, 0.83)
    azure = Color.new_rgb(0.94, 1, 1)
    beige = Color.new_rgb(0.96, 0.96, 0.86)
    bisque = Color.new_rgb(1, 0.89, 0.77)
    black = Color.new_rgb(0, 0, 0)
    blanchedalmond = Color.new_rgb(1, 0.92, 0.8)
    blue = Color.new_rgb(0, 0, 1)
    blueviolet = Color.new_rgb(0.54, 0.17, 0.89)
    brown = Color.new_rgb(0.65, 0.16, 0.16)
    burlywood = Color.new_rgb(0.87, 0.72, 0.53)
    cadetblue = Color.new_rgb(0.37, 0.62, 0.63)
    chartreuse = Color.new_rgb(0.5, 1, 0)
    chocolate = Color.new_rgb(0.82, 0.41, 0.12)
    coral = Color.new_rgb(1, 0.5, 0.31)
    cornflower = Color.new_rgb(0.39, 0.58, 0.93)
    cornsilk = Color.new_rgb(1, 0.97, 0.86)
    crimson = Color.new_rgb(0.86, 0.08, 0.24)
    cyan = Color.new_rgb(0, 1, 1)
    darkblue = Color.new_rgb(0, 0, 0.55)
    darkcyan = Color.new_rgb(0, 0.55, 0.55)
    darkgoldenrod = Color.new_rgb(0.72, 0.53, 0.04)
    darkgray = Color.new_rgb(0.66, 0.66, 0.66)
    darkgreen = Color.new_rgb(0, 0.39, 0)
    darkkhaki = Color.new_rgb(0.74, 0.72, 0.42)
    darkmagenta = Color.new_rgb(0.55, 0, 0.55)
    darkolivegreen = Color.new_rgb(0.33, 0.42, 0.18)
    darkorange = Color.new_rgb(1, 0.55, 0)
    darkorchid = Color.new_rgb(0.6, 0.2, 0.8)
    darkred = Color.new_rgb(0.55, 0, 0)
    darksalmon = Color.new_rgb(0.91, 0.59, 0.48)
    darkseagreen = Color.new_rgb(0.56, 0.74, 0.56)
    darkslateblue = Color.new_rgb(0.28, 0.24, 0.55)
    darkslategray = Color.new_rgb(0.18, 0.31, 0.31)
    darkturquoise = Color.new_rgb(0, 0.81, 0.82)
    darkviolet = Color.new_rgb(0.58, 0, 0.83)
    deeppink = Color.new_rgb(1, 0.08, 0.58)
    deepskyblue = Color.new_rgb(0, 0.75, 1)
    dimgray = Color.new_rgb(0.41, 0.41, 0.41)
    dodgerblue = Color.new_rgb(0.12, 0.56, 1)
    firebrick = Color.new_rgb(0.7, 0.13, 0.13)
    floralwhite = Color.new_rgb(1, 0.98, 0.94)
    forestgreen = Color.new_rgb(0.13, 0.55, 0.13)
    fuchsia = Color.new_rgb(1, 0, 1)
    gainsboro = Color.new_rgb(0.86, 0.86, 0.86)
    ghostwhite = Color.new_rgb(0.97, 0.97, 1)
    gold = Color.new_rgb(1, 0.84, 0)
    goldenrod = Color.new_rgb(0.85, 0.65, 0.13)
    green = Color.new_rgb(0, 1, 0)
    greenyellow = Color.new_rgb(0.68, 1, 0.18)
    honeydew = Color.new_rgb(0.94, 1, 0.94)
    hotpink = Color.new_rgb(1, 0.41, 0.71)
    indianred = Color.new_rgb(0.8, 0.36, 0.36)
    indigo = Color.new_rgb(0.29, 0, 0.51)
    ivory = Color.new_rgb(1, 1, 0.94)
    khaki = Color.new_rgb(0.94, 0.9, 0.55)
    lavender = Color.new_rgb(0.9, 0.9, 0.98)
    lavenderblush = Color.new_rgb(1, 0.94, 0.96)
    lawngreen = Color.new_rgb(0.49, 0.99, 0)
    lemonchiffon = Color.new_rgb(1, 0.98, 0.8)
    lightblue = Color.new_rgb(0.68, 0.85, 0.9)
    lightcoral = Color.new_rgb(0.94, 0.5, 0.5)
    lightcyan = Color.new_rgb(0.88, 1, 1)
    lightgoldenrod = Color.new_rgb(0.98, 0.98, 0.82)
    lightgray = Color.new_rgb(0.83, 0.83, 0.83)
    lightgreen = Color.new_rgb(0.56, 0.93, 0.56)
    lightpink = Color.new_rgb(1, 0.71, 0.76)
    lightsalmon = Color.new_rgb(1, 0.63, 0.48)
    lightseagreen = Color.new_rgb(0.13, 0.7, 0.67)
    lightskyblue = Color.new_rgb(0.53, 0.81, 0.98)
    lightslategray = Color.new_rgb(0.47, 0.53, 0.6)
    lightsteelblue = Color.new_rgb(0.69, 0.77, 0.87)
    lightyellow = Color.new_rgb(1, 1, 0.88)
    lime = Color.new_rgb(0, 1, 0)
    limegreen = Color.new_rgb(0.2, 0.8, 0.2)
    linen = Color.new_rgb(0.98, 0.94, 0.9)
    magenta = Color.new_rgb(1, 0, 1)
    maroon = Color.new_rgb(0.69, 0.19, 0.38)
    mediumaquamarine = Color.new_rgb(0.4, 0.8, 0.67)
    mediumblue = Color.new_rgb(0, 0, 0.8)
    mediumorchid = Color.new_rgb(0.73, 0.33, 0.83)
    mediumpurple = Color.new_rgb(0.58, 0.44, 0.86)
    mediumseagreen = Color.new_rgb(0.24, 0.7, 0.44)
    mediumslateblue = Color.new_rgb(0.48, 0.41, 0.93)
    mediumspringgreen = Color.new_rgb(0, 0.98, 0.6)
    mediumturquoise = Color.new_rgb(0.28, 0.82, 0.8)
    mediumvioletred = Color.new_rgb(0.78, 0.08, 0.52)
    midnightblue = Color.new_rgb(0.1, 0.1, 0.44)
    mintcream = Color.new_rgb(0.96, 1, 0.98)
    mistyrose = Color.new_rgb(1, 0.89, 0.88)
    moccasin = Color.new_rgb(1, 0.89, 0.71)
    navajowhite = Color.new_rgb(1, 0.87, 0.68)
    navyblue = Color.new_rgb(0, 0, 0.5)
    oldlace = Color.new_rgb(0.99, 0.96, 0.9)
    olive = Color.new_rgb(0.5, 0.5, 0)
    olivedrab = Color.new_rgb(0.42, 0.56, 0.14)
    orange = Color.new_rgb(1, 0.65, 0)
    orangered = Color.new_rgb(1, 0.27, 0)
    orchid = Color.new_rgb(0.85, 0.44, 0.84)
    palegoldenrod = Color.new_rgb(0.93, 0.91, 0.67)
    palegreen = Color.new_rgb(0.6, 0.98, 0.6)
    paleturquoise = Color.new_rgb(0.69, 0.93, 0.93)
    palevioletred = Color.new_rgb(0.86, 0.44, 0.58)
    papayawhip = Color.new_rgb(1, 0.94, 0.84)
    peachpuff = Color.new_rgb(1, 0.85, 0.73)
    peru = Color.new_rgb(0.8, 0.52, 0.25)
    pink = Color.new_rgb(1, 0.75, 0.8)
    plum = Color.new_rgb(0.87, 0.63, 0.87)
    powderblue = Color.new_rgb(0.69, 0.88, 0.9)
    purple = Color.new_rgb(0.63, 0.13, 0.94)
    rebeccapurple = Color.new_rgb(0.4, 0.2, 0.6)
    red = Color.new_rgb(1, 0, 0)
    rosybrown = Color.new_rgb(0.74, 0.56, 0.56)
    royalblue = Color.new_rgb(0.25, 0.41, 0.88)
    saddlebrown = Color.new_rgb(0.55, 0.27, 0.07)
    salmon = Color.new_rgb(0.98, 0.5, 0.45)
    sandybrown = Color.new_rgb(0.96, 0.64, 0.38)
    seagreen = Color.new_rgb(0.18, 0.55, 0.34)
    seashell = Color.new_rgb(1, 0.96, 0.93)
    sienna = Color.new_rgb(0.63, 0.32, 0.18)
    silver = Color.new_rgb(0.75, 0.75, 0.75)
    skyblue = Color.new_rgb(0.53, 0.81, 0.92)
    slateblue = Color.new_rgb(0.42, 0.35, 0.8)
    slategray = Color.new_rgb(0.44, 0.5, 0.56)
    snow = Color.new_rgb(1, 0.98, 0.98)
    springgreen = Color.new_rgb(0, 1, 0.5)
    steelblue = Color.new_rgb(0.27, 0.51, 0.71)
    tan = Color.new_rgb(0.82, 0.71, 0.55)
    teal = Color.new_rgb(0, 0.5, 0.5)
    thistle = Color.new_rgb(0.85, 0.75, 0.85)
    tomato = Color.new_rgb(1, 0.39, 0.28)
    turquoise = Color.new_rgb(0.25, 0.88, 0.82)
    violet = Color.new_rgb(0.93, 0.51, 0.93)
    webgray = Color.new_rgb(0.5, 0.5, 0.5)
    webgreen = Color.new_rgb(0, 0.5, 0)
    webmaroon = Color.new_rgb(0.5, 0, 0)
    webpurple = Color.new_rgb(0.5, 0, 0.5)
    wheat = Color.new_rgb(0.96, 0.87, 0.7)
    white = Color.new_rgb(1, 1, 1)
    whitesmoke = Color.new_rgb(0.96, 0.96, 0.96)
    yellow = Color.new_rgb(1, 1, 0)
    yellowgreen = Color.new_rgb(0.6, 0.8, 0.2)
