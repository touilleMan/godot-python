{% macro render_pool_array_pxd(t) %}
@cython.final
cdef class {{ t.py_pool }}:
    cdef {{ t.gd_pool }} _gd_data

    @staticmethod
    cdef inline {{ t.py_pool }} new()

    @staticmethod
    cdef inline {{ t.py_pool }} new_with_array(Array other)

    # Operators

    cdef inline bint operator_equal(self, {{ t.py_pool }} other)
    cdef inline {{ t.py_value }} operator_getitem(self, godot_int index)
    cdef inline {{ t.py_pool }} operator_getslice(self, godot_int start, godot_int end, godot_int step)

    # Methods

    cpdef inline {{ t.py_pool }} copy(self)
    cpdef inline void append(self, {{ t.py_value }} data)
    cdef inline void append_array(self, {{ t.py_pool }} array)
    cpdef inline void invert(self)
    cpdef inline void push_back(self, {{ t.py_value }} data)
    cpdef inline void resize(self, godot_int size)
    cdef inline godot_int size(self)


@cython.final
cdef class {{ t.py_pool }}WriteAccess:
    cdef {{ t.gd_value }} *_gd_ptr

{% endmacro %}
