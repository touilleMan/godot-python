class NodePath(BaseBuiltin):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_NODE_PATH

    def __init__(self, path):
        self._check_param_type('path', path, str)
        self._gd_ptr = ffi.new('godot_node_path*')
        gd_str = pyobj_to_raw(path)
        lib.godot_node_path_new(self._gd_ptr, gd_str)

    def __eq__(self, other):
        return isinstance(other, NodePath) and self.path == other.path

    def __ne__(self, other):
        return not self == other

    def __del__(self):
        lib.godot_node_path_destroy(self._gd_ptr)

    def __repr__(self):
        return "<%s(path=%r)>" % (type(self).__name__, self.path)

    @property
    def path(self):
        gd_repr = lib.godot_node_path_as_string(self._gd_ptr)
        return ffi.string(lib.godot_string_unicode_str(ffi.addressof(gd_repr)))

    def get_name(self, idx):
        self._check_param_type('idx', idx, int)
        name = lib.godot_node_path_get_name(self._gd_ptr, idx)
        return godot_string_to_pyobj(ffi.addressof(name))

    def get_name_count(self):
        return lib.godot_node_path_get_name_count(self._gd_ptr)

    def get_property(self):
        prop = lib.godot_node_path_get_property(self._gd_ptr)
        return godot_string_to_pyobj(ffi.addressof(prop))

    def get_subname(self, idx):
        self._check_param_type('idx', idx, int)
        subname = lib.godot_node_path_get_subname(self._gd_ptr, idx)
        return godot_string_to_pyobj(ffi.addressof(subname))

    def get_subname_count(self):
        return lib.godot_node_path_get_subname_count(self._gd_ptr)

    def is_absolute(self):
        return bool(lib.godot_node_path_is_absolute(self._gd_ptr))

    def is_empty(self):
        return bool(lib.godot_node_path_is_empty(self._gd_ptr))
