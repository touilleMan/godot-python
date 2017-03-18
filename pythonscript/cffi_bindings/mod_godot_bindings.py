class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.__gdobj = ffi.new('godot_vector2*')
        lib.godot_vector2_new(self.__gdobj, x, y)

    @property
    def x(self):
        return lib.godot_vector2_get_x(self.__gdobj)

    @property
    def y(self):
        return lib.godot_vector2_get_y(self.__gdobj)

    @x.setter
    def x(self, val):
        return lib.godot_vector2_set_x(self.__gdobj, val)

    @y.setter
    def y(self, val):
        return lib.godot_vector2_set_y(self.__gdobj, val)

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)


module = imp.new_module("godot.bindings")
module.Vector2 = Vector2
sys.modules["godot.bindings"] = module
