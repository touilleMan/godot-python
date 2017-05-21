import pytest

from godot.bindings import Array, PoolIntArray, PoolByteArray, Node, Resource, Area2D, Vector2


class TestPoolByteArray:

    def test_base(self):
        v = PoolByteArray()
        assert type(v) == PoolByteArray

    @pytest.mark.parametrize('arg', [
        Array,
        PoolByteArray,
        list,
    ])
    def test_equal(self, arg):
        arr = PoolByteArray()
        other = arg()
        for item in [1, 2, 3, 4]:
            arr.append(item)
            other.append(item)
        assert arr == other
        bad = PoolByteArray([0, 0, 0])
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Vector2(),
        Node(),
        [1],
        PoolByteArray([1]),
        Array([1]),
    ])
    def test_bad_equal(self, arg):
        arr = PoolByteArray()
        assert arr != arg

    def test_add(self):
        arr = PoolByteArray([1])
        arr += PoolByteArray([2, 3])  # __iadd__
        assert arr == PoolByteArray([1, 2, 3])
        arr2 = arr + PoolByteArray([4])  # __add__
        assert arr2 == PoolByteArray([1, 2, 3, 4])

    def test_add_with_non_PoolBytearray(self):
        arr = PoolByteArray([0])
        arr += [1, 2]  # __iadd__
        assert arr == PoolByteArray([0, 1, 2])
        arr2 = arr + [3]  # __add__
        assert arr2 == PoolByteArray([0, 1, 2, 3])
        # Test __radd__ as well
        arr3 = [0] + arr
        assert arr3 == PoolByteArray([0, 0, 1, 2])

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Vector2(),
        Node(),
    ])
    def test_bad_add(self, arg):
        with pytest.raises(TypeError):
            assert PoolByteArray() + arg

    def test_repr(self):
        v = PoolByteArray()
        assert repr(v) == '<PoolByteArray([])>'
        v = PoolByteArray([1, 2, 3])
        assert repr(v) == "<PoolByteArray([1, 2, 3])>"

    @pytest.mark.parametrize('arg', [
        42,
        'dummy',
        Node(),
        Vector2(),
        [object()],
        Array(['not', 'bytes']),
    ])
    def test_bad_instantiate(self, arg):
        with pytest.raises(TypeError):
            PoolByteArray(arg)

    @pytest.mark.parametrize('arg', [
        PoolByteArray(),
        Array([1, 2]),
        [],
        (),
        [42, 43, 44],
    ])
    def test_instantiate_from_copy(self, arg):
        arr = PoolByteArray(arg)
        if hasattr(arg, '_gd_ptr'):
            assert arr._gd_ptr != arg._gd_ptr

    def test_byte_overflow(self):
        with pytest.raises(ValueError):
            PoolByteArray([256])
        with pytest.raises(ValueError):
            PoolByteArray([1, 2, 256, 4])
        arr = PoolByteArray([1])
        with pytest.raises(ValueError):
            arr.append(256)
        with pytest.raises(ValueError):
            arr.insert(1, 256)
        with pytest.raises(ValueError):
            arr.push_back(256)
        with pytest.raises(ValueError):
            arr.insert(1, 256)

    @pytest.mark.parametrize('arg', [
        'foo',
        None,
    ], ids=lambda x: x[0])
    def test_bad_byte(self, arg):
        with pytest.raises(TypeError):
            PoolByteArray([arg])
        with pytest.raises(TypeError):
            PoolByteArray([1, 2, arg, 4])
        arr = PoolByteArray([1])
        with pytest.raises(TypeError):
            arr.append(arg)
        with pytest.raises(TypeError):
            arr.insert(1, arg)
        with pytest.raises(TypeError):
            arr.push_back(arg)
        with pytest.raises(TypeError):
            arr.insert(1, arg)

    @pytest.mark.parametrize('args', [
        ['append', type(None), (42, )],
        ['insert', type(None), (0, 42)],
        ['push_back', type(None), (42, )],
        ['remove', type(None), (0, )],
        ['resize', type(None), (2, )],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = PoolByteArray([1])
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    def test_len(self):
        v = PoolByteArray()
        assert len(v) == 0
        v.append(42)
        assert len(v) == 1

    def test_getitem(self):
        v = PoolByteArray([0, 1, 2])
        assert v[0] == 0
        assert v[1] == 1

    def test_getitem_slice(self):
        v = PoolByteArray([0, 1, 2])
        assert isinstance(v[:-1], PoolByteArray)
        assert v[1:] == PoolByteArray([v[1], v[2]])

    def test_outofrange_getitem(self):
        v = PoolByteArray([0, 1])
        with pytest.raises(IndexError):
            v[2]

    def test_setitem(self):
        v = PoolByteArray([0, 1, 2])
        v[0] = 0xff
        assert len(v) == 3
        assert v[0] == 0xff

    def test_outofrange_setitem(self):
        v = PoolByteArray([0, 1])
        with pytest.raises(IndexError):
            v[2] = 0xff

    def test_iter(self):
        items = [0, 1, 2]
        v = PoolByteArray(items)
        items_from_v = [x for x in v]
        assert items_from_v == items

    def test_append(self):
        items = [0, 1, 2]
        v = PoolByteArray()
        for item in items:
            v.append(item)
        assert len(v) == 3
        assert v == PoolByteArray(items)
