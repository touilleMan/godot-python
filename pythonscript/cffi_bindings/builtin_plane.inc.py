
class Plane(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_PLANE

    def __init__(self):
        self._gd_ptr = ffi.new('godot_plane*')
        lib.godot_plane_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, Plane) and lib.godot_plane_operator_equal(self._gd_ptr, other._gd_ptr)

    def __ne__(self, other):
        return not self == other

    # Properties

    # Methods
