import pytest

from godot.bindings import Vector2


class TestVector2:

    def test_base(self):
        v = Vector2()
        assert type(v) == Vector2
        v2 = Vector2(1, -2)
        assert type(v) == Vector2
        assert v2 == Vector2(1, -2)
        assert v != v2

    def test_repr(self):
        v = Vector2(1, 2)
        assert repr(v) == '<Vector2(x=1.0, y=2.0)>'

    def test_instanciate(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_x, expected_y in (
                [(), 0, 0],
                [(0.5, 0.5), 0.5, 0.5],
                [(1, 2), 1, 2],
                [(1,), 1, 0]):
            v = Vector2(*args)
            assert v.x == expected_x, msg_tmpl % (v.x, expected_x, args)
            assert v.y == expected_y, msg_tmpl % (v.y, expected_y, args)
            assert v.width == expected_x, msg_tmpl % (v.width, expected_y, args)
            assert v.height == expected_y, msg_tmpl % (v.height, expected_x, args)
        with pytest.raises(TypeError):
            Vector2("a", 2)
        with pytest.raises(TypeError):
            Vector2("a", 2)
        with pytest.raises(TypeError):
            Vector2(1, "b")
        with pytest.raises(TypeError):
            Vector2(None, 2)

    @pytest.mark.parametrize('args', [
        ['abs', Vector2, ()],
        ['angle', float, ()],
        ['angle_to', float, (Vector2(), )],
        ['angle_to_point', float, (Vector2(), )],
        ['clamped', Vector2, (0.5, )],
        ['cubic_interpolate', Vector2, (Vector2(), Vector2(), Vector2(), 0.5)],
        ['distance_squared_to', float, (Vector2(), )],
        ['distance_to', float, (Vector2(), )],
        ['dot', float, (Vector2(), )],
        ['floor', Vector2, ()],
        ['aspect', float, ()],
        ['length', float, ()],
        ['length_squared', float, ()],
        ['linear_interpolate', Vector2, (Vector2(), 0.5)],
        ['normalized', Vector2, ()],
        ['reflect', Vector2, (Vector2(), )],
        ['rotated', Vector2, (0.5, )],
        ['slide', Vector2, (Vector2(), )],
        ['snapped', Vector2, (Vector2(), )],
        ['tangent', Vector2, ()]
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Vector2()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    @pytest.mark.parametrize('args', [
        ('height', float),
        ('width', float),
        ('x', float),
        ('y', float),
    ], ids=lambda x: x[0])
    def test_properties(self, args):
        v = Vector2()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert type(field_val) == ret_type
        for val in (0, 10, 10., 42.5):
            setattr(v, field, val)
            field_val = getattr(v, field)
            assert field_val == val

    @pytest.mark.parametrize('args', [
        ('height', 'NaN'),
        ('width', 'NaN'),
        ('x', 'NaN'),
        ('y', 'NaN')
    ], ids=lambda x: x[0])
    def test_bad_properties(self, args):
        v = Vector2()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)

    def test_unary(self):
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
