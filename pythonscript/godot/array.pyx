# cython: language_level=3

cimport cython

from godot._hazmat.gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
)
from godot._hazmat.gdnative_api_struct cimport godot_array, godot_int, godot_real, godot_variant
from godot._hazmat.conversion cimport godot_variant_to_pyobj, pyobj_to_godot_variant


@cython.final
cdef class Array:

    def __init__(self, iterable=None):
        if not iterable:
            gdapi.godot_array_new(&self._gd_data)
        elif isinstance(iterable, Array):
            gdapi.godot_array_new_copy(&self._gd_data, &(<Array>iterable)._gd_data)
        # TODO: handle Pool*Array
        else:
            gdapi.godot_array_new(&self._gd_data)
            for x in iterable:
                self.append(x)

    def __dealloc__(self):
        gdapi.godot_array_destroy(&self._gd_data)

    @staticmethod
    cdef inline Array new():
        # Call to __new__ bypasses __init__ constructor
        cdef Array ret = Array.__new__(Array)
        gdapi.godot_array_new(&ret._gd_data)
        return ret

    @staticmethod
    cdef inline Array from_ptr(const godot_array *_ptr):
        # Call to __new__ bypasses __init__ constructor
        cdef Array ret = Array.__new__(Array)
        # `godot_array` is a cheap structure pointing on a refcounted vector
        # of variants. Unlike it name could let think, `godot_array_new_copy`
        # only increment the refcount of the underlying structure.
        gdapi.godot_array_new_copy(&ret._gd_data, _ptr)
        return ret

    def __repr__(self):
        return f"<{type(self).__name__}({', '.join(iter(self))})>"

    # Operators

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.operator_getslice(index)
        else:
            return self.operator_getitem(index)

    # TODO: support slice
    def __setitem__(self, godot_int index, object value):
        self.operator_setitem(index, value)

    # TODO: support slice
    def __delitem__(self, godot_int index):
        self.operator_delitem(index)

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

    def __eq__(self, Array other):
        return self.operator_equal(other)

    def __ne__(self, other):
        return not self.operator_equal(other)

    def __contains__(self, object key):
        return self.operator_contains(key)

    # TODO: support __iadd__ for other types than Array ?
    def __iadd__(self, Array items):
        cdef godot_int self_size = self.size()
        cdef godot_int items_size = items.size()
        gdapi.godot_array_resize(&self._gd_data, self_size + items_size)
        cdef int i
        for i in range(items_size):
            self.operator_set(self_size + i, items.get(i))
        return self

    # TODO: support __add__ for other types than Array ?
    def __add__(self, Array items):
        cdef godot_int self_size = self.size()
        cdef godot_int items_size = items.size()
        cdef Array arr = Array.new()
        gdapi.godot_array_resize(&arr._gd_data, self_size + items_size)
        cdef int i
        for i in range(self_size):
            arr.operator_set(i, self.get(i))
        for i in range(items_size):
            arr.operator_set(self_size + i, items.get(i))
        return arr

    cdef inline bint operator_equal(self, Array other):
        # TODO `godot_array_operator_equal` is missing in gdapi, submit a PR ?
        cdef godot_int size = self.size()
        if size != other.size():
            return False
        cdef int i
        for i in range(size):
            if not gdapi.godot_variant_operator_equal(
                    gdapi.godot_array_operator_index(&self._gd_data, i),
                    gdapi.godot_array_operator_index(&other._gd_data, i)
                ):
                return False
        return True

    cdef inline bint operator_contains(self, object key):
        cdef godot_variant var_key
        pyobj_to_godot_variant(key, &var_key)
        cdef bint ret = gdapi.godot_array_has(&self._gd_data, &var_key)
        gdapi.godot_variant_destroy(&var_key)
        return ret

    cdef inline Array operator_getslice(self, object slice_):
        cdef Array ret = Array.new()
        # TODO: optimize with `godot_array_resize` ?
        cdef int i
        for i in range(slice_.start, slice_.end, slice_.step or 1):
            ret.append(self.operator_getitem(i))
        return ret

    cdef inline object operator_getitem(self, godot_int index):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        return self.get(index)

    cdef inline void operator_setitem(self, godot_int index, object value):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        self.set(index, value)

    cdef inline void operator_delitem(self, godot_int index):
        cdef godot_int size = self.size()
        index = size + index if index < 0 else index
        if abs(index) >= size:
            raise IndexError("list index out of range")
        self.remove(index)

    # Methods

    cpdef inline godot_int hash(self):
        return gdapi.godot_array_hash(&self._gd_data)

    cpdef inline godot_int size(self):
        return gdapi.godot_array_size(&self._gd_data)

    cpdef inline Array duplicate(self, bint deep):
        cdef Array ret = Array.__new__(Array)
        ret._gd_data = gdapi11.godot_array_duplicate(&self._gd_data, deep)
        return ret

    cpdef inline object get(self, godot_int idx):
        cdef godot_variant *p_ret = gdapi.godot_array_operator_index(&self._gd_data, idx)
        return godot_variant_to_pyobj(p_ret)

    # TODO: good idea to use expose `set` ?
    cpdef inline void set(self, godot_int idx, object item):
        cdef godot_variant *p_ret = gdapi.godot_array_operator_index(&self._gd_data, idx)
        gdapi.godot_variant_destroy(p_ret)
        pyobj_to_godot_variant(item, p_ret)

    cpdef inline void append(self, object item):
        cdef godot_variant var_item
        pyobj_to_godot_variant(item, &var_item)
        gdapi.godot_array_append(&self._gd_data, &var_item)
        gdapi.godot_variant_destroy(&var_item)

    cpdef inline void clear(self):
        gdapi.godot_array_clear(&self._gd_data)

    cpdef inline bint empty(self):
        return gdapi.godot_array_empty(&self._gd_data)

    cpdef inline void erase(self, object item):
        cdef godot_variant var_item
        pyobj_to_godot_variant(item, &var_item)
        gdapi.godot_array_erase(&self._gd_data, &var_item)
        gdapi.godot_variant_destroy(&var_item)

    cpdef inline object front(self):
        cdef godot_variant var_ret = gdapi.godot_array_front(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline object back(self):
        cdef godot_variant var_ret = gdapi.godot_array_back(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline godot_int find(self, object what, godot_int from_):
        cdef godot_variant var_what
        pyobj_to_godot_variant(what, &var_what)
        cdef godot_int ret = gdapi.godot_array_find(&self._gd_data, &var_what, from_)
        gdapi.godot_variant_destroy(&var_what)
        return ret

    cpdef inline godot_int find_last(self, object what):
        cdef godot_variant var_what
        pyobj_to_godot_variant(what, &var_what)
        cdef godot_int ret = gdapi.godot_array_find_last(&self._gd_data, &var_what)
        gdapi.godot_variant_destroy(&var_what)
        return ret

    cpdef inline void insert(self, godot_int pos, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi.godot_array_insert(&self._gd_data, pos, &var_value)
        gdapi.godot_variant_destroy(&var_value)

    cpdef inline void invert(self):
        gdapi.godot_array_invert(&self._gd_data)

    cpdef inline object pop_back(self):
        cdef godot_variant var_ret = gdapi.godot_array_pop_back(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline object pop_front(self):
        cdef godot_variant var_ret = gdapi.godot_array_pop_front(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline void push_back(self, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi.godot_array_push_back(&self._gd_data, &var_value)
        gdapi.godot_variant_destroy(&var_value)

    cpdef inline void push_front(self, object value):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        gdapi.godot_array_push_front(&self._gd_data, &var_value)
        gdapi.godot_variant_destroy(&var_value)

    cpdef inline void remove(self, godot_int idx):
        gdapi.godot_array_remove(&self._gd_data, idx)

    cpdef inline void resize(self, godot_int size):
        gdapi.godot_array_resize(&self._gd_data, size)

    cpdef inline bint rfind(self, object what, godot_int from_):
        cdef godot_variant var_what
        pyobj_to_godot_variant(what, &var_what)
        cdef bint ret = gdapi.godot_array_rfind(&self._gd_data, &var_what, from_)
        gdapi.godot_variant_destroy(&var_what)
        return ret

    cpdef inline void sort(self):
        gdapi.godot_array_sort(&self._gd_data)

    cdef inline void sort_custom(self, godot_object *p_obj, godot_string *p_func):
        gdapi.godot_array_sort_custom(&self._gd_data, p_obj, p_func)

    cpdef inline godot_int bsearch(self, object value, bint before):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        cdef godot_int ret = gdapi.godot_array_bsearch(&self._gd_data, &var_value, before)
        gdapi.godot_variant_destroy(&var_value)
        return ret

    cdef inline godot_int bsearch_custom(self, object value, godot_object *p_obj, godot_string *p_func, bint before):
        cdef godot_variant var_value
        pyobj_to_godot_variant(value, &var_value)
        cdef godot_int ret = gdapi.godot_array_bsearch_custom(&self._gd_data, &var_value, p_obj, p_func, before)
        gdapi.godot_variant_destroy(&var_value)
        return ret

    cpdef inline object max(self):
        cdef godot_variant var_ret = gdapi11.godot_array_max(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline object min(self):
        cdef godot_variant var_ret = gdapi11.godot_array_min(&self._gd_data)
        cdef object ret = godot_variant_to_pyobj(&var_ret)
        gdapi.godot_variant_destroy(&var_ret)
        return ret

    cpdef inline void shuffle(self):
        gdapi11.godot_array_shuffle(&self._gd_data)
