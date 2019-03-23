# cython: language_level=3

cimport cython

from gdnative_api_struct cimport godot_vector2, godot_real


@cython.final
cdef class Vector2:
    cdef godot_vector2 _c_vector2

    @staticmethod
    cdef Vector2 new(godot_real x=*, godot_real y=*)

    cdef inline godot_vector2 *_c_vector2_ptr(Vector2 self)
    # TODO
    # cdef operator_equal(self, other)
    # cdef operator_neg(self)
    # cdef operator_add(self, val)
    # cdef operator_substract(self, val)
    # cdef operator_multiply_vector(self, val)
    # cdef operator_multiply_scalar(self, val)
    # cdef Vector2 operator_divide_vector(self, val)
    # cdef Vector2 operator_divide_scalar(self, val)

    # Properties

    cdef godot_real get_x(self)
    cdef void set_x(self, godot_real val)
    cdef godot_real get_y(self)
    cdef void set_y(self, godot_real val)

    # Methods

    cpdef Vector2 abs(self)
    cpdef godot_real angle(self)
    cpdef godot_real angle_to(self, Vector2 to)
    cpdef godot_real angle_to_point(self, Vector2 to)

