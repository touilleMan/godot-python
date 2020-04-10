import pytest

from godot import Basis, Quat, Vector3


def test_base():
    v = Quat()
    assert type(v) == Quat


@pytest.mark.parametrize(
    "field,args",
    [
        ["from_axis_angle", (Vector3.ONE, 1.1)],
        ["from_euler", (Vector3.ONE,)],
        ["from_basis", (Basis(),)],
    ],
)
def test_inits(field, args):
    build = getattr(Quat, field)
    v = build(*args)
    assert isinstance(v, Quat)


@pytest.mark.parametrize(
    "field,args",
    [
        ["from_axis_angle", (None, 1.1)],
        ["from_euler", (None,)],
        ["from_basis", (None,)],
        ["from_axis_angle", (Vector3.ONE, None)],
        ["from_axis_angle", (Vector3.ONE, "dummy")],
        ["from_axis_angle", ("dummy", 1.1)],
        ["from_euler", ("dummy",)],
        ["from_basis", ("dummy",)],
    ],
)
def test_bad_inits(field, args):
    build = getattr(Quat, field)
    with pytest.raises(TypeError):
        v = build(*args)


def test_repr():
    v = Quat(1.0, 2.0, 3.0, 4.0)
    assert repr(v) == "<Quat(x=1.0, y=2.0, z=3.0, w=4.0)>"


@pytest.mark.parametrize(
    "args",
    [
        [(), 0, 0, 0, 0],
        [(0.1, 0.2, 0.3, 0.4), 0.1, 0.2, 0.3, 0.4],
        [(1, 2, 3), 1, 2, 3, 0],
        [(1,), 1, 0, 0, 0],
    ],
)
def test_instantiate(args):
    # Can build it with int or float or nothing
    msg_tmpl = "%s vs (expected) %s (args=%s)"
    args, expected_x, expected_y, expected_z, expected_w = args
    v = Quat(*args)
    assert pytest.approx(v.x) == expected_x, msg_tmpl % (v.x, expected_x, args)
    assert pytest.approx(v.y) == expected_y, msg_tmpl % (v.y, expected_y, args)
    assert pytest.approx(v.z) == expected_z, msg_tmpl % (v.z, expected_z, args)
    assert pytest.approx(v.w) == expected_w, msg_tmpl % (v.w, expected_w, args)


def test_bad_instantiate():
    with pytest.raises(TypeError):
        Quat("a", 2, 3, 4)
    with pytest.raises(TypeError):
        Quat(1, "b", 2, 4)
    with pytest.raises(TypeError):
        Quat(1, 2, "c", 4)
    with pytest.raises(TypeError):
        Quat(1, 2, 3, "d")
    with pytest.raises(TypeError):
        Quat(None, 2, 3, 4)
    with pytest.raises(TypeError):
        Quat(1, None, 2, 4)
    with pytest.raises(TypeError):
        Quat(1, 2, None, 4)
    with pytest.raises(TypeError):
        Quat(1, 2, 3, None)


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["length", float, ()],
        ["length_squared", float, ()],
        ["normalized", Quat, ()],
        ["is_normalized", bool, ()],
        ["inverse", Quat, ()],
        ["dot", float, (Quat(),)],
        ["xform", Vector3, (Vector3(),)],
        ["slerp", Quat, (Quat(), 1.0)],
        ["slerpni", Quat, (Quat(), 1.0)],
        ["cubic_slerp", Quat, (Quat(), Quat(), Quat(), 1.0)],
        ["set_axis_angle", type(None), (Vector3(1, 2, 3), 3.3)],
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = Quat()
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


@pytest.mark.parametrize(
    "field,ret_type", [("x", float), ("y", float), ("z", float), ("w", float)], ids=lambda x: x[0]
)
def test_properties(field, ret_type):
    v = Quat()
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert type(field_val) == ret_type
    for val in (0, 10, 10.0, 42.5):
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert pytest.approx(field_val) == val


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("x", "NaN"),
        ("y", "NaN"),
        ("z", "NaN"),
        ("w", "NaN"),
        ("x", None),
        ("y", None),
        ("z", None),
        ("w", None),
    ],
    ids=lambda x: x[0],
)
def test_bad_properties(field, bad_value):
    v = Quat()
    with pytest.raises(TypeError):
        setattr(v, field, bad_value)


