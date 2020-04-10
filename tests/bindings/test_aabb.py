import pytest

from godot import AABB, Vector3, Plane


def test_base():
    v = AABB(Vector3(1, 2, 3), Vector3(4, 5, 6))
    assert type(v) == AABB
    v2 = AABB(Vector3(1, 2, 3), Vector3(4, 5, 7))
    assert type(v) == AABB
    assert v2 == AABB(Vector3(1, 2, 3), Vector3(4, 5, 7))
    assert v != v2


def test_repr():
    v = AABB(Vector3(1, 2, 3), Vector3(4, 5, 6))
    assert repr(v) == "<AABB(1, 2, 3 - 4, 5, 6)>"


def test_instantiate():
    # Can build it with int or float or nothing
    msg_tmpl = "%s vs (expected) %s (args=%s)"
    for args, expected_pos, expected_size in (
        [(), Vector3(0, 0, 0), Vector3(0, 0, 0)],
        [(Vector3(0, 1, 0), Vector3(0, 0, 1)), Vector3(0, 1, 0), Vector3(0, 0, 1)],
    ):
        v = AABB(*args)
        assert v.position == expected_pos, msg_tmpl % (v.position, expected_pos, args)
        assert v.size == expected_size, msg_tmpl % (v.size, expected_size, args)
    with pytest.raises(TypeError):
        AABB("a", Vector3())
    with pytest.raises(TypeError):
        AABB(Vector3(), "b")


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["get_area", float, ()],
        ["has_no_area", bool, ()],
        ["has_no_surface", bool, ()],
        ["intersects", bool, (AABB(Vector3(1, 2, 3), Vector3(4, 5, 6)),)],
        ["encloses", bool, (AABB(Vector3(1, 2, 3), Vector3(4, 5, 6)),)],
        ["merge", AABB, (AABB(Vector3(1, 2, 3), Vector3(4, 5, 6)),)],
        ["intersection", AABB, (AABB(Vector3(1, 2, 3), Vector3(4, 5, 6)),)],
        # ['intersects_plane', bool, (Plane(), )],  # TODO: wait for plane
        ["intersects_segment", bool, (Vector3(1, 2, 3), Vector3(4, 5, 6))],
        ["has_point", bool, (Vector3(1, 2, 3),)],
        ["get_support", Vector3, (Vector3(1, 2, 3),)],
        ["get_longest_axis", Vector3, ()],
        ["get_longest_axis_index", int, ()],
        ["get_longest_axis_size", float, ()],
        ["get_shortest_axis", Vector3, ()],
        ["get_shortest_axis_index", int, ()],
        ["get_shortest_axis_size", float, ()],
        ["expand", AABB, (Vector3(1, 2, 3),)],
        ["grow", AABB, (0.5,)],
        ["get_endpoint", Vector3, (0,)],
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = AABB()
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


@pytest.mark.parametrize(
    "field,ret_type", [("position", Vector3), ("size", Vector3)], ids=lambda x: x[0]
)
def test_properties(field, ret_type):
    v = AABB(Vector3(1, 2, 3), Vector3(4, 5, 6))
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert type(field_val) == ret_type
    for val in (Vector3(), Vector3(0.1, -0.1, 2)):
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert field_val == val


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
def test_bad_properties(field, bad_value):
    v = AABB()
    with pytest.raises(TypeError):
        setattr(v, field, bad_value)


def test_equal():
    arr = AABB(Vector3(1, 2, 3), Vector3(4, 5, 6))
    other = AABB(Vector3(1, 2, 3), Vector3(4, 5, 6))
    assert arr == other
    bad = AABB(Vector3(6, 5, 4), Vector3(3, 2, 1))
    assert not arr == bad  # Force use of __eq__


@pytest.mark.parametrize("arg", [None, 0, "foo", AABB(Vector3(6, 5, 4), Vector3(3, 2, 1))])
def test_bad_equal(arg):
    arr = AABB(Vector3(1, 2, 3), Vector3(4, 5, 6))
    assert arr != arg
