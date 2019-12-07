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
    gray = Color.new_rgb(<godot_real>0.75, <godot_real>0.75, <godot_real>0.75)
    aliceblue = Color.new_rgb(<godot_real>0.94, <godot_real>0.97, <godot_real>1)
    antiquewhite = Color.new_rgb(<godot_real>0.98, <godot_real>0.92, <godot_real>0.84)
    aqua = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>1)
    aquamarine = Color.new_rgb(<godot_real>0.5, <godot_real>1, <godot_real>0.83)
    azure = Color.new_rgb(<godot_real>0.94, <godot_real>1, <godot_real>1)
    beige = Color.new_rgb(<godot_real>0.96, <godot_real>0.96, <godot_real>0.86)
    bisque = Color.new_rgb(<godot_real>1, <godot_real>0.89, <godot_real>0.77)
    black = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0)
    blanchedalmond = Color.new_rgb(<godot_real>1, <godot_real>0.92, <godot_real>0.8)
    blue = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>1)
    blueviolet = Color.new_rgb(<godot_real>0.54, <godot_real>0.17, <godot_real>0.89)
    brown = Color.new_rgb(<godot_real>0.65, <godot_real>0.16, <godot_real>0.16)
    burlywood = Color.new_rgb(<godot_real>0.87, <godot_real>0.72, <godot_real>0.53)
    cadetblue = Color.new_rgb(<godot_real>0.37, <godot_real>0.62, <godot_real>0.63)
    chartreuse = Color.new_rgb(<godot_real>0.5, <godot_real>1, <godot_real>0)
    chocolate = Color.new_rgb(<godot_real>0.82, <godot_real>0.41, <godot_real>0.12)
    coral = Color.new_rgb(<godot_real>1, <godot_real>0.5, <godot_real>0.31)
    cornflower = Color.new_rgb(<godot_real>0.39, <godot_real>0.58, <godot_real>0.93)
    cornsilk = Color.new_rgb(<godot_real>1, <godot_real>0.97, <godot_real>0.86)
    crimson = Color.new_rgb(<godot_real>0.86, <godot_real>0.08, <godot_real>0.24)
    cyan = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>1)
    darkblue = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0.55)
    darkcyan = Color.new_rgb(<godot_real>0, <godot_real>0.55, <godot_real>0.55)
    darkgoldenrod = Color.new_rgb(<godot_real>0.72, <godot_real>0.53, <godot_real>0.04)
    darkgray = Color.new_rgb(<godot_real>0.66, <godot_real>0.66, <godot_real>0.66)
    darkgreen = Color.new_rgb(<godot_real>0, <godot_real>0.39, <godot_real>0)
    darkkhaki = Color.new_rgb(<godot_real>0.74, <godot_real>0.72, <godot_real>0.42)
    darkmagenta = Color.new_rgb(<godot_real>0.55, <godot_real>0, <godot_real>0.55)
    darkolivegreen = Color.new_rgb(<godot_real>0.33, <godot_real>0.42, <godot_real>0.18)
    darkorange = Color.new_rgb(<godot_real>1, <godot_real>0.55, <godot_real>0)
    darkorchid = Color.new_rgb(<godot_real>0.6, <godot_real>0.2, <godot_real>0.8)
    darkred = Color.new_rgb(<godot_real>0.55, <godot_real>0, <godot_real>0)
    darksalmon = Color.new_rgb(<godot_real>0.91, <godot_real>0.59, <godot_real>0.48)
    darkseagreen = Color.new_rgb(<godot_real>0.56, <godot_real>0.74, <godot_real>0.56)
    darkslateblue = Color.new_rgb(<godot_real>0.28, <godot_real>0.24, <godot_real>0.55)
    darkslategray = Color.new_rgb(<godot_real>0.18, <godot_real>0.31, <godot_real>0.31)
    darkturquoise = Color.new_rgb(<godot_real>0, <godot_real>0.81, <godot_real>0.82)
    darkviolet = Color.new_rgb(<godot_real>0.58, <godot_real>0, <godot_real>0.83)
    deeppink = Color.new_rgb(<godot_real>1, <godot_real>0.08, <godot_real>0.58)
    deepskyblue = Color.new_rgb(<godot_real>0, <godot_real>0.75, <godot_real>1)
    dimgray = Color.new_rgb(<godot_real>0.41, <godot_real>0.41, <godot_real>0.41)
    dodgerblue = Color.new_rgb(<godot_real>0.12, <godot_real>0.56, <godot_real>1)
    firebrick = Color.new_rgb(<godot_real>0.7, <godot_real>0.13, <godot_real>0.13)
    floralwhite = Color.new_rgb(<godot_real>1, <godot_real>0.98, <godot_real>0.94)
    forestgreen = Color.new_rgb(<godot_real>0.13, <godot_real>0.55, <godot_real>0.13)
    fuchsia = Color.new_rgb(<godot_real>1, <godot_real>0, <godot_real>1)
    gainsboro = Color.new_rgb(<godot_real>0.86, <godot_real>0.86, <godot_real>0.86)
    ghostwhite = Color.new_rgb(<godot_real>0.97, <godot_real>0.97, <godot_real>1)
    gold = Color.new_rgb(<godot_real>1, <godot_real>0.84, <godot_real>0)
    goldenrod = Color.new_rgb(<godot_real>0.85, <godot_real>0.65, <godot_real>0.13)
    green = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>0)
    greenyellow = Color.new_rgb(<godot_real>0.68, <godot_real>1, <godot_real>0.18)
    honeydew = Color.new_rgb(<godot_real>0.94, <godot_real>1, <godot_real>0.94)
    hotpink = Color.new_rgb(<godot_real>1, <godot_real>0.41, <godot_real>0.71)
    indianred = Color.new_rgb(<godot_real>0.8, <godot_real>0.36, <godot_real>0.36)
    indigo = Color.new_rgb(<godot_real>0.29, <godot_real>0, <godot_real>0.51)
    ivory = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>0.94)
    khaki = Color.new_rgb(<godot_real>0.94, <godot_real>0.9, <godot_real>0.55)
    lavender = Color.new_rgb(<godot_real>0.9, <godot_real>0.9, <godot_real>0.98)
    lavenderblush = Color.new_rgb(<godot_real>1, <godot_real>0.94, <godot_real>0.96)
    lawngreen = Color.new_rgb(<godot_real>0.49, <godot_real>0.99, <godot_real>0)
    lemonchiffon = Color.new_rgb(<godot_real>1, <godot_real>0.98, <godot_real>0.8)
    lightblue = Color.new_rgb(<godot_real>0.68, <godot_real>0.85, <godot_real>0.9)
    lightcoral = Color.new_rgb(<godot_real>0.94, <godot_real>0.5, <godot_real>0.5)
    lightcyan = Color.new_rgb(<godot_real>0.88, <godot_real>1, <godot_real>1)
    lightgoldenrod = Color.new_rgb(<godot_real>0.98, <godot_real>0.98, <godot_real>0.82)
    lightgray = Color.new_rgb(<godot_real>0.83, <godot_real>0.83, <godot_real>0.83)
    lightgreen = Color.new_rgb(<godot_real>0.56, <godot_real>0.93, <godot_real>0.56)
    lightpink = Color.new_rgb(<godot_real>1, <godot_real>0.71, <godot_real>0.76)
    lightsalmon = Color.new_rgb(<godot_real>1, <godot_real>0.63, <godot_real>0.48)
    lightseagreen = Color.new_rgb(<godot_real>0.13, <godot_real>0.7, <godot_real>0.67)
    lightskyblue = Color.new_rgb(<godot_real>0.53, <godot_real>0.81, <godot_real>0.98)
    lightslategray = Color.new_rgb(<godot_real>0.47, <godot_real>0.53, <godot_real>0.6)
    lightsteelblue = Color.new_rgb(<godot_real>0.69, <godot_real>0.77, <godot_real>0.87)
    lightyellow = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>0.88)
    lime = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>0)
    limegreen = Color.new_rgb(<godot_real>0.2, <godot_real>0.8, <godot_real>0.2)
    linen = Color.new_rgb(<godot_real>0.98, <godot_real>0.94, <godot_real>0.9)
    magenta = Color.new_rgb(<godot_real>1, <godot_real>0, <godot_real>1)
    maroon = Color.new_rgb(<godot_real>0.69, <godot_real>0.19, <godot_real>0.38)
    mediumaquamarine = Color.new_rgb(<godot_real>0.4, <godot_real>0.8, <godot_real>0.67)
    mediumblue = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0.8)
    mediumorchid = Color.new_rgb(<godot_real>0.73, <godot_real>0.33, <godot_real>0.83)
    mediumpurple = Color.new_rgb(<godot_real>0.58, <godot_real>0.44, <godot_real>0.86)
    mediumseagreen = Color.new_rgb(<godot_real>0.24, <godot_real>0.7, <godot_real>0.44)
    mediumslateblue = Color.new_rgb(<godot_real>0.48, <godot_real>0.41, <godot_real>0.93)
    mediumspringgreen = Color.new_rgb(<godot_real>0, <godot_real>0.98, <godot_real>0.6)
    mediumturquoise = Color.new_rgb(<godot_real>0.28, <godot_real>0.82, <godot_real>0.8)
    mediumvioletred = Color.new_rgb(<godot_real>0.78, <godot_real>0.08, <godot_real>0.52)
    midnightblue = Color.new_rgb(<godot_real>0.1, <godot_real>0.1, <godot_real>0.44)
    mintcream = Color.new_rgb(<godot_real>0.96, <godot_real>1, <godot_real>0.98)
    mistyrose = Color.new_rgb(<godot_real>1, <godot_real>0.89, <godot_real>0.88)
    moccasin = Color.new_rgb(<godot_real>1, <godot_real>0.89, <godot_real>0.71)
    navajowhite = Color.new_rgb(<godot_real>1, <godot_real>0.87, <godot_real>0.68)
    navyblue = Color.new_rgb(<godot_real>0, <godot_real>0, <godot_real>0.5)
    oldlace = Color.new_rgb(<godot_real>0.99, <godot_real>0.96, <godot_real>0.9)
    olive = Color.new_rgb(<godot_real>0.5, <godot_real>0.5, <godot_real>0)
    olivedrab = Color.new_rgb(<godot_real>0.42, <godot_real>0.56, <godot_real>0.14)
    orange = Color.new_rgb(<godot_real>1, <godot_real>0.65, <godot_real>0)
    orangered = Color.new_rgb(<godot_real>1, <godot_real>0.27, <godot_real>0)
    orchid = Color.new_rgb(<godot_real>0.85, <godot_real>0.44, <godot_real>0.84)
    palegoldenrod = Color.new_rgb(<godot_real>0.93, <godot_real>0.91, <godot_real>0.67)
    palegreen = Color.new_rgb(<godot_real>0.6, <godot_real>0.98, <godot_real>0.6)
    paleturquoise = Color.new_rgb(<godot_real>0.69, <godot_real>0.93, <godot_real>0.93)
    palevioletred = Color.new_rgb(<godot_real>0.86, <godot_real>0.44, <godot_real>0.58)
    papayawhip = Color.new_rgb(<godot_real>1, <godot_real>0.94, <godot_real>0.84)
    peachpuff = Color.new_rgb(<godot_real>1, <godot_real>0.85, <godot_real>0.73)
    peru = Color.new_rgb(<godot_real>0.8, <godot_real>0.52, <godot_real>0.25)
    pink = Color.new_rgb(<godot_real>1, <godot_real>0.75, <godot_real>0.8)
    plum = Color.new_rgb(<godot_real>0.87, <godot_real>0.63, <godot_real>0.87)
    powderblue = Color.new_rgb(<godot_real>0.69, <godot_real>0.88, <godot_real>0.9)
    purple = Color.new_rgb(<godot_real>0.63, <godot_real>0.13, <godot_real>0.94)
    rebeccapurple = Color.new_rgb(<godot_real>0.4, <godot_real>0.2, <godot_real>0.6)
    red = Color.new_rgb(<godot_real>1, <godot_real>0, <godot_real>0)
    rosybrown = Color.new_rgb(<godot_real>0.74, <godot_real>0.56, <godot_real>0.56)
    royalblue = Color.new_rgb(<godot_real>0.25, <godot_real>0.41, <godot_real>0.88)
    saddlebrown = Color.new_rgb(<godot_real>0.55, <godot_real>0.27, <godot_real>0.07)
    salmon = Color.new_rgb(<godot_real>0.98, <godot_real>0.5, <godot_real>0.45)
    sandybrown = Color.new_rgb(<godot_real>0.96, <godot_real>0.64, <godot_real>0.38)
    seagreen = Color.new_rgb(<godot_real>0.18, <godot_real>0.55, <godot_real>0.34)
    seashell = Color.new_rgb(<godot_real>1, <godot_real>0.96, <godot_real>0.93)
    sienna = Color.new_rgb(<godot_real>0.63, <godot_real>0.32, <godot_real>0.18)
    silver = Color.new_rgb(<godot_real>0.75, <godot_real>0.75, <godot_real>0.75)
    skyblue = Color.new_rgb(<godot_real>0.53, <godot_real>0.81, <godot_real>0.92)
    slateblue = Color.new_rgb(<godot_real>0.42, <godot_real>0.35, <godot_real>0.8)
    slategray = Color.new_rgb(<godot_real>0.44, <godot_real>0.5, <godot_real>0.56)
    snow = Color.new_rgb(<godot_real>1, <godot_real>0.98, <godot_real>0.98)
    springgreen = Color.new_rgb(<godot_real>0, <godot_real>1, <godot_real>0.5)
    steelblue = Color.new_rgb(<godot_real>0.27, <godot_real>0.51, <godot_real>0.71)
    tan = Color.new_rgb(<godot_real>0.82, <godot_real>0.71, <godot_real>0.55)
    teal = Color.new_rgb(<godot_real>0, <godot_real>0.5, <godot_real>0.5)
    thistle = Color.new_rgb(<godot_real>0.85, <godot_real>0.75, <godot_real>0.85)
    tomato = Color.new_rgb(<godot_real>1, <godot_real>0.39, <godot_real>0.28)
    turquoise = Color.new_rgb(<godot_real>0.25, <godot_real>0.88, <godot_real>0.82)
    violet = Color.new_rgb(<godot_real>0.93, <godot_real>0.51, <godot_real>0.93)
    webgray = Color.new_rgb(<godot_real>0.5, <godot_real>0.5, <godot_real>0.5)
    webgreen = Color.new_rgb(<godot_real>0, <godot_real>0.5, <godot_real>0)
    webmaroon = Color.new_rgb(<godot_real>0.5, <godot_real>0, <godot_real>0)
    webpurple = Color.new_rgb(<godot_real>0.5, <godot_real>0, <godot_real>0.5)
    wheat = Color.new_rgb(<godot_real>0.96, <godot_real>0.87, <godot_real>0.7)
    white = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>1)
    whitesmoke = Color.new_rgb(<godot_real>0.96, <godot_real>0.96, <godot_real>0.96)
    yellow = Color.new_rgb(<godot_real>1, <godot_real>1, <godot_real>0)
    yellowgreen = Color.new_rgb(<godot_real>0.6, <godot_real>0.8, <godot_real>0.2)
