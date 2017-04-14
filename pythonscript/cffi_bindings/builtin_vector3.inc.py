class Vector3:

    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._gd_obj = ffi.new('godot_vector3*')
        lib.godot_vector3_new(self._gd_obj, x, y, z)

    def __repr__(self):
        return "<%s(x=%s, y=%s, z=%s)>" % (type(self).__name__, self.x, self.y, self.z)

    def __eq__(self, other):
        return (isinstance(other, Vector3) and other.x == self.x and
                other.y == self.y and other.z == self.z)

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self

    # Properties

    @property
    def x(self):
        return lib.godot_vector3_get_axis(self._gd_obj, self.AXIS_X)

    @property
    def y(self):
        return lib.godot_vector3_get_axis(self._gd_obj, self.AXIS_Y)

    @property
    def z(self):
        return lib.godot_vector3_get_axis(self._gd_obj, self.AXIS_Z)

    @x.setter
    def x(self, val):
        lib.godot_vector3_set_axis(self._gd_obj, self.AXIS_X, val)

    @y.setter
    def y(self, val):
        lib.godot_vector3_set_axis(self._gd_obj, self.AXIS_Y, val)

    @z.setter
    def z(self, val):
        lib.godot_vector3_set_axis(self._gd_obj, self.AXIS_Z, val)

    # Methods

    def min_axis(self):
        return lib.godot_vector3_min_axis(self._gd_obj)

    def max_axis(self):
        return lib.godot_vector3_max_axis(self._gd_obj)

    def length(self):
        return lib.godot_vector3_length(self._gd_obj)

    def length_squared(self):
        return lib.godot_vector3_length_squared(self._gd_obj)

    def normalize(self):
        return lib.godot_vector3_normalize(self._gd_obj)

    def normalized(self):
        dest = Vector3()
        lib.godot_vector3_normalized(dest._gd_obj, self._gd_obj)
        return dest

    def inverse(self):
        dest = Vector3()
        lib.godot_vector3_inverse(dest._gd_obj, self._gd_obj)
        return dest

    def zero(self):
        lib.godot_vector3_zero(self._gd_obj)

    def snap(self, val):
        assert isinstance(val, float)
        lib.godot_vector3_snap(self._gd_obj)

    def snapped(self, val):
        assert isinstance(val, float)
        dest = Vector3()
        lib.godot_vector3_snapped(dest._gd_obj, self._gd_obj, val)
        return dest

    def rotate(self, axis, phi):
        assert isinstance(axis, Vector3)
        assert isinstance(phi, float)
        lib.godot_vector3_rotate(self._gd_obj, axis._gd_obj, phi)

    def rotated(self, axis, phi):
        assert isinstance(axis, Vector3)
        assert isinstance(phi, float)
        dest = Vector3()
        lib.godot_vector3_rotated(dest._gd_obj, self._gd_obj, axis._gd_obj, phi)
        return dest

    def linear_interpolate(self, b, t):
        assert isinstance(b, Vector3)
        assert isinstance(t, float)
        dest = Vector3()
        lib.godot_vector3_linear_interpolate(dest._gd_obj, self._gd_obj, b._gd_obj, t)
        return dest

    def cubic_interpolate(self, b, pre_a, post_b, t):
        assert isinstance(b, Vector3)
        assert isinstance(pre_a, Vector3)
        assert isinstance(post_b, Vector3)
        assert isinstance(t, float)
        dest = Vector3()
        lib.godot_vector3_cubic_interpolate(dest._gd_obj, self._gd_obj, b._gd_obj, pre_a._gd_obj, post_b._gd_obj, t)
        return dest

    def cubic_interpolaten(self, b, pre_a, post_b, t):
        assert isinstance(b, Vector3)
        assert isinstance(pre_a, Vector3)
        assert isinstance(post_b, Vector3)
        assert isinstance(t, float)
        dest = Vector3()
        lib.godot_vector3_cubic_interpolaten(dest._gd_obj, self._gd_obj, b._gd_obj, pre_a._gd_obj, post_b._gd_obj, t)
        return dest

    def cross(self, b):
        assert isinstance(b, Vector3)
        dest = Vector3()
        lib.godot_vector3_cross(dest._gd_obj, self._gd_obj, b._gd_obj)
        return dest

    def dot(self, b):
        assert isinstance(b, Vector3)
        return lib.godot_vector3_dot(self._gd_obj, b._gd_obj)

    def outer(self, b):
        assert isinstance(b, Vector3)
        dest = Basis()
        lib.godot_vector3_outer(dest._gd_obj, self._gd_obj, b._gd_obj)
        return dest

    def to_diagonal_matrix(self):
        dest = Basis()
        lib.godot_vector3_to_diagonal_matrix(dest._gd_obj, self._gd_obj)
        return dest

    def abs(self):
        dest = Vector3()
        lib.godot_vector3_abs(dest._gd_obj, self._gd_obj)
        return dest

    def floor(self):
        dest = Vector3()
        lib.godot_vector3_floor(dest._gd_obj, self._gd_obj)
        return dest

    def ceil(self):
        dest = Vector3()
        lib.godot_vector3_ceil(dest._gd_obj, self._gd_obj)
        return dest

    def distance_to(self, b):
        assert isinstance(b, Vector3)
        return lib.godot_vector3_distance_to(self._gd_obj, b._gd_obj)

    def distance_squared_to(self, b):
        assert isinstance(b, Vector3)
        return lib.godot_vector3_distance_squared_to(self._gd_obj, b._gd_obj)

    def angle_to(self, b):
        assert isinstance(b, Vector3)
        return lib.godot_vector3_angle_to(self._gd_obj, b._gd_obj)

    def slide(self, vec):
        assert isinstance(vec, Vector3)
        dest = Vector3()
        lib.godot_vector3_slide(dest._gd_obj, self._gd_obj, vec._gd_obj)
        return dest

    def bounce(self, vec):
        assert isinstance(vec, Vector3)
        dest = Vector3()
        lib.godot_vector3_bounce(dest._gd_obj, self._gd_obj, vec._gd_obj)
        return dest

    def reflect(self, vec):
        assert isinstance(vec, Vector3)
        dest = Vector3()
        lib.godot_vector3_reflect(dest._gd_obj, self._gd_obj, vec._gd_obj)
        return dest
