# cython: language_level=3

cimport cython

from godot.hazmat.gdnative_api_struct cimport godot_vector2, godot_real


@cython.final
cdef class Vector2:
    cdef godot_vector2 _c_vector2

    @staticmethod
    cdef Vector2 new(godot_real x=*, godot_real y=*)

    @staticmethod
    cdef Vector2 from_ptr(const godot_vector2 *_ptr)

    cdef inline godot_vector2 *_c_vector2_ptr(Vector2 self)

    # Operators
    cdef inline Vector2 operator_add(self, Vector2 b)
    cdef inline Vector2 operator_subtract(self, Vector2 b)
    cdef inline Vector2 operator_multiply_vector(self, Vector2 b)
    cdef inline Vector2 operator_multiply_scalar(self, godot_real b)
    cdef inline Vector2 operator_divide_vector(self, Vector2 b)
    cdef inline Vector2 operator_divide_scalar(self, godot_real b)
    cdef inline bint operator_equal(self, Vector2 b)
    cdef inline bint operator_less(self, Vector2 b)
    cdef inline Vector2 operator_neg(self)

    # Properties

    cdef inline godot_real get_x(self)
    cdef inline void set_x(self, godot_real val)
    cdef inline godot_real get_y(self)
    cdef inline void set_y(self, godot_real val)

    # Methods

    cpdef Vector2 normalized(self)
    cpdef godot_real length(self)
    cpdef godot_real angle(self)
    cpdef godot_real length_squared(self)
    cpdef bint is_normalized(self)
    cpdef godot_real distance_to(self, Vector2 to)
    cpdef godot_real distance_squared_to(self, Vector2 to)
    cpdef godot_real angle_to(self, Vector2 to)
    cpdef godot_real angle_to_point(self, Vector2 to)
    cpdef Vector2 linear_interpolate(self, Vector2 b, godot_real t)
    cpdef Vector2 cubic_interpolate(self, Vector2 b, Vector2 pre_a, Vector2 post_b, godot_real t)
    cpdef Vector2 move_toward(self, Vector2 to, godot_real delta)
    cpdef Vector2 rotated(self, godot_real phi)
    cpdef Vector2 tangent(self)
    cpdef Vector2 floor(self)
    cpdef Vector2 snapped(self, Vector2 by)
    cpdef godot_real aspect(self)
    cpdef godot_real dot(self, Vector2 with_)
    cpdef Vector2 slide(self, Vector2 n)
    cpdef Vector2 bounce(self, Vector2 n)
    cpdef Vector2 reflect(self, Vector2 n)
    cpdef Vector2 abs(self)
    cpdef Vector2 clamped(self, godot_real length)
