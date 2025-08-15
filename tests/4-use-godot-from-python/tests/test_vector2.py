import clodotest

from godot import Vector2


@clodotest.xfail(reason="TODO")
def test_base():
    v = Vector2()
    assert type(v) == Vector2
    v2 = Vector2(1, -2)
    assert type(v) == Vector2
    assert v2 == Vector2(1, -2)
    assert v != v2


def test_repr():
    v = Vector2(1, 2)
    assert repr(v) == "Vector2(x=1.0, y=2.0)"


@clodotest.xfail(reason="TODO")
def test_instantiate():
    # Can build it with int or float or nothing
    msg_tmpl = "%s vs (expected) %s (args=%s)"
    for args, expected_x, expected_y in (
        [(), 0, 0],
        [(0.5, 0.5), 0.5, 0.5],
        [(1, 2), 1, 2],
        [(1,), 1, 0],
    ):
        v = Vector2(*args)
        assert v.x == expected_x, msg_tmpl % (v.x, expected_x, args)
        assert v.y == expected_y, msg_tmpl % (v.y, expected_y, args)
        assert v.width == expected_x, msg_tmpl % (v.width, expected_y, args)
        assert v.height == expected_y, msg_tmpl % (v.height, expected_x, args)
    with clodotest.raises(TypeError):
        Vector2("a", 2)
    with clodotest.raises(TypeError):
        Vector2("a", 2)
    with clodotest.raises(TypeError):
        Vector2(1, "b")
    with clodotest.raises(TypeError):
        Vector2(None, 2)


