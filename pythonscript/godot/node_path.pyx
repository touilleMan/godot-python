# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_node_path, godot_real, godot_int, godot_string
from godot._hazmat.conversion cimport pyobj_to_godot_string, godot_string_to_pyobj


@cython.final
cdef class NodePath:

    def __init__(self, str from_):
        cdef godot_string gd_from
        pyobj_to_godot_string(from_, &gd_from)
        gdapi.godot_node_path_new(&self._gd_data, &gd_from)
        gdapi.godot_string_destroy(&gd_from)

    def __dealloc__(self):
        gdapi.godot_node_path_destroy(&self._gd_data)

    @staticmethod
    cdef inline NodePath new(str from_):
        # Call to __new__ bypasses __init__ constructor
        cdef NodePath ret = NodePath.__new__(NodePath)
        cdef godot_string gd_from
        pyobj_to_godot_string(from_, &gd_from)
        gdapi.godot_node_path_new(&ret._gd_data, &gd_from)
        gdapi.godot_string_destroy(&gd_from)
        return ret

    @staticmethod
    cdef inline NodePath from_ptr(const godot_node_path *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef NodePath ret = NodePath.__new__(NodePath)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<NodePath({self.as_string()})>"

    # Operators

    cdef inline bint operator_equal(self, NodePath b):
        return gdapi.godot_node_path_operator_equal(&self._gd_data, &b._gd_data)

    def __eq__(self, other):
        return self.operator_equal(<NodePath?>other)

    # Properties

    # Methods

    cdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_node_path_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline bint is_absolute(self):
        return gdapi.godot_node_path_is_absolute(&self._gd_data)

    cpdef inline godot_int get_name_count(self):
        return gdapi.godot_node_path_get_name_count(&self._gd_data)

    cpdef inline str get_name(self, godot_int idx):
        cdef godot_string gd_ret = gdapi.godot_node_path_get_name(&self._gd_data, idx)
        cdef str ret = godot_string_to_pyobj(&gd_ret)
        gdapi.godot_string_destroy(&gd_ret)
        return ret

    cpdef inline godot_int get_subname_count(self):
        return gdapi.godot_node_path_get_subname_count(&self._gd_data)
 
    cpdef inline str get_subname(self, godot_int idx):
        cdef godot_string gd_ret = gdapi.godot_node_path_get_subname(&self._gd_data, idx)
        cdef str ret = godot_string_to_pyobj(&gd_ret)
        gdapi.godot_string_destroy(&gd_ret)
        return ret

    cpdef inline str get_concatenated_subnames(self):
        cdef godot_string gdret = gdapi.godot_node_path_get_concatenated_subnames(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&gdret)
        gdapi.godot_string_destroy(&gdret)
        return ret

    cpdef inline bint is_empty(self):
        return gdapi.godot_node_path_is_empty(&self._gd_data)

    cpdef inline NodePath get_as_property_path(self):
        cdef NodePath ret = NodePath.__new__(NodePath)
        ret._gd_data = gdapi11.godot_node_path_get_as_property_path(&self._gd_data)
        return ret
