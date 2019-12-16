import pytest

from godot import Transform, Basis, Vector3


class TestTransform3D:
    def test_base(self):
        v = Transform()
        assert type(v) == Transform
        v2 = Transform.from_basis_origin(Basis(), Vector3(1, 2, 3))
        assert type(v) == Transform
        assert v2 == Transform.from_basis_origin(Basis(), Vector3(1, 2, 3))
        assert v != v2
