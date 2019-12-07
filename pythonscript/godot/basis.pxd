# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_basis, godot_real, godot_int
from godot.vector3 cimport Vector3
from godot.quat cimport Quat


@cython.final
cdef class Basis:
    cdef godot_basis _gd_data

    @staticmethod
    cdef inline Basis new()

    @staticmethod
    cdef inline Basis new_with_rows(Vector3 x, Vector3 y, Vector3 z)

    @staticmethod
    cdef inline Basis new_with_axis_and_angle(Vector3 axis, godot_real phi)

    @staticmethod
    cdef inline Basis new_with_euler(Vector3 from_)

    @staticmethod
    cdef inline Basis new_with_euler_quat(Quat from_)

    @staticmethod
    cdef inline Basis from_ptr(const godot_basis *_ptr)

    # Operators

    cdef inline Basis operator_add(self, Basis b)
    cdef inline Basis operator_subtract(self, Basis b)
    cdef inline Basis operator_multiply_vector(self, Basis b)
    cdef inline Basis operator_multiply_scalar(self, godot_real b)
    cdef inline bint operator_equal(self, Basis b)

    # Property

    cdef inline Vector3 get_x(self)
    cdef inline void set_x(self, Vector3 val)
    cdef inline Vector3 get_y(self)
    cdef inline void set_y(self, Vector3 val)
    cdef inline Vector3 get_z(self)
    cdef inline void set_z(self, Vector3 val)

    # Methods

    cdef inline str as_string(self)
    cpdef inline Basis inverse(self)
    cpdef inline Basis transposed(self)
    cpdef inline Basis orthonormalized(self)
    cpdef inline godot_real determinant(self)
    cpdef inline Basis rotated(self, Vector3 axis, godot_real phi)
    cpdef inline Basis scaled(self, Vector3 scale)
    cpdef inline Vector3 get_scale(self)
    cpdef inline Vector3 get_euler(self)
    cpdef inline Quat get_quat(self)
    cpdef inline void set_quat(self, Quat quat)
    cpdef inline void set_axis_angle_scale(self, Vector3 axis, godot_real phi, Vector3 scale)
    cpdef inline void set_euler_scale(self, Vector3 euler, Vector3 scale)
    cpdef inline void set_quat_scale(self, Quat quat, Vector3 scale)
    cpdef inline godot_real tdotx(self, Vector3 with_)
    cpdef inline godot_real tdoty(self, Vector3 with_)
    cpdef inline godot_real tdotz(self, Vector3 with_)
    cpdef inline Vector3 xform(self, Vector3 v)
    cpdef inline Vector3 xform_inv(self, Vector3 v)
    cpdef inline godot_int get_orthogonal_index(self)
    cpdef inline void get_elements(self, Vector3 elements)
    cpdef inline void set_row(self, godot_int row, Vector3 value)
    cpdef inline Vector3 get_row(self, godot_int row)
    cpdef inline Basis slerp(self, Basis b, godot_real t)
