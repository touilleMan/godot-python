# cython: language_level=3

cimport cython
from libc.stdint cimport uint8_t

from godot._hazmat.gdnative_api_struct cimport (
    godot_color,
    godot_int,
    godot_real,
    godot_bool
)


@cython.final
cdef class Color:
    cdef godot_color _gd_data

    @staticmethod
    cdef Color new_rgba(godot_real r, godot_real g, godot_real b, godot_real a)
    @staticmethod
    cdef Color new_rgb(godot_real r, godot_real g, godot_real b)
    @staticmethod
    cdef Color from_ptr(const godot_color *_ptr)

    # Operators

    cdef inline bint operator_equal(self, Color b)
    cdef inline bint operator_less(self, Color b)

    # Properties

    cdef inline godot_real get_r(self)
    cdef inline void set_r(self, godot_real val)
    cdef inline godot_real get_g(self)
    cdef inline void set_g(self, godot_real val)
    cdef inline godot_real get_b(self)
    cdef inline void set_b(self, godot_real val)
    cdef inline godot_real get_a(self)
    cdef inline void set_a(self, godot_real val)
    cdef inline uint8_t get_r8(self)
    cdef inline void set_r8(self, uint8_t val)
    cdef inline uint8_t get_g8(self)
    cdef inline void set_g8(self, uint8_t val)
    cdef inline uint8_t get_b8(self)
    cdef inline void set_b8(self, uint8_t val)
    cdef inline uint8_t get_a8(self)
    cdef inline void set_a8(self, uint8_t val)
    cdef inline godot_real get_h(self)
    cdef inline godot_real get_s(self)
    cdef inline godot_real get_v(self)

    # Methods

    cpdef inline str as_string(self)
    cpdef inline godot_int to_rgba32(self)
    cpdef inline godot_int to_abgr32(self)
    cpdef inline godot_int to_abgr64(self)
    cpdef inline godot_int to_argb64(self)
    cpdef inline godot_int to_rgba64(self)
    cpdef inline godot_int to_argb32(self)
    cpdef inline godot_real gray(self)
    cpdef inline Color inverted(self)
    cpdef inline Color contrasted(self)
    cpdef inline Color linear_interpolate(self, Color b, godot_real t)
    cpdef inline Color blend(self, Color over)
    cpdef inline Color darkened(self, godot_real amount)
    cpdef inline Color from_hsv(self, godot_real h, godot_real s, godot_real v, godot_real a=*)
    cpdef inline Color lightened(self, godot_real amount)
    cpdef inline str to_html(self, godot_bool with_alpha=*)
