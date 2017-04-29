import pytest

from godot.bindings import Rect2, Vector2


class TestRect2:

    def test_base(self):
        v = Rect2(4, 3, 2, 1)
        assert type(v) == Rect2
        v2 = Rect2(1, 2, 3, 4)
        assert type(v) == Rect2
        assert v2 == Rect2(1, 2, 3, 4)
        assert v != v2

    def test_repr(self):
        v = Rect2(1, 2)
        assert repr(v) == '<Rect2(1, 2, 0, 0)>'

    def test_instantiate(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_pos, expected_size in (
                [(), Vector2(0, 0), Vector2(0, 0)],
                [(0.5, 0.5), Vector2(0.5, 0.5), Vector2(0, 0)],
                [(1, 2, 1, 2), Vector2(1, 2), Vector2(1, 2)]):
            v = Rect2(*args)
            assert v.pos == expected_pos, msg_tmpl % (v.x, expected_pos, args)
            assert v.size == expected_size, msg_tmpl % (v.y, expected_size, args)
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

    @pytest.mark.parametrize('args', [
        ['clip', Rect2, (Rect2(), )],
        ['encloses', bool, (Rect2(), )],
        ['expand', Rect2, (Vector2(), )],
        ['get_area', float, ()],
        ['grow', Rect2, (0.5, )],
        ['has_no_area', bool, ()],
        ['has_point', bool, (Vector2(), )],
        ['intersects', bool, (Rect2(), )],
        ['merge', Rect2, (Rect2(), )],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Rect2()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    @pytest.mark.parametrize('args', [
        ('pos', Vector2),
        ('size', Vector2),
    ], ids=lambda x: x[0])
    def test_properties(self, args):
        v = Rect2()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert type(field_val) == ret_type
        for val in (Vector2(), Vector2(0.1, -0.1)):
            setattr(v, field, val)
            field_val = getattr(v, field)
            assert field_val == val

    @pytest.mark.parametrize('args', [
        ('pos', 'dummy'),
        ('size', 'dummy'),
        ('pos', None),
        ('size', None),
        ('pos', 42),
        ('size', 42),
    ], ids=lambda x: x[0])
    def test_bad_properties(self, args):
        v = Rect2()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)
