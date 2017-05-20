class Quat(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_QUAT

    def __init__(self):
        self._gd_ptr = ffi.new('godot_quat*')
