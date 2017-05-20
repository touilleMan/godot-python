
class Rect3(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_RECT3

    def __init__(self):
        self._gd_ptr = ffi.new('godot_rect3*')
        lib.godot_rect3_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, Rect3) and lib.godot_rect3_operator_equal(self._gd_ptr, other._gd_ptr)

    # Properties

    # Methods
