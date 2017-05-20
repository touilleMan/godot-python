
class Transform(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_TRANSFORM

    def __init__(self):
        self._gd_ptr = ffi.new('godot_transform*')
        lib.godot_transform_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, Transform) and lib.godot_transform_operator_equal(self._gd_ptr, other._gd_ptr)

    # Properties

    # Methods
