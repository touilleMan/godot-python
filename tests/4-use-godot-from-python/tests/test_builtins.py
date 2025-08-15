import godot


def test_vector2():
    v = godot.Vector2(x=1, y=2)
    assert v.x == 1
    assert v.y == 2
