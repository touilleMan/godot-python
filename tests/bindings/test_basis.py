import pytest

from godot import Basis, Vector3, Quat


def test_default():
    v = Basis()
    assert isinstance(v, Basis)
    assert v.x == Vector3(1, 0, 0)
    assert v.y == Vector3(0, 1, 0)
    assert v.z == Vector3(0, 0, 1)


def test_init_from_rows():
    v = Basis(Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
    assert isinstance(v, Basis)
    assert (v.x, v.y, v.z) == (Vector3(1, 4, 7), Vector3(2, 5, 8), Vector3(3, 6, 9))


@pytest.mark.parametrize(
    "args",
    [
        (0, Vector3.ONE, Vector3.ONE),
        (None, Vector3.ONE, Vector3.ONE),
        (Vector3.ONE, 0, Vector3.ONE),
        (Vector3.ONE, None, Vector3.ONE),
        (Vector3.ONE, Vector3.ONE, 0),
        (Vector3.ONE, Vector3.ONE, None),
    ],
)
def test_bad_init_from_rows(args):
    with pytest.raises(TypeError):
        Basis(*args)


@pytest.mark.parametrize(
    "field,args",
    [
        ["from_axis_angle", (Vector3.ONE, 1.1)],
        ["from_euler", (Vector3.ONE,)],
        ["from_euler", (Quat(),)],
    ],
)
def test_inits(field, args):
    build = getattr(Basis, field)
    v = build(*args)
    assert isinstance(v, Basis)


@pytest.mark.parametrize(
    "field,args",
    [
        ["from_axis_angle", (None, 1.1)],
        ["from_euler", (None,)],
        ["from_axis_angle", (Vector3.ONE, None)],
        ["from_axis_angle", (Vector3.ONE, "dummy")],
        ["from_axis_angle", ("dummy", 1.1)],
        ["from_euler", ("dummy",)],
    ],
)
def test_bad_inits(field, args):
    build = getattr(Basis, field)
    with pytest.raises(TypeError):
        v = build(*args)


def test_equal():
    basis1 = Basis.from_euler(Vector3(1, 2, 3))
    basis2 = Basis.from_euler(Vector3(1, 2, 3))
    assert basis1 == basis2
    basis2.x = Vector3(1, 2, 3)
    assert basis1 != basis2
    basis1.x = Vector3(1, 2, 3)
    assert basis1 == basis2
    bad = Basis.from_euler(Vector3(1, 2, 4))
    assert not basis1 == bad  # Force use of __eq__


@pytest.mark.parametrize("arg", [None, 0, "foo", Basis.from_euler(Vector3(1, 2, 4))])
def test_bad_equal(arg):
    basis = Basis.from_euler(Vector3(1, 2, 3))
    assert basis != arg


def test_repr():
    v = Basis(Vector3(1, 2, 3), Vector3(4, 5, 6), Vector3(7, 8, 9))
    assert repr(v) == "<Basis(1, 2, 3, 4, 5, 6, 7, 8, 9)>"


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["inverse", Basis, ()],
        ["transposed", Basis, ()],
        ["orthonormalized", Basis, ()],
        ["determinant", float, ()],
        ["rotated", Basis, (Vector3(), 0.5)],
        ["scaled", Basis, (Vector3(),)],
        ["get_scale", Vector3, ()],
        ["get_euler", Vector3, ()],
        ["get_quat", Quat, ()],
        ["set_quat", type(None), (Quat(),)],
        ["set_axis_angle_scale", type(None), (Vector3.ONE, 1.1, Vector3.ONE)],
        ["set_euler_scale", type(None), (Vector3.ONE, Vector3.ONE)],
        ["set_quat_scale", type(None), (Quat(), Vector3.ONE)],
        ["tdotx", float, (Vector3(),)],
        ["tdoty", float, (Vector3(),)],
        ["tdotz", float, (Vector3(),)],
        ["xform", Vector3, (Vector3(),)],
        ["xform_inv", Vector3, (Vector3(),)],
        ["get_orthogonal_index", int, ()],
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = Basis()
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert isinstance(ret, ret_type)


@pytest.mark.parametrize(
    "field,ret_type", [("x", Vector3), ("y", Vector3), ("z", Vector3)], ids=lambda x: x[0]
)
def test_properties(field, ret_type):
    v = Basis()
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert isinstance(field_val, ret_type)
    val = Vector3(1, 2, 3)
    setattr(v, field, val)
    field_val = getattr(v, field)
    assert field_val == val


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("x", "Not a Vector3"),
        ("y", "Not a Vector3"),
        ("z", "Not a Vector3"),
        ("x", 1),
        ("y", 2),
        ("z", 3),
        ("x", None),
        ("y", None),
        ("z", None),
    ],
    ids=lambda x: x[0],
)
def test_bad_properties(field, bad_value):
    v = Basis()
    with pytest.raises(TypeError):
        setattr(v, field, bad_value)
