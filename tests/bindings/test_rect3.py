import pytest

from godot.bindings import Rect3, Vector3, Plane


class TestRect3:

    def test_base(self):
        v = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6))
        assert type(v) == Rect3
        v2 = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 7))
        assert type(v) == Rect3
        assert v2 == Rect3(Vector3(1, 2, 3), Vector3(4, 5, 7))
        assert v != v2

    def test_repr(self):
        v = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6))
        assert repr(v) == '<Rect3(pos=<Vector3(x=1.0, y=2.0, z=3.0)>, size=<Vector3(x=4.0, y=5.0, z=6.0)>)>'

    def test_instantiate(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_pos, expected_size in (
                [(), Vector3(0, 0, 0), Vector3(0, 0, 0)],
                [(Vector3(0, 1, 0), Vector3(0, 0, 1)), Vector3(0, 1, 0), Vector3(0, 0, 1)],
                ):
            v = Rect3(*args)
            assert v.pos == expected_pos, msg_tmpl % (v.pos, expected_pos, args)
            assert v.size == expected_size, msg_tmpl % (v.size, expected_size, args)
        with pytest.raises(TypeError):
            Rect3("a", Vector3())
        with pytest.raises(TypeError):
            Rect3(Vector3(), "b")

    @pytest.mark.parametrize('args', [
        ['get_area', float, ()],
        ['has_no_area', bool, ()],
        ['has_no_surface', bool, ()],
        ['intersects', bool, (Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6)), )],
        ['encloses', bool, (Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6)), )],
        ['merge', Rect3, (Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6)), )],
        ['intersection', Rect3, (Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6)), )],
        # ['intersects_plane', bool, (Plane(), )],  # TODO: wait for plane
        ['intersects_segment', bool, (Vector3(1, 2, 3), Vector3(4, 5, 6))],
        ['has_point', bool, (Vector3(1, 2, 3), )],
        ['get_support', Vector3, (Vector3(1, 2, 3), )],
        ['get_longest_axis', Vector3, ()],
        ['get_longest_axis_index', int, ()],
        ['get_longest_axis_size', float, ()],
        ['get_shortest_axis', Vector3, ()],
        ['get_shortest_axis_index', int, ()],
        ['get_shortest_axis_size', float, ()],
        ['expand', Rect3, (Vector3(1, 2, 3), )],
        ['grow', Rect3, (0.5, )],
        ['get_endpoint', Vector3, (0, )],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Rect3()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    @pytest.mark.parametrize('args', [
        ('pos', Vector3),
        ('size', Vector3),
    ], ids=lambda x: x[0])
    def test_properties(self, args):
        v = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6))
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert type(field_val) == ret_type
        for val in (Vector3(), Vector3(0.1, -0.1, 2)):
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
        v = Rect3()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)

    def test_equal(self):
        arr = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6))
        other = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6))
        assert arr == other
        bad = Rect3(Vector3(6, 5, 4), Vector3(3, 2, 1))
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Rect3(Vector3(6, 5, 4), Vector3(3, 2, 1))
    ])
    def test_bad_equal(self, arg):
        arr = Rect3(Vector3(1, 2, 3), Vector3(4, 5, 6))
        assert arr != arg
