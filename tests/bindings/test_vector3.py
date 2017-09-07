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

    def test_repr(self):
        v = Vector3(1, 2, 3)
        assert repr(v) == '<Vector3(x=1.0, y=2.0, z=3.0)>'

    def test_instantiate(self):
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

    @pytest.mark.parametrize('args', [
        ['abs', Vector3, ()],
        ['angle_to', float, (Vector3(), )],
        ['ceil', Vector3, ()],
        ['cross', Vector3, (Vector3(), )],
        ['cubic_interpolate', Vector3, (Vector3(), Vector3(), Vector3(), 0.5)],
        ['distance_squared_to', float, (Vector3(), )],
        ['distance_to', float, (Vector3(), )],
        ['dot', float, (Vector3(), )],
        ['floor', Vector3, ()],
        ['inverse', Vector3, ()],
        ['length', float, ()],
        ['length_squared', float, ()],
        ['linear_interpolate', Vector3, (Vector3(), 0.5)],
        ['max_axis', int, ()],
        ['min_axis', int, ()],
        ['normalized', Vector3, ()],
        ['reflect', Vector3, (Vector3(), )],
        ['rotated', Vector3, (Vector3(), 0.5)],
        ['slide', Vector3, (Vector3(), )],
        ['snapped', Vector3, (Vector3(), )],
    ], ids=lambda x: x[0])
    def test_methods(self, args):
        v = Vector3()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert isinstance(ret, ret_type)

    @pytest.mark.parametrize('args', [
        ('x', float),
        ('y', float),
        ('z', float),
    ], ids=lambda x: x[0])
    def test_properties(self, args):
        v = Vector3()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert isinstance(field_val, ret_type)
        val = 10.
        setattr(v, field, val)
        field_val = getattr(v, field)
        assert field_val == val

    @pytest.mark.parametrize('args', [
        ('x', 'NaN'),
        ('y', 'NaN'),
        ('z', 'NaN'),
    ], ids=lambda x: x[0])
    def test_bad_properties(self, args):
        v = Vector3()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)

    @pytest.mark.parametrize('args', [
        ('AXIS_X', int),
        ('AXIS_Y', int),
        ('AXIS_Z', int)
    ], ids=lambda x: x[0])
    def test_contants(self, args):
        v = Vector3()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert isinstance(field_val, ret_type)

    @pytest.mark.parametrize('args', [
        (0, Vector3(0, 0, 0)),
        (1, Vector3(2, 3, 4)),
        (2.5, Vector3(5, 7.5, 10)),
        (Vector3(1, 1, 1), Vector3(2, 3, 4)),
        (Vector3(2, 3, 4), Vector3(4, 9, 16))
    ], ids=lambda x: x[0])
    def test_mult(self, args):
        param, result = args
        calc = Vector3(2, 3, 4) * param
        assert calc == result

    @pytest.mark.parametrize('args', [
        (1, Vector3(2, 3, 4)),
        (.5, Vector3(4, 6, 8)),
        (2, Vector3(1, 1.5, 2)),
        (Vector3(1, 1, 1), Vector3(2, 3, 4)),
        (Vector3(2, 3, 4), Vector3(1, 1, 1))
    ], ids=lambda x: x[0])
    def test_div(self, args):
        param, result = args
        calc = Vector3(2, 3, 4) / param
        assert calc == result

    @pytest.mark.parametrize('args', [
        (Vector3(0, 0, 0), Vector3(2, 3, 4)),
        (Vector3(3, 2, 1), Vector3(5, 5, 5)),
        (Vector3(-1, -4, -2), Vector3(1, -1, 2)),
    ], ids=lambda x: x[0])
    def test_add(self, args):
        param, result = args
        calc = Vector3(2, 3, 4) + param
        assert calc == result

    @pytest.mark.parametrize('args', [
        (Vector3(0, 0, 0), Vector3(2, 3, 4)),
        (Vector3(3, 2, 1), Vector3(-1, 1, 3)),
        (Vector3(-1, -1, -1), Vector3(3, 4, 5)),
    ], ids=lambda x: x[0])
    def test_sub(self, args):
        param, result = args
        calc = Vector3(2, 3, 4) - param
        assert calc == result

    @pytest.mark.parametrize('arg', [
        None, 1, 'dummy'
    ], ids=lambda x: x[0])
    def test_bad_add(self, arg):
        with pytest.raises(TypeError):
            Vector3(2, 3, 4) + arg

    @pytest.mark.parametrize('arg', [
        None, 1, 'dummy'
    ], ids=lambda x: x[0])
    def test_bad_sub(self, arg):
        with pytest.raises(TypeError):
            Vector3(2, 3, 4) - arg

    @pytest.mark.parametrize('arg', [
        None, 'dummy'
    ], ids=lambda x: x[0])
    def test_bad_div(self, arg):
        with pytest.raises(TypeError):
            Vector3(2, 3, 4) / arg

    @pytest.mark.parametrize('arg', [
        0, Vector3(0, 1, 1), Vector3(1, 0, 1), Vector3(1, 1, 0), Vector3(0, 0, 0)
    ], ids=lambda x: x[0])
    def test_zero_div(self, arg):
        with pytest.raises(ZeroDivisionError):
            Vector3(2, 3, 4) / arg

    @pytest.mark.parametrize('arg', [
        None, 'dummy'
    ], ids=lambda x: x[0])
    def test_bad_mult(self, arg):
        with pytest.raises(TypeError):
            Vector3(2, 3, 4) * arg

    def test_equal(self):
        arr = Vector3(1, 2, 3)
        other = Vector3(1, 2, 3)
        assert arr == other
        bad = Vector3(1, 2, 4)
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize('arg', [
        None,
        0,
        'foo',
        Vector3(1, 2, 4),
    ])
    def test_bad_equal(self, arg):
        arr = Vector3(1, 2, 3)
        assert arr != arg
