class Basis:
    def __init__(self):
        self._gd_obj = ffi.new('godot_basis*')
        lib.godot_basis_new(self._gd_obj)
