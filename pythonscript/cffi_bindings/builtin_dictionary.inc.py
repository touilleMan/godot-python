
class Dictionary(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_DICTIONARY

    def __init__(self):
        self._gd_ptr = ffi.new('godot_dictionary*')
        lib.godot_dictionary_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, Dictionary) and lib.godot_dictionary_operator_equal(self._gd_ptr, other._gd_ptr)

    # Properties

    # Methods
