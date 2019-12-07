# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_plane, godot_real, godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj
from godot.vector3 cimport Vector3
from godot.plane cimport Plane


@cython.final
cdef class Plane:

    def __init__(self, a=None, b=None, c=None, d=None, v1=None, v2=None, v3=None, normal=None):
        if a is not None or b is not None or c is not None:  # d is shared with normal
            if a is None or b is None or c is None or d is None:
                raise ValueError("`a`, `b`, `c` and `d` params must be provided together")
            gdapi.godot_plane_new_with_reals(&self._gd_data, a, b, c, d)

        elif v1 is not None or v2 is not None or v3 is not None:
            if v1 is None or v2 is None or v3 is None:
                raise ValueError("`v1`, `v2` and `v3` params must be provided together")
            gdapi.godot_plane_new_with_vectors(&self._gd_data, &(<Vector3>v1)._gd_data, &(<Vector3>v2)._gd_data, &(<Vector3>v3)._gd_data)

        elif normal is not None or d is not None:
            if normal is None or d is None:
                raise ValueError("`normal` and `d` params must be provided together")
            gdapi.godot_plane_new_with_normal(&self._gd_data, &(<Vector3>normal)._gd_data, d)

        else:
            raise ValueError("Missing params")

    @staticmethod
    cdef inline Plane new_with_reals(godot_real a, godot_real b, godot_real c, godot_real d):
        # Call to __new__ bypasses __init__ constructor
        cdef Plane ret = Plane.__new__(Plane)
        gdapi.godot_plane_new_with_reals(&ret._gd_data, a, b, c, d)
        return ret

    @staticmethod
    cdef inline Plane new_with_vectors(Vector3 v1, Vector3 v2, Vector3 v3):
        # Call to __new__ bypasses __init__ constructor
        cdef Plane ret = Plane.__new__(Plane)
        gdapi.godot_plane_new_with_vectors(&ret._gd_data, &v1._gd_data, &v2._gd_data, &v3._gd_data)
        return ret

    @staticmethod
    cdef inline Plane new_with_normal(Vector3 normal, godot_real d):
        # Call to __new__ bypasses __init__ constructor
        cdef Plane ret = Plane.__new__(Plane)
        gdapi.godot_plane_new_with_normal(&ret._gd_data, &normal._gd_data, d)
        return ret

    @staticmethod
    cdef inline Plane from_ptr(const godot_plane *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Plane ret = Plane.__new__(Plane)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Plane({self.as_string()})>"

    # Operators

    cdef inline bint operator_equal(self, Plane b):
        cdef Plane ret  = Plane.__new__(Plane)
        return gdapi.godot_plane_operator_equal(&self._gd_data, &b._gd_data)

    cdef inline Plane operator_neg(self):
        cdef Plane ret  = Plane.__new__(Plane)
        ret._gd_data = gdapi.godot_plane_operator_neg(&self._gd_data)
        return ret

    def __eq__(self, other):
        cdef Plane _other = <Plane?>other
        return self.operator_equal(_other)

    def __ne__(self, other):
        cdef Plane _other = <Plane?>other
        return not self.operator_equal(_other)

    def __neg__(self):
        return self.operator_neg()

    # Property

    cdef inline godot_real get_d(self):
        return gdapi.godot_plane_get_d(&self._gd_data)

    cdef inline void set_d(self, godot_real d):
        gdapi.godot_plane_set_d(&self._gd_data, d)

    @property
    def d(self):
        return self.get_d()

    @d.setter
    def d(self, val):
        self.set_d(val)

    cdef inline Vector3 get_normal(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_plane_get_normal(&self._gd_data)
        return ret

    cdef inline void set_normal(self, Vector3 normal):
        gdapi.godot_plane_set_normal(&self._gd_data, &normal._gd_data)

    @property
    def normal(self):
        return self.get_normal()

    @normal.setter
    def normal(self, val):
        self.set_normal(val)

    # Methods

    cpdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_plane_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline Plane normalized(self):
        cdef Plane ret = Plane.__new__(Plane)
        ret._gd_data = gdapi.godot_plane_normalized(&self._gd_data)
        return ret

    cpdef inline Vector3 center(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_plane_center(&self._gd_data)
        return ret

    cpdef inline Vector3 get_any_point(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_plane_get_any_point(&self._gd_data)
        return ret

    cpdef inline bint is_point_over(self, Vector3 point):
        return gdapi.godot_plane_is_point_over(&self._gd_data, &point._gd_data)

    cpdef inline bint has_point(self, Vector3 point, godot_real epsilon):
        return gdapi.godot_plane_has_point(&self._gd_data, &point._gd_data, epsilon)

    cpdef inline Vector3 project(self, Vector3 point):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_plane_project(&self._gd_data, &point._gd_data)
        return ret

    cpdef inline Vector3 intersect_3(self, Plane b, Plane c):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        gdapi.godot_plane_intersect_3(&self._gd_data, &ret._gd_data, &b._gd_data, &c._gd_data)
        return ret

    cpdef inline Vector3 intersects_ray(self, Vector3 from_, Vector3 dir):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        gdapi.godot_plane_intersects_ray(&self._gd_data, &ret._gd_data, &from_._gd_data, &dir._gd_data)
        return ret

    cpdef inline Vector3 intersects_segment(self, Vector3 begin, Vector3 end):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        gdapi.godot_plane_intersects_segment(&self._gd_data, &ret._gd_data, &begin._gd_data, &end._gd_data)
        return ret

    PLANE_YZ = Plane(1, 0, 0, 0)
    PLANE_XZ = Plane(0, 1, 0, 0)
    PLANE_XY = Plane(0, 0, 1, 0)
