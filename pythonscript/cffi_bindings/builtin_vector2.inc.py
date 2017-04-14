class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self._gd_obj = ffi.new('godot_vector2*')
        lib.godot_vector2_new(self._gd_obj, x, y)

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector2) and other.x == self.x and other.y == self.y

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __pos__(self):
        return self

    # Properties

    @property
    def x(self):
        return lib.godot_vector2_get_x(self._gd_obj)

    @property
    def y(self):
        return lib.godot_vector2_get_y(self._gd_obj)

    @x.setter
    def x(self, val):
        lib.godot_vector2_set_x(self._gd_obj, val)

    @y.setter
    def y(self, val):
        lib.godot_vector2_set_y(self._gd_obj, val)

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
        dest = Vector2()
        lib.godot_vector2_abs(dest._gd_obj, self._gd_obj)
        return dest

    def angle(self):
        return lib.godot_vector2_angle(self._gd_obj)

    def angle_to(self, to):
        assert isinstance(to, Vector2)
        return lib.godot_vector2_angle_to(self._gd_obj, to._gd_obj)

    def angle_to_point(self, to):
        assert isinstance(to, Vector2)
        return lib.godot_vector2_angle_to_point(self._gd_obj, to._gd_obj)

    def clamped(self, length):
        assert isinstance(length, float)
        dest = Vector2()
        lib.godot_vector2_clamped(dest._gd_obj, self._gd_obj, length)
        return dest

    def cubic_interpolate(self, b, pre_a, post_b, t):
        assert isinstance(b, Vector2)
        assert isinstance(pre_a, Vector2)
        assert isinstance(post_b, Vector2)
        assert isinstance(t, float)
        dest = Vector2()
        lib.godot_vector2_cubic_interpolate(
            dest._gd_obj, self._gd_obj, b._gd_obj, pre_a._gd_obj, post_b._gd_obj, t)
        return dest

    def distance_squared_to(self, to):
        assert isinstance(to, Vector2)
        return lib.godot_vector2_distance_squared_to(self._gd_obj, to._gd_obj)

    def distance_to(self, to):
        assert isinstance(to, Vector2)
        return lib.godot_vector2_distance_to(self._gd_obj, to._gd_obj)

    def dot(self, with_):
        assert isinstance(with_, Vector2)
        return lib.godot_vector2_dot(self._gd_obj, with_._gd_obj)

    def floor(self):
        dest = Vector2()
        lib.godot_vector2_floor(dest._gd_obj, self._gd_obj)
        return dest

    def floorf(self):
        dest = Vector2()
        lib.godot_vector2_floorf(dest._gd_obj, self._gd_obj)
        return dest

    def aspect(self):
        return lib.godot_vector2_aspect(self._gd_obj)

    def length(self):
        return lib.godot_vector2_length(self._gd_obj)

    def length_squared(self):
        return lib.godot_vector2_length_squared(self._gd_obj)

    def linear_interpolate(self, b, t):
        assert isinstance(b, Vector2)
        assert isinstance(t, float)
        dest = Vector2()
        lib.godot_vector2_linear_interpolate(dest._gd_obj, self._gd_obj, b._gd_obj, t)
        return dest

    def normalized(self):
        dest = Vector2()
        lib.godot_vector2_normalized(dest._gd_obj, self._gd_obj)
        return dest

    def reflect(self, vec):
        assert isinstance(vec, Vector2)
        dest = Vector2()
        lib.godot_vector2_reflect(dest._gd_obj, self._gd_obj, vec._gd_obj)
        return dest

    def rotated(self, phi):
        assert isinstance(phi, float)
        dest = Vector2()
        lib.godot_vector2_rotated(dest._gd_obj, self._gd_obj, phi)
        return dest

    def slide(self, vec):
        assert isinstance(vec, Vector2)
        dest = Vector2()
        lib.godot_vector2_slide(dest._gd_obj, self._gd_obj, vec._gd_obj)
        return dest

    def snapped(self, by):
        assert isinstance(by, Vector2)
        dest = Vector2()
        lib.godot_vector2_snapped(dest._gd_obj, self._gd_obj, by._gd_obj)
        return dest

    def tangent(self):
        dest = Vector2()
        lib.godot_vector2_tangent(dest._gd_obj, self._gd_obj)
        return dest

    def to_string(self):
        dest = Vector2()
        lib.godot_vector2_to_string(dest._gd_obj, self._gd_obj)
        return dest
