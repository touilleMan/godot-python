import pytest

from godot import Transform, Basis, Vector3


def test_base():
    v = Transform()
    assert type(v) == Transform
    v2 = Transform.from_basis_origin(Basis(), Vector3(1, 2, 3))
    assert type(v) == Transform
    assert v2 == Transform.from_basis_origin(Basis(), Vector3(1, 2, 3))
    assert v != v2


def test_repr():
    v = Transform()
    assert repr(v).startswith("<Transform(")
