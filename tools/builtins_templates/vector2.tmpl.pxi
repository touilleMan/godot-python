{%- set gd_functions = cook_c_signatures("""
// GDAPI: 1.0
void godot_vector2_new(godot_vector2* r_dest, godot_real p_x, godot_real p_y)
godot_string godot_vector2_as_string(godot_vector2* p_self)
godot_vector2 godot_vector2_normalized(godot_vector2* p_self)
godot_real godot_vector2_length(godot_vector2* p_self)
godot_real godot_vector2_angle(godot_vector2* p_self)
godot_real godot_vector2_length_squared(godot_vector2* p_self)
godot_bool godot_vector2_is_normalized(godot_vector2* p_self)
godot_real godot_vector2_distance_to(godot_vector2* p_self, godot_vector2* p_to)
godot_real godot_vector2_distance_squared_to(godot_vector2* p_self, godot_vector2* p_to)
godot_real godot_vector2_angle_to(godot_vector2* p_self, godot_vector2* p_to)
godot_real godot_vector2_angle_to_point(godot_vector2* p_self, godot_vector2* p_to)
godot_vector2 godot_vector2_linear_interpolate(godot_vector2* p_self, godot_vector2* p_b, godot_real p_t)
godot_vector2 godot_vector2_cubic_interpolate(godot_vector2* p_self, godot_vector2* p_b, godot_vector2* p_pre_a, godot_vector2* p_post_b, godot_real p_t)
godot_vector2 godot_vector2_rotated(godot_vector2* p_self, godot_real p_phi)
godot_vector2 godot_vector2_tangent(godot_vector2* p_self)
godot_vector2 godot_vector2_floor(godot_vector2* p_self)
godot_vector2 godot_vector2_snapped(godot_vector2* p_self, godot_vector2* p_by)
godot_real godot_vector2_aspect(godot_vector2* p_self)
godot_real godot_vector2_dot(godot_vector2* p_self, godot_vector2* p_with)
godot_vector2 godot_vector2_slide(godot_vector2* p_self, godot_vector2* p_n)
godot_vector2 godot_vector2_bounce(godot_vector2* p_self, godot_vector2* p_n)
godot_vector2 godot_vector2_reflect(godot_vector2* p_self, godot_vector2* p_n)
godot_vector2 godot_vector2_abs(godot_vector2* p_self)
godot_vector2 godot_vector2_clamped(godot_vector2* p_self, godot_real p_length)
godot_vector2 godot_vector2_operator_add(godot_vector2* p_self, godot_vector2* p_b)
godot_vector2 godot_vector2_operator_subtract(godot_vector2* p_self, godot_vector2* p_b)
godot_vector2 godot_vector2_operator_multiply_vector(godot_vector2* p_self, godot_vector2* p_b)
godot_vector2 godot_vector2_operator_multiply_scalar(godot_vector2* p_self, godot_real p_b)
godot_vector2 godot_vector2_operator_divide_vector(godot_vector2* p_self, godot_vector2* p_b)
godot_vector2 godot_vector2_operator_divide_scalar(godot_vector2* p_self, godot_real p_b)
godot_bool godot_vector2_operator_equal(godot_vector2* p_self, godot_vector2* p_b)
godot_bool godot_vector2_operator_less(godot_vector2* p_self, godot_vector2* p_b)
godot_vector2 godot_vector2_operator_neg(godot_vector2* p_self)
void godot_vector2_set_x(godot_vector2* p_self, godot_real p_x)
void godot_vector2_set_y(godot_vector2* p_self, godot_real p_y)
godot_real godot_vector2_get_x(godot_vector2* p_self)
godot_real godot_vector2_get_y(godot_vector2* p_self)
// GDAPI: 1.1
// GDAPI: 1.2
godot_vector2 godot_vector2_move_toward(godot_vector2* p_self, godot_vector2* p_to, godot_real p_delta)
""") -%}

