# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_transform2d, godot_real
from godot.vector2 cimport Vector2
from godot.rect2 cimport Rect2


@cython.final
cdef class Transform2D:
    cdef godot_transform2d _gd_data

    @staticmethod
    cdef inline Transform2D new(godot_real rotation, Vector2 position)

    @staticmethod
    cdef inline Transform2D new_identity()

    @staticmethod
    cdef inline Transform2D new_axis_origin(Vector2 x_axis, Vector2 y_axis, Vector2 origin)

    @staticmethod
    cdef inline Transform2D from_ptr(const godot_transform2d *_ptr)

    # Operators

    cdef inline Transform2D operator_multiply(self, Transform2D b)
    cdef inline bint operator_equal(self, Transform2D b)

    # Properties

    # TODO: origin/x/y are stored in godot's Transform2D as `elements`
    # attributes which are not exposed by gdapi
    cdef inline Vector2 get_origin(self)
    # cdef inline void set_origin(self, Vector2 val)
    # cdef inline Vector2 get_x(self)
    # cdef inline void set_x(self, Vector2 val)
    # cdef inline Vector2 get_y(self)
    # cdef inline void set_y(self, Vector2 val)

    # Methods

    cpdef inline str as_string(self)
    cpdef inline Transform2D inverse(self)
    cpdef inline Transform2D affine_inverse(self)
    cpdef inline godot_real get_rotation(self)
    cpdef inline Vector2 get_scale(self)
    cpdef inline Transform2D orthonormalized(self)
    cpdef inline Transform2D rotated(self, godot_real phi)
    cpdef inline Transform2D scaled(self, Vector2 scale)
    cpdef inline Transform2D translated(self, Vector2 offset)
    cpdef inline Vector2 xform_vector2(self, Vector2 v)
    cpdef inline Vector2 xform_inv_vector2(self, Vector2 offset)
    cpdef inline Vector2 basis_xform_vector2(self, Vector2 offset)
    cpdef inline Vector2 basis_xform_inv_vector2(self, Vector2 offset)
    cpdef inline Transform2D interpolate_with(self, Transform2D m, godot_real c)
    cpdef inline Rect2 xform_rect2(self, Rect2 v)
    cpdef inline Rect2 xform_inv_rect2(self, Rect2 v)
