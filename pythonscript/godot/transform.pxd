# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_transform, godot_real, godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj
from godot.aabb cimport AABB
from godot.basis cimport Basis
from godot.vector3 cimport Vector3
from godot.plane cimport Plane
from godot.quat cimport Quat


@cython.final
cdef class Transform:
    cdef godot_transform _gd_data

    @staticmethod
    cdef inline Transform new_identity()

    @staticmethod
    cdef inline Transform new(Basis basis, Vector3 origin)

    @staticmethod
    cdef inline Transform new_with_axis_origin(Vector3 x_axis, Vector3 y_axis, Vector3 z_axis, Vector3 origin)

    @staticmethod
    cdef inline Transform new_with_quat(Quat quat)

    @staticmethod
    cdef inline Transform from_ptr(const godot_transform *_ptr)

    # Operators

    cdef inline Transform operator_multiply(self, Transform b)
    cdef inline bint operator_equal(self, Transform b)

    # Properties

    cdef inline Basis get_basis(self)
    cdef inline void set_basis(self, Basis val)
    cdef inline Vector3 get_origin(self)
    cdef inline void set_origin(self, Vector3 val)

    # Methods

    cpdef inline str as_string(self)
    cpdef inline Transform inverse(self)
    cpdef inline Transform affine_inverse(self)
    cpdef inline Transform orthonormalized(self)
    cpdef inline Transform rotated(self, Vector3 axis, godot_real phi)
    cpdef inline Transform scaled(self, Vector3 scale)
    cpdef inline Transform translated(self, Vector3 ofs)
    cpdef inline Transform looking_at(self, Vector3 target, Vector3 up)
    cpdef inline Plane xform_plane(self, Plane v)
    cpdef inline Plane xform_inv_plane(self, Plane v)
    cpdef inline Vector3 xform_vector3(self, Vector3 v)
    cpdef inline Vector3 xform_inv_vector3(self, Vector3 v)
    cpdef inline AABB xform_aabb(self, AABB v)
    cpdef inline AABB xform_inv_aabb(self, AABB v)
