# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_node_path, godot_real, godot_int
from godot.gdstring cimport GDString


@cython.final
cdef class NodePath:
    cdef godot_node_path _gd_data

    @staticmethod
    cdef inline NodePath new(GDString from_)

    @staticmethod
    cdef inline NodePath from_ptr(const godot_node_path *_ptr)

    # Operators

    cdef inline bint operator_equal(self, NodePath b)

    # Properties

    # Methods

    cdef inline str as_string(self)
    cpdef inline bint is_absolute(self)
    cpdef inline godot_int get_name_count(self)
    cpdef inline str get_name(self, godot_int idx)
    cpdef inline godot_int get_subname_count(self)
    cpdef inline str get_subname(self, godot_int idx)
    cpdef inline str get_concatenated_subnames(self)
    cpdef inline bint is_empty(self)
    cpdef inline NodePath get_as_property_path(self)
