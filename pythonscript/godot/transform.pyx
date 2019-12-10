# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
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

    def __init__(self, quat=None, basis=None, x_axis=None, y_axis=None, z_axis=None, origin=None):
        if quat is not None:
            gdapi11.godot_transform_new_with_quat(&self._gd_data, &(<Quat?>quat)._gd_data)
        elif basis is not None:
            if basis is None or origin is None:
                raise ValueError("`basis` and `origin` params must be provided together")
            gdapi.godot_transform_new(&self._gd_data, &(<Basis>basis)._gd_data, &(<Vector3?>origin)._gd_data)
        elif x_axis is not None or y_axis is not None or z_axis is not None:
            if x_axis is None or y_axis is None or z_axis is None or origin is None:
                raise ValueError("`x_axis`, `y_axis`, `z_axis` and `origin` params must be provided together")
            gdapi.godot_transform_new_with_axis_origin(&self._gd_data, &(<Vector3?>x_axis)._gd_data, &(<Vector3?>y_axis)._gd_data, &(<Vector3?>z_axis)._gd_data, &(<Vector3?>origin)._gd_data)
        else:
            gdapi.godot_transform_new_identity(&self._gd_data)

    @staticmethod
    cdef inline Transform new_identity():
        # Call to __new__ bypasses __init__ constructor
        cdef Transform ret = Transform.__new__(Transform)
        gdapi.godot_transform_new_identity(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Transform new(Basis basis, Vector3 origin):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform ret = Transform.__new__(Transform)
        gdapi.godot_transform_new(&ret._gd_data, &(<Basis?>basis)._gd_data, &(<Vector3>origin)._gd_data)
        return ret

    @staticmethod
    cdef inline Transform new_with_axis_origin(Vector3 x_axis, Vector3 y_axis, Vector3 z_axis, Vector3 origin):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform ret = Transform.__new__(Transform)
        gdapi.godot_transform_new_with_axis_origin(&ret._gd_data, &(<Vector3?>x_axis)._gd_data, &(<Vector3?>y_axis)._gd_data, &(<Vector3?>x_axis)._gd_data, &(<Vector3?>origin)._gd_data)
        return ret

    @staticmethod
    cdef inline Transform new_with_quat(Quat quat):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform ret = Transform.__new__(Transform)
        gdapi11.godot_transform_new_with_quat(&ret._gd_data, &(<Quat?>quat)._gd_data)
        return ret

    @staticmethod
    cdef inline Transform from_ptr(const godot_transform *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Transform({self.as_string()})>"

    # Operators

    cdef inline Transform operator_multiply(self, Transform b):
        cdef Transform ret  = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_operator_multiply(&self._gd_data, &b._gd_data)
        return ret

    cdef inline bint operator_equal(self, Transform b):
        cdef Transform ret  = Transform.__new__(Transform)
        return gdapi.godot_transform_operator_equal(&self._gd_data, &b._gd_data)

    def __eq__(self, other):
        return Transform.operator_equal(self, other)

    def __ne__(self, other):
        return not Transform.operator_equal(self, other)

    def __mul__(self, val):
        return Transform.operator_multiply(self, val)

    # Properties

    cdef inline Basis get_basis(self):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_transform_get_basis(&self._gd_data)
        return ret

    cdef inline void set_basis(self, Basis val):
        gdapi.godot_transform_set_basis(&self._gd_data, &val._gd_data)

    @property
    def basis(self):
        return self.get_basis()

    @basis.setter
    def basis(self, val):
        self.set_basis(val)

    cdef inline Vector3 get_origin(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_transform_get_origin(&self._gd_data)
        return ret

    cdef inline void set_origin(self, Vector3 val):
        gdapi.godot_transform_set_origin(&self._gd_data, &val._gd_data)

    @property
    def origin(self):
        return self.get_origin()

    @origin.setter
    def origin(self, val):
        self.set_origin(val)

    # Methods

    cpdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_transform_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline Transform inverse(self):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_inverse(&self._gd_data)
        return ret

    cpdef inline Transform affine_inverse(self):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_affine_inverse(&self._gd_data)
        return ret

    cpdef inline Transform orthonormalized(self):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_orthonormalized(&self._gd_data)
        return ret

    cpdef inline Transform rotated(self, Vector3 axis, godot_real phi):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_rotated(&self._gd_data, &axis._gd_data, phi)
        return ret

    cpdef inline Transform scaled(self, Vector3 scale):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_scaled(&self._gd_data, &scale._gd_data)
        return ret

    cpdef inline Transform translated(self, Vector3 ofs):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_translated(&self._gd_data, &ofs._gd_data)
        return ret

    cpdef inline Transform looking_at(self, Vector3 target, Vector3 up):
        cdef Transform ret = Transform.__new__(Transform)
        ret._gd_data = gdapi.godot_transform_looking_at(&self._gd_data, &target._gd_data, &up._gd_data)
        return ret

    cpdef inline Plane xform_plane(self, Plane v):
        cdef Plane ret = Plane.__new__(Plane)
        ret._gd_data = gdapi.godot_transform_xform_plane(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline Plane xform_inv_plane(self, Plane v):
        cdef Plane ret = Plane.__new__(Plane)
        ret._gd_data = gdapi.godot_transform_xform_inv_plane(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline Vector3 xform_vector3(self, Vector3 v):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_transform_xform_vector3(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline Vector3 xform_inv_vector3(self, Vector3 v):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_transform_xform_inv_vector3(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline AABB xform_aabb(self, AABB v):
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_transform_xform_aabb(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline AABB xform_inv_aabb(self, AABB v):
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_transform_xform_inv_aabb(&self._gd_data, &v._gd_data)
        return ret

    IDENTITY = Transform(x_axis=Vector3(1, 0, 0), y_axis=Vector3(0, 1, 0), z_axis=Vector3(0, 0, 1), origin=Vector3(0, 0, 0))
    FLIP_X = Transform(x_axis=Vector3(-1, 0, 0), y_axis=Vector3(0, 1, 0), z_axis=Vector3(0, 0, 1), origin=Vector3(0, 0, 0))
    FLIP_Y = Transform(x_axis=Vector3(1, 0, 0), y_axis=Vector3(0, -1, 0), z_axis=Vector3(0, 0, 1), origin=Vector3(0, 0, 0))
    FLIP_Z = Transform(x_axis=Vector3(1, 0, 0), y_axis=Vector3(0, 1, 0), z_axis=Vector3(0, 0, -1), origin=Vector3(0, 0, 0))
