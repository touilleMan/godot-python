from pythonscriptcffi import lib, ffi

from godot.hazmat.base import BaseBuiltinWithGDObjOwnership
from godot.hazmat.allocator import godot_node_path_alloc, godot_variant_alloc
from godot.hazmat.tools import pyobj_to_gdobj, godot_string_to_pyobj


def str_to_gd_node_path(path, to_variant=False):
    gd_str = pyobj_to_gdobj(path)
    gd_ptr = godot_node_path_alloc()
    lib.godot_node_path_new(gd_ptr, gd_str)
    if to_variant:
        gdvar_ptr = godot_variant_alloc()
        lib.godot_variant_new_node_path(gdvar_ptr, gd_ptr)
    return gd_ptr


class NodePath(BaseBuiltinWithGDObjOwnership):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_NODE_PATH

    @staticmethod
    def _copy_gdobj(gdobj):
        cpy_gdobj = godot_node_path_alloc()
        lib.godot_node_path_new_copy(cpy_gdobj, gdobj)
        return cpy_gdobj

    def __init__(self, path):
        self._check_param_type("path", path, str)
        gd_str = pyobj_to_gdobj(path)
        self._gd_ptr = godot_node_path_alloc()
        lib.godot_node_path_new(self._gd_ptr, gd_str)

    def __eq__(self, other):
        # Note we could also use `godot_node_path_operator_equal` for this...
        return isinstance(other, NodePath) and self.path == other.path

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "<%s(path=%r)>" % (type(self).__name__, self.path)

    @property
    def path(self):
        gd_repr = lib.godot_node_path_as_string(self._gd_ptr)
        return ffi.string(lib.godot_string_wide_str(ffi.addressof(gd_repr)))

    def get_name(self, idx):
        self._check_param_type("idx", idx, int)
        name = lib.godot_node_path_get_name(self._gd_ptr, idx)
        return godot_string_to_pyobj(ffi.addressof(name))

    def get_name_count(self):
        return lib.godot_node_path_get_name_count(self._gd_ptr)

    def get_concatenated_subnames(self):
        concatenated = lib.godot_node_path_get_concatenated_subnames(self._gd_ptr)
        return godot_string_to_pyobj(ffi.addressof(concatenated))

    def get_subname(self, idx):
        self._check_param_type("idx", idx, int)
        subname = lib.godot_node_path_get_subname(self._gd_ptr, idx)
        return godot_string_to_pyobj(ffi.addressof(subname))

    def get_subname_count(self):
        return lib.godot_node_path_get_subname_count(self._gd_ptr)

    def is_absolute(self):
        return bool(lib.godot_node_path_is_absolute(self._gd_ptr))

    def is_empty(self):
        return bool(lib.godot_node_path_is_empty(self._gd_ptr))
