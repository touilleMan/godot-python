# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_node_path, godot_real, godot_int


@cython.final
cdef class NodePath:
    cdef godot_node_path _gd_data

    @staticmethod
    cdef NodePath new(str from_)

    @staticmethod
    cdef NodePath from_ptr(const godot_node_path *_ptr)

    # Operators

    cdef inline bint operator_equal(self, NodePath b)

    # Properties

    # Methods

    cdef inline str as_string(self)
    cpdef bint is_absolute(self)
    cpdef godot_int get_name_count(self)
    cpdef str get_name(self, godot_int idx)
    cpdef godot_int get_subname_count(self)
    cpdef str get_subname(self, godot_int idx)
    cpdef str get_concatenated_subnames(self)
    cpdef bint is_empty(self)
    cpdef NodePath get_as_property_path(self)
