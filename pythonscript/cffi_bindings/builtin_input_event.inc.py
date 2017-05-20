
class InputEvent(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_INPUT_EVENT

    def __init__(self):
        self._gd_ptr = ffi.new('godot_input_event*')
        lib.godot_input_event_new(self._gd_ptr)


    def __repr__(self):
        return "<%s()>" % (type(self).__name__)

    def __eq__(self, other):
        return isinstance(other, InputEvent) and lib.godot_input_event_operator_equal(self._gd_ptr, other._gd_ptr)

    # Properties

    # Methods
