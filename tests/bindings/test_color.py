import pytest

from godot.bindings import Color, Vector2, Node


class TestColor:

    def test_base(self):
        v = Color()
        assert type(v) == Color

    @pytest.mark.parametrize('arg', [
        (),
        (0xFF,),
        (0xFF, 0x77),
        (0xFF, 0x77, 0x33),
        (0xFF, 0x77, 0x33, 0x11),
        {'r': 0xFF, 'g': 0x77, 'b': 0x33, 'a': 0x11},
    ])
    def test_initialize(self, arg):
        if isinstance(arg, dict):
            v1 = Color(**arg)
            v2 = Color(**arg)
        else:
            v1 = Color(*arg)
            v2 = Color(*arg)
        assert v1 == v2

    def test_equal(self):
        v1 = Color()
        v2 = Color()
        assert v1 == v2
        vrgba = Color(1, 2, 3, 4)
        vrgb = Color(1, 2, 3)
        assert not vrgb == vrgba  # Force use of __eq__

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Color(1, 2, 3, 5),
    ])
    def test_bad_equal(self, arg):
        basis = Color(1, 2, 3, 4)
        assert basis != arg

    def test_repr(self):
        v = Color()
        assert repr(v) == '<Color(r=0.0, g=0.0, b=0.0, a=1.0)>'

    @pytest.mark.parametrize('arg', [
        (None, ),
        (1, None),
        (1, 2, None),
        ('dummy', ),
        (Node(), ),
        (Vector2(), )
    ])
    def test_bad_instantiate(self, arg):
        with pytest.raises(TypeError):
            Color(*arg)

    @pytest.mark.parametrize('args', [
        ['to_32', int, ()],
        ['to_ARGB32', int, ()],
        ['gray', float, ()],
        ['inverted', Color, ()],
        ['contrasted', Color, ()],
        ['linear_interpolate', Color, (Color(0xAA, 0xBB, 0xCC), 2.2)],
        ['blend', Color, (Color(0xAA, 0xBB, 0xCC), )],
        ['to_html', str, (True, )],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Color()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    @pytest.mark.parametrize('arg', [
        (Color(0, 0, 0), Color(1, 0, 0)),
        (Color(0, 1, 0), Color(1, 0, 0)),
        (Color(1, 0, 0), Color(1, 0, 1)),
    ], ids=lambda x: x[0])
    def test_lt(self, arg):
        small, big = arg
        assert small < big

    @pytest.mark.parametrize('args', [
        ('r', float),
        ('r8', int),
        ('g', float),
        ('g8', int),
        ('b', float),
        ('b8', int),
        ('a', float),
        ('a8', int),
    ], ids=lambda x: x[0])
    def test_properties_rw(self, args):
        v = Color()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert type(field_val) == ret_type
        if ret_type is float:
            vals = (0, 10, 10., 42.5)
        else:
            vals = (0, 10, 0xFF)
        for val in vals:
            setattr(v, field, val)
            field_val = getattr(v, field)
            assert field_val == val

    @pytest.mark.parametrize('args', [
        ('h', float),
        ('s', float),
        ('v', float),
    ], ids=lambda x: x[0])
    def test_properties_ro(self, args):
        v = Color(4.2)
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert type(field_val) == ret_type
        with pytest.raises(AttributeError):
            setattr(v, field, 0.5)

    @pytest.mark.parametrize('args', [
        ('r', 'Nan'),
        ('r8', 'Nan'),
        ('g', 'Nan'),
        ('g8', 'Nan'),
        ('b', 'Nan'),
        ('b8', 'Nan'),
        ('a', 'Nan'),
        ('a8', 'Nan'),
    ], ids=lambda x: x[0])
    def test_bad_properties(self, args):
        v = Color()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)
