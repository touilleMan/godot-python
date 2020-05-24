import sys
import pytest
from random import Random
from inspect import isfunction
from functools import partial

from godot import (
    Array,
    Vector2,
    Vector3,
    Color,
    GDString,
    PoolIntArray,
    PoolRealArray,
    PoolByteArray,
    PoolVector2Array,
    PoolVector3Array,
    PoolColorArray,
    PoolStringArray,
    Node,
)

from conftest import generate_global_obj


is_windows_32 = (sys.platform == "win32") and (sys.maxsize <= 2 ** 32)


NODE = generate_global_obj(Node)


class BasePoolArrayBench:
    cls = None

    def __init__(self):
        # Fixed seed for reproducibility
        self.random = Random(0)

    def generate_value(self):
        raise NotImplemented

    def generate_values(self, count):
        return [self.generate_value() for _ in range(count)]

    def expand_arg(self, arg):
        if isfunction(arg):
            return arg(self)
        else:
            return arg


class PoolIntArrayBench(BasePoolArrayBench):
    cls = PoolIntArray

    def generate_value(self):
        return self.random.randint(-(2 ** 31), 2 ** 31 - 1)


class PoolRealArrayBench(BasePoolArrayBench):
    cls = PoolRealArray

    def generate_value(self):
        # Use integer instead of float to avoid floating point imprecision in comparisons
        return float(self.random.randint(0, 100))


class PoolByteArrayBench(BasePoolArrayBench):
    cls = PoolByteArray

    def generate_value(self):
        return self.random.randint(0, 255)


class PoolColorArrayBench(BasePoolArrayBench):
    cls = PoolColorArray

    def generate_value(self):
        # Use integer instead of float to avoid floating point imprecision in comparisons
        return Color(self.random.randint(0, 100))


class PoolStringArrayBench(BasePoolArrayBench):
    cls = PoolStringArray

    def generate_value(self):
        return GDString(str(self.random.random()))


class PoolVector2ArrayBench(BasePoolArrayBench):
    cls = PoolVector2Array

    def generate_value(self):
        # Use integer instead of float to avoid floating point imprecision in comparisons
        return Vector2(self.random.randint(0, 100))


class PoolVector3ArrayBench(BasePoolArrayBench):
    cls = PoolVector3Array

    def generate_value(self):
        # Use integer instead of float to avoid floating point imprecision in comparisons
        return Vector3(self.random.randint(0, 100))


@pytest.fixture(
    scope="module",
    ids=lambda x: x.cls.__name__,
    params=[
        PoolIntArrayBench,
        PoolRealArrayBench,
        PoolByteArrayBench,
        PoolColorArrayBench,
        PoolStringArrayBench,
        PoolVector2ArrayBench,
        PoolVector3ArrayBench,
    ],
)
def pool_x_array(request):
    return request.param()


def test_empty_init(pool_x_array):
    v1 = pool_x_array.cls()
    v2 = pool_x_array.cls()
    assert type(v1) == pool_x_array.cls
    assert v1 == v2
    assert len(v1) == 0


@pytest.mark.parametrize(
    "bad_val",
    [
        lambda x: x.generate_value(),
        lambda x: (object() for _ in range(1)),  # Must be generated each time
        42,
        "dummy",
        NODE,
        Vector2(),
        [object()],
        lambda x: [x.generate_value(), object(), x.generate_value()],
    ],
)
def test_bad_init(pool_x_array, bad_val):
    bad_val = pool_x_array.expand_arg(bad_val)
    with pytest.raises(TypeError):
        pool_x_array.cls(bad_val)


def test_initialized_init(pool_x_array):
    if is_windows_32:
        pytest.skip("Cause segfault on windows-32, see issue #185")

    vals = pool_x_array.generate_values(4)
    v1 = pool_x_array.cls(vals)
    v2 = pool_x_array.cls(Array(vals))
    v3 = pool_x_array.cls(v2)
    assert type(v1) == pool_x_array.cls
    assert type(v2) == pool_x_array.cls
    assert type(v3) == pool_x_array.cls
    assert v1 == v2
    assert v2 == v3
    assert len(v1) == 4


def test_equal(pool_x_array):
    vals = pool_x_array.generate_values(4)

    v1 = pool_x_array.cls(vals)
    v2 = pool_x_array.cls()
    for item in vals:
        v2.append(item)
    v3 = pool_x_array.cls()
    v3 += v2

    # Test __eq__ operator
    assert v1 == v2
    assert v2 == v3

    # Test __ne__ operator
    assert not v1 != v2
    assert not v2 != v3


@pytest.mark.parametrize("other_type", [list, tuple, Array])
def test_bad_equal_on_different_types(pool_x_array, other_type):
    if is_windows_32 and other_type is Array:
        pytest.skip("Cause segfault on windows-32, see issue #185")

    vals = pool_x_array.generate_values(4)

    pool = pool_x_array.cls(vals)
    other = other_type(vals)

    # Test __eq__ operator
    assert not pool == other

    # Test __ne__ operator
    assert pool != other


@pytest.mark.parametrize(
    "arg",
    [
        None,
        0,
        Array(),
        [],
        (),
        "",
        Vector2(),
        NODE,
        lambda s: s.generate_value(),
        lambda s: s.cls(s.generate_values(2)),
    ],
)
def test_bad_equal(pool_x_array, arg):
    pool = pool_x_array.cls()
    other = pool_x_array.expand_arg(arg)

    # Test __ne__ operator
    assert not pool == other

    # Test __eq__ operator
    assert pool != other