def test_unary():
    v = Quat(1, 2, 3, 4)
    v2 = -v
    assert v2.x == -1
    assert v2.y == -2
    assert v2.z == -3
    assert v2.w == -4
    v3 = +v
    assert v3.x == 1
    assert v3.y == 2
    assert v3.z == 3
    assert v3.w == 4
    v = Quat(1.5, 2.5, 3.5, 4.5)
    v2 = -v
    assert v2.x == -1.5
    assert v2.y == -2.5
    assert v2.z == -3.5
    assert v2.w == -4.5
    v3 = +v
    assert v3.x == 1.5
    assert v3.y == 2.5
    assert v2.z == -3.5
    assert v2.w == -4.5


@pytest.mark.parametrize(
    "param,result",
    [
        (Quat(0, 0, 0, 0), Quat(2, 3, 4, 5)),
        (Quat(4, 3, 2, 1), Quat(6, 6, 6, 6)),
        (Quat(-4, -3, -2, -1), Quat(-2, -0, 2, 4)),
    ],
    ids=lambda x: x[0],
)
def test_add(param, result):
    calc = Quat(2, 3, 4, 5) + param
    assert calc == result


@pytest.mark.parametrize(
    "param,result",
    [
        (Quat(0, 0, 0, 0), Quat(2, 3, 4, 5)),
        (Quat(5, 4, 3, 2), Quat(-3, -1, 1, 3)),
        (Quat(-1, -1, -1, -1), Quat(3, 4, 5, 6)),
    ],
    ids=lambda x: x[0],
)
def test_sub(param, result):
    calc = Quat(2, 3, 4, 5) - param
    assert calc == result


@pytest.mark.parametrize("arg", [None, 1, "dummy"], ids=lambda x: x[0])
def test_bad_add(arg):
    with pytest.raises(TypeError):
        Quat(2, 3, 4, 5) + arg


@pytest.mark.parametrize("arg", [None, 1, "dummy"], ids=lambda x: x[0])
def test_bad_sub(arg):
    with pytest.raises(TypeError):
        Quat(2, 3, 4, 5) - arg


@pytest.mark.parametrize("arg", [None, "dummy", Quat(1, 1, 1, 1)], ids=lambda x: x[0])
def test_bad_div(arg):
    with pytest.raises(TypeError):
        Quat(2, 3, 4, 5) / arg


def test_zero_div():
    with pytest.raises(ZeroDivisionError):
        Quat(2, 3, 4, 5) / 0


@pytest.mark.parametrize("arg", [None, "dummy"], ids=lambda x: x[0])
def test_bad_mul(arg):
    with pytest.raises(TypeError):
        Quat(2, 3, 4, 5) * arg


@pytest.mark.parametrize(
    "param,result",
    [(0, Quat(0, 0, 0, 0)), (1, Quat(2, 3, 4, 5)), (2.5, Quat(5, 7.5, 10, 12.5))],
    ids=lambda x: x[0],
)
def test_mul(param, result):
    calc = Quat(2, 3, 4, 5) * param
    assert calc == result


@pytest.mark.parametrize(
    "param,result",
    [(1, Quat(2, 3, 4, 5)), (0.5, Quat(4, 6, 8, 10)), (2, Quat(1, 1.5, 2, 2.5))],
    ids=lambda x: x[0],
)
def test_div(param, result):
    calc = Quat(2, 3, 4, 5) / param
    assert calc == result


def test_equal():
    arr = Quat(0.1, 1, 2, 3)
    other = Quat(0.1, 1, 2, 3)
    assert arr == other
    bad = Quat(0.1, 1, 2, 4)
    assert not arr == bad  # Force use of __eq__


@pytest.mark.parametrize("arg", [None, 0, "foo", Quat(0.1, 1, 2, 4)])
def test_bad_equal(arg):
    arr = Quat(0.1, 1, 2, 3)
    assert arr != arg
