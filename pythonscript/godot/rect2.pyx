# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12
)
from godot._hazmat.gdnative_api_struct cimport godot_rect2, godot_int, godot_real, godot_string
from godot._hazmat.conversion cimport godot_string_to_pyobj
from godot.vector2 cimport Vector2


@cython.final
cdef class Rect2:

    def __init__(self, godot_real x=0.0, godot_real y=0.0, godot_real width=0.0, godot_real height=0.0):
        gdapi.godot_rect2_new(&self._gd_data, x, y, width, height)

    @staticmethod
    def from_pos_size(Vector2 position not None, Vector2 size not None):
        return Rect2.new_with_position_and_size(position, size)

    @staticmethod
    cdef inline Rect2 new(godot_real x=0.0, godot_real y=0.0, godot_real width=0.0, godot_real height=0.0):
        # Call to __new__ bypasses __init__ constructor
        cdef Rect2 ret = Rect2.__new__(Rect2)
        gdapi.godot_rect2_new(&ret._gd_data, x, y, width, height)
        return ret

    @staticmethod
    cdef inline Rect2 new_with_position_and_size(Vector2 position, Vector2 size):
        # Call to __new__ bypasses __init__ constructor
        cdef Rect2 ret = Rect2.__new__(Rect2)
        gdapi.godot_rect2_new_with_position_and_size(&ret._gd_data, &position._gd_data, &size._gd_data)
        return ret

    @staticmethod
    cdef inline Rect2 from_ptr(const godot_rect2 *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<Rect2({self.as_string()})>"

    # Operators

    cdef inline bint operator_equal(self, Rect2 b):
        cdef Rect2 ret  = Rect2.__new__(Rect2)
        return gdapi.godot_rect2_operator_equal(&self._gd_data, &b._gd_data)

    def __eq__(self, other):
        try:
            return Rect2.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Rect2.operator_equal(self, other)
        except TypeError:
            return True

    # Properties

    cdef inline Vector2 get_size(self):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_rect2_get_size(&self._gd_data)
        return ret

    cdef inline void set_size(self, Vector2 val):
        gdapi.godot_rect2_set_size(&self._gd_data, &val._gd_data)

    @property
    def size(self):
        return self.get_size()

    @size.setter
    def size(self, Vector2 val not None):
        self.set_size(val)

    cdef inline Vector2 get_position(self):
        cdef Vector2 ret = Vector2.__new__(Vector2)
        ret._gd_data = gdapi.godot_rect2_get_position(&self._gd_data)
        return ret

    cdef inline void set_position(self, Vector2 val):
        gdapi.godot_rect2_set_position(&self._gd_data, &val._gd_data)

    @property
    def position(self):
        return self.get_position()

    @position.setter
    def position(self, Vector2 val not None):
        self.set_position(val)

    cdef inline Vector2 get_end(self):
        return self.get_position() + self.get_size()

    @property
    def end(self):
        return self.get_position() + self.get_size()

    # Methods

    cpdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_rect2_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline godot_real get_area(self):
        return gdapi.godot_rect2_get_area(&self._gd_data)

    cpdef inline bint intersects(self, Rect2 b):
        return gdapi.godot_rect2_intersects(&self._gd_data, &b._gd_data)

    cpdef inline bint encloses(self, Rect2 b):
        return gdapi.godot_rect2_encloses(&self._gd_data, &b._gd_data)

    cpdef inline bint has_no_area(self):
        return gdapi.godot_rect2_has_no_area(&self._gd_data)

    cpdef inline Rect2 clip(self, Rect2 b):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi.godot_rect2_clip(&self._gd_data, &b._gd_data)
        return ret

    cpdef inline Rect2 merge(self, Rect2 b):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi.godot_rect2_merge(&self._gd_data, &b._gd_data)
        return ret

    cpdef inline bint has_point(self, Vector2 point):
        return gdapi.godot_rect2_has_point(&self._gd_data, &point._gd_data)

    cpdef inline Rect2 grow(self, godot_real by):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi.godot_rect2_grow(&self._gd_data, by)
        return ret

    cpdef inline Rect2 grow_individual(self, godot_real left, godot_real top, godot_real right, godot_real bottom):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi11.godot_rect2_grow_individual(&self._gd_data, left, top, right, bottom)
        return ret

    cpdef inline Rect2 grow_margin(self, godot_int margin, godot_real by):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi11.godot_rect2_grow_margin(&self._gd_data, margin, by)
        return ret

    cpdef inline Rect2 abs(self):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi11.godot_rect2_abs(&self._gd_data)
        return ret

    cpdef inline Rect2 expand(self, Vector2 to):
        cdef Rect2 ret = Rect2.__new__(Rect2)
        ret._gd_data = gdapi.godot_rect2_expand(&self._gd_data, &to._gd_data)
        return ret
