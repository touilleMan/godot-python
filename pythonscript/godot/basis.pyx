# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_basis, godot_real, godot_int, godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj
from godot.vector3 cimport Vector3
from godot.quat cimport Quat


@cython.final
cdef class Basis:

    def __init__(self, x=None, y=None, z=None, axis=None, phi=None, from_=None):
        if from_ is not None:
            try:
                gdapi.godot_basis_new_with_euler_quat(&self._gd_data, &(<Quat>from_)._gd_data)
            except TypeError:
                try:
                    gdapi.godot_basis_new_with_euler(&self._gd_data, &(<Vector3>from_)._gd_data)
                except TypeError:
                    raise ValueError('`from_` must be Quat or Vector3')

        elif axis is not None or phi is not None:
            if axis is None or phi is None:
                raise ValueError("`axis` and `phi` must be provided together")
            gdapi.godot_basis_new_with_axis_and_angle(&self._gd_data, &(<Vector3>axis)._gd_data, phi)

        elif x is None and y is None and z is None:
            gdapi.godot_basis_new(&self._gd_data)

        else:
            if x is None or y is None or z is None:
                raise ValueError("`x`, `y` and `z` params must be provided together")
            gdapi.godot_basis_new_with_rows(&self._gd_data, &(<Vector3>x)._gd_data, &(<Vector3>y)._gd_data, &(<Vector3>z)._gd_data)

    @staticmethod
    cdef inline Basis new():
        # Call to __new__ bypasses __init__ constructor
        cdef Basis ret = Basis.__new__(Basis)
        gdapi.godot_basis_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Basis new_with_rows(Vector3 x, Vector3 y, Vector3 z):
        # Call to __new__ bypasses __init__ constructor
        cdef Basis ret = Basis.__new__(Basis)
        gdapi.godot_basis_new_with_rows(&ret._gd_data, &x._gd_data, &y._gd_data, &z._gd_data)
        return ret

    @staticmethod
    cdef inline Basis new_with_axis_and_angle(Vector3 axis, godot_real phi):
        # Call to __new__ bypasses __init__ constructor
        cdef Basis ret = Basis.__new__(Basis)
        gdapi.godot_basis_new_with_axis_and_angle(&ret._gd_data, &axis._gd_data, phi)
        return ret

    @staticmethod
    cdef inline Basis new_with_euler(Vector3 from_):
        # Call to __new__ bypasses __init__ constructor
        cdef Basis ret = Basis.__new__(Basis)
        gdapi.godot_basis_new_with_euler(&ret._gd_data, &from_._gd_data)
        return ret

    @staticmethod
    cdef inline Basis new_with_euler_quat(Quat from_):
        # Call to __new__ bypasses __init__ constructor
        cdef Basis ret = Basis.__new__(Basis)
        gdapi.godot_basis_new_with_euler_quat(&ret._gd_data, &from_._gd_data)
        return ret

    @staticmethod
    cdef inline Basis from_ptr(const godot_basis *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Basis({self.as_string()})>"

    # Operators

    cdef inline Basis operator_add(self, Basis b):
        cdef Basis ret  = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_operator_add(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Basis operator_subtract(self, Basis b):
        cdef Basis ret  = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_operator_subtract(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Basis operator_multiply_vector(self, Basis b):
        cdef Basis ret  = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_operator_multiply_vector(&self._gd_data, &b._gd_data)
        return ret

    cdef inline Basis operator_multiply_scalar(self, godot_real b):
        cdef Basis ret  = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_operator_multiply_scalar(&self._gd_data, b)
        return ret

    cdef inline bint operator_equal(self, Basis b):
        cdef Basis ret  = Basis.__new__(Basis)
        return gdapi.godot_basis_operator_equal(&self._gd_data, &b._gd_data)

    def __eq__(self, other):
        try:
            return Basis.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Basis.operator_equal(self, other)
        except TypeError:
            return True

    def __add__(self, val):
        cdef Basis _val = <Basis?>val
        return Basis.operator_add(self, _val)

    def __sub__(self, val):
        cdef Basis _val = <Basis?>val
        return Basis.operator_subtract(self, _val)

    def __mul__(self, val):
        cdef Basis _val

        try:
            _val = <Basis?>val

        except TypeError:
            return Basis.operator_multiply_scalar(self, val)

        else:
            return Basis.operator_multiply_vector(self, _val)

    # Property

    cdef inline Vector3 get_x(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_get_axis(&self._gd_data, 0)
        return ret

    cdef inline void set_x(self, Vector3 val):
        gdapi.godot_basis_set_axis(&self._gd_data, 0, &val._gd_data)

    @property
    def x(self):
        return self.get_x()

    @x.setter
    def x(self, val):
        self.set_x(val)

    cdef inline Vector3 get_y(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_get_axis(&self._gd_data, 1)
        return ret

    cdef inline void set_y(self, Vector3 val):
        gdapi.godot_basis_set_axis(&self._gd_data, 1, &val._gd_data)

    @property
    def y(self):
        return self.get_y()

    @y.setter
    def y(self, val):
        self.set_y(val)

    cdef inline Vector3 get_z(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_get_axis(&self._gd_data, 2)
        return ret

    cdef inline void set_z(self, Vector3 val):
        gdapi.godot_basis_set_axis(&self._gd_data, 2, &val._gd_data)

    @property
    def z(self):
        return self.get_z()

    @z.setter
    def z(self, val):
        self.set_z(val)

    # Methods

    cdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_basis_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline Basis inverse(self):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_inverse(&self._gd_data)
        return ret

    cpdef inline Basis transposed(self):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_transposed(&self._gd_data)
        return ret

    cpdef inline Basis orthonormalized(self):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_orthonormalized(&self._gd_data)
        return ret

    cpdef inline godot_real determinant(self):
        return gdapi.godot_basis_determinant(&self._gd_data)

    cpdef inline Basis rotated(self, Vector3 axis, godot_real phi):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_rotated(&self._gd_data, &axis._gd_data, phi)
        return ret

    cpdef inline Basis scaled(self, Vector3 scale):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi.godot_basis_scaled(&self._gd_data, &scale._gd_data)
        return ret

    cpdef inline Vector3 get_scale(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_get_scale(&self._gd_data)
        return ret

    cpdef inline Vector3 get_euler(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_get_euler(&self._gd_data)
        return ret

    cpdef inline Quat get_quat(self):
        cdef Quat ret = Quat.__new__(Quat)
        ret._gd_data = gdapi11.godot_basis_get_quat(&self._gd_data)
        return ret

    cpdef inline void set_quat(self, Quat quat):
        gdapi11.godot_basis_set_quat(&self._gd_data, &quat._gd_data)

    cpdef inline void set_axis_angle_scale(self, Vector3 axis, godot_real phi, Vector3 scale):
        gdapi11.godot_basis_set_axis_angle_scale(&self._gd_data, &axis._gd_data, phi, &scale._gd_data)

    cpdef inline void set_euler_scale(self, Vector3 euler, Vector3 scale):
        gdapi11.godot_basis_set_euler_scale(&self._gd_data, &euler._gd_data, &scale._gd_data)

    cpdef inline void set_quat_scale(self, Quat quat, Vector3 scale):
        gdapi11.godot_basis_set_quat_scale(&self._gd_data, &quat._gd_data, &scale._gd_data)

    cpdef inline godot_real tdotx(self, Vector3 with_):
        return gdapi.godot_basis_tdotx(&self._gd_data, &with_._gd_data)

    cpdef inline godot_real tdoty(self, Vector3 with_):
        return gdapi.godot_basis_tdoty(&self._gd_data, &with_._gd_data)

    cpdef inline godot_real tdotz(self, Vector3 with_):
        return gdapi.godot_basis_tdotz(&self._gd_data, &with_._gd_data)

    cpdef inline Vector3 xform(self, Vector3 v):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_xform(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline Vector3 xform_inv(self, Vector3 v):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_xform_inv(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline godot_int get_orthogonal_index(self):
        return gdapi.godot_basis_get_orthogonal_index(&self._gd_data)

    cpdef inline void get_elements(self, Vector3 elements):
        gdapi.godot_basis_get_elements(&self._gd_data, &elements._gd_data)

    cpdef inline void set_row(self, godot_int row, Vector3 value):
        gdapi.godot_basis_set_row(&self._gd_data, row, &value._gd_data)

    cpdef inline Vector3 get_row(self, godot_int row):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_basis_get_row(&self._gd_data, row)
        return ret

    cpdef inline Basis slerp(self, Basis b, godot_real t):
        cdef Basis ret = Basis.__new__(Basis)
        ret._gd_data = gdapi11.godot_basis_slerp(&self._gd_data, &b._gd_data, t)
        return ret
