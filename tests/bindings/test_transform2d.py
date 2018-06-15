import pytest

from godot.bindings import Transform2D, Vector2, Rect2


class TestTransform2D:
    def test_base(self):
        v = Transform2D()
        assert type(v) == Transform2D
        v2 = Transform2D(1, Vector2(1, 2))
        assert type(v) == Transform2D
        assert v2 == Transform2D(1, Vector2(1, 2))
        assert v != v2

    def test_repr(self):
        v = Transform2D(1, Vector2(1, 2))
        assert repr(v).startswith("<Transform2D(")

    # def test_instantiate(self):
    #     # Can build it with int or float or nothing
    #     msg_tmpl = "%s vs (expected) %s (args=%s)"
    #     for args, expected_x, expected_y in (
    #             [(), 0, 0],
    #             [(0.5, 0.5), 0.5, 0.5],
    #             [(1, 2), 1, 2],
    #             [(1,), 1, 0]):
    #         v = Transform2D(*args)
    #         assert v.x == expected_x, msg_tmpl % (v.x, expected_x, args)
    #         assert v.y == expected_y, msg_tmpl % (v.y, expected_y, args)
    #         assert v.width == expected_x, msg_tmpl % (v.width, expected_y, args)
    #         assert v.height == expected_y, msg_tmpl % (v.height, expected_x, args)
    #     with pytest.raises(TypeError):
    #         Transform2D("a", 2)
    #     with pytest.raises(TypeError):
    #         Transform2D("a", 2)
    #     with pytest.raises(TypeError):
    #         Transform2D(1, "b")
    #     with pytest.raises(TypeError):
    #         Transform2D(None, 2)

    @pytest.mark.parametrize(
        "args",
        [
            ["inverse", Transform2D, ()],
            ["affine_inverse", Transform2D, ()],
            ["get_rotation", float, ()],
            ["get_origin", Vector2, ()],
            ["get_scale", Vector2, ()],
            ["orthonormalized", Transform2D, ()],
            ["rotated", Transform2D, (1.0,)],
            ["scaled", Transform2D, (Vector2(),)],
            ["translated", Transform2D, (Vector2(),)],
            ["xform", Vector2, (Vector2(),)],
            ["xform_inv", Vector2, (Vector2(),)],
            ["basis_xform", Vector2, (Vector2(),)],
            ["basis_xform_inv", Vector2, (Vector2(),)],
            ["interpolate_with", Transform2D, (Transform2D(), 1.0)],
            ["xform", Rect2, (Rect2(),)],
            ["xform_inv", Rect2, (Rect2(),)],
        ],
        ids=lambda x: x[0],
    )
    def test_methods(self, args):
        v = Transform2D()
        # Don't test methods' validity but bindings one
        field, ret_type, params = args
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert type(ret) == ret_type

    # @pytest.mark.parametrize('arg', [
    #     None, 'dummy'
    # ], ids=lambda x: x[0])
    # def test_bad_mult(self, arg):
    #     with pytest.raises(TypeError):
    #         Transform2D(2, 3) * arg

    # @pytest.mark.parametrize('args', [
    #     (0, Transform2D(0, 0)),
    #     (1, Transform2D(2, 3)),
    #     (2.5, Transform2D(5, 7.5)),
    #     (Transform2D(1, 1), Transform2D(2, 3)),
    #     (Transform2D(2, 3), Transform2D(4, 9))
    # ], ids=lambda x: x[0])
    # def test_mult(self, args):
    #     param, result = args
    #     calc = Transform2D(2, 3) * param
    #     assert calc == result

    def test_equal(self):
        arr = Transform2D(1, Vector2(1, 2))
        other = Transform2D(1, Vector2(1, 2))
        assert arr == other
        bad = Transform2D(1, Vector2(1, 3))
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize("arg", [None, 0, "foo", Transform2D(1, Vector2(1, 3))])
    def test_bad_equal(self, arg):
        arr = Transform2D(1, Vector2(1, 2))
        assert arr != arg
