from functools import partial
from collections.abc import MutableSequence


class BasePoolArray(BaseBuiltinWithGDObjOwnership, MutableSequence):
    __slots__ = ()
    GD_TYPE = None

    def _gd_to_py(self, value):
        return self._contained_cls.build_from_gdobj(value)

    def _py_to_gd(self, value):
        self._check_param_type('value', value, self._contained_cls)
        return value._gd_ptr

    def __init__(self, items=None):
        try:
            self._gd_ptr = self._gd_new_ptr_mem()
            # TODO: use godot_pool_*_array_new_with_array
            if items:
                if isinstance(items, self._cls):
                    self._gd_ptr[0] = self._gd_array_copy(items._gd_ptr)
                else:
                        self._gd_array_new(self._gd_ptr)
                        self += items
            else:
                self._gd_array_new(self._gd_ptr)
        except:
            # Unset _gd_ptr anyway to avoid segfault in __del__
            self._gd_ptr = None
            raise

    def __del__(self):
        if self._gd_ptr:
            self._gd_array_destroy(self._gd_ptr)

    @classmethod
    def _copy_gdobj(cls, gdobj):
        gdobj = cls._gd_new_ptr_mem()
        gdobj[0] = cls._gd_array_copy(gdobj)
        return gdobj

    def __repr__(self):
        return "<%s(%s)>" % (type(self).__name__, [x for x in self])

    def __eq__(self, other):
        # TODO: should be able to optimize this...
        try:
            return list(self) == list(other)
        except TypeError:
            return False

    def __ne__(self, other):
        return not self == other        

    def __iadd__(self, items):
        if isinstance(items, (str, bytes)):
            return NotImplemented
        # TODO: use godot_pool_vector3_array_append_array
        for x in items:
            self.append(x)
        return self

    def __radd__(self, items):
        return self._cls(items) + self

    def __add__(self, items):
        if isinstance(items, (str, bytes)):
            return NotImplemented
        arr = self._cls()
        # TODO: use godot_pool_vector3_array_append_array
        for x in self:
            arr.append(x)
        for x in items:
            arr.append(x)
        return arr

    def __iter__(self):
        # TODO: mid iteration mutation should throw exception ?
        for c in range(len(self)):
            yield self[c]

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self._cls([x for x in self][idx])
        size = len(self)
        idx = size + idx if idx < 0 else idx
        if abs(idx) >= size:
            raise IndexError('list index out of range')
        raw = self._gd_array_get(self._gd_ptr, idx)
        return self._gd_to_py(raw)

    def __setitem__(self, idx, value):
        size = len(self)
        idx = size + idx if idx < 0 else idx
        if abs(idx) >= size:
            raise IndexError('list index out of range')
        value = self._py_to_gd(value)
        self._gd_array_set(self._gd_ptr, idx, value)

    def __delitem__(self, idx):
        size = len(self)
        idx = size + idx if idx < 0 else idx
        if abs(idx) >= size:
            raise IndexError('list index out of range')
        self._gd_array_remove(self._gd_ptr, idx)

    def __len__(self):
        return self._gd_array_size(self._gd_ptr)

    # Methods

    def append(self, value):
        value = self._py_to_gd(value)
        self._gd_array_append(self._gd_ptr, value)

    def insert(self, pos, value):
        value = self._py_to_gd(value)
        if self._gd_array_insert(self._gd_ptr, pos, value) != lib.GODOT_OK:
            raise IndexError("list assignment index out of range")

    def invert(self):
        self._gd_array_invert(self._gd_ptr)

    def push_back(self, value):
        value = self._py_to_gd(value)
        self._gd_array_push_back(self._gd_ptr, value)

    def resize(self, size):
        self._check_param_type('size', size, int)
        self._gd_array_resize(self._gd_ptr, size)


def _generate_pool_array(clsname, pycls, gdname, py_to_gd=None, gd_to_py=None):
    nmspc = {
        '__slots__': (),
        'GD_TYPE': getattr(lib, 'GODOT_VARIANT_TYPE_%s' % gdname.upper()),
        '_gd_new_ptr_mem': partial(ffi.new, 'godot_%s*' % gdname),
        '_contained_cls': pycls
    }
    for suffix in ('new', 'copy', 'destroy', 'get',
                   'set', 'remove', 'size', 'append',
                   'insert', 'invert', 'push_back', 'resize'):
        nmspc['_gd_array_%s' % suffix] = getattr(lib, 'godot_%s_%s' % (gdname, suffix))
    if py_to_gd:
        nmspc['_py_to_gd'] = py_to_gd
    if gd_to_py:
        nmspc['_gd_to_py'] = gd_to_py
    cls = type(clsname, (BasePoolArray, ), nmspc)
    cls._cls = cls
    return cls


PoolColorArray = _generate_pool_array('PoolColorArray', Color, 'pool_color_array')
PoolVector2Array = _generate_pool_array('PoolVector2Array', Vector2, 'pool_vector2_array')
PoolVector3Array = _generate_pool_array('PoolVector3Array', Vector3, 'pool_vector3_array')


def _identity(self, value):
    return value

def _byte_py_to_gd(self, value):
    if not isinstance(value, int):
        raise TypeError("'%s' object cannot be interpreted as an integer" % type(value).__name__)
    if not 0 <= int(value) < 256:
        raise ValueError('bytes must be in range(0, 256)')
    return value


def _int_py_to_gd(self, value):
    self._check_param_type('value', value, int)
    return value


def _real_py_to_gd(self, value):
    self._check_param_float('value', value)
    return value


def _string_gd_to_py(self, value):
    return godot_string_to_pyobj(ffi.addressof(value))


def _string_py_to_gd(self, value):
    self._check_param_type('value', value, str)
    return pyobj_to_gdobj(value)


PoolByteArray = _generate_pool_array('PoolByteArray', int, 'pool_byte_array', py_to_gd=_byte_py_to_gd, gd_to_py=_identity)
PoolIntArray = _generate_pool_array('PoolIntArray', int, 'pool_int_array', py_to_gd=_int_py_to_gd, gd_to_py=_identity)
PoolRealArray = _generate_pool_array('PoolRealArray', float, 'pool_real_array', py_to_gd=_real_py_to_gd, gd_to_py=_identity)
PoolStringArray = _generate_pool_array('PoolStringArray', str, 'pool_string_array', py_to_gd=_string_py_to_gd, gd_to_py=_string_gd_to_py)
