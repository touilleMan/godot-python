# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_rect2, godot_int, godot_real
from godot.vector2 cimport Vector2


@cython.final
cdef class Rect2:
    cdef godot_rect2 _gd_data

    @staticmethod
    cdef inline Rect2 new(godot_real x=*, godot_real y=*, godot_real width=*, godot_real height=*)

    @staticmethod
    cdef inline Rect2 new_with_position_and_size(Vector2 position, Vector2 size)

    @staticmethod
    cdef inline Rect2 from_ptr(const godot_rect2 *_ptr)

    # Operators

    cdef inline bint operator_equal(self, Rect2 b)

    # Properties

    cdef inline Vector2 get_size(self)
    cdef inline void set_size(self, Vector2 val)
    cdef inline Vector2 get_position(self)
    cdef inline void set_position(self, Vector2 val)
    cdef inline Vector2 get_end(self)

    # Methods

    cpdef inline str as_string(self)
    cpdef inline godot_real get_area(self)
    cpdef inline bint intersects(self, Rect2 b)
    cpdef inline bint encloses(self, Rect2 b)
    cpdef inline bint has_no_area(self, Rect2 b)
    cpdef inline Rect2 clip(self, Rect2 b)
    cpdef inline Rect2 merge(self, Rect2 b)
    cpdef inline bint has_point(self, Vector2 point)
    cpdef inline Rect2 grow(self, godot_real by)
    cpdef inline Rect2 grow_individual(self, godot_real left, godot_real top, godot_real right, godot_real bottom)
    cpdef inline Rect2 grow_margin(self, godot_int margin, godot_real by)
    cpdef inline Rect2 abs(self)
    cpdef inline Rect2 expand(self, Vector2 to)
