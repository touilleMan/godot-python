class Quat:
    def __init__(self):
        self._gd_ptr = ffi.new('godot_quat*')
