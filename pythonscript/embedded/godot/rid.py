from pythonscriptcffi import lib

from godot.hazmat.base import BaseBuiltin
from godot.hazmat.allocator import godot_rid_alloc


class RID(BaseBuiltin):
    __slots__ = ()
    GD_TYPE = lib.GODOT_VARIANT_TYPE_RID

    @staticmethod
    def _copy_gdobj(gdobj):
        return godot_rid_alloc(gdobj[0])

    def __init__(self, from_=None):
        self._gd_ptr = godot_rid_alloc()
        if from_:
            from godot.bindings import Resource

            self._check_param_type("from_", from_, Resource)
            lib.godot_rid_new_with_resource(self._gd_ptr, from_._gd_ptr)

    def __repr__(self):
        return "<%s(id=%s)>" % (type(self).__name__, self.get_id())

    def __eq__(self, other):
        return isinstance(other, RID) and lib.godot_rid_operator_equal(
            self._gd_ptr, other._gd_ptr
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, RID):
            return lib.godot_rid_operator_less(self._gd_ptr, other._gd_ptr)

        return NotImplemented

    # Properties

    # Methods

    def get_id(self):
        return lib.godot_rid_get_id(self._gd_ptr)
