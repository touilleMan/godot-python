{% macro gd_to_py(type, src, dst) %}
{% if type['gd_value'] == type['py_value'] %}
{{ dst }} = {{ src }}
{% else %}
dst = godot_string_to_pyobj(&src)
gdapi10.godot_string_destroy(&src)
{% endif %}
{% endmacro %}

{% macro py_to_gd(target) %}
{% endmacro %}

{% macro render_pool_array_pyx(t) %}
@cython.final
cdef class {{ t.py_pool }}:

    def __init__(self, other=None):
        cdef {{ t.py_pool }} other_as_pool_array
        cdef Array other_as_array
        if other is None:
            gdapi10.{{ t.gd_pool }}_new(&self._gd_data)
        else:
            try:
                other_as_pool_array = <{{ t.py_pool }}?>other
                gdapi10.{{ t.gd_pool }}_new_copy(&self._gd_data, &other_as_pool_array._gd_data)
            except TypeError:
                try:
                    other_as_array = <Array?>other
                    gdapi10.{{ t.gd_pool }}_new_with_array(&self._gd_data, &other_as_array._gd_data)
                except TypeError:
                    gdapi10.{{ t.gd_pool }}_new(&self._gd_data)
                    for item in other:
{% if t.is_base_type %}
                        {{ t.py_pool }}.append(self, item)
{% else %}
                        {{ t.py_pool }}.append(self, (<{{ t.py_value }}?>item))
{% endif %}

    def __dealloc__(self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.{{ t.gd_pool }}_destroy(&self._gd_data)

    @staticmethod
    cdef inline {{ t.py_pool }} new():
        # Call to __new__ bypasses __init__ constructor
        cdef {{ t.py_pool }} ret = {{ t.py_pool }}.__new__({{ t.py_pool }})
        gdapi10.{{ t.gd_pool }}_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline {{ t.py_pool }} new_with_array(Array other):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ t.py_pool }} ret = {{ t.py_pool }}.__new__({{ t.py_pool }})
        gdapi10.{{ t.gd_pool }}_new_with_array(&ret._gd_data, &other._gd_data)
        return ret

    def __repr__(self):
        return f"<{{ t.py_pool }}([{', '.join(repr(x) for x in self)}])>"

    # Operators

    def __getitem__(self, index):
        cdef godot_int size = self.size()
        cdef godot_int start
        cdef godot_int stop
        cdef godot_int step
        if isinstance(index, slice):
            step = index.step if index.step is not None else 1
            if step == 0:
                raise ValueError("range() arg 3 must not be zero")
            elif step > 0:
                start = index.start if index.start is not None else 0
                stop = index.stop if index.stop is not None else size
            else:
                start = index.start if index.start is not None else size
                stop = index.stop if index.stop is not None else -size - 1
            return self.operator_getslice(
                start,
                stop,
                step,
            )
        else:
            if index < 0:
                index = index + size
            if index < 0 or index >= size:
                raise IndexError("list index out of range")
            return self.operator_getitem(index)

    cdef inline {{ t.py_value }} operator_getitem(self, godot_int index):
{% if t.is_base_type %}
        return gdapi10.{{ t.gd_pool }}_get(&self._gd_data, index)
{% else %}
        cdef {{ t.py_value }} ret = {{ t.py_value }}.__new__({{ t.py_value }})
        ret._gd_data = gdapi10.{{ t.gd_pool }}_get(&self._gd_data, index)
        return ret
{% endif %}

    cdef inline {{ t.py_pool }} operator_getslice(self, godot_int start, godot_int stop, godot_int step):
        cdef {{ t.py_pool }} ret = {{ t.py_pool }}.new()
        cdef godot_int size = self.size()

        if start > size - 1:
            start = size - 1
        elif start < 0:
            start += size
            if start < 0:
                start = 0

        if stop > size:
            stop = size
        elif stop < -size:
            stop = -1
        elif stop < 0:
            stop += size

        if step > 0:
            if start >= stop:
                return ret
            items = 1 + (stop - start - 1) // step
            if items <= 0:
                return ret
        else:
            if start <= stop:
                return ret
            items = 1 + (stop - start + 1) // step
            if items <= 0:
                return ret

        ret.resize(items)
        cdef {{ t.gd_pool }}_read_access *src_access = gdapi10.{{ t.gd_pool }}_read(
            &self._gd_data
        )
        cdef {{ t.gd_pool }}_write_access *dst_access = gdapi10.{{ t.gd_pool }}_write(
            &ret._gd_data
        )
        cdef const {{ t.gd_value }} *src_ptr = gdapi10.{{ t.gd_pool }}_read_access_ptr(src_access)
        cdef {{ t.gd_value }} *dst_ptr = gdapi10.{{ t.gd_pool }}_write_access_ptr(dst_access)
        cdef godot_int i
        for i in range(items):
{% if t.is_stack_only %}
            dst_ptr[i] = src_ptr[i * step + start]
{% else %}
            gdapi10.{{ t.gd_value }}_destroy(&dst_ptr[i])
            gdapi10.{{ t.gd_value }}_new_copy(&dst_ptr[i], &src_ptr[i * step + start])
{% endif %}
        gdapi10.{{ t.gd_pool }}_read_access_destroy(src_access)
        gdapi10.{{ t.gd_pool }}_write_access_destroy(dst_access)

        return ret

    # TODO: support slice
    def __setitem__(self, godot_int index, {{ t.py_value }} value):
        cdef godot_int size
        size = self.size()
        if index < 0:
            index += size
        if index < 0 or index >= size:
            raise IndexError("list index out of range")
{% if t.is_base_type %}
        gdapi10.{{ t.gd_pool }}_set(&self._gd_data, index, value)
{% else %}
        gdapi10.{{ t.gd_pool }}_set(&self._gd_data, index, &value._gd_data)
{% endif %}

    # TODO: support slice
    def __delitem__(self, godot_int index):
        cdef godot_int size
        size = self.size()
        if index < 0:
            index += size
        if index < 0 or index >= size:
            raise IndexError("list index out of range")
        gdapi10.{{ t.gd_pool }}_remove(&self._gd_data, index)

    def __len__(self):
        return self.size()

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        cdef int i
        {% if not t.is_base_type %}
        cdef {{ t.py_value }} item
        {% endif %}
        for i in range(self.size()):
{% if t.is_base_type %}
            yield gdapi10.{{ t.gd_pool }}_get(&self._gd_data, i)
{% else %}
            item = {{ t.py_value }}.__new__({{ t.py_value }})
            item._gd_data = gdapi10.{{ t.gd_pool }}_get(&self._gd_data, i)
            yield item
{% endif %}

    def __copy__(self):
        return self.copy()

    def __eq__(self, other):
        try:
            return {{ t.py_pool }}.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not {{ t.py_pool }}.operator_equal(self, other)
        except TypeError:
            return True

    def __iadd__(self, {{ t.py_pool }} items not None):
        self.append_array(items)
        return self

    def __add__(self, {{ t.py_pool }} items not None):
        cdef {{ t.py_pool }} ret = {{ t.py_pool }}.copy(self)
        ret.append_array(items)
        return ret

    cdef inline bint operator_equal(self, {{ t.py_pool }} other):
        if other is None:
            return False
        # TODO `godot_array_operator_equal` is missing in gdapi, submit a PR ?
        cdef godot_int size = self.size()
        if size != other.size():
            return False

        cdef {{ t.gd_pool }}_read_access *a_access = gdapi10.{{ t.gd_pool }}_read(
            &self._gd_data
        )
        cdef {{ t.gd_pool }}_read_access *b_access = gdapi10.{{ t.gd_pool }}_read(
            &other._gd_data
        )
        cdef const {{ t.gd_value }} *a_ptr = gdapi10.{{ t.gd_pool }}_read_access_ptr(a_access)
        cdef const {{ t.gd_value }} *b_ptr = gdapi10.{{ t.gd_pool }}_read_access_ptr(b_access)
        cdef godot_int i
        cdef bint ret = True
        for i in range(size):
{% if t.is_base_type %}
            if a_ptr[i] != b_ptr[i]:
{% else %}
            if not gdapi10.{{ t.gd_value }}_operator_equal(&a_ptr[i], &b_ptr[i]):
{% endif %}
                ret = False
                break
        gdapi10.{{ t.gd_pool }}_read_access_destroy(a_access)
        gdapi10.{{ t.gd_pool }}_read_access_destroy(b_access)
        return ret

    # Methods

    cpdef inline {{ t.py_pool }} copy(self):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ t.py_pool }} ret = {{ t.py_pool }}.__new__({{ t.py_pool }})
        gdapi10.{{ t.gd_pool }}_new_copy(&ret._gd_data, &self._gd_data)
        return ret

    cpdef inline void append(self, {{ t.py_value }} data):
{% if t.is_base_type %}
        gdapi10.{{ t.gd_pool }}_append(&self._gd_data, data)
{% else %}
        gdapi10.{{ t.gd_pool }}_append(&self._gd_data, &data._gd_data)
{% endif %}

    cdef inline void append_array(self, {{ t.py_pool }} array):
        gdapi10.{{ t.gd_pool }}_append_array(&self._gd_data, &array._gd_data)

    cpdef inline void invert(self):
        gdapi10.{{ t.gd_pool }}_invert(&self._gd_data)

    cpdef inline void push_back(self, {{ t.py_value }} data):
{% if t.is_base_type %}
        gdapi10.{{ t.gd_pool }}_push_back(&self._gd_data, data)
{% else %}
        gdapi10.{{ t.gd_pool }}_push_back(&self._gd_data, &data._gd_data)
{% endif %}

    cpdef inline void resize(self, godot_int size):
        gdapi10.{{ t.gd_pool }}_resize(&self._gd_data, size)

    cdef inline godot_int size(self):
        return gdapi10.{{ t.gd_pool }}_size(&self._gd_data)

    # Raw access

    @contextmanager
    def raw_access(self):
        cdef {{ t.gd_pool }}_write_access *access = gdapi10.{{ t.gd_pool }}_write(
            &self._gd_data
        )
        cdef {{ t.py_pool }}WriteAccess pyaccess = {{ t.py_pool }}WriteAccess.__new__({{ t.py_pool }}WriteAccess)
        pyaccess._gd_ptr = gdapi10.{{ t.gd_pool }}_write_access_ptr(access)
        try:
            yield pyaccess

        finally:
            gdapi10.{{ t.gd_pool }}_write_access_destroy(access)


@cython.final
cdef class {{ t.py_pool }}WriteAccess:

    def get_address(self):
        return <uintptr_t>self._gd_ptr

    def __getitem__(self, int idx):
{% if t.is_base_type %}
        return self._gd_ptr[idx]
{% else %}
        cdef {{ t.py_value }} ret = {{ t.py_value }}.__new__({{ t.py_value }})
{% if t.is_stack_only %}
        ret._gd_data = self._gd_ptr[idx]
{% else %}
        gdapi10.{{ t.gd_value }}_new_copy(&ret._gd_data, &self._gd_ptr[idx])
{% endif %}
        return ret
{% endif %}

    def __setitem__(self, int idx, {{ t.py_value }} val):
{% if t.is_base_type %}
        self._gd_ptr[idx] = val
{% elif t.is_stack_only %}
        self._gd_ptr[idx] = val._gd_data
{% else %}
        gdapi10.{{ t.gd_value }}_new_copy(&self._gd_ptr[idx], &val._gd_data)
{% endif %}

{% endmacro %}
