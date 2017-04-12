# TODO: use pybind11 for this ?
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self._gd_obj = ffi.new('godot_vector2*')
        lib.godot_vector2_new(self._gd_obj, x, y)

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

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector2) and other.x == self.x and other.y == self.y

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __pos__(self):
        return self


class Vector3:
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._gd_obj = ffi.new('godot_vector3*')
        lib.godot_vector3_new(self._gd_obj, x, y, z)

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

    def __repr__(self):
        return "<%s(x=%s, y=%s, z=%s)>" % (type(self).__name__, self.x, self.y, self.z)

    def __eq__(self, other):
        return (isinstance(other, Vector3) and other.x == self.x and
                other.y == self.y and other.z == self.z)

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self


def get_builtins():
    return {
        'Vector2': Vector2,
        'Vector3': Vector3
    }
