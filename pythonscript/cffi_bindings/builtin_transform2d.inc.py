
class Transform2d(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_TRANSFORM2D

    def __init__(self):
        self._gd_ptr = ffi.new('godot_transform2d*')
        lib.godot_transform2d_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, Transform2d) and lib.godot_transform2d_operator_equal(self._gd_ptr, other._gd_ptr)

    # Properties

    # Methods
