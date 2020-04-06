import pytest

from godot import Color, Vector2, GDString, Node

from conftest import generate_global_obj


NODE = generate_global_obj(Node)


def test_base():
    v = Color()
    assert type(v) == Color


@pytest.mark.parametrize(
    "arg",
    [
        (),
        (0xFF,),
        (0xFF, 0x77),
        (0xFF, 0x77, 0x33),
        (0xFF, 0x77, 0x33, 0x11),
        {"r": 0xFF, "g": 0x77, "b": 0x33, "a": 0x11},
    ],
)
def test_initialize(arg):
    if isinstance(arg, dict):
        v1 = Color(**arg)
        v2 = Color(**arg)
    else:
        v1 = Color(*arg)
        v2 = Color(*arg)
    assert v1 == v2


def test_equal():
    v1 = Color()
    v2 = Color()
    assert v1 == v2
    vrgba = Color(1, 2, 3, 4)
    vrgb = Color(1, 2, 3)
    assert not vrgb == vrgba  # Force use of __eq__


@pytest.mark.parametrize("arg", [None, 0, "foo", Color(1, 2, 3, 5)])
def test_bad_equal(arg):
    basis = Color(1, 2, 3, 4)
    assert basis != arg


def test_repr():
    v = Color()
    assert repr(v) == "<Color(r=0.0, g=0.0, b=0.0, a=1.0)>"


@pytest.mark.parametrize(
    "arg", [(None,), (1, None), (1, 2, None), ("dummy",), (NODE,), (Vector2(),)]
)
def test_bad_instantiate(arg):
    with pytest.raises(TypeError):
        Color(*arg)


@pytest.mark.parametrize(
    "field,ret_type,params",
    [
        ["to_rgba32", int, ()],
        ["to_abgr32", int, ()],
        ["to_abgr64", int, ()],
        ["to_argb64", int, ()],
        ["to_rgba64", int, ()],
        ["to_argb32", int, ()],
        ["gray", float, ()],
        ["inverted", Color, ()],
        ["contrasted", Color, ()],
        ["linear_interpolate", Color, (Color(0xAA, 0xBB, 0xCC), 2.2)],
        ["blend", Color, (Color(0xAA, 0xBB, 0xCC),)],
        ["darkened", Color, (2.2,)],
        ["from_hsv", Color, (1.1, 2.2, 3.3, 4.4)],
        ["lightened", Color, (2.2,)],
        ["to_html", GDString, (True,)],
    ],
    ids=lambda x: x[0],
)
def test_methods(field, ret_type, params):
    v = Color()
    # Don't test methods' validity but bindings one
    assert hasattr(v, field)
    method = getattr(v, field)
    assert callable(method)
    ret = method(*params)
    assert type(ret) == ret_type


@pytest.mark.parametrize(
    "small,big",
    [
        (Color(0, 0, 0), Color(1, 0, 0)),
        (Color(0, 1, 0), Color(1, 0, 0)),
        (Color(1, 0, 0), Color(1, 0, 1)),
    ],
    ids=lambda x: x[0],
)
def test_lt(small, big):
    assert small < big


@pytest.mark.parametrize(
    "field,ret_type",
    [
        ("r", float),
        ("r8", int),
        ("g", float),
        ("g8", int),
        ("b", float),
        ("b8", int),
        ("a", float),
        ("a8", int),
    ],
    ids=lambda x: x[0],
)
def test_properties_rw(field, ret_type):
    v = Color()
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert type(field_val) == ret_type
    if ret_type is float:
        vals = (0, 10, 10.0, 42.5)
    else:
        vals = (0, 10, 0xFF)
    for val in vals:
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert field_val == val


@pytest.mark.parametrize("args", [("h", float), ("s", float), ("v", float)], ids=lambda x: x[0])
def test_properties_ro(args):
    v = Color(4.2)
    field, ret_type = args
    assert hasattr(v, field)
    field_val = getattr(v, field)
    assert type(field_val) == ret_type
    with pytest.raises(AttributeError):
        setattr(v, field, 0.5)


@pytest.mark.parametrize(
    "args",
    [
        ("r", "Nan"),
        ("r8", "Nan"),
        ("g", "Nan"),
        ("g8", "Nan"),
        ("b", "Nan"),
        ("b8", "Nan"),
        ("a", "Nan"),
        ("a8", "Nan"),
        ("r", None),
        ("r8", None),
        ("g", None),
        ("g8", None),
        ("b", None),
        ("b8", None),
        ("a", None),
        ("a8", None),
    ],
    ids=lambda x: x[0],
)
def test_bad_properties(args):
    v = Color()
    field, bad_value = args
    with pytest.raises(TypeError):
        setattr(v, field, bad_value)


def test_constants():
    assert isinstance(Color.LEMONCHIFFON, Color)
    # I don't have a single clue what those colors are...
    assert Color.LEMONCHIFFON != Color.MEDIUMSPRINGGREEN
