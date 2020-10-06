{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
from libc.stdint cimport uint8_t
{% endblock -%}


@cython.final
cdef class Color:
{% block cdef_attributes %}
    cdef godot_color _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real r=0, godot_real g=0, godot_real b=0, a=None):
        if a is None:
            {{ force_mark_rendered("godot_color_new_rgb")}}
            gdapi10.godot_color_new_rgb(&self._gd_data, r, g, b)
        else:
            {{ force_mark_rendered("godot_color_new_rgba")}}
            gdapi10.godot_color_new_rgba(&self._gd_data, r, g, b, a)

    def __repr__(self):
        return f"<Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})>"

    @staticmethod
    def from_resource(Resource resource not None):
        # Call to __new__ bypasses __init__ constructor
        cdef RID ret = RID.__new__(RID)
        gdapi10.godot_rid_new_with_resource(&ret._gd_data, resource._gd_ptr)
        return ret

    @property
    def r8(Color self):
        return int(self.r * 256)

    @r8.setter
    def r8(Color self, uint8_t val):
        self.r = (float(val) / 256)

    @property
    def g8(Color self):
        return int(self.g * 256)

    @g8.setter
    def g8(Color self, uint8_t val):
        self.g = (float(val) / 256)

    @property
    def b8(Color self):
        return int(self.b * 256)

    @b8.setter
    def b8(Color self, uint8_t val):
        self.b = (float(val) / 256)

    @property
    def a8(Color self):
        return int(self.a * 256)

    @a8.setter
    def a8(Color self, uint8_t val):
        self.a = (float(val) / 256)

    {{ render_property("r", getter="get_r", setter="set_r") | indent }}
    {{ render_property("g", getter="get_g", setter="set_g") | indent }}
    {{ render_property("b", getter="get_b", setter="set_b") | indent }}
    {{ render_property("a", getter="get_a", setter="set_a") | indent }}

    {{ render_property("h", getter="get_h") | indent }}
    {{ render_property("s", getter="get_s") | indent }}
    {{ render_property("v", getter="get_v") | indent }}

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method("as_string") | indent }}
    {{ render_method("to_rgba32") | indent }}
    {{ render_method("to_abgr32") | indent }}
    {{ render_method("to_abgr64") | indent }}
    {{ render_method("to_argb64") | indent }}
    {{ render_method("to_rgba64") | indent }}
    {{ render_method("to_argb32") | indent }}
    {{ render_method("gray") | indent }}
    {{ render_method("inverted") | indent }}
    {{ render_method("contrasted") | indent }}
    {{ render_method("linear_interpolate") | indent }}
    {{ render_method("blend") | indent }}
    {{ render_method("darkened") | indent }}
    {{ render_method("from_hsv") | indent }}
    {{ render_method("lightened") | indent }}
    {{ render_method("to_html") | indent }}

{% endblock %}

