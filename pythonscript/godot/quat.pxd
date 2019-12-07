# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_quat, godot_real
from godot.vector3 cimport Vector3
from godot.basis cimport Basis


@cython.final
cdef class Quat:
    cdef godot_quat _gd_data

    @staticmethod
    cdef inline Quat new(godot_real x, godot_real y, godot_real z, godot_real w)

    @staticmethod
    cdef inline Quat new_with_axis_angle(Vector3 axis, godot_real angle)

    @staticmethod
    cdef inline Quat new_with_basis(Basis basis)

    @staticmethod
    cdef inline Quat new_with_euler(Vector3 euler)

    @staticmethod
    cdef inline Quat from_ptr(const godot_quat *_ptr)

    # Operators

    cdef inline Quat operator_add(self, Quat b)
    cdef inline Quat operator_subtract(self, Quat b)
    cdef inline Quat operator_multiply(self, godot_real b)
    cdef inline Quat operator_divide(self, godot_real b)
    cdef inline bint operator_equal(self, Quat b)
    cdef inline Quat operator_neg(self)

    # Property

    cdef inline godot_real get_x(self)
    cdef inline void set_x(self, godot_real val)
    cdef inline godot_real get_y(self)
    cdef inline void set_y(self, godot_real val)
    cdef inline godot_real get_z(self)
    cdef inline void set_z(self, godot_real val)
    cdef inline godot_real get_w(self)
    cdef inline void set_w(self, godot_real val)

    # Methods

    cdef inline str as_string(self)
    cpdef inline godot_real length(self)
    cpdef inline godot_real length_squared(self)
    cpdef inline Quat normalized(self)
    cpdef inline bint is_normalized(self)
    cpdef inline Quat inverse(self)
    cpdef inline godot_real dot(self, Quat b)
    cpdef inline Vector3 xform(self, Vector3 v)
    cpdef inline Quat slerp(self, Quat b, godot_real t)
    cpdef inline Quat slerpni(self, Quat b, godot_real t)
    cpdef inline Quat cubic_slerp(self, Quat b, Quat pre_a, Quat post_b, godot_real t)
    cpdef inline void set_axis_angle(self, Vector3 axis, godot_real angle)