@clodotest.parametrize(
    "field,ret_type,params",
    [
        ("abs", Vector2, ()),
        ("angle", float, ()),
        ("angle_to", float, (Vector2(),)),
        ("angle_to_point", float, (Vector2(),)),
        # ("clamped", Vector2, (0.5,)),  # TODO: missing field ?
        ("cubic_interpolate", Vector2, (Vector2(), Vector2(), Vector2(), 0.5)),
        ("distance_squared_to", float, (Vector2(),)),
        ("distance_to", float, (Vector2(),)),
        ("dot", float, (Vector2(),)),
        ("floor", Vector2, ()),
        ("aspect", float, ()),
        ("length", float, ()),
        ("length_squared", float, ()),
        # ("linear_interpolate", Vector2, (Vector2(), 0.5)),  # TODO: missing field ?
        ("normalized", Vector2, ()),
        # ("reflect", Vector2, (Vector2(),)),  # TODO: cause a "ERROR: The normal Vector2 (0.0, 0.0)must be normalized." log
        ("rotated", Vector2, (0.5,)),
        # ("slide", Vector2, (Vector2(),)),  # TODO: cause a "ERROR: The normal Vector2 (0.0, 0.0)must be normalized." log
        ("snapped", Vector2, (Vector2(),)),
        # ("tangent", Vector2, ()),  # TODO: missing field ?
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = Vector2()
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


@clodotest.parametrize(
    "field,ret_type",
    [
        # ("height", float),  # TODO: missing field ?
        # ("width", float),  # TODO: missing field ?
        ("x", float),
        ("y", float),
    ],
    ids=lambda x: x[0],
)
def test_properties(field, ret_type):
    v = Vector2()
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert type(field_val) == ret_type
    for val in (0, 10, 10.0, 42.5):
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert field_val == val


@clodotest.parametrize(
    "field,bad_value",
    [
        # ("height", "NaN"),  # TODO: missing field ?
        # ("width", "NaN"),  # TODO: missing field ?
        ("x", "NaN"),
        ("y", "NaN"),
        # ("height", None),  # TODO: missing field ?
        # ("width", None),  # TODO: missing field ?
        ("x", None),
        ("y", None),
    ],
    ids=lambda x: x[0],
)
def test_bad_properties(field, bad_value):
    v = Vector2()
    with clodotest.raises(TypeError):
        setattr(v, field, bad_value)


@clodotest.xfail(reason="TODO")
def test_unary():
    v = Vector2(1, 2)
    v2 = -v
    assert v2.x == -1
    assert v2.y == -2
    v3 = +v
    assert v3.x == 1
    assert v3.y == 2
    v = Vector2(1.5, 2.5)
    v2 = -v
    assert v2.x == -1.5
    assert v2.y == -2.5
    v3 = +v
    assert v3.x == 1.5
    assert v3.y == 2.5


@clodotest.xfail(reason="TODO")
@clodotest.parametrize(
    "param,result",
    [
        (Vector2(0, 0), Vector2(2, 3)),
        (Vector2(3, 2), Vector2(5, 5)),
        (Vector2(-1, -4), Vector2(1, -1)),
    ],
    ids=lambda x: x[0],
)
def test_add(param, result):
    calc = Vector2(2, 3) + param
    assert calc == result


@clodotest.xfail(reason="TODO")
@clodotest.parametrize(
    "param,result",
    [
        (Vector2(0, 0), Vector2(2, 3)),
        (Vector2(3, 2), Vector2(-1, 1)),
        (Vector2(-1, -1), Vector2(3, 4)),
    ],
    ids=lambda x: x[0],
)
def test_sub(param, result):
    calc = Vector2(2, 3) - param
    assert calc == result


@clodotest.xfail(reason="TODO")
@clodotest.parametrize("arg", [None, 1, "dummy"])
def test_bad_add(arg):
    with clodotest.raises(TypeError):
        Vector2(2, 3) + arg  # type: ignore


@clodotest.parametrize("arg", [None, 1, "dummy"])
def test_bad_sub(arg):
    with clodotest.raises(TypeError):
        Vector2(2, 3) - arg  # type: ignore


@clodotest.parametrize("arg", [None, "dummy"])
def test_bad_div(arg):
    with clodotest.raises(TypeError):
        Vector2(2, 3) / arg  # type: ignore


@clodotest.xfail(reason="TODO")
@clodotest.parametrize("arg", [0, Vector2(0, 1), Vector2(1, 0), Vector2(0, 0)])
def test_zero_div(arg):
    with clodotest.raises(ZeroDivisionError):
        Vector2(2, 3) / arg  # type: ignore


@clodotest.parametrize("arg", [None, "dummy"])
def test_bad_mult(arg):
    with clodotest.raises(TypeError):
        Vector2(2, 3) * arg  # type: ignore


@clodotest.xfail(reason="TODO")
@clodotest.parametrize(
    "param,result",
    [
        (0, Vector2(0, 0)),
        (1, Vector2(2, 3)),
        (2.5, Vector2(5, 7.5)),
        (Vector2(1, 1), Vector2(2, 3)),
        (Vector2(2, 3), Vector2(4, 9)),
    ],
    ids=lambda x: x[0],
)
def test_mult(param, result):
    calc = Vector2(2, 3) * param
    assert calc == result


@clodotest.xfail(reason="TODO")
@clodotest.parametrize(
    "param,result",
    [
        (1, Vector2(2, 3)),
        (0.5, Vector2(4, 6)),
        (2, Vector2(1, 1.5)),
        (Vector2(1, 1), Vector2(2, 3)),
        (Vector2(2, 3), Vector2(1, 1)),
    ],
    ids=lambda x: x[0],
)
def test_div(param, result):
    calc = Vector2(2, 3) / param
    assert calc == result


@clodotest.xfail(reason="TODO")
def test_equal():
    arr = Vector2(1, 2)
    other = Vector2(1, 2)
    assert arr == other
    bad = Vector2(1, 3)
    assert not arr == bad  # Force use of __eq__


@clodotest.parametrize("arg", [None, 0, "foo", Vector2(1, 3)])
def test_bad_equal(arg):
    arr = Vector2(1, 2)
    assert arr != arg


@clodotest.xfail(reason="TODO")
@clodotest.parametrize(
    "field,type",
    [
        ("AXIS_X", int),
        ("AXIS_Y", int),
        ("ZERO", Vector2),
        ("ONE", Vector2),
        ("INF", Vector2),
        ("LEFT", Vector2),
        ("RIGHT", Vector2),
        ("UP", Vector2),
        ("DOWN", Vector2),
    ],
    ids=lambda x: x[0],
)
def test_contants(field, type):
    field_val = getattr(Vector2, field)
    assert isinstance(field_val, type)
