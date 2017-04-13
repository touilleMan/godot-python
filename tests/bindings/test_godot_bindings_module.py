from godot import bindings


class TestGodotBindingsModule:

    def test_expose_contains_constant(self):
        assert 'OK' in dir(bindings)
        assert 'OK' in bindings.__all__

    def test_expose_contains_builtin(self):
        assert 'Vector3' in dir(bindings)
        assert 'Vector3' in bindings.__all__

    def test_expose_contains_dynamic_binded(self):
        assert 'Node' in dir(bindings)
        assert 'Node' in bindings.__all__
