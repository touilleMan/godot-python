
class PoolByteArray(BaseBuiltin, list):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY

    def __init__(self, items=None):
        self._gd_ptr = ffi.new('godot_pool_byte_array*')
        # TODO: use godot_pool_byte_array_new_with_array
        if items:
            if isinstance(items, PoolByteArray):
                self._gd_ptr[0] = lib.godot_pool_byte_array_copy(items._gd_ptr)
            else:
                lib.godot_pool_byte_array_new(self._gd_ptr)
                self += items

    def __del__(self):
        lib.godot_pool_byte_array_destroy(self._gd_ptr)

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
        # TODO: use godot_pool_byte_array_append_array
        for x in items:
            self.append(x)
        return self

    def __radd__(self, items):
        return PoolByteArray(items) + self

    def __add__(self, items):
        if isinstance(items, (str, bytes)):
            return NotImplemented
        arr = PoolByteArray()
        # TODO: use godot_pool_byte_array_append_array
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
            return PoolByteArray([x for x in self][idx])
        size = len(self)
        if abs(idx) >= size:
            raise IndexError('list index out of range')
        idx = size - idx if idx < 0 else idx
        ret = lib.godot_pool_byte_array_get(self._gd_ptr, idx)
        return ret

    def __setitem__(self, idx, value):
        size = len(self)
        if abs(idx) >= size:
            raise IndexError('list index out of range')
        self._check_byte(value)
        idx = size - idx if idx < 0 else idx
        lib.godot_pool_byte_array_set(self._gd_ptr, idx, value)

    def __len__(self):
        return lib.godot_pool_byte_array_size(self._gd_ptr)

    @staticmethod
    def _check_byte(value):
        if not isinstance(value, int):
            raise TypeError("'%s' object cannot be interpreted as an integer" % type(value).__name__)
        if not 0 <= int(value) < 256:
            raise ValueError('bytes must be in range(0, 256)')

    # Methods

    def append(self, value):
        self._check_byte(value)
        lib.godot_pool_byte_array_append(self._gd_ptr, value)

    def insert(self, pos, value):
        self._check_byte(value)
        if lib.godot_pool_byte_array_insert(self._gd_ptr, pos, value) != lib.GODOT_OK:
            raise IndexError("list assignment index out of range")

    def invert(self):
        lib.godot_pool_byte_array_invert(self._gd_ptr)

    def push_back(self, value):
        self._check_byte(value)
        lib.godot_pool_byte_array_push_back(self._gd_ptr, value)

    def remove(self, idx):
        lib.godot_pool_byte_array_remove(self._gd_ptr, idx)

    def resize(self, size):
        lib.godot_pool_byte_array_resize(self._gd_ptr, size)