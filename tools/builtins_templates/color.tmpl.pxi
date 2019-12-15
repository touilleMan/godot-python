{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_color_new_rgba(godot_color* r_dest, godot_real p_r, godot_real p_g, godot_real p_b, godot_real p_a)
void godot_color_new_rgb(godot_color* r_dest, godot_real p_r, godot_real p_g, godot_real p_b)
godot_real godot_color_get_r(godot_color* p_self)
void godot_color_set_r(godot_color* p_self, godot_real r)
godot_real godot_color_get_g(godot_color* p_self)
void godot_color_set_g(godot_color* p_self, godot_real g)
godot_real godot_color_get_b(godot_color* p_self)
void godot_color_set_b(godot_color* p_self, godot_real b)
godot_real godot_color_get_a(godot_color* p_self)
void godot_color_set_a(godot_color* p_self, godot_real a)
godot_real godot_color_get_h(godot_color* p_self)
godot_real godot_color_get_s(godot_color* p_self)
godot_real godot_color_get_v(godot_color* p_self)
godot_string godot_color_as_string(godot_color* p_self)
godot_int godot_color_to_rgba32(godot_color* p_self)
godot_int godot_color_to_argb32(godot_color* p_self)
godot_real godot_color_gray(godot_color* p_self)
godot_color godot_color_inverted(godot_color* p_self)
godot_color godot_color_contrasted(godot_color* p_self)
godot_color godot_color_linear_interpolate(godot_color* p_self, godot_color* p_b, godot_real p_t)
godot_color godot_color_blend(godot_color* p_self, godot_color* p_over)
godot_string godot_color_to_html(godot_color* p_self, godot_bool p_with_alpha)
godot_bool godot_color_operator_equal(godot_color* p_self, godot_color* p_b)
godot_bool godot_color_operator_less(godot_color* p_self, godot_color* p_b)
// GDAPI: 1.1
godot_int godot_color_to_abgr32(godot_color* p_self)
godot_int godot_color_to_abgr64(godot_color* p_self)
godot_int godot_color_to_argb64(godot_color* p_self)
godot_int godot_color_to_rgba64(godot_color* p_self)
godot_color godot_color_darkened(godot_color* p_self, godot_real p_amount)
godot_color godot_color_from_hsv(godot_color* p_self, godot_real p_h, godot_real p_s, godot_real p_v, godot_real p_a)
godot_color godot_color_lightened(godot_color* p_self, godot_real p_amount)
// GDAPI: 1.2
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Color:
{% block cdef_attributes %}
    cdef godot_color _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real r=0, godot_real g=0, godot_real b=0, a=None):
        if a is None:
            gdapi10.godot_color_new_rgb(&self._gd_data, r, g, b)
        else:
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
    def r8(Color self, val):
        self.r = (float(val) / 256)

    @property
    def g8(Color self):
        return int(self.g * 256)

    @g8.setter
    def g8(Color self, val):
        self.g = (float(val) / 256)

    @property
    def b8(Color self):
        return int(self.b * 256)

    @b8.setter
    def b8(Color self, val):
        self.b = (float(val) / 256)

    @property
    def a8(Color self):
        return int(self.a * 256)

    @a8.setter
    def a8(Color self, val):
        self.a = (float(val) / 256)

    {{ render_property("r", "godot_real", "get_r", "set_r") | indent }}
    {{ render_property("g", "godot_real", "get_g", "set_g") | indent }}
    {{ render_property("b", "godot_real", "get_b", "set_b") | indent }}
    {{ render_property("a", "godot_real", "get_a", "set_a") | indent }}

    {{ render_property("h", "godot_real", "get_h") | indent }}
    {{ render_property("s", "godot_real", "get_s") | indent }}
    {{ render_property("v", "godot_real", "get_v") | indent }}

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["to_rgba32"]) | indent }}
    {{ render_method(**gd_functions["to_abgr32"]) | indent }}
    {{ render_method(**gd_functions["to_abgr64"]) | indent }}
    {{ render_method(**gd_functions["to_argb64"]) | indent }}
    {{ render_method(**gd_functions["to_rgba64"]) | indent }}
    {{ render_method(**gd_functions["to_argb32"]) | indent }}
    {{ render_method(**gd_functions["gray"]) | indent }}
    {{ render_method(**gd_functions["inverted"]) | indent }}
    {{ render_method(**gd_functions["contrasted"]) | indent }}
    {{ render_method(**gd_functions["linear_interpolate"]) | indent }}
    {{ render_method(**gd_functions["blend"]) | indent }}
    {{ render_method(**gd_functions["darkened"]) | indent }}
    {{ render_method(**gd_functions["from_hsv"]) | indent }}
    {{ render_method(**gd_functions["lightened"]) | indent }}
    {{ render_method(**gd_functions["to_html"]) | indent }}

