import pytest

from godot.bindings import Vector3


class TestVector3:

    def test_base(self):
        v = Vector3()
        assert isinstance(v, Vector3)
        v2 = Vector3(1, -2, 5)
        assert isinstance(v2, Vector3)
        assert v2 == Vector3(1, -2, 5)
        assert v != v2

    def test_instanciate(self):
        # Can build it with int or float or nothing
        for args, expected_x, expected_y, expected_z in (
                [(), 0, 0, 0],
                [(0.5, 0.5, 0.5), 0.5, 0.5, 0.5],
                [(1,), 1, 0, 0],
                [(1, 1), 1, 1, 0],
                [(1, 2, 3), 1, 2, 3]):
            v = Vector3(*args)
            assert v.x == expected_x
            assert v.y == expected_y
            assert v.z == expected_z
        with pytest.raises(TypeError):
            Vector3("a", 2, 3)
        with pytest.raises(TypeError):
            Vector3("a", 2)
        with pytest.raises(TypeError):
            Vector3(1, "b", 5)
        with pytest.raises(TypeError):
            Vector3(None, 2, "c")

    @pytest.mark.xfail(reason='Not implemented yet')
    def test_methods(self):
        v = Vector3()
        # Don't test methods' validity but bindings one
        for field, ret_type, params in (
                ['abs', Vector3, ()],
                ['angle_to', float, (v, )],
                ['ceil', Vector3, ()],
                ['cross', Vector3, (v, )],
                ['cubic_interpolate', Vector3, (v, v, v, 0.5)],
                ['distance_squared_to', float, (v, )],
                ['distance_to', float, (v, )],
                ['dot', float, (v, )],
                ['floor', Vector3, ()],
                ['inverse', Vector3, ()],
                ['length', float, ()],
                ['length_squared', float, ()],
                ['linear_interpolate', Vector3, (v, 0.5)],
                ['max_axis', int, ()],
                ['min_axis', int, ()],
                ['normalized', Vector3, ()],
                ['reflect', Vector3, (v, )],
                ['rotated', Vector3, (v, 0.5)],
                ['slide', Vector3, (v, )],
                ['snapped', Vector3, (v, )]):
            assert hasattr(v, field)
            method = getattr(v, field)
            assert callable(method)
            ret = method(*params)
            assert isinstance(ret, ret_type)

    def test_properties(self):
        v = Vector3()
        for field, ret_type in (
                ('x', float),
                ('y', float),
                ('z', float)):
            assert hasattr(v, field)
            field_val = getattr(v, field)
            assert isinstance(field_val, ret_type)
            val = 10.
            setattr(v, field, val)
            field_val = getattr(v, field)
            assert field_val, val
