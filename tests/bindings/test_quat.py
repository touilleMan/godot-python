import pytest

from godot.bindings import Quat, Vector3


class TestQuat:
    def test_base(self):
        v = Quat()
        assert type(v) == Quat

    def test_repr(self):
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
    def test_instantiate(self, args):
        # Can build it with int or float or nothing
        msg_tmpl = "%s vs (expected) %s (args=%s)"
        args, expected_x, expected_y, expected_z, expected_w = args
        v = Quat(*args)
        assert pytest.approx(v.x) == expected_x, msg_tmpl % (v.x, expected_x, args)
        assert pytest.approx(v.y) == expected_y, msg_tmpl % (v.y, expected_y, args)
        assert pytest.approx(v.z) == expected_z, msg_tmpl % (v.z, expected_z, args)
        assert pytest.approx(v.w) == expected_w, msg_tmpl % (v.w, expected_w, args)

    def test_bad_instantiate(self):
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
        "args",
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
        ],
        ids=lambda x: x[0],
    )
    def test_methods(self, args):
        v = Quat()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    @pytest.mark.parametrize(
        "args",
        [("x", float), ("y", float), ("z", float), ("w", float)],
        ids=lambda x: x[0],
    )
    def test_properties(self, args):
        v = Quat()
        field, ret_type = args
        assert hasattr(v, field)
        field_val = getattr(v, field)
        assert type(field_val) == ret_type
        for val in (0, 10, 10.0, 42.5):
            setattr(v, field, val)
            field_val = getattr(v, field)
            assert pytest.approx(field_val) == val

    @pytest.mark.parametrize(
        "args",
        [("x", "NaN"), ("y", "NaN"), ("z", "NaN"), ("w", "NaN")],
        ids=lambda x: x[0],
    )
    def test_bad_properties(self, args):
        v = Quat()
        field, bad_value = args
        with pytest.raises(TypeError):
            setattr(v, field, bad_value)

    def test_unary(self):
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
        "args",
        [
            (Quat(0, 0, 0, 0), Quat(2, 3, 4, 5)),
            (Quat(4, 3, 2, 1), Quat(6, 6, 6, 6)),
            (Quat(-4, -3, -2, -1), Quat(-2, -0, 2, 4)),
        ],
        ids=lambda x: x[0],
    )
    def test_add(self, args):
        param, result = args
        calc = Quat(2, 3, 4, 5) + param
        assert calc == result

    @pytest.mark.parametrize(
        "args",
        [
            (Quat(0, 0, 0, 0), Quat(2, 3, 4, 5)),
            (Quat(5, 4, 3, 2), Quat(-3, -1, 1, 3)),
            (Quat(-1, -1, -1, -1), Quat(3, 4, 5, 6)),
        ],
        ids=lambda x: x[0],
    )
    def test_sub(self, args):
        param, result = args
        calc = Quat(2, 3, 4, 5) - param
        assert calc == result

    @pytest.mark.parametrize("arg", [None, 1, "dummy"], ids=lambda x: x[0])
    def test_bad_add(self, arg):
        with pytest.raises(TypeError):
            Quat(2, 3, 4, 5) + arg

    @pytest.mark.parametrize("arg", [None, 1, "dummy"], ids=lambda x: x[0])
    def test_bad_sub(self, arg):
        with pytest.raises(TypeError):
            Quat(2, 3, 4, 5) - arg

    @pytest.mark.parametrize(
        "arg", [None, "dummy", Quat(1, 1, 1, 1)], ids=lambda x: x[0]
    )
    def test_bad_div(self, arg):
        with pytest.raises(TypeError):
            Quat(2, 3, 4, 5) / arg

    def test_zero_div(self):
        with pytest.raises(ZeroDivisionError):
            Quat(2, 3, 4, 5) / 0

    @pytest.mark.parametrize("arg", [None, "dummy"], ids=lambda x: x[0])
    def test_bad_mul(self, arg):
        with pytest.raises(TypeError):
            Quat(2, 3, 4, 5) * arg

    @pytest.mark.parametrize(
        "args",
        [(0, Quat(0, 0, 0, 0)), (1, Quat(2, 3, 4, 5)), (2.5, Quat(5, 7.5, 10, 12.5))],
        ids=lambda x: x[0],
    )
    def test_mul(self, args):
        param, result = args
        calc = Quat(2, 3, 4, 5) * param
        assert calc == result

    @pytest.mark.parametrize(
        "args",
        [(1, Quat(2, 3, 4, 5)), (0.5, Quat(4, 6, 8, 10)), (2, Quat(1, 1.5, 2, 2.5))],
        ids=lambda x: x[0],
    )
    def test_div(self, args):
        param, result = args
        calc = Quat(2, 3, 4, 5) / param
        assert calc == result

    def test_equal(self):
        arr = Quat(0.1, 1, 2, 3)
        other = Quat(0.1, 1, 2, 3)
        assert arr == other
        bad = Quat(0.1, 1, 2, 4)
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize("arg", [None, 0, "foo", Quat(0.1, 1, 2, 4)])
    def test_bad_equal(self, arg):
        arr = Quat(0.1, 1, 2, 3)
        assert arr != arg

    @pytest.mark.xfail
    def test_build_with_axis_angle(self):
        pass