{% endblock %}

{%- block python_consts %}
    # TODO: gdapi should expose those constants to us
    GRAY = Color.new_rgb(0.75, 0.75, 0.75)
    ALICEBLUE = Color.new_rgb(0.94, 0.97, 1)
    ANTIQUEWHITE = Color.new_rgb(0.98, 0.92, 0.84)
    AQUA = Color.new_rgb(0, 1, 1)
    AQUAMARINE = Color.new_rgb(0.5, 1, 0.83)
    AZURE = Color.new_rgb(0.94, 1, 1)
    BEIGE = Color.new_rgb(0.96, 0.96, 0.86)
    BISQUE = Color.new_rgb(1, 0.89, 0.77)
    BLACK = Color.new_rgb(0, 0, 0)
    BLANCHEDALMOND = Color.new_rgb(1, 0.92, 0.8)
    BLUE = Color.new_rgb(0, 0, 1)
    BLUEVIOLET = Color.new_rgb(0.54, 0.17, 0.89)
    BROWN = Color.new_rgb(0.65, 0.16, 0.16)
    BURLYWOOD = Color.new_rgb(0.87, 0.72, 0.53)
    CADETBLUE = Color.new_rgb(0.37, 0.62, 0.63)
    CHARTREUSE = Color.new_rgb(0.5, 1, 0)
    CHOCOLATE = Color.new_rgb(0.82, 0.41, 0.12)
    CORAL = Color.new_rgb(1, 0.5, 0.31)
    CORNFLOWER = Color.new_rgb(0.39, 0.58, 0.93)
    CORNSILK = Color.new_rgb(1, 0.97, 0.86)
    CRIMSON = Color.new_rgb(0.86, 0.08, 0.24)
    CYAN = Color.new_rgb(0, 1, 1)
    DARKBLUE = Color.new_rgb(0, 0, 0.55)
    DARKCYAN = Color.new_rgb(0, 0.55, 0.55)
    DARKGOLDENROD = Color.new_rgb(0.72, 0.53, 0.04)
    DARKGRAY = Color.new_rgb(0.66, 0.66, 0.66)
    DARKGREEN = Color.new_rgb(0, 0.39, 0)
    DARKKHAKI = Color.new_rgb(0.74, 0.72, 0.42)
    DARKMAGENTA = Color.new_rgb(0.55, 0, 0.55)
    DARKOLIVEGREEN = Color.new_rgb(0.33, 0.42, 0.18)
    DARKORANGE = Color.new_rgb(1, 0.55, 0)
    DARKORCHID = Color.new_rgb(0.6, 0.2, 0.8)
    DARKRED = Color.new_rgb(0.55, 0, 0)
    DARKSALMON = Color.new_rgb(0.91, 0.59, 0.48)
    DARKSEAGREEN = Color.new_rgb(0.56, 0.74, 0.56)
    DARKSLATEBLUE = Color.new_rgb(0.28, 0.24, 0.55)
    DARKSLATEGRAY = Color.new_rgb(0.18, 0.31, 0.31)
    DARKTURQUOISE = Color.new_rgb(0, 0.81, 0.82)
    DARKVIOLET = Color.new_rgb(0.58, 0, 0.83)
    DEEPPINK = Color.new_rgb(1, 0.08, 0.58)
    DEEPSKYBLUE = Color.new_rgb(0, 0.75, 1)
    DIMGRAY = Color.new_rgb(0.41, 0.41, 0.41)
    DODGERBLUE = Color.new_rgb(0.12, 0.56, 1)
    FIREBRICK = Color.new_rgb(0.7, 0.13, 0.13)
    FLORALWHITE = Color.new_rgb(1, 0.98, 0.94)
    FORESTGREEN = Color.new_rgb(0.13, 0.55, 0.13)
    FUCHSIA = Color.new_rgb(1, 0, 1)
    GAINSBORO = Color.new_rgb(0.86, 0.86, 0.86)
    GHOSTWHITE = Color.new_rgb(0.97, 0.97, 1)
    GOLD = Color.new_rgb(1, 0.84, 0)
    GOLDENROD = Color.new_rgb(0.85, 0.65, 0.13)
    GREEN = Color.new_rgb(0, 1, 0)
    GREENYELLOW = Color.new_rgb(0.68, 1, 0.18)
    HONEYDEW = Color.new_rgb(0.94, 1, 0.94)
    HOTPINK = Color.new_rgb(1, 0.41, 0.71)
    INDIANRED = Color.new_rgb(0.8, 0.36, 0.36)
    INDIGO = Color.new_rgb(0.29, 0, 0.51)
    IVORY = Color.new_rgb(1, 1, 0.94)
    KHAKI = Color.new_rgb(0.94, 0.9, 0.55)
    LAVENDER = Color.new_rgb(0.9, 0.9, 0.98)
    LAVENDERBLUSH = Color.new_rgb(1, 0.94, 0.96)
    LAWNGREEN = Color.new_rgb(0.49, 0.99, 0)
    LEMONCHIFFON = Color.new_rgb(1, 0.98, 0.8)
    LIGHTBLUE = Color.new_rgb(0.68, 0.85, 0.9)
    LIGHTCORAL = Color.new_rgb(0.94, 0.5, 0.5)
    LIGHTCYAN = Color.new_rgb(0.88, 1, 1)
    LIGHTGOLDENROD = Color.new_rgb(0.98, 0.98, 0.82)
    LIGHTGRAY = Color.new_rgb(0.83, 0.83, 0.83)
    LIGHTGREEN = Color.new_rgb(0.56, 0.93, 0.56)
    LIGHTPINK = Color.new_rgb(1, 0.71, 0.76)
    LIGHTSALMON = Color.new_rgb(1, 0.63, 0.48)
    LIGHTSEAGREEN = Color.new_rgb(0.13, 0.7, 0.67)
    LIGHTSKYBLUE = Color.new_rgb(0.53, 0.81, 0.98)
    LIGHTSLATEGRAY = Color.new_rgb(0.47, 0.53, 0.6)
    LIGHTSTEELBLUE = Color.new_rgb(0.69, 0.77, 0.87)
    LIGHTYELLOW = Color.new_rgb(1, 1, 0.88)
    LIME = Color.new_rgb(0, 1, 0)
    LIMEGREEN = Color.new_rgb(0.2, 0.8, 0.2)
    LINEN = Color.new_rgb(0.98, 0.94, 0.9)
    MAGENTA = Color.new_rgb(1, 0, 1)
    MAROON = Color.new_rgb(0.69, 0.19, 0.38)
    MEDIUMAQUAMARINE = Color.new_rgb(0.4, 0.8, 0.67)
    MEDIUMBLUE = Color.new_rgb(0, 0, 0.8)
    MEDIUMORCHID = Color.new_rgb(0.73, 0.33, 0.83)
    MEDIUMPURPLE = Color.new_rgb(0.58, 0.44, 0.86)
    MEDIUMSEAGREEN = Color.new_rgb(0.24, 0.7, 0.44)
    MEDIUMSLATEBLUE = Color.new_rgb(0.48, 0.41, 0.93)
    MEDIUMSPRINGGREEN = Color.new_rgb(0, 0.98, 0.6)
    MEDIUMTURQUOISE = Color.new_rgb(0.28, 0.82, 0.8)
    MEDIUMVIOLETRED = Color.new_rgb(0.78, 0.08, 0.52)
    MIDNIGHTBLUE = Color.new_rgb(0.1, 0.1, 0.44)
    MINTCREAM = Color.new_rgb(0.96, 1, 0.98)
    MISTYROSE = Color.new_rgb(1, 0.89, 0.88)
    MOCCASIN = Color.new_rgb(1, 0.89, 0.71)
    NAVAJOWHITE = Color.new_rgb(1, 0.87, 0.68)
    NAVYBLUE = Color.new_rgb(0, 0, 0.5)
    OLDLACE = Color.new_rgb(0.99, 0.96, 0.9)
    OLIVE = Color.new_rgb(0.5, 0.5, 0)
    OLIVEDRAB = Color.new_rgb(0.42, 0.56, 0.14)
    ORANGE = Color.new_rgb(1, 0.65, 0)
    ORANGERED = Color.new_rgb(1, 0.27, 0)
    ORCHID = Color.new_rgb(0.85, 0.44, 0.84)
    PALEGOLDENROD = Color.new_rgb(0.93, 0.91, 0.67)
    PALEGREEN = Color.new_rgb(0.6, 0.98, 0.6)
    PALETURQUOISE = Color.new_rgb(0.69, 0.93, 0.93)
    PALEVIOLETRED = Color.new_rgb(0.86, 0.44, 0.58)
    PAPAYAWHIP = Color.new_rgb(1, 0.94, 0.84)
    PEACHPUFF = Color.new_rgb(1, 0.85, 0.73)
    PERU = Color.new_rgb(0.8, 0.52, 0.25)
    PINK = Color.new_rgb(1, 0.75, 0.8)
    PLUM = Color.new_rgb(0.87, 0.63, 0.87)
    POWDERBLUE = Color.new_rgb(0.69, 0.88, 0.9)
    PURPLE = Color.new_rgb(0.63, 0.13, 0.94)
    REBECCAPURPLE = Color.new_rgb(0.4, 0.2, 0.6)
    RED = Color.new_rgb(1, 0, 0)
    ROSYBROWN = Color.new_rgb(0.74, 0.56, 0.56)
    ROYALBLUE = Color.new_rgb(0.25, 0.41, 0.88)
    SADDLEBROWN = Color.new_rgb(0.55, 0.27, 0.07)
    SALMON = Color.new_rgb(0.98, 0.5, 0.45)
    SANDYBROWN = Color.new_rgb(0.96, 0.64, 0.38)
    SEAGREEN = Color.new_rgb(0.18, 0.55, 0.34)
    SEASHELL = Color.new_rgb(1, 0.96, 0.93)
    SIENNA = Color.new_rgb(0.63, 0.32, 0.18)
    SILVER = Color.new_rgb(0.75, 0.75, 0.75)
    SKYBLUE = Color.new_rgb(0.53, 0.81, 0.92)
    SLATEBLUE = Color.new_rgb(0.42, 0.35, 0.8)
    SLATEGRAY = Color.new_rgb(0.44, 0.5, 0.56)
    SNOW = Color.new_rgb(1, 0.98, 0.98)
    SPRINGGREEN = Color.new_rgb(0, 1, 0.5)
    STEELBLUE = Color.new_rgb(0.27, 0.51, 0.71)
    TAN = Color.new_rgb(0.82, 0.71, 0.55)
    TEAL = Color.new_rgb(0, 0.5, 0.5)
    THISTLE = Color.new_rgb(0.85, 0.75, 0.85)
    TOMATO = Color.new_rgb(1, 0.39, 0.28)
    TURQUOISE = Color.new_rgb(0.25, 0.88, 0.82)
    VIOLET = Color.new_rgb(0.93, 0.51, 0.93)
    WEBGRAY = Color.new_rgb(0.5, 0.5, 0.5)
    WEBGREEN = Color.new_rgb(0, 0.5, 0)
    WEBMAROON = Color.new_rgb(0.5, 0, 0)
    WEBPURPLE = Color.new_rgb(0.5, 0, 0.5)
    WHEAT = Color.new_rgb(0.96, 0.87, 0.7)
    WHITE = Color.new_rgb(1, 1, 1)
    WHITESMOKE = Color.new_rgb(0.96, 0.96, 0.96)
    YELLOW = Color.new_rgb(1, 1, 0)
    YELLOWGREEN = Color.new_rgb(0.6, 0.8, 0.2)
{% endblock %}
