{%- block pxd_header %}
{% endblock -%}
{%- block pyx_header %}
{% endblock -%}


@cython.final
cdef class Array:
{% block cdef_attributes %}
    @staticmethod
    cdef inline Array new()
    @staticmethod
    cdef inline Array from_ptr(const godot_array *_ptr)
    cdef inline Array operator_getslice(self, godot_int start, godot_int stop, godot_int step)
    cdef inline bint operator_equal(self, Array other)
    cdef inline Array operator_add(self, Array items)
    cdef inline operator_iadd(self, Array items)

    cdef godot_array _gd_data

{% endblock %}

{% block python_defs %}
    def __init__(self, iterable=None):
        if not iterable:
            gdapi10.godot_array_new(&self._gd_data)
        elif isinstance(iterable, Array):
            self._gd_data = gdapi11.godot_array_duplicate(&(<Array>iterable)._gd_data, False)
        # TODO: handle Pool*Array
        else:
            gdapi10.godot_array_new(&self._gd_data)
            for x in iterable:
                self.append(x)

    @staticmethod
    cdef inline Array new():
        # Call to __new__ bypasses __init__ constructor
        cdef Array ret = Array.__new__(Array)
        gdapi10.godot_array_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Array from_ptr(const godot_array *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Array ret = Array.__new__(Array)
        # `godot_array` is a cheap structure pointing on a refcounted vector
        # of variants. Unlike it name could let think, `godot_array_new_copy`
        # only increment the refcount of the underlying structure.
        gdapi10.godot_array_new_copy(&ret._gd_data, _ptr)
        return ret

    def __dealloc__(self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.godot_array_destroy(&self._gd_data)

    def __repr__(self):
        return f"<{type(self).__name__}([{', '.join([repr(x) for x in self])}])>"

    # Operators

    cdef inline Array operator_getslice(self, godot_int start, godot_int stop, godot_int step):
        cdef Array ret = Array.new()
        # TODO: optimize with `godot_array_resize` ?
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

        gdapi10.godot_array_resize(&ret._gd_data, items)
        cdef int i
        cdef godot_variant *p_item
        for i in range(items):
            p_item = gdapi10.godot_array_operator_index(&self._gd_data, i * step + start)
            gdapi10.godot_array_append(&ret._gd_data, p_item)
            gdapi10.godot_variant_destroy(p_item)

        return ret

    # TODO: support slice
    def __getitem__(self, index):
        cdef godot_int size = self.size()
        # cdef godot_int start
        # cdef godot_int stop
        # cdef godot_int step
        # cdef godot_int items
        # if isinstance(index, slice):
        #     cook_slice(index, size, &start, &stop, &step, &items)
        #     gdapi10.godot_array_resize(&ret._gd_data, items)
        #     cdef int i
        #     cdef godot_variant *p_item
        #     for i in range(items):
        #         p_item = gdapi10.godot_array_operator_index(&self._gd_data, i * step + start)
        #         gdapi10.godot_array_append(&ret._gd_data, p_item)
        #         gdapi10.godot_variant_destroy(p_item)


        #     step = index.step if index.step is not None else 1
        #     if step == 0:
        #     elif step > 0:
        #         start = index.start if index.start is not None else 0
        #         stop = index.stop if index.stop is not None else size
        #     else:
        #         start = index.start if index.start is not None else size
        #         stop = index.stop if index.stop is not None else -size - 1
        #     return Array.operator_getslice(self, start, stop, step)
        # else:
        if index < 0:
            index = index + size
        if index < 0 or index >= size:
            raise IndexError("list index out of range")

        cdef godot_variant *p_ret = gdapi10.godot_array_operator_index(&self._gd_data, index)
        return godot_variant_to_pyobj(p_ret)

    # TODO: support slice
    def __setitem__(self, godot_int index, object value):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")

        cdef godot_variant *p_ret = gdapi10.godot_array_operator_index(&self._gd_data, index)
        gdapi10.godot_variant_destroy(p_ret)
        pyobj_to_godot_variant(value, p_ret)

    # TODO: support slice
    def __delitem__(self, godot_int index):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")

        gdapi10.godot_array_remove(&self._gd_data, index)

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        cdef int i
        for i in range(self.size()):
            yield self.get(i)

    def __copy__(self):
        return self.duplicate(False)

    def __deepcopy__(self):
        return self.duplicate(True)

    cdef inline bint operator_equal(self, Array other):
        # TODO `godot_array_operator_equal` is missing in gdapi, submit a PR ?
        cdef godot_int size = self.size()
        if size != other.size():
            return False
        cdef int i
        for i in range(size):
            if not gdapi10.godot_variant_operator_equal(
                    gdapi10.godot_array_operator_index(&self._gd_data, i),
                    gdapi10.godot_array_operator_index(&other._gd_data, i)
                ):
                return False
        return True

    def __eq__(self, other):
        try:
            return Array.operator_equal(self, <Array?>other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Array.operator_equal(self, <Array?>other)
        except TypeError:
            return True

    cdef inline operator_iadd(self, Array items):
        cdef godot_int self_size = self.size()
        cdef godot_int items_size = items.size()
        gdapi10.godot_array_resize(&self._gd_data, self_size + items_size)
        cdef int i
        for i in range(items_size):
            Array.set(self, self_size + i, items.get(i))

    # TODO: support __iadd__ for other types than Array ?
    def __iadd__(self, items not None):
        try:
            Array.operator_iadd(self, items)
        except TypeError:
            for x in items:
                self.append(x)
        return self

    cdef inline Array operator_add(self, Array items):
        cdef godot_int self_size = self.size()
        cdef godot_int items_size = items.size()
        cdef Array ret = Array.new()
        gdapi10.godot_array_resize(&ret._gd_data, self_size + items_size)
        cdef int i
        for i in range(self_size):
            Array.set(ret, i, self.get(i))
        for i in range(items_size):
            Array.set(ret, self_size + i, items.get(i))
        return ret

    # TODO: support __add__ for other types than Array ?
    def __add__(self, items not None):
        try:
            return Array.operator_add(self, items)
        except TypeError:
            ret = Array.duplicate(self, False)
            for x in items:
                ret.append(x)
            return ret

    {{ render_method("size", py_name="__len__") | indent }}
    {{ render_method("hash", py_name="__hash__") | indent }}
    {{ render_method("has", py_name="__contains__") | indent }}

    {{ render_method("hash") | indent }}
    {{ render_method("size") | indent }}
    {{ render_method("duplicate") | indent }}
    {{ render_method("get") | indent }}
    {{ render_method("set") | indent }}
    {{ render_method("append") | indent }}
    {{ render_method("clear") | indent }}
    {{ render_method("empty") | indent }}
    {{ render_method("count") | indent }}
    {{ render_method("erase") | indent }}
    {{ render_method("front") | indent }}
    {{ render_method("back") | indent }}
    {{ render_method("find") | indent }}
    {{ render_method("find_last") | indent }}
    {{ render_method("insert") | indent }}
    {{ render_method("invert") | indent }}
    {{ render_method("pop_back") | indent }}
    {{ render_method("pop_front") | indent }}
    {{ render_method("push_back") | indent }}
    {{ render_method("push_front") | indent }}
    {{ render_method("remove") | indent }}
    {{ render_method("resize") | indent }}
    {{ render_method("rfind") | indent }}
    {{ render_method("sort") | indent }}
{# {{ render_method("sort_custom") | indent }} #}
    {{ render_method("bsearch") | indent }}
{# {{ render_method("bsearch_custom") | indent }} #}
    {{ render_method("max") | indent }}
    {{ render_method("min") | indent }}
    {{ render_method("shuffle") | indent }}
{% endblock %}

{%- block python_consts %}
{% endblock %}
