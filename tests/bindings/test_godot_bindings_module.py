from godot import bindings


class TestGodotBindingsModule:

    def test_expose_contains_constant(self):
        assert 'OK' in dir(bindings)
        assert 'OK' in bindings.__all__
        assert bindings.OK is not None

    def test_expose_contains_builtin(self):
        assert 'Vector3' in dir(bindings)
        assert 'Vector3' in bindings.__all__
        assert bindings.Vector3 is not None

    def test_expose_contains_dynamic_binded(self):
        assert 'Node' in dir(bindings)
        assert 'Node' in bindings.__all__
        assert bindings.Node is not None
