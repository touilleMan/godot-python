import pytest
import random
from inspect import isfunction

from godot.bindings import (
    Node, Resource, Area2D, Vector2, Vector3, Color, Array,
    PoolIntArray, PoolByteArray, PoolRealArray, PoolColorArray,
    PoolStringArray, PoolVector2Array, PoolVector3Array
)


class BaseTestPoolArray:

    def _expand_arg(self, arg):
        return arg(self) if isfunction(arg) else arg

    def test_base(self):
        v = self.acls()
        assert type(v) == self.acls

    @pytest.mark.parametrize('arg', [
        Array,
        lambda s: s.acls,
        list,
    ])
    def test_equal(self, arg):
        arg = self._expand_arg(arg)
        arr = self.acls()
        other = arg()
        for item in [self.vg() for _ in range(4)]:
            arr.append(item)
            other.append(item)
        assert arr == other
        bad = self.acls([self.vg()])
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Vector2(),
        Node(),
        lambda s: s.vg(1),
        lambda s: s.acls(s.vg(1)),
        lambda s: Array(s.vg(1)),
    ])
    def test_bad_equal(self, arg):
        arg = self._expand_arg(arg)
        arr = self.acls()
        assert arr != arg

    def test_add(self):
        v0 = self.vg(1)
        arr = self.acls(v0)
        v1 = self.vg(2)
        arr += self.acls(v1)  # __iadd__
        assert arr == self.acls(v0 + v1)
        v2 = self.vg(1)
        arr2 = arr + self.acls(v2)  # __add__
        assert arr2 == self.acls(v0 + v1 + v2)

    def test_add_with_non_PoolBytearray(self):
        v0 = self.vg(1)
        arr = self.acls(v0)
        v1 = self.vg(2)
        arr += v1  # __iadd__
        assert arr == self.acls(v0 + v1)
        v2 = self.vg(1)
        arr2 = arr + v2  # __add__
        assert arr2 == self.acls(v0 + v1 + v2)
        # Test __radd__ as well
        v3 = self.vg(1)
        arr3 = v3 + arr2
        assert arr3 == self.acls(v3 + v0 + v1 + v2)

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Vector2(),
        Node(),
    ])
    def test_bad_add(self, arg):
        with pytest.raises(TypeError):
            assert self.acls() + arg

    def test_repr(self):
        name = self.acls.__name__
        v = self.acls()
        assert repr(v) == '<%s([])>' % name
        items = self.vg(3)
        v = self.acls(items)
        assert repr(v) == "<%s(%s)>" % (name, items)

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
        lambda s: s.acls(),
        lambda s: Array(s.vg(2)),
        [],
        (),
        lambda s: s.vg(3),
    ])
    def test_instantiate_from_copy(self, arg):
        arg = self._expand_arg(arg)
        arr = self.acls(arg)
        if hasattr(arg, '_gd_ptr'):
            assert arr._gd_ptr != arg._gd_ptr

    @pytest.mark.parametrize('args', [
        ['append', type(None), lambda s: (s.vg(), )],
        ['insert', type(None), lambda s: (0, s.vg())],
        ['push_back', type(None), lambda s: (s.vg(), )],
        ['resize', type(None), (2, )],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = self.acls(self.vg(1))
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        params = self._expand_arg(params)
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    def test_len(self):
        arr = self.acls()
        assert len(arr) == 0
        arr.append(self.vg())
        assert len(arr) == 1

    def test_getitem(self):
        v = self.vg(3)
        arr = self.acls(v)
        assert arr[0] == v[0]
        assert arr[1] == v[1]
        assert arr[-1] == v[-1]

    def test_getitem_slice(self):
        arr = self.acls(self.vg(3))
        assert isinstance(arr[:-1], self.acls)
        assert arr[1:] == self.acls([arr[1], arr[2]])

    def test_outofrange_getitem(self):
        arr = self.acls(self.vg(2))
        with pytest.raises(IndexError):
            arr[2]

    def test_setitem(self):
        arr = self.acls(self.vg(3))
        v = self.vg()
        arr[0] = v
        assert len(arr) == 3
        assert arr[0] == v
        arr[-1] = v
        assert len(arr) == 3
        assert arr[-1] == v

    def test_outofrange_setitem(self):
        arr = self.acls(self.vg(2))
        v = self.vg()
        with pytest.raises(IndexError):
            arr[2] = v

    def test_delitem(self):
        items = self.vg(3)
        arr = self.acls(items)
        del arr[0]
        assert len(arr) == 2
        assert arr[0] == items[1]
        assert arr[1] == items[2]
        del arr[-1]
        assert len(arr) == 1
        assert arr[-1] == items[1]

    def test_outofrange_delitem(self):
        arr = self.acls(self.vg(2))
        with pytest.raises(IndexError):
            del arr[2]

    def test_iter(self):
        items = self.vg(3)
        arr = self.acls(items)
        items_from_v = [x for x in arr]
        assert items_from_v == items

    def test_append(self):
        items = self.vg(3)
        arr = self.acls()
        for item in items:
            arr.append(item)
        assert len(arr) == 3
        assert arr == self.acls(items)


class TestPoolByteArray(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolByteArray
        random.seed(0)  # Fix seed for reproducibility
        self.vg = lambda c=None: random.randint(0, 255) if c is None else [random.randint(0, 255) for x in range(c)]

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


class TestPoolIntArray(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolIntArray
        random.seed(0)  # Fix seed for reproducibility
        self.vg = lambda c=None: random.randint(-2**31, 2**31-1) if c is None else [random.randint(-2**31, 2**31-1) for x in range(c)]


class TestPoolRealArray(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolRealArray
        random.seed(0)  # Fix seed for reproducibility
        # Use integer instead of float to avoid floating point imprecision in comparisons
        self.vg = lambda c=None: float(random.randint(0, 100)) if c is None else [float(random.randint(0, 100)) for x in range(c)]


class TestPoolColorArray(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolColorArray
        random.seed(0)  # Fix seed for reproducibility
        # Use integer instead of float to avoid floating point imprecision in comparisons
        self.vg = lambda c=None: Color(random.randint(0, 100)) if c is None else [Color(random.randint(0, 100)) for x in range(c)]


class TestPoolStringArray(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolStringArray
        random.seed(0)  # Fix seed for reproducibility
        self.vg = lambda c=None: str(random.random()) if c is None else [str(random.random()) for x in range(c)]


class TestPoolVector2Array(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolVector2Array
        random.seed(0)  # Fix seed for reproducibility
        # Use integer instead of float to avoid floating point imprecision in comparisons
        self.vg = lambda c=None: Vector2(random.randint(0, 100)) if c is None else [Vector2(random.randint(0, 100)) for x in range(c)]


class TestPoolVector3Array(BaseTestPoolArray):
    def setup(self):
        self.acls = PoolVector3Array
        random.seed(0)  # Fix seed for reproducibility
        # Use integer instead of float to avoid floating point imprecision in comparisons
        self.vg = lambda c=None: Vector3(random.randint(0, 100)) if c is None else [Vector3(random.randint(0, 100)) for x in range(c)]

# Extra tests
class TestPoolVector3ArraySize:
    def test_size(self):
        a = PoolVector3Array()
        a.resize(1000)
        assert len(a) == 1000
    def test_size_in_array(self):
        a = Array()
        a.resize(9)
        a[0] = PoolVector3Array()
        a[0].resize(1000)
        assert len(a[0]) == 1000
    def test_as_both(self):
        a = Array()
        a.resize(9)
        pa = PoolVector3Array()
        pa.resize(1000)
        assert len(pa) == 1000
        a[0] = pa
        assert len(pa) == 1000
        pa.resize(2000)
        assert len(pa) == 2000
        assert len(a[0]) == 2000
        a[0].resize(3000)
        assert len(a[0]) == 3000
