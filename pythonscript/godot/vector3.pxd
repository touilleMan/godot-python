# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_vector3, godot_int, godot_real
from godot.basis cimport Basis


@cython.final
cdef class Vector3:
    cdef godot_vector3 _gd_data

    @staticmethod
    cdef inline Vector3 new(godot_real x=*, godot_real y=*, godot_real z=*)

    @staticmethod
    cdef inline Vector3 from_ptr(const godot_vector3 *_ptr)

    # Operators

    cdef inline Vector3 operator_add(self, Vector3 b)
    cdef inline Vector3 operator_subtract(self, Vector3 b)
    cdef inline Vector3 operator_multiply_vector(self, Vector3 b)
    cdef inline Vector3 operator_multiply_scalar(self, godot_real b)
    cdef inline Vector3 operator_divide_vector(self, Vector3 b)
    cdef inline Vector3 operator_divide_scalar(self, godot_real b)
    cdef inline bint operator_equal(self, Vector3 b)
    cdef inline bint operator_less(self, Vector3 b)
    cdef inline Vector3 operator_neg(self)

    # Properties

    cdef inline godot_real get_x(self)
    cdef inline void set_x(self, godot_real val)
    cdef inline godot_real get_y(self)
    cdef inline void set_y(self, godot_real val)
    cdef inline godot_real get_z(self)
    cdef inline void set_z(self, godot_real val)

    # Methods

    cpdef inline godot_int min_axis(self)
    cpdef inline godot_int max_axis(self)
    cpdef inline godot_real length(self)
    cpdef inline godot_real length_squared(self)
    cpdef inline bint is_normalized(self)
    cpdef inline Vector3 normalized(self)
    cpdef inline Vector3 inverse(self)
    cpdef inline Vector3 snapped(self, Vector3 by)
    cpdef inline Vector3 rotated(self, Vector3 axis, godot_real phi)
    cpdef inline Vector3 linear_interpolate(self, Vector3 b, godot_real t)
    cpdef inline Vector3 cubic_interpolate(self, Vector3 b, Vector3 pre_a, Vector3 post_b, godot_real t)
    cpdef inline Vector3 move_toward(self, Vector3 to, godot_real delta)
    cpdef inline godot_real dot(self, Vector3 b)
    cpdef inline Vector3 cross(self, Vector3 b)
    cpdef inline Basis outer(self, Vector3 b)
    cpdef inline Basis to_diagonal_matrix(self)
    cpdef inline Vector3 abs(self)
    cpdef inline Vector3 floor(self)
    cpdef inline Vector3 ceil(self)
    cpdef inline godot_real distance_to(self, Vector3 b)
    cpdef inline godot_real distance_squared_to(self, Vector3 b)
    cpdef inline godot_real angle_to(self, Vector3 to)
    cpdef inline Vector3 slide(self, Vector3 n)
    cpdef inline Vector3 bounce(self, Vector3 n)
    cpdef inline Vector3 reflect(self, Vector3 n)
