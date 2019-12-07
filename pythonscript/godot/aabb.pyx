# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_aabb, godot_bool, godot_int, godot_real, godot_string, godot_vector3
from godot._hazmat.conversion cimport godot_string_to_pyobj
from godot.plane cimport Plane
from godot.vector3 cimport Vector3


@cython.final
cdef class AABB:

    def __init__(self, Vector3 pos, Vector3 size):
        gdapi.godot_aabb_new(&self._gd_data, &pos._gd_data, &size._gd_data)

    @staticmethod
    cdef AABB new(godot_vector3 *pos, godot_vector3 *size):
        # Call to __new__ bypasses __init__ constructor
        cdef AABB ret = AABB.__new__(AABB)
        gdapi.godot_aabb_new(&ret._gd_data, pos, size)
        return ret

    @staticmethod
    cdef AABB from_ptr(const godot_aabb *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = _ptr[0]
        return ret

    def __repr__(self):
        return f"<AABB({self.as_string()})>"

    # Operators

    cdef inline bint operator_equal(self, AABB b):
        cdef AABB ret  = AABB.__new__(AABB)
        return gdapi.godot_aabb_operator_equal(&self._gd_data, &b._gd_data)

    def __eq__(self, other):
        cdef AABB _other = <AABB?>other
        return self.operator_equal(_other)

    def __ne__(self, other):
        cdef AABB _other = <AABB?>other
        return not self.operator_equal(_other)

    # Properties

    cdef inline Vector3 get_position(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_aabb_get_position(&self._gd_data)
        return ret

    cdef inline Vector3 set_position(self, Vector3 val):
        gdapi.godot_aabb_set_position(&self._gd_data, &val._gd_data)

    @property
    def position(self):
        return self.get_position()

    @position.setter
    def position(self, val):
        self.set_position(val)

    cdef inline Vector3 get_size(self):
        cdef Vector3 ret = Vector3.__new__(Vector3)
        ret._gd_data = gdapi.godot_aabb_get_size(&self._gd_data)
        return ret

    cdef inline Vector3 set_size(self, Vector3 val):
        gdapi.godot_aabb_set_size(&self._gd_data, &val._gd_data)

    @property
    def size(self):
        return self.get_size()

    @size.setter
    def size(self, val):
        self.set_size(val)

    @property
    def end(self):
        return self.get_end()

    cdef inline Vector3 get_end(self):
        return self.get_position() + self.get_size()

    # Methods

    cpdef inline str as_string(self):
        cdef godot_string var_ret = gdapi.godot_aabb_as_string(&self._gd_data)
        cdef str ret = godot_string_to_pyobj(&var_ret)
        gdapi.godot_string_destroy(&var_ret)
        return ret

    cpdef inline godot_real get_area(self):
        return gdapi.godot_aabb_get_area(&self._gd_data)

    cpdef inline bint has_no_area(self):
        return gdapi.godot_aabb_has_no_area(&self._gd_data)

    cpdef inline bint has_no_surface(self):
        return gdapi.godot_aabb_has_no_surface(&self._gd_data)

    cpdef inline bint intersects(self, AABB with_):
        return gdapi.godot_aabb_intersects(&self._gd_data, &with_._gd_data)

    cpdef inline bint encloses(self, AABB with_):
        return gdapi.godot_aabb_encloses(&self._gd_data, &with_._gd_data)

    cpdef inline AABB merge(self, AABB with_):
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_merge(&self._gd_data, &with_._gd_data)
        return ret

    cpdef inline AABB intersection(self, AABB with_):
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_intersection(&self._gd_data, &with_._gd_data)
        return ret

    cpdef inline bint intersects_plane(self, Plane plane):
        return gdapi.godot_aabb_intersects_plane(&self._gd_data, &plane._gd_data)

    cpdef inline bint intersects_segment(self, Vector3 from_, Vector3 to):
        return gdapi.godot_aabb_intersects_segment(&self._gd_data, &from_._gd_data, &to._gd_data)

    cpdef inline bint has_point(self, Vector3 point):
        return gdapi.godot_aabb_has_point(&self._gd_data, &point._gd_data)

    cpdef inline Vector3 get_support(self, Vector3 dir):
        cdef Vector3 ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_get_support(&self._gd_data, &dir._gd_data)
        return ret

    cpdef inline Vector3 get_longest_axis(self):
        cdef Vector3 ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_get_longest_axis(&self._gd_data)
        return ret

    cpdef inline godot_int get_longest_axis_index(self, Vector3 point):
        return gdapi.godot_aabb_get_longest_axis_index(&self._gd_data)

    cpdef inline godot_real get_longest_axis_size(self, Vector3 point):
        return gdapi.godot_aabb_get_longest_axis_size(&self._gd_data)

    cpdef inline Vector3 get_shortest_axis(self):
        cdef Vector3 ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_get_shortest_axis(&self._gd_data)
        return ret

    cpdef inline godot_int get_shortest_axis_index(self, Vector3 point):
        return gdapi.godot_aabb_get_shortest_axis_index(&self._gd_data)

    cpdef inline godot_real get_shortest_axis_size(self, Vector3 point):
        return gdapi.godot_aabb_get_shortest_axis_size(&self._gd_data)

    cpdef inline AABB expand(self, Vector3 to_point):
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_expand(&self._gd_data, &to_point._gd_data)
        return ret

    cpdef inline AABB grow(self, godot_real by):
        cdef AABB ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_grow(&self._gd_data, by)
        return ret

    cpdef inline Vector3 get_endpoint(self, godot_int idx):
        cdef Vector3 ret = AABB.__new__(AABB)
        ret._gd_data = gdapi.godot_aabb_get_endpoint(&self._gd_data, idx)
        return ret
