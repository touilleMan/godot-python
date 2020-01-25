# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi10 as gdapi10,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_array, godot_int, godot_real, godot_variant
from godot._hazmat.conversion cimport godot_variant_to_pyobj, pyobj_to_godot_variant


@cython.final
cdef class Array:

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

    def __dealloc__(self):
        # /!\ if `__init__` is skipped, `_gd_data` must be initialized by
        # hand otherwise we will get a segfault here
        gdapi10.godot_array_destroy(&self._gd_data)

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
        return Array.get(self, index)

    # TODO: support slice
    def __setitem__(self, godot_int index, object value):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        self.set(index, value)

    # TODO: support slice
    def __delitem__(self, godot_int index):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        self.remove(index)

    def __len__(self):
        return self.size()

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        cdef int i
        for i in range(self.size()):
            yield self.get(i)

    def __copy__(self):
        return self.duplicate(False)

    def __deepcopy__(self):
        return self.duplicate(True)

    def __hash__(self):
        return self.hash()

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

    def __eq__(self, Array other):
        try:
            return Array.operator_equal(self, other)
        except TypeError:
            return False

    def __ne__(self, other):
        try:
            return not Array.operator_equal(self, other)
        except TypeError:
            return True

    cdef inline bint operator_contains(self, object key):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef bint ret = gdapi10.godot_array_has(&self._gd_data, &var_key)
        gdapi10.godot_variant_destroy(&var_key)
        return ret

    def __contains__(self, object key):
        return Array.operator_contains(self, key)

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

    # Methods

    cpdef inline godot_int hash(self):
        return gdapi10.godot_array_hash(&self._gd_data)

    cpdef inline godot_int size(self):
        return gdapi10.godot_array_size(&self._gd_data)

    cpdef inline Array duplicate(self, bint deep):
        cdef Array ret = Array.__new__(Array)
        ret._gd_data = gdapi11.godot_array_duplicate(&self._gd_data, deep)
        return ret

    cpdef inline object get(self, godot_int idx):
        cdef godot_variant *p_ret = gdapi10.godot_array_operator_index(&self._gd_data, idx)
        return godot_variant_to_pyobj(p_ret)

    # TODO: good idea to use expose `set` ?
    cpdef inline void set(self, godot_int idx, object item):
        cdef godot_variant *p_ret = gdapi10.godot_array_operator_index(&self._gd_data, idx)
        gdapi10.godot_variant_destroy(p_ret)
        pyobj_to_godot_variant(item, p_ret)

    cpdef inline void append(self, object item):
        cdef godot_variant var_item
        pyobj_to_godot_variant(item, &var_item)
        gdapi10.godot_array_append(&self._gd_data, &var_item)
        gdapi10.godot_variant_destroy(&var_item)

    cpdef inline void clear(self):
        gdapi10.godot_array_clear(&self._gd_data)

    cpdef inline bint empty(self):
        return gdapi10.godot_array_empty(&self._gd_data)

    cpdef inline godot_int count(self, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        cdef godot_int ret = gdapi10.godot_array_count(&self._gd_data, &var_value)
        gdapi10.godot_variant_destroy(&var_value)
        return ret

    cpdef inline void erase(self, object item):
        cdef godot_variant var_item
        pyobj_to_godot_variant(item, &var_item)
        gdapi10.godot_array_erase(&self._gd_data, &var_item)
        gdapi10.godot_variant_destroy(&var_item)

    cpdef inline object front(self):
        cdef godot_variant var_ret = gdapi10.godot_array_front(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline object back(self):
        cdef godot_variant var_ret = gdapi10.godot_array_back(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline godot_int find(self, object what, godot_int from_):
        cdef godot_variant var_what
        pyobj_to_godot_variant(what, &var_what)
        cdef godot_int ret = gdapi10.godot_array_find(&self._gd_data, &var_what, from_)
        gdapi10.godot_variant_destroy(&var_what)
        return ret

    cpdef inline godot_int find_last(self, object what):
        cdef godot_variant var_what
        pyobj_to_godot_variant(what, &var_what)
        cdef godot_int ret = gdapi10.godot_array_find_last(&self._gd_data, &var_what)
        gdapi10.godot_variant_destroy(&var_what)
        return ret

    cpdef inline void insert(self, godot_int pos, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi10.godot_array_insert(&self._gd_data, pos, &var_value)
        gdapi10.godot_variant_destroy(&var_value)

    cpdef inline void invert(self):
        gdapi10.godot_array_invert(&self._gd_data)

    cpdef inline object pop_back(self):
        cdef godot_variant var_ret = gdapi10.godot_array_pop_back(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline object pop_front(self):
        cdef godot_variant var_ret = gdapi10.godot_array_pop_front(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline void push_back(self, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi10.godot_array_push_back(&self._gd_data, &var_value)
        gdapi10.godot_variant_destroy(&var_value)

    cpdef inline void push_front(self, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi10.godot_array_push_front(&self._gd_data, &var_value)
        gdapi10.godot_variant_destroy(&var_value)

    cpdef inline void remove(self, godot_int idx):
        gdapi10.godot_array_remove(&self._gd_data, idx)

    cpdef inline void resize(self, godot_int size):
        gdapi10.godot_array_resize(&self._gd_data, size)

    cpdef inline godot_int rfind(self, object what, godot_int from_):
        cdef godot_variant var_what
        pyobj_to_godot_variant(what, &var_what)
        cdef godot_int ret = gdapi10.godot_array_rfind(&self._gd_data, &var_what, from_)
        gdapi10.godot_variant_destroy(&var_what)
        return ret

    cpdef inline void sort(self):
        gdapi10.godot_array_sort(&self._gd_data)

    cdef inline void sort_custom(self, godot_object *p_obj, godot_string *p_func):
        gdapi10.godot_array_sort_custom(&self._gd_data, p_obj, p_func)

    cpdef inline godot_int bsearch(self, object value, bint before):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        cdef godot_int ret = gdapi10.godot_array_bsearch(&self._gd_data, &var_value, before)
        gdapi10.godot_variant_destroy(&var_value)
        return ret

    cdef inline godot_int bsearch_custom(self, object value, godot_object *p_obj, godot_string *p_func, bint before):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        cdef godot_int ret = gdapi10.godot_array_bsearch_custom(&self._gd_data, &var_value, p_obj, p_func, before)
        gdapi10.godot_variant_destroy(&var_value)
        return ret

    cpdef inline object max(self):
        cdef godot_variant var_ret = gdapi11.godot_array_max(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline object min(self):
        cdef godot_variant var_ret = gdapi11.godot_array_min(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi10.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline void shuffle(self):
        gdapi11.godot_array_shuffle(&self._gd_data)
