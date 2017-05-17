class Vector2:
    GD_TYPE = lib.GODOT_VARIANT_TYPE_VECTOR2

    @classmethod
    def build_from_gd_obj(cls, gd_obj):
        # TODO: optimize this
        v = cls()
        v._gd_obj = gd_obj
        v._gd_obj_ptr = ffi.addressof(gd_obj)
        return v

    @classmethod
    def build_from_gd_obj_ptr(cls, gd_obj_ptr):
        # TODO: optimize this
        v = cls()
        v._gd_obj_ptr = gd_obj_ptr
        v._gd_obj = gd_obj_ptr[0]
        return v

    @staticmethod
    def check_param_type(argname, arg, type):
        if not isinstance(arg, type):
            raise TypeError('Param `%s` should be of type `%s`' % (argname, type))

    @staticmethod
    def check_param_float(argname, arg):
        if not isinstance(arg, (int, float)):
            raise TypeError('Param `%s` should be of type `float`' % argname)

    def __init__(self, x=0.0, y=0.0):
        self._gd_obj_ptr = ffi.new('godot_vector2*')
        lib.godot_vector2_new(self._gd_obj_ptr, x, y)
        self._gd_obj = self._gd_obj_ptr[0]

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector2) and other.x == self.x and other.y == self.y

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __pos__(self):
        return self

    def __mul__(self, val):
        if isinstance(val, Vector2):
            gd_obj = lib.godot_vector2_operator_multiply_vector(self._gd_obj_ptr, val._gd_obj)
        else:
            gd_obj = lib.godot_vector2_operator_multiply_scalar(self._gd_obj_ptr, val)
        return Vector2.build_from_gd_obj(gd_obj)

    def __truediv__(self, val):
        if isinstance(val, Vector2):
            gd_obj = lib.godot_vector2_operator_divide_vector(self._gd_obj_ptr, val._gd_obj)
        else:
            gd_obj = lib.godot_vector2_operator_divide_scalar(self._gd_obj_ptr, val)
        return Vector2.build_from_gd_obj(gd_obj)

    # Properties

    @property
    def x(self):
        return lib.godot_vector2_get_x(self._gd_obj_ptr)

    @property
    def y(self):
        return lib.godot_vector2_get_y(self._gd_obj_ptr)

    @x.setter
    def x(self, val):
        self.check_param_float('val', val)
        lib.godot_vector2_set_x(self._gd_obj_ptr, val)

    @y.setter
    def y(self, val):
        self.check_param_float('val', val)
        lib.godot_vector2_set_y(self._gd_obj_ptr, val)

    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y

    @width.setter
    def width(self, val):
        self.x = val

    @height.setter
    def height(self, val):
        self.y = val

    # Methods

    def abs(self):
        ret = Vector2()
        lib.godot_vector2_abs(self._gd_obj_ptr, ret._gd_obj_ptr)
        return ret

    def angle(self):
        return lib.godot_vector2_angle(self._gd_obj_ptr)

    def angle_to(self, to):
        self.check_param_type('to', to, Vector2)
        return lib.godot_vector2_angle_to(self._gd_obj_ptr, to._gd_obj)

    def angle_to_point(self, to):
        self.check_param_type('to', to, Vector2)
        return lib.godot_vector2_angle_to_point(self._gd_obj_ptr, to._gd_obj)

    def clamped(self, length):
        self.check_param_float('length', length)
        gd_obj = lib.godot_vector2_clamped(self._gd_obj_ptr, length)
        return Vector2.build_from_gd_obj(gd_obj)

    def cubic_interpolate(self, b, pre_a, post_b, t):
        self.check_param_type('b', b, Vector2)
        self.check_param_type('pre_a', pre_a, Vector2)
        self.check_param_type('post_b', post_b, Vector2)
        self.check_param_float('t', t)
        gd_obj = lib.godot_vector2_cubic_interpolate(
            self._gd_obj_ptr, b._gd_obj, pre_a._gd_obj, post_b._gd_obj, t)
        return Vector2.build_from_gd_obj(gd_obj)

    def distance_squared_to(self, to):
        self.check_param_type('to', to, Vector2)
        return lib.godot_vector2_distance_squared_to(self._gd_obj_ptr, to._gd_obj)

    def distance_to(self, to):
        self.check_param_type('to', to, Vector2)
        return lib.godot_vector2_distance_to(self._gd_obj_ptr, to._gd_obj)

    def dot(self, with_):
        self.check_param_type('with_', with_, Vector2)
        return lib.godot_vector2_dot(self._gd_obj_ptr, with_._gd_obj)

    def floor(self):
        gd_obj = lib.godot_vector2_floor(self._gd_obj_ptr)
        return Vector2.build_from_gd_obj(gd_obj)

    def floorf(self):
        gd_obj = lib.godot_vector2_floorf(self._gd_obj_ptr)
        return Vector2.build_from_gd_obj(gd_obj)

    def aspect(self):
        return lib.godot_vector2_aspect(self._gd_obj_ptr)

    def length(self):
        return lib.godot_vector2_length(self._gd_obj_ptr)

    def length_squared(self):
        return lib.godot_vector2_length_squared(self._gd_obj_ptr)

    def linear_interpolate(self, b, t):
        self.check_param_type('b', b, Vector2)
        self.check_param_float('t', t)
        gd_obj = lib.godot_vector2_linear_interpolate(self._gd_obj_ptr, b._gd_obj, t)
        return Vector2.build_from_gd_obj(gd_obj)

    def normalized(self):
        gd_obj = lib.godot_vector2_normalized(self._gd_obj_ptr)
        return Vector2.build_from_gd_obj(gd_obj)

    def reflect(self, vec):
        self.check_param_type('vec', vec, Vector2)
        gd_obj = lib.godot_vector2_reflect(self._gd_obj_ptr, vec._gd_obj)
        return Vector2.build_from_gd_obj(gd_obj)

    def rotated(self, phi):
        self.check_param_float('phi', phi)
        gd_obj = lib.godot_vector2_rotated(self._gd_obj_ptr, phi)
        return Vector2.build_from_gd_obj(gd_obj)

    def slide(self, vec):
        self.check_param_type('vec', vec, Vector2)
        gd_obj = lib.godot_vector2_slide(self._gd_obj_ptr, vec._gd_obj)
        return Vector2.build_from_gd_obj(gd_obj)

    def snapped(self, by):
        self.check_param_type('by', by, Vector2)
        gd_obj = lib.godot_vector2_snapped(self._gd_obj_ptr, by._gd_obj)
        return Vector2.build_from_gd_obj(gd_obj)

    def tangent(self):
        gd_obj = lib.godot_vector2_tangent(self._gd_obj_ptr)
        return Vector2.build_from_gd_obj(gd_obj)