{%- block python_consts %}
    # TODO: gdapi should expose those constants to us
    GRAY = Color(0.75, 0.75, 0.75)
    ALICEBLUE = Color(0.94, 0.97, 1)
    ANTIQUEWHITE = Color(0.98, 0.92, 0.84)
    AQUA = Color(0, 1, 1)
    AQUAMARINE = Color(0.5, 1, 0.83)
    AZURE = Color(0.94, 1, 1)
    BEIGE = Color(0.96, 0.96, 0.86)
    BISQUE = Color(1, 0.89, 0.77)
    BLACK = Color(0, 0, 0)
    BLANCHEDALMOND = Color(1, 0.92, 0.8)
    BLUE = Color(0, 0, 1)
    BLUEVIOLET = Color(0.54, 0.17, 0.89)
    BROWN = Color(0.65, 0.16, 0.16)
    BURLYWOOD = Color(0.87, 0.72, 0.53)
    CADETBLUE = Color(0.37, 0.62, 0.63)
    CHARTREUSE = Color(0.5, 1, 0)
    CHOCOLATE = Color(0.82, 0.41, 0.12)
    CORAL = Color(1, 0.5, 0.31)
    CORNFLOWER = Color(0.39, 0.58, 0.93)
    CORNSILK = Color(1, 0.97, 0.86)
    CRIMSON = Color(0.86, 0.08, 0.24)
    CYAN = Color(0, 1, 1)
    DARKBLUE = Color(0, 0, 0.55)
    DARKCYAN = Color(0, 0.55, 0.55)
    DARKGOLDENROD = Color(0.72, 0.53, 0.04)
    DARKGRAY = Color(0.66, 0.66, 0.66)
    DARKGREEN = Color(0, 0.39, 0)
    DARKKHAKI = Color(0.74, 0.72, 0.42)
    DARKMAGENTA = Color(0.55, 0, 0.55)
    DARKOLIVEGREEN = Color(0.33, 0.42, 0.18)
    DARKORANGE = Color(1, 0.55, 0)
    DARKORCHID = Color(0.6, 0.2, 0.8)
    DARKRED = Color(0.55, 0, 0)
    DARKSALMON = Color(0.91, 0.59, 0.48)
    DARKSEAGREEN = Color(0.56, 0.74, 0.56)
    DARKSLATEBLUE = Color(0.28, 0.24, 0.55)
    DARKSLATEGRAY = Color(0.18, 0.31, 0.31)
    DARKTURQUOISE = Color(0, 0.81, 0.82)
    DARKVIOLET = Color(0.58, 0, 0.83)
    DEEPPINK = Color(1, 0.08, 0.58)
    DEEPSKYBLUE = Color(0, 0.75, 1)
    DIMGRAY = Color(0.41, 0.41, 0.41)
    DODGERBLUE = Color(0.12, 0.56, 1)
    FIREBRICK = Color(0.7, 0.13, 0.13)
    FLORALWHITE = Color(1, 0.98, 0.94)
    FORESTGREEN = Color(0.13, 0.55, 0.13)
    FUCHSIA = Color(1, 0, 1)
    GAINSBORO = Color(0.86, 0.86, 0.86)
    GHOSTWHITE = Color(0.97, 0.97, 1)
    GOLD = Color(1, 0.84, 0)
    GOLDENROD = Color(0.85, 0.65, 0.13)
    GREEN = Color(0, 1, 0)
    GREENYELLOW = Color(0.68, 1, 0.18)
    HONEYDEW = Color(0.94, 1, 0.94)
    HOTPINK = Color(1, 0.41, 0.71)
    INDIANRED = Color(0.8, 0.36, 0.36)
    INDIGO = Color(0.29, 0, 0.51)
    IVORY = Color(1, 1, 0.94)
    KHAKI = Color(0.94, 0.9, 0.55)
    LAVENDER = Color(0.9, 0.9, 0.98)
    LAVENDERBLUSH = Color(1, 0.94, 0.96)
    LAWNGREEN = Color(0.49, 0.99, 0)
    LEMONCHIFFON = Color(1, 0.98, 0.8)
    LIGHTBLUE = Color(0.68, 0.85, 0.9)
    LIGHTCORAL = Color(0.94, 0.5, 0.5)
    LIGHTCYAN = Color(0.88, 1, 1)
    LIGHTGOLDENROD = Color(0.98, 0.98, 0.82)
    LIGHTGRAY = Color(0.83, 0.83, 0.83)
    LIGHTGREEN = Color(0.56, 0.93, 0.56)
    LIGHTPINK = Color(1, 0.71, 0.76)
    LIGHTSALMON = Color(1, 0.63, 0.48)
    LIGHTSEAGREEN = Color(0.13, 0.7, 0.67)
    LIGHTSKYBLUE = Color(0.53, 0.81, 0.98)
    LIGHTSLATEGRAY = Color(0.47, 0.53, 0.6)
    LIGHTSTEELBLUE = Color(0.69, 0.77, 0.87)
    LIGHTYELLOW = Color(1, 1, 0.88)
    LIME = Color(0, 1, 0)
    LIMEGREEN = Color(0.2, 0.8, 0.2)
    LINEN = Color(0.98, 0.94, 0.9)
    MAGENTA = Color(1, 0, 1)
    MAROON = Color(0.69, 0.19, 0.38)
    MEDIUMAQUAMARINE = Color(0.4, 0.8, 0.67)
    MEDIUMBLUE = Color(0, 0, 0.8)
    MEDIUMORCHID = Color(0.73, 0.33, 0.83)
    MEDIUMPURPLE = Color(0.58, 0.44, 0.86)
    MEDIUMSEAGREEN = Color(0.24, 0.7, 0.44)
    MEDIUMSLATEBLUE = Color(0.48, 0.41, 0.93)
    MEDIUMSPRINGGREEN = Color(0, 0.98, 0.6)
    MEDIUMTURQUOISE = Color(0.28, 0.82, 0.8)
    MEDIUMVIOLETRED = Color(0.78, 0.08, 0.52)
    MIDNIGHTBLUE = Color(0.1, 0.1, 0.44)
    MINTCREAM = Color(0.96, 1, 0.98)
    MISTYROSE = Color(1, 0.89, 0.88)
    MOCCASIN = Color(1, 0.89, 0.71)
    NAVAJOWHITE = Color(1, 0.87, 0.68)
    NAVYBLUE = Color(0, 0, 0.5)
    OLDLACE = Color(0.99, 0.96, 0.9)
    OLIVE = Color(0.5, 0.5, 0)
    OLIVEDRAB = Color(0.42, 0.56, 0.14)
    ORANGE = Color(1, 0.65, 0)
    ORANGERED = Color(1, 0.27, 0)
    ORCHID = Color(0.85, 0.44, 0.84)
    PALEGOLDENROD = Color(0.93, 0.91, 0.67)
    PALEGREEN = Color(0.6, 0.98, 0.6)
    PALETURQUOISE = Color(0.69, 0.93, 0.93)
    PALEVIOLETRED = Color(0.86, 0.44, 0.58)
    PAPAYAWHIP = Color(1, 0.94, 0.84)
    PEACHPUFF = Color(1, 0.85, 0.73)
    PERU = Color(0.8, 0.52, 0.25)
    PINK = Color(1, 0.75, 0.8)
    PLUM = Color(0.87, 0.63, 0.87)
    POWDERBLUE = Color(0.69, 0.88, 0.9)
    PURPLE = Color(0.63, 0.13, 0.94)
    REBECCAPURPLE = Color(0.4, 0.2, 0.6)
    RED = Color(1, 0, 0)
    ROSYBROWN = Color(0.74, 0.56, 0.56)
    ROYALBLUE = Color(0.25, 0.41, 0.88)
    SADDLEBROWN = Color(0.55, 0.27, 0.07)
    SALMON = Color(0.98, 0.5, 0.45)
    SANDYBROWN = Color(0.96, 0.64, 0.38)
    SEAGREEN = Color(0.18, 0.55, 0.34)
    SEASHELL = Color(1, 0.96, 0.93)
    SIENNA = Color(0.63, 0.32, 0.18)
    SILVER = Color(0.75, 0.75, 0.75)
    SKYBLUE = Color(0.53, 0.81, 0.92)
    SLATEBLUE = Color(0.42, 0.35, 0.8)
    SLATEGRAY = Color(0.44, 0.5, 0.56)
    SNOW = Color(1, 0.98, 0.98)
    SPRINGGREEN = Color(0, 1, 0.5)
    STEELBLUE = Color(0.27, 0.51, 0.71)
    TAN = Color(0.82, 0.71, 0.55)
    TEAL = Color(0, 0.5, 0.5)
    THISTLE = Color(0.85, 0.75, 0.85)
    TOMATO = Color(1, 0.39, 0.28)
    TURQUOISE = Color(0.25, 0.88, 0.82)
    VIOLET = Color(0.93, 0.51, 0.93)
    WEBGRAY = Color(0.5, 0.5, 0.5)
    WEBGREEN = Color(0, 0.5, 0)
    WEBMAROON = Color(0.5, 0, 0)
    WEBPURPLE = Color(0.5, 0, 0.5)
    WHEAT = Color(0.96, 0.87, 0.7)
    WHITE = Color(1, 1, 1)
    WHITESMOKE = Color(0.96, 0.96, 0.96)
    YELLOW = Color(1, 1, 0)
    YELLOWGREEN = Color(0.6, 0.8, 0.2)
{% endblock %}
