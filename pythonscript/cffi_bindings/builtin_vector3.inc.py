class Vector3:
    GD_TYPE = lib.GODOT_VARIANT_TYPE_VECTOR3

    @classmethod
    def build_from_gd_obj(cls, gd_obj):
        # TODO: optimize this
        v = cls()
        v._gd_obj = gd_obj
        v._gd_obj_ptr = ffi.addressof(gd_obj)
        return v

    @staticmethod
    def check_param_type(argname, arg, type):
        if not isinstance(arg, type):
            raise TypeError('Param `%s` should be of type `%s`' % (argname, type))

    @staticmethod
    def check_param_float(argname, arg):
        if not isinstance(arg, (int, float)):
            raise TypeError('Param `%s` should be of type `float`' % argname)

    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._gd_obj = lib.godot_vector3_new(x, y, z)
        self._gd_obj_ptr = ffi.addressof(self._gd_obj)

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
        return lib.godot_vector3_get_axis(self._gd_obj_ptr, self.AXIS_X)

    @property
    def y(self):
        return lib.godot_vector3_get_axis(self._gd_obj_ptr, self.AXIS_Y)

    @property
    def z(self):
        return lib.godot_vector3_get_axis(self._gd_obj_ptr, self.AXIS_Z)

    @x.setter
    def x(self, val):
        self.check_param_float('val', val)
        lib.godot_vector3_set_axis(self._gd_obj_ptr, self.AXIS_X, val)

    @y.setter
    def y(self, val):
        self.check_param_float('val', val)
        lib.godot_vector3_set_axis(self._gd_obj_ptr, self.AXIS_Y, val)

    @z.setter
    def z(self, val):
        self.check_param_float('val', val)
        lib.godot_vector3_set_axis(self._gd_obj_ptr, self.AXIS_Z, val)

    # Methods

    def min_axis(self):
        return lib.godot_vector3_min_axis(self._gd_obj_ptr)

    def max_axis(self):
        return lib.godot_vector3_max_axis(self._gd_obj_ptr)

    def length(self):
        return lib.godot_vector3_length(self._gd_obj_ptr)

    def length_squared(self):
        return lib.godot_vector3_length_squared(self._gd_obj_ptr)

    def normalize(self):
        return lib.godot_vector3_normalize(self._gd_obj_ptr)

    def normalized(self):
        gd_obj = lib.godot_vector3_normalized(self._gd_obj_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def inverse(self):
        gd_obj = lib.godot_vector3_inverse(self._gd_obj_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def zero(self):
        lib.godot_vector3_zero(self._gd_obj_ptr)

    def snap(self, val):
        self.check_param_float('val', val)
        lib.godot_vector3_snap(self._gd_obj_ptr)

    def snapped(self, val):
        self.check_param_float('val', val)
        gd_obj = lib.godot_vector3_snapped(self._gd_obj_ptr, val)
        return Vector3.build_from_gd_obj(gd_obj)

    def rotate(self, axis, phi):
        self.check_param_type('axis', axis, Vector3)
        self.check_param_float('phi', phi)
        lib.godot_vector3_rotate(self._gd_obj_ptr, axis._gd_obj, phi)

    def rotated(self, axis, phi):
        self.check_param_type('axis', axis, Vector3)
        self.check_param_float('phi', phi)
        gd_obj = lib.godot_vector3_rotated(self._gd_obj_ptr, axis._gd_obj, phi)
        return Vector3.build_from_gd_obj(gd_obj)

    def linear_interpolate(self, b, t):
        self.check_param_type('b', b, Vector3)
        self.check_param_float('t', t)
        gd_obj = lib.godot_vector3_linear_interpolate(self._gd_obj_ptr, b._gd_obj, t)
        return Vector3.build_from_gd_obj(gd_obj)

    def cubic_interpolate(self, b, pre_a, post_b, t):
        self.check_param_type('b', b, Vector3)
        self.check_param_type('pre_a', pre_a, Vector3)
        self.check_param_type('post_b', post_b, Vector3)
        self.check_param_float('t', t)
        gd_obj = lib.godot_vector3_cubic_interpolate(self._gd_obj_ptr, b._gd_obj, pre_a._gd_obj, post_b._gd_obj, t)
        return Vector3.build_from_gd_obj(gd_obj)

    def cubic_interpolaten(self, b, pre_a, post_b, t):
        self.check_param_type('b', b, Vector3)
        self.check_param_type('pre_a', pre_a, Vector3)
        self.check_param_type('post_b', post_b, Vector3)
        self.check_param_float('t', t)
        gd_obj = lib.godot_vector3_cubic_interpolaten(self._gd_obj_ptr, b._gd_obj, pre_a._gd_obj, post_b._gd_obj, t)
        return Vector3.build_from_gd_obj(gd_obj)

    def cross(self, b):
        self.check_param_type('b', b, Vector3)
        gd_obj = lib.godot_vector3_cross(self._gd_obj_ptr, b._gd_obj)
        return Vector3.build_from_gd_obj(gd_obj)

    def dot(self, b):
        self.check_param_type('b', b, Vector3)
        return lib.godot_vector3_dot(self._gd_obj_ptr, b._gd_obj)

    def outer(self, b):
        self.check_param_type('b', b, Vector3)
        gd_obj = lib.godot_vector3_outer(self._gd_obj_ptr, b._gd_obj)
        return Basis.build_from_gd_obj(gd_obj)

    def to_diagonal_matrix(self):
        gd_obj = lib.godot_vector3_to_diagonal_matrix(self._gd_obj_ptr)
        return Basis.build_from_gd_obj(gd_obj)

    def abs(self):
        gd_obj = lib.godot_vector3_abs(self._gd_obj_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def floor(self):
        gd_obj = lib.godot_vector3_floor(self._gd_obj_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def ceil(self):
        gd_obj = lib.godot_vector3_ceil(self._gd_obj_ptr)
        return Vector3.build_from_gd_obj(gd_obj)

    def distance_to(self, b):
        self.check_param_type('b', b, Vector3)
        return lib.godot_vector3_distance_to(self._gd_obj_ptr, b._gd_obj)

    def distance_squared_to(self, b):
        self.check_param_type('b', b, Vector3)
        return lib.godot_vector3_distance_squared_to(self._gd_obj_ptr, b._gd_obj)

    def angle_to(self, b):
        self.check_param_type('b', b, Vector3)
        return lib.godot_vector3_angle_to(self._gd_obj_ptr, b._gd_obj)

    def slide(self, vec):
        self.check_param_type('vec', vec, Vector3)
        gd_obj = lib.godot_vector3_slide(self._gd_obj_ptr, vec._gd_obj)
        return Vector3.build_from_gd_obj(gd_obj)

    def bounce(self, vec):
        self.check_param_type('vec', vec, Vector3)
        gd_obj = lib.godot_vector3_bounce(self._gd_obj_ptr, vec._gd_obj)
        return Vector3.build_from_gd_obj(gd_obj)

    def reflect(self, vec):
        self.check_param_type('vec', vec, Vector3)
        gd_obj = lib.godot_vector3_reflect(self._gd_obj_ptr, vec._gd_obj)
        return Vector3.build_from_gd_obj(gd_obj)
