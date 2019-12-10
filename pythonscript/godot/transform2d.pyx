# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_transform2d, godot_real, godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj
from godot.vector2 cimport Vector2
from godot.rect2 cimport Rect2


@cython.final
cdef class Transform2D:

    def __init__(self, rotation=None, position=None, x_axis=None, y_axis=None, origin=None):
        if rotation is not None or position is not None:
            if rotation is None or position is None:
                raise ValueError("`rotation` and `position` params must be provided together")
            gdapi.godot_transform2d_new(&self._gd_data, rotation, &(<Vector2?>position)._gd_data)
        elif x_axis is not None or y_axis is not None or origin is not None:
            if x_axis is None or y_axis is None or origin is None:
                raise ValueError("`x_axis`, `y_axis` and `origin` params must be provided together")
            gdapi.godot_transform2d_new_axis_origin(&self._gd_data, &(<Vector2?>x_axis)._gd_data, &(<Vector2?>y_axis)._gd_data, &(<Vector2?>origin)._gd_data)
        else:
            gdapi.godot_transform2d_new_identity(&self._gd_data)

    @staticmethod
    cdef inline Transform2D new(godot_real rotation, Vector2 position):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        gdapi.godot_transform2d_new(&ret._gd_data, rotation, &(<Vector2?>position)._gd_data)
        return ret

    @staticmethod
    cdef inline Transform2D new_identity():
        # Call to __new__ bypasses __init__ constructor
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        gdapi.godot_transform2d_new_identity(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Transform2D new_axis_origin(Vector2 x_axis, Vector2 y_axis, Vector2 origin):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        gdapi.godot_transform2d_new_axis_origin(&ret._gd_data, &(<Vector2?>x_axis)._gd_data, &(<Vector2?>y_axis)._gd_data, &(<Vector2?>origin)._gd_data)
        return ret

    @staticmethod
    cdef inline Transform2D from_ptr(const godot_transform2d *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Transform2D({self.as_string()})>"

    # Operators

    cdef inline Transform2D operator_multiply(self, Transform2D b):
        cdef Transform2D ret  = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_operator_multiply(&self._gd_data, &b._gd_data)
        return ret

    cdef inline bint operator_equal(self, Transform2D b):
        cdef Transform2D ret  = Transform2D.__new__(Transform2D)
        return gdapi.godot_transform2d_operator_equal(&self._gd_data, &b._gd_data)

    def __eq__(self, other):
        try:
            return Transform2D.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Transform2D.operator_equal(self, other)
        except TypeError:
            return True

    def __mul__(self, val):
        return Transform2D.operator_multiply(self, val)

    # Properties

    cdef inline Vector2 get_origin(self):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_transform2d_get_origin(&self._gd_data)
        return ret

    # cdef inline void set_origin(self, Vector2 val):
    #     gdapi.godot_transform2d_set_origin(&self._gd_data, &val._gd_data)

    @property
    def origin(self):
        return self.get_origin()

    # @origin.setter
    # def origin(self, val):
    #     self.set_origin(val)

    # cdef inline Vector2 get_x(self):
    #     return gdapi.godot_transform2d_get_x(&self._gd_data)

    # cdef inline void set_x(self, Vector2 val):
    #     gdapi.godot_transform2d_set_x(&self._gd_data, &val._gd_data)

    # @property
    # def x(self):
    #     return self.get_x()

    # @x.setter
    # def x(self, val):
    #     self.set_x(val)

    # cdef inline Vector2 get_y(self):
    #     return gdapi.godot_transform2d_get_y(&self._gd_data)

    # cdef inline void set_y(self, Vector2 val):
    #     gdapi.godot_transform2d_set_y(&self._gd_data, &val._gd_data)

    # @property
    # def y(self):
    #     return self.get_y()

    # @y.setter
    # def y(self, val):
    #     self.set_y(val)

    # Methods

    cpdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_transform2d_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline Transform2D inverse(self):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_inverse(&self._gd_data)
        return ret

    cpdef inline Transform2D affine_inverse(self):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_affine_inverse(&self._gd_data)
        return ret

    cpdef inline godot_real get_rotation(self):
        return gdapi.godot_transform2d_get_rotation(&self._gd_data)

    cpdef inline Vector2 get_scale(self):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_transform2d_get_scale(&self._gd_data)
        return ret

    cpdef inline Transform2D orthonormalized(self):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_orthonormalized(&self._gd_data)
        return ret

    cpdef inline Transform2D rotated(self, godot_real phi):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_rotated(&self._gd_data, phi)
        return ret

    cpdef inline Transform2D scaled(self, Vector2 scale):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_scaled(&self._gd_data, &scale._gd_data)
        return ret

    cpdef inline Transform2D translated(self, Vector2 offset):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_translated(&self._gd_data, &offset._gd_data)
        return ret

    cpdef inline Vector2 xform_vector2(self, Vector2 v):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_transform2d_xform_vector2(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline Vector2 xform_inv_vector2(self, Vector2 offset):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_transform2d_xform_inv_vector2(&self._gd_data, &offset._gd_data)
        return ret

    cpdef inline Vector2 basis_xform_vector2(self, Vector2 offset):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_transform2d_basis_xform_vector2(&self._gd_data, &offset._gd_data)
        return ret

    cpdef inline Vector2 basis_xform_inv_vector2(self, Vector2 offset):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_transform2d_basis_xform_inv_vector2(&self._gd_data, &offset._gd_data)
        return ret

    cpdef inline Transform2D interpolate_with(self, Transform2D m, godot_real c):
        cdef Transform2D ret = Transform2D.__new__(Transform2D)
        ret._gd_data = gdapi.godot_transform2d_interpolate_with(&self._gd_data, &m._gd_data, c)
        return ret

    cpdef inline Rect2 xform_rect2(self, Rect2 v):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi.godot_transform2d_xform_rect2(&self._gd_data, &v._gd_data)
        return ret

    cpdef inline Rect2 xform_inv_rect2(self, Rect2 v):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi.godot_transform2d_xform_inv_rect2(&self._gd_data, &v._gd_data)
        return ret

    IDENTITY = Transform2D(x_axis=Vector2(1, 0), y_axis=Vector2(0, 1), origin=Vector2(0, 0))
    FLIP_X = Transform2D(x_axis=Vector2(-1, 0), y_axis=Vector2(0, 1), origin=Vector2(0, 0))
    FLIP_Y = Transform2D(x_axis=Vector2(1, 0), y_axis=Vector2(0, -1), origin=Vector2(0, 0))
