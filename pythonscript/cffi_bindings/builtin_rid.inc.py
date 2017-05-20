class RID(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_RID

    def __init__(self, from_=None):
        self._gd_ptr = ffi.new('godot_rid*')
        if from_:
            self._check_param_type('from_', from_, godot_bindings_module.Resource)
            lib.godot_rid_new_with_resource(self._gd_ptr, from_._gd_ptr)
        else:
            lib.godot_rid_new(self._gd_ptr)

    def __repr__(self):
        return "<%s(id=%s)>" % (type(self).__name__, self.get_id())

    def __eq__(self, other):
        return isinstance(other, RID) and lib.godot_rid_operator_equal(self._gd_ptr, other._gd_ptr)

    def __lt__(self, other):
        if isinstance(other, RID):
            return lib.godot_rid_operator_less(self._gd_ptr, other._gd_ptr)
        return NotImplemented

    # Properties

    # Methods

    def get_id(self):
        return lib.godot_rid_get_id(self._gd_ptr)
