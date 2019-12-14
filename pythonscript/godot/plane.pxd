# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_plane, godot_real
from godot.vector3 cimport Vector3
from godot.plane cimport Plane


@cython.final
cdef class Plane:
    cdef godot_plane _gd_data

    @staticmethod
    cdef inline Plane new_with_reals(godot_real a, godot_real b, godot_real c, godot_real d)

    @staticmethod
    cdef inline Plane new_with_vectors(Vector3 v1, Vector3 v2, Vector3 v3)

    @staticmethod
    cdef inline Plane new_with_normal(Vector3 normal, godot_real d)

    @staticmethod
    cdef inline Plane from_ptr(const godot_plane *_ptr)

    # Operators

    cdef inline bint operator_equal(self, Plane b)
    cdef inline Plane operator_neg(self)

    # Property

    cdef inline godot_real get_d(self)
    cdef inline void set_d(self, godot_real d)
    cdef inline Vector3 get_normal(self)
    cdef inline void set_normal(self, Vector3 normal)

    # Methods

    cpdef inline str as_string(self)
    cpdef inline Plane normalized(self)
    cpdef inline Vector3 center(self)
    cpdef inline Vector3 get_any_point(self)
    cpdef inline bint is_point_over(self, Vector3 point)
    cpdef inline godot_real distance_to(self, Vector3 point)
    cpdef inline bint has_point(self, Vector3 point, godot_real epsilon)
    cpdef inline Vector3 project(self, Vector3 point)
    cpdef inline Vector3 intersect_3(self, Plane b, Plane c)
    cpdef inline Vector3 intersects_ray(self, Vector3 from_, Vector3 dir)
    cpdef inline Vector3 intersects_segment(self, Vector3 begin, Vector3 end)
