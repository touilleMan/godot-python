# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_aabb, godot_int, godot_real, godot_vector3
from godot.plane cimport Plane
from godot.vector3 cimport Vector3


@cython.final
cdef class AABB:
    cdef godot_aabb _gd_data

    @staticmethod
    cdef AABB new(godot_vector3 *pos, godot_vector3 *size)

    @staticmethod
    cdef AABB from_ptr(const godot_aabb *_ptr)

    # Operators

    cdef inline bint operator_equal(self, AABB b)

    # Properties

    cdef inline Vector3 get_position(self)
    cdef inline Vector3 set_position(self, Vector3 val)
    cdef inline Vector3 get_size(self)
    cdef inline Vector3 set_size(self, Vector3 val)
    cdef inline Vector3 get_end(self)

    # Methods

    cpdef inline str as_string(self)
    cpdef inline godot_real get_area(self)
    cpdef inline bint has_no_area(self)
    cpdef inline bint has_no_surface(self)
    cpdef inline bint intersects(self, AABB with_)
    cpdef inline bint encloses(self, AABB with_)
    cpdef inline AABB merge(self, AABB with_)
    cpdef inline AABB intersection(self, AABB with_)
    cpdef inline bint intersects_plane(self, Plane plane)
    cpdef inline bint intersects_segment(self, Vector3 from_, Vector3 to)
    cpdef inline bint has_point(self, Vector3 point)
    cpdef inline Vector3 get_support(self, Vector3 dir)
    cpdef inline Vector3 get_longest_axis(self)
    cpdef inline godot_int get_longest_axis_index(self, Vector3 point)
    cpdef inline godot_real get_longest_axis_size(self, Vector3 point)
    cpdef inline Vector3 get_shortest_axis(self)
    cpdef inline godot_int get_shortest_axis_index(self, Vector3 point)
    cpdef inline godot_real get_shortest_axis_size(self, Vector3 point)
    cpdef inline AABB expand(self, Vector3 to_point)
    cpdef inline AABB grow(self, godot_real by)
    cpdef inline Vector3 get_endpoint(self, godot_int idx)
