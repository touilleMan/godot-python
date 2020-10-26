import pytest

from godot import (
    GDString,
    Array,
    Vector2,
    PoolColorArray,
    PoolVector3Array,
    PoolVector2Array,
    PoolStringArray,
    PoolRealArray,
    PoolIntArray,
    PoolByteArray,
    Node,
    Resource,
    Area2D,
    OS,
)


def test_base():
    v = Array()
    assert type(v) == Array


def test_equal(current_node):
    arr = Array()
    other = Array()
    for item in [1, "foo", current_node, OS, Vector2()]:
        arr.append(item)
        other.append(item)
    assert arr == other
    bad = Array([0, 0, 0])
    assert not arr == bad  # Force use of __eq__
    assert not arr == None  # Force use of __eq__


@pytest.mark.parametrize(
    "arg", [None, 0, "foo", Vector2(), [1], Array([1, 2]), PoolByteArray([1]), PoolIntArray([1])]
)
def test_bad_equal(arg):
    arr = Array([1])
    assert arr != arg


def test_add():
    arr = Array([None])
    arr += Array([1, "two"])  # __iadd__
    assert arr == Array([None, 1, "two"])
    arr2 = arr + Array([3])  # __add__
    assert arr2 == Array([None, 1, "two", 3])


def test_add_with_non_array():
    arr = Array([0])
    arr += [1, "two"]  # __iadd__
    assert arr == Array([0, 1, "two"])
    arr2 = arr + [3]  # __add__
    assert arr2 == Array([0, 1, "two", 3])
    assert arr == Array([0, 1, "two"])  # arr shouldn't have been modified

    # list.__iadd__ only works with other lists
    arr3 = ["-1"]
    with pytest.raises(TypeError):
        arr3 += arr

    # list.__add__ only works with other lists
    with pytest.raises(TypeError):
        ["-1"] + arr

    arr4 = ["-1"] + list(arr)
    assert arr4 == ["-1", 0, 1, GDString("two")]


@pytest.mark.parametrize("arg", [None, 0, Vector2(), OS])
def test_bad_add(arg):
    v = Array()
    with pytest.raises(TypeError):
        v + arg  # __add__
    with pytest.raises(TypeError):
        v += arg  # __iadd__


@pytest.mark.parametrize("deep", [False, True])
def test_duplicate(deep):
    inner = Array([0])
    arr = Array([inner])
    arr2 = arr.duplicate(deep)
    arr[0].append(1)
    arr2[0].append(2)

    if deep:
        assert arr == Array([Array([0, 1])])
        assert arr2 == Array([Array([0, 2])])
    else:
        assert arr == Array([Array([0, 1, 2])])
        assert arr2 == arr


def test_mix_add_duplicate():
    arr = Array([0])
    arr2 = arr.duplicate(True)
    arr.append(1)
    arr2.append(2)
    arr3 = arr + arr2
    arr.append(3)
    arr3 += arr

    assert list(arr) == [0, 1, 3]
    assert list(arr2) == [0, 2]
    assert list(arr3) == [0, 1, 0, 2, 0, 1, 3]


def test_repr():
    v = Array()
    assert repr(v) == "<Array([])>"
    v = Array([1, "foo", Vector2()])
    assert repr(v) == "<Array([1, <GDString('foo')>, <Vector2(x=0.0, y=0.0)>])>"


@pytest.mark.parametrize("arg", [42, OS, Vector2()])
def test_bad_instantiate(arg):
    with pytest.raises(TypeError):
        Array(arg)


def test_instantiate_with_non_godot_data(recwarn):
    with pytest.raises(TypeError):
        Array([object()])


def test_append_with_non_godot_data(recwarn):
    v = Array()
    with pytest.raises(TypeError):
        v.append(object())


def test_add_with_non_godot_data(recwarn):
    v = Array()
    with pytest.raises(TypeError):
        v += [object()]


@pytest.mark.parametrize(
    "arg",
    [
        Array(),
        PoolColorArray(),
        PoolVector3Array(),
        PoolVector2Array(),
        PoolStringArray(),
        PoolRealArray(),
        PoolIntArray(),
        PoolByteArray(),
        [],
        (),
        [42, 43, 44],
        (GDString("foo"), GDString("bar"), GDString("spam")),
        (OS,),
        [Vector2(), Vector2(), Vector2()],
        (OS, Vector2(), GDString("foo"), 0),  # Enjoy the mix
    ],
)
def test_instantiate_from_copy(arg):
    v = Array(arg)
    assert list(v) == list(arg)
    original_len = len(arg)
    v.append(42)
    assert len(arg) == original_len
    assert len(v) == original_len + 1


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["append", type(None), ("bar",)],
        ["clear", type(None), ()],
        ["count", int, ("foo",)],
        ["empty", bool, ()],
        ["erase", type(None), ("foo",)],
        ["front", GDString, ()],
        ["back", GDString, ()],
        ["find", int, ("foo", 0)],
        ["find_last", int, ("foo",)],
        # ["has", bool, ("foo",)],  # provided by __in__ instead
        ["hash", int, ()],
        ["insert", type(None), (0, "bar")],
        ["invert", type(None), ()],
        ["pop_back", GDString, ()],
        ["pop_front", GDString, ()],
        ["push_back", type(None), ("bar",)],
        ["push_front", type(None), ("bar",)],
        ["resize", type(None), (2,)],
        ["rfind", int, ("foo", 0)],
        ["sort", type(None), ()],
        # ['sort_custom', type(None), (obj, func)],
    ],
    ids=lambda f, r, p: f,
)
def test_methods(field, ret_type, params):
    v = Array(["foo"])
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


def test_len():
    v = Array()
    assert len(v) == 0
    v.append("foo")
    assert len(v) == 1


def test_getitem():
    v = Array(["foo", 0, OS, 0.42])
    assert v[0] == GDString("foo")
    assert v[1] == 0
    assert v[-1] == 0.42


@pytest.mark.skip(reason="Not supported yet")
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
def test_getitem_slice(slice_):
    vals = [GDString("foo"), 0, OS, False]
    arr = Array(vals)
    expected = vals[slice_]
    sub_arr = arr[slice_]
    assert isinstance(sub_arr, Array)
    assert list(sub_arr) == expected


def test_outofrange_getitem():
    v = Array(["foo", 0])
    with pytest.raises(IndexError):
        v[2]


def test_setitem():
    v = Array(["foo", 0, OS])
    v[0] = "bar"
    assert len(v) == 3
    assert v[0] == GDString("bar")
    v[-1] = 4
    assert len(v) == 3
    assert v[2] == 4


def test_outofrange_setitem():
    v = Array(["foo", 0])
    with pytest.raises(IndexError):
        v[2] = 42


def test_delitem():
    v = Array(["foo", 0, OS])
    del v[0]
    assert len(v) == 2
    assert v[0] == 0
    del v[-1]
    assert len(v) == 1
    v[0] == 0


def test_outofrange_delitem():
    v = Array(["foo", 0])
    with pytest.raises(IndexError):
        del v[2]


def test_iter():
    items = [GDString("foo"), 0, OS]
    v = Array(items)
    items_from_v = [x for x in v]
    assert items_from_v == items


def test_append():
    items = [1, "foo", OS]
    v = Array()
    for item in items:
        v.append(item)
    assert len(v) == 3
    assert v == Array(items)
