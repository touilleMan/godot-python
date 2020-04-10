import pytest

from godot import Rect2, Vector2


def test_base():
    v = Rect2(4, 3, 2, 1)
    assert type(v) == Rect2
    v2 = Rect2(1, 2, 3, 4)
    assert type(v) == Rect2
    assert v2 == Rect2(1, 2, 3, 4)
    assert v != v2


def test_repr():
    v = Rect2(1, 2)
    assert repr(v) == "<Rect2(1, 2, 0, 0)>"


def test_instantiate():
    # Can build it with int or float or nothing
    msg_tmpl = "%s vs (expected) %s (args=%s)"
    for args, expected_pos, expected_size in (
        [(), Vector2(0, 0), Vector2(0, 0)],
        [(0.5, 0.5), Vector2(0.5, 0.5), Vector2(0, 0)],
        [(1, 2, 1, 2), Vector2(1, 2), Vector2(1, 2)],
    ):
        v = Rect2(*args)
        assert v.position == expected_pos, msg_tmpl % (v.position, expected_pos, args)
        assert v.size == expected_size, msg_tmpl % (v.size, expected_size, args)
    with pytest.raises(TypeError):
        Rect2("a", 2, 3, 4)
    with pytest.raises(TypeError):
        Rect2(1, "b", 3, 4)
    with pytest.raises(TypeError):
        Rect2(1, 2, "c", 4)
    with pytest.raises(TypeError):
        Rect2(1, 2, 3, "d")
    with pytest.raises(TypeError):
        Rect2(None, 2)


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["get_area", float, ()],
        ["intersects", bool, (Rect2(),)],
        ["encloses", bool, (Rect2(),)],
        ["has_no_area", bool, ()],
        ["clip", Rect2, (Rect2(),)],
        ["merge", Rect2, (Rect2(),)],
        ["has_point", bool, (Vector2(),)],
        ["grow", Rect2, (0.5,)],
        ["grow_individual", Rect2, (0.1, 0.2, 0.3, 0.4)],
        ["grow_margin", Rect2, (42, 0.5)],
        ["abs", Rect2, ()],
        ["expand", Rect2, (Vector2(),)],
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = Rect2()
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


@pytest.mark.parametrize(
    "field,ret_type", [("position", Vector2), ("size", Vector2)], ids=lambda x: x[0]
)
def test_rw_properties(field, ret_type):
    v = Rect2()
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert type(field_val) == ret_type
    for val in (Vector2(), Vector2(0.1, -0.1)):
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert field_val == val


def test_ro_end_property():
    v = Rect2()
    assert hasattr(v, "end")
    assert type(v.end) == Vector2
    with pytest.raises(AttributeError):
        v.end = Vector2()


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("position", "dummy"),
        ("size", "dummy"),
        ("position", None),
        ("size", None),
        ("position", 42),
        ("size", 42),
    ],
    ids=lambda x: x[0],
)
def test_bad_rw_properties(field, bad_value):
    v = Rect2()
    with pytest.raises(TypeError):
        setattr(v, field, bad_value)


def test_equal():
    arr = Rect2(0.1, 1, 2, 3)
    other = Rect2(0.1, 1, 2, 3)
    assert arr == other
    bad = Rect2(0.1, 1, 2, 4)
    assert not arr == bad  # Force use of __eq__


@pytest.mark.parametrize("arg", [None, 0, "foo", Rect2(0.1, 1, 2, 4)])
def test_bad_equal(arg):
    arr = Rect2(0.1, 1, 2, 3)
    assert arr != arg
