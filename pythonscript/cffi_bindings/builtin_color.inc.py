
class Color(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_COLOR

    def __init__(self):
        self._gd_ptr = ffi.new('godot_color*')
        lib.godot_color_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, Color) and lib.godot_color_operator_equal(self._gd_ptr, other._gd_ptr)

    # Properties

    # Methods
