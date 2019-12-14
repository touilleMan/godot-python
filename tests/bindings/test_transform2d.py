import pytest

from godot import Transform2D, Vector2, Rect2


class TestTransform2D:
    def test_init(self):
        v = Transform2D()
        assert type(v) == Transform2D
        args = (Vector2(1, 2), Vector2(3, 4), Vector2(5, 6))
        v2 = Transform2D(*args)
        assert type(v) == Transform2D
        assert v2 == Transform2D(*args)
        assert v != v2

    @pytest.mark.parametrize(
        "args", [
        ("NaN", Vector2(), Vector2()),
        (Vector2(), "NaN", Vector2()),
        (Vector2(), Vector2(), "Nan"),
        (None, Vector2(), Vector2()),
        (Vector2(), None, Vector2()),
        (Vector2(), Vector2(), None),
    ])
    def test_bad_init(self, args):
        with pytest.raises(TypeError):
            Transform2D(*args)

    def test_repr(self):
        v = Transform2D()
        assert repr(v).startswith("<Transform2D(")

    def test_init_from_rot_pos(self):
        v = Transform2D.from_rot_pos(1, Vector2())
        assert isinstance(v, Transform2D)

    @pytest.mark.parametrize(
        "args", [
        (1, ),
        (None, Vector2()),
        ("NaN", Vector2()),
        (1, "bad"),
    ])
    def test_bad_init_from_rot_pos(self, args):
        with pytest.raises(TypeError):
            Transform2D.from_rot_pos(*args)

    @pytest.mark.parametrize(
        "args",
        [
            ["inverse", Transform2D, ()],
            ["affine_inverse", Transform2D, ()],
            ["get_rotation", float, ()],
            # ["get_origin", Vector2, ()],
            ["get_scale", Vector2, ()],
            ["orthonormalized", Transform2D, ()],
            ["rotated", Transform2D, (1.0,)],
            ["scaled", Transform2D, (Vector2(),)],
            ["translated", Transform2D, (Vector2(),)],
            ["xform", Vector2, (Vector2(),)],
            ["xform_inv", Vector2, (Vector2(),)],
            ["xform", Rect2, (Rect2(),)],
            ["xform_inv", Rect2, (Rect2(),)],
            ["basis_xform", Vector2, (Vector2(),)],
            ["basis_xform_inv", Vector2, (Vector2(),)],
            ["interpolate_with", Transform2D, (Transform2D(), 1.0)],
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

    def test_mult(self):
        v1 = Transform2D()
        v2 = Transform2D()
        v3 = v1 * v2
        assert isinstance(v3, Transform2D)
        v2 *= v1
        assert v3 == v2

    @pytest.mark.parametrize('arg', [
        None, 'dummy'
    ], ids=lambda x: x[0])
    def test_bad_mult(self, arg):
        with pytest.raises(TypeError):
            Transform2D(2, 3) * arg

    def test_equal(self):
        arr = Transform2D(Vector2(1, 2), Vector2(3, 4), Vector2(5, 6))
        other = Transform2D(Vector2(1, 2), Vector2(3, 4), Vector2(5, 6))
        assert arr == other
        bad = Transform2D(Vector2(0, 2), Vector2(3, 4), Vector2(5, 6))
        assert not arr == bad  # Force use of __eq__

    @pytest.mark.parametrize("arg", [None, 0, "foo", Transform2D()])
    def test_not_equal(self, arg):
        arr = Transform2D(Vector2(1, 2), Vector2(3, 4), Vector2(5, 6))
        assert arr != arg
        assert not arr != arr  # Force use of __ne__