{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
import math

cdef inline Vector2 Vector2_multiply_vector(Vector2 self, Vector2 b):
    cdef Vector2 ret  = Vector2.__new__(Vector2)
    ret._gd_data = gdapi10.godot_vector2_operator_multiply_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector2 Vector2_multiply_scalar(Vector2 self, godot_real b):
    cdef Vector2 ret  = Vector2.__new__(Vector2)
    ret._gd_data = gdapi10.godot_vector2_operator_multiply_scalar(&self._gd_data, b)
    return ret

cdef inline Vector2 Vector2_divide_vector(Vector2 self, Vector2 b):
    cdef Vector2 ret  = Vector2.__new__(Vector2)
    ret._gd_data = gdapi10.godot_vector2_operator_divide_vector(&self._gd_data, &b._gd_data)
    return ret

cdef inline Vector2 Vector2_divide_scalar(Vector2 self, godot_real b):
    cdef Vector2 ret  = Vector2.__new__(Vector2)
    ret._gd_data = gdapi10.godot_vector2_operator_divide_scalar(&self._gd_data, b)
    return ret
{% endblock -%}


@cython.final
cdef class Vector2:
{% block cdef_attributes %}
    cdef godot_vector2 _gd_data
{% endblock %}

{% block python_defs %}
    def __init__(self, godot_real x=0.0, godot_real y=0.0):
        gdapi10.godot_vector2_new(&self._gd_data, x, y)

    def __repr__(Vector2 self):
        return f"<Vector2(x={self.x}, y={self.y})>"

    {{ render_operator_eq() | indent }}
    {{ render_operator_ne() | indent }}
    {{ render_operator_lt() | indent }}

    {{ render_method("__neg__", "godot_vector2", gdname="operator_neg") | indent }}

    def __pos__(Vector2 self):
        return self

    {{ render_method("__add__", "godot_vector2", args=[
        ("godot_vector2*", "val")
    ], gdname="operator_add") | indent }}
    {{ render_method("__sub__", "godot_vector2", args=[
        ("godot_vector2*", "val")
    ], gdname="operator_subtract") | indent }}

    def __mul__(Vector2 self, val):
        cdef Vector2 _val
        try:
            _val = <Vector2?>val
        except TypeError:
            return Vector2_multiply_scalar(self, val)
        else:
            return Vector2_multiply_vector(self, _val)

    def __truediv__(Vector2 self, val):
        cdef Vector2 _val
        try:
            _val = <Vector2?>val
        except TypeError:
            if val is 0:
                raise ZeroDivisionError()
            return Vector2_divide_scalar(self, val)
        else:
            if _val.x == 0 or _val.y == 0:
                raise ZeroDivisionError()
            return Vector2_divide_vector(self, _val)

    {{ render_property("x", "godot_real", "get_x", "set_x") | indent }}
    {{ render_property("y", "godot_real", "get_y", "set_y") | indent }}
    {{ render_property("width", "godot_real", "get_x", "set_x") | indent }}
    {{ render_property("height", "godot_real", "get_y", "set_y") | indent }}

    {{ render_method(**gd_functions["as_string"]) | indent }}
    {{ render_method(**gd_functions["normalized"]) | indent }}
    {{ render_method(**gd_functions["length"]) | indent }}
    {{ render_method(**gd_functions["angle"]) | indent }}
    {{ render_method(**gd_functions["length_squared"]) | indent }}
    {{ render_method(**gd_functions["is_normalized"]) | indent }}
    {{ render_method(**gd_functions["distance_to"]) | indent }}
    {{ render_method(**gd_functions["distance_squared_to"]) | indent }}
    {{ render_method(**gd_functions["angle_to"]) | indent }}
    {{ render_method(**gd_functions["angle_to_point"]) | indent }}
    {{ render_method(**gd_functions["linear_interpolate"]) | indent }}
    {{ render_method(**gd_functions["cubic_interpolate"]) | indent }}
    {{ render_method(**gd_functions["move_toward"]) | indent }}
    {{ render_method(**gd_functions["rotated"]) | indent }}
    {{ render_method(**gd_functions["tangent"]) | indent }}
    {{ render_method(**gd_functions["floor"]) | indent }}
    {{ render_method(**gd_functions["snapped"]) | indent }}
    {{ render_method(**gd_functions["aspect"]) | indent }}
    {{ render_method(**gd_functions["dot"]) | indent }}
    {{ render_method(**gd_functions["slide"]) | indent }}
    {{ render_method(**gd_functions["bounce"]) | indent }}
    {{ render_method(**gd_functions["reflect"]) | indent }}
    {{ render_method(**gd_functions["abs"]) | indent }}
    {{ render_method(**gd_functions["clamped"]) | indent }}
{% endblock %}

{%- block python_consts %}
    AXIS_X = 0
    AXIS_Y = 0

    ZERO = Vector2(0, 0)
    ONE = Vector2(1, 1)
    INF = Vector2(math.inf, math.inf)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
{% endblock %}
