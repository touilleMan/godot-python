import pytest

from godot import Vector3, Plane


def test_init():
    v = Plane(1, 2, 3, 4)
    assert type(v) == Plane
    assert v.normal == Vector3(1, 2, 3)
    assert v.d == 4


@pytest.mark.parametrize(
    "args",
    [
        ("NaN", 2.2, 3.3, 4.4),
        (1.1, "NaN", 3.3, 4.4),
        (1.1, 2.2, "NaN", 4.4),
        (1.1, 2.2, 3.3, "NaN"),
        (None, 2.2, 3.3, 4.4),
        (1.1, None, 3.3, 4.4),
        (1.1, 2.2, None, 4.4),
        (1.1, 2.2, 3.3, None),
    ],
)
def test_bad_init(args):
    with pytest.raises(TypeError):
        Plane(*args)


@pytest.mark.parametrize(
    "expected_normal,expected_d", [(Vector3(0, 0, 0), 0), (Vector3(1, 2, 3), 1)]
)
def test_init_from_normal(expected_normal, expected_d):
    v = Plane.from_normal(expected_normal, expected_d)
    assert v.normal == expected_normal, msg_tmpl % (v.normal, expected_normal)
    assert v.d == expected_d, msg_tmpl % (v.d, expected_d)


@pytest.mark.parametrize(
    "bad_normal,bad_d",
    [("dummy", 0), (None, 0), (Vector3(1, 2, 3), "NaN"), (Vector3(1, 2, 3), None)],
)
def test_bad_init_from_normal(bad_normal, bad_d):
    with pytest.raises(TypeError):
        Plane.from_normal(bad_normal, bad_d)


def test_init_from_vectors():
    v = Plane.from_vectors(Vector3(), Vector3(), Vector3())
    assert v.normal == Vector3()
    assert v.d == 0


@pytest.mark.parametrize(
    "bad_v1,bad_v2,bad_v3",
    [
        ("dummy", Vector3(4, 5, 6), Vector3(7, 8, 9)),
        (Vector3(1, 2, 3), "dummy", Vector3(7, 8, 9)),
        (Vector3(1, 2, 3), Vector3(4, 5, 6), "dummy"),
        (None, Vector3(4, 5, 6), Vector3(7, 8, 9)),
        (Vector3(1, 2, 3), None, Vector3(7, 8, 9)),
        (Vector3(1, 2, 3), Vector3(4, 5, 6), None),
    ],
)
def test_bad_init_from_vectors(bad_v1, bad_v2, bad_v3):
    with pytest.raises(TypeError):
        Plane.from_vectors(bad_v1, bad_v2, bad_v3)


def test_repr():
    v = Plane(1, 2, 3, 4)
    assert repr(v) == "<Plane(1, 2, 3, 4)>"


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["normalized", Plane, ()],
        ["center", Vector3, ()],
        ["get_any_point", Vector3, ()],
        ["is_point_over", bool, (Vector3(),)],
        ["distance_to", float, (Vector3(),)],
        ["has_point", bool, (Vector3(), 0.5)],
        ["project", Vector3, (Vector3(),)],
        ["intersect_3", Vector3, (Plane.PLANE_XZ, Plane.PLANE_XY)],
        ["intersects_ray", Vector3, (Vector3(1, 0, 0), Vector3(-1, 0, 0))],
        ["intersects_segment", Vector3, (Vector3(1, 0, 0), Vector3(-1, 0, 0))],
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = Plane.PLANE_YZ
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


@pytest.mark.parametrize(
    "field,params",
    [
        ["is_point_over", (None,)],
        ["distance_to", (None,)],
        ["has_point", (None, 0.5)],
        ["project", (None,)],
        ["intersect_3", (None, Plane(1, 1, 1, 1))],
        ["intersect_3", (Plane(1, 1, 1, 1), None)],
        ["intersects_ray", (None, Vector3())],
        ["intersects_ray", (Vector3(), None)],
        ["intersects_segment", (None, Vector3())],
        ["intersects_segment", (Vector3(), None)],
    ],
    ids=lambda x: x[0],
)
def test_methods_call_with_none(field, params):
    v = Plane(1, 2, 3, 4)
    method = getattr(v, field)
    with pytest.raises(TypeError):
        method(*params)


def test_property_d():
    v = Plane(1, 2, 3, 4)
    assert hasattr(v, "d")
    field_val = v.d
    assert isinstance(field_val, (float, int))
    for val in (0.5, -1, 2):
        v.d = val
        field_val = v.d
        assert field_val == val
    for bad in ("dummy", None, b"b"):
        with pytest.raises(TypeError):
            v.d = bad


def test_property_normal():
    v = Plane(1, 2, 3, 4)
    assert hasattr(v, "normal")
    field_val = v.normal
    assert isinstance(field_val, Vector3)
    for val in (Vector3(), Vector3(0.1, -0.1, 2)):
        v.normal = val
        field_val = v.normal
        assert field_val == val
    for bad in ("dummy", None, b"b"):
        with pytest.raises(TypeError):
            v.normal = bad


def test_equal():
    arr = Plane(1, 2, 3, 4)
    same = Plane(1, 2, 3, 4)
    assert arr == same  # Force use of __eq__
    assert not arr != same  # Force use of __ne__


@pytest.mark.parametrize("bad", [None, 0, "foo", Plane(1, 2, 3, 5)])
def test_not_equal(bad):
    arr = Plane(1, 2, 3, 4)
    assert not arr == bad  # Force use of __eq__
    assert arr != bad  # Force use of __ne__
