import pytest

from godot.bindings import Transform, Basis, Vector3


class TestTransform3D:
    def test_base(self):
        v = Transform()
        assert type(v) == Transform
        v2 = Transform(Basis(), Vector3(1, 2, 3))
        assert type(v) == Transform
        assert v2 == Transform(Basis(), Vector3(1, 2, 3))
        assert v != v2
