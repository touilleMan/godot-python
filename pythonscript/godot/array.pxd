# cython: language_level=3

cimport cython

from godot._hazmat.gdnative_api_struct cimport (
    godot_array,
    godot_bool,
    godot_int,
    godot_string,
    godot_object,
)


@cython.final
cdef class Array:
    cdef godot_array _gd_data

    @staticmethod
    cdef Array new()

    @staticmethod
    cdef Array from_ptr(const godot_array *_ptr)

    # Operators

    cdef inline godot_bool operator_equal(self, Array other)
    cdef inline godot_bool operator_contains(self, object key)
    cdef inline Array operator_getslice(self, object slice_)
    cdef inline object operator_getitem(self, godot_int index)
    cdef inline void operator_setitem(self, godot_int index, object value)
    cdef inline void operator_delitem(self, godot_int index)

    # Methods

    cpdef inline godot_int hash(self)
    cpdef inline godot_int size(self)
    cpdef inline Array duplicate(self, godot_bool deep)
    cpdef inline object get(self, godot_int idx)
    cpdef inline void set(self, godot_int idx, object item)
    cpdef inline void append(self, object item)
    cpdef inline void clear(self)
    cpdef inline godot_bool empty(self)
    cpdef inline void erase(self, object item)
    cpdef inline object front(self)
    cpdef inline object back(self)
    cpdef inline godot_int find(self, object what, godot_int from_)
    cpdef inline godot_int find_last(self, object what)
    cpdef inline void insert(self, godot_int pos, object value)
    cpdef inline void invert(self)
    cpdef inline object pop_back(self)
    cpdef inline object pop_front(self)
    cpdef inline void push_back(self, object value)
    cpdef inline void push_front(self, object value)
    cpdef inline void remove(self, godot_int idx)
    cpdef inline void resize(self, godot_int size)
    cpdef inline godot_bool rfind(self, object what, godot_int from_)
    cpdef inline void sort(self)
    cdef inline void sort_custom(self, godot_object *p_obj, godot_string *p_func)
    cpdef inline godot_int bsearch(self, object value, godot_bool before)
    cdef inline godot_int bsearch_custom(self, object value, godot_object *p_obj, godot_string *p_func, godot_bool before)
    cpdef inline object max(self)
    cpdef inline object min(self)
    cpdef inline void shuffle(self)