def test_add(pool_x_array):
    v0 = pool_x_array.generate_values(2)
    arr = pool_x_array.cls(v0)
    v1 = pool_x_array.generate_values(2)
    arr += pool_x_array.cls(v1)  # __iadd__
    assert arr == pool_x_array.cls(v0 + v1)
    v2 = pool_x_array.generate_values(2)
    arr2 = arr + pool_x_array.cls(v2)  # __add__
    assert arr2 == pool_x_array.cls(v0 + v1 + v2)


@pytest.mark.parametrize("arg", [None, [], (), Array(), 0, "foo", Vector2(), NODE])
def test_bad_add(pool_x_array, arg):
    with pytest.raises(TypeError):
        pool_x_array.cls() + arg


@pytest.mark.parametrize("arg", [None, [], (), Array(), 0, "foo", Vector2(), NODE])
def test_bad_iadd(pool_x_array, arg):
    arr = pool_x_array.cls()
    with pytest.raises(TypeError):
        arr += arg


def test_repr(pool_x_array):
    name = pool_x_array.cls.__name__
    v = pool_x_array.cls()
    assert repr(v) == f"<{name}([])>"
    items = pool_x_array.generate_values(3)
    v = pool_x_array.cls(items)
    assert repr(v) == f"<{name}({items!r})>"


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["append", type(None), lambda x: (x.generate_value(),)],
        ["push_back", type(None), lambda x: (x.generate_value(),)],
        ["resize", type(None), (2,)],
    ],
    ids=lambda x: x[0],
)
def test_methods(pool_x_array, field, ret_type, params):
    # Don't test methods' validity but bindings one
    v = pool_x_array.cls(pool_x_array.generate_values(1))
    params = pool_x_array.expand_arg(params)
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


def test_len(pool_x_array):
    arr = pool_x_array.cls()
    assert len(arr) == 0
    arr.append(pool_x_array.generate_value())
    assert len(arr) == 1


def test_getitem(pool_x_array):
    vals = pool_x_array.generate_values(3)
    arr = pool_x_array.cls(vals)
    assert arr[0] == vals[0]
    assert arr[1] == vals[1]
    assert arr[-1] == vals[-1]


@pytest.mark.parametrize(
    "slice_",
    [
        slice(1, 3),
        slice(1, 3, -1),
        slice(None, None, -1),
        slice(None, None, 2),
        slice(None, None, 10),
        slice(-10, 10, 1),
        slice(-10, None, 1),
        slice(-1, None, 1),
        slice(-1, 1, -1),
    ],
)
def test_getitem_slice(pool_x_array, slice_):
    vals = pool_x_array.generate_values(4)
    arr = pool_x_array.cls(vals)
    expected = vals[slice_]
    sub_arr = arr[slice_]
    assert isinstance(sub_arr, pool_x_array.cls)
    assert sub_arr == pool_x_array.cls(expected)


def test_getitem_slice_zero_step(pool_x_array):
    arr = pool_x_array.cls(pool_x_array.generate_values(2))
    with pytest.raises(ValueError):
        arr[::0]


def test_outofrange_getitem(pool_x_array):
    arr = pool_x_array.cls(pool_x_array.generate_values(2))
    with pytest.raises(IndexError):
        arr[2]
    with pytest.raises(IndexError):
        arr[-3]


def test_setitem(pool_x_array):
    arr = pool_x_array.cls(pool_x_array.generate_values(3))
    v = pool_x_array.generate_value()
    arr[0] = v
    assert len(arr) == 3
    assert arr[0] == v
    arr[-1] = v
    assert len(arr) == 3
    assert arr[-1] == v


def test_outofrange_setitem(pool_x_array):
    arr = pool_x_array.cls(pool_x_array.generate_values(2))
    v = pool_x_array.generate_value()
    with pytest.raises(IndexError):
        arr[2] = v
    with pytest.raises(IndexError):
        arr[-3] = v


def test_delitem(pool_x_array):
    items = pool_x_array.generate_values(3)
    arr = pool_x_array.cls(items)
    del arr[0]
    assert len(arr) == 2
    assert arr[0] == items[1]
    assert arr[1] == items[2]
    del arr[-1]
    assert len(arr) == 1
    assert arr[-1] == items[1]


def test_outofrange_delitem(pool_x_array):
    arr = pool_x_array.cls(pool_x_array.generate_values(2))
    with pytest.raises(IndexError):
        del arr[2]
    with pytest.raises(IndexError):
        del arr[-3]


def test_iter(pool_x_array):
    items = pool_x_array.generate_values(3)
    arr = pool_x_array.cls(items)
    items_from_v = [x for x in arr]
    assert items_from_v == items


def test_append(pool_x_array):
    items = pool_x_array.generate_values(3)
    arr = pool_x_array.cls()
    for item in items:
        arr.append(item)
    assert len(arr) == 3
    assert arr == pool_x_array.cls(items)


def test_raw_access(pool_x_array):
    arr = pool_x_array.cls()
    arr.resize(100)
    values = pool_x_array.generate_values(10)

    with arr.raw_access() as ptr:
        assert isinstance(ptr.get_address(), int)

        for i in range(100):
            ptr[i] = values[i % len(values)]

    with arr.raw_access() as ptr:
        for i in range(100):
            assert ptr[i] == values[i % len(values)]


def test_pool_byte_array_overflow():
    with pytest.raises(OverflowError):
        PoolByteArray([256])
    with pytest.raises(OverflowError):
        PoolByteArray([1, 2, 256, 4])
    arr = PoolByteArray([1])
    with pytest.raises(OverflowError):
        arr.append(256)
    with pytest.raises(OverflowError):
        arr.push_back(256)
