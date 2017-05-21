import pytest

from godot.bindings import Plane, Vector3, Plane


class TestPlane:

    def test_base(self):
        v = Plane(Vector3(1, 2, 3), 0.5)
        assert type(v) == Plane
        v2 = Plane(Vector3(1, 2, 3), 1)
        assert type(v) == Plane
        assert v2 == Plane(Vector3(1, 2, 3), 1)
        assert v != v2

    def test_repr(self):
        v = Plane(Vector3(1, 2, 3), 0.5)
        assert repr(v) == '<Plane(normal=<Vector3(x=1.0, y=2.0, z=3.0)>, d=0.5)>'

    def test_instantiate(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s"
        for expected_normal, expected_d in (
                [Vector3(0, 0, 0), 0],
                [Vector3(1, 2, 3), 1],
                ):
            v = Plane(expected_normal, expected_d)
            assert v.normal == expected_normal, msg_tmpl % (v.normal, expected_normal)
            assert v.d == expected_d, msg_tmpl % (v.d, expected_d)
        with pytest.raises(TypeError):
            Plane("a", 1)
        with pytest.raises(TypeError):
            Plane(Vector3(), "b")

    def test_build_from_reals(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_normal, expected_d in (
                [(), Vector3(0, 0, 0), 0],
                [(1, 2, 3, 4), Vector3(1, 2, 3), 4],
                ):
            v = Plane.build_from_reals(*args)
            assert v.normal == expected_normal, msg_tmpl % (v.normal, expected_normal, args)
            assert v.d == expected_d, msg_tmpl % (v.d, expected_d, args)
        with pytest.raises(TypeError):
            Plane.build_from_reals("a", 2, 3, 4)
        with pytest.raises(TypeError):
            Plane.build_from_reals(1, "b", 3, 4)
        with pytest.raises(TypeError):
            Plane.build_from_reals(1, 2, "c", 4)
        with pytest.raises(TypeError):
            Plane.build_from_reals(1, 2, 3, "d")

    def test_build_from_vectors(self):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        for args, expected_normal, expected_d in (
                [(), (0, 0, 0), 0],
                [(Vector3(0, 0, 0), Vector3(4, 5, 6), Vector3(7, 8, 9)), (0.40824827551841736, -0.8164965510368347, 0.40824827551841736), 0.0],
                ):
            v = Plane.build_from_vectors(*args)
            normal = (pytest.approx(v.normal.x), pytest.approx(v.normal.y), pytest.approx(v.normal.z))
            assert normal == expected_normal, msg_tmpl % (v.normal, expected_normal, args)
            assert v.d == expected_d, msg_tmpl % (v.d, expected_d, args)
        with pytest.raises(TypeError):
            Plane.build_from_vectors("a", Vector3(4, 5, 6), Vector3(7, 8, 9))
        with pytest.raises(TypeError):
            Plane.build_from_vectors(Vector3(1, 2, 3), "b", Vector3(7, 8, 9))
        with pytest.raises(TypeError):
            Plane.build_from_vectors(Vector3(1, 2, 3), Vector3(4, 5, 6), "c")

    @pytest.mark.parametrize('args', [
        ['normalized', Plane, ()],
        ['center', Vector3, ()],
        ['get_any_point', Vector3, ()],
        ['is_point_over', bool, (Vector3(), )],
        ['distance_to', float, (Vector3(), )],
        ['has_point', bool, (Vector3(), 0.5)],
        ['project', Vector3, (Vector3(), )],
        # ['intersect_3', Vector3, (Plane(1, 1, 1, 1), Plane(1, 1, 1, 1))],  # TODO: think about values...
        # ['intersects_ray', Vector3, (Vector3(), Vector3())],  # TODO: think about values...
        # ['intersects_segment', Vector3, (Vector3(), Vector3())],  # TODO: think about values...
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Plane(Vector3(1, 1, 1), 1)
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    def test_property_d(self):
        v = Plane(Vector3(1, 2, 3), 4)
        assert hasattr(v, 'd')
        field_val = v.d
        assert isinstance(field_val, (float, int))
        for val in (0.5, -1, 2):
            v.d = val
            field_val = v.d
            assert field_val == val
        for bad in ('dummy', None, b'b'):
            with pytest.raises(TypeError):
                v.d = bad

    def test_property_normal(self):
        v = Plane(Vector3(1, 2, 3), 4)
        assert hasattr(v, 'normal')
        field_val = v.normal
        assert isinstance(field_val, Vector3)
        for val in (Vector3(), Vector3(0.1, -0.1, 2)):
            v.normal = val
            field_val = v.normal
            assert field_val == val
        for bad in ('dummy', None, b'b'):
            with pytest.raises(TypeError):
                v.normal = bad

    def test_equal(self):
        arr = Plane(Vector3(1, 2, 3), 4)
        other = Plane(Vector3(1, 2, 3), 4)
        assert arr == other
        bad = Plane(Vector3(1, 2, 3), 5)
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Plane(Vector3(1, 2, 3), 5),
    ])
    def test_bad_equal(self, arg):
        arr = Plane(Vector3(1, 2, 3), 4)
        assert arr != arg
