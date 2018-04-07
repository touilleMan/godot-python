import pytest

from godot import bindings


class TestGodotBindingsModule:

    def test_expose_contains_constant(self):
        assert "OK" in dir(bindings)
        assert "OK" in bindings.__all__
        assert bindings.OK is not None

    def test_expose_contains_builtin(self):
        assert "Vector3" in dir(bindings)
        assert "Vector3" in bindings.__all__
        assert bindings.Vector3 is not None

    def test_expose_contains_dynamic_binded(self):
        assert "Node" in dir(bindings)
        assert "Node" in bindings.__all__
        assert bindings.Node is not None


class TestGodotBindingsModuleMethodCalls:

    def test_call_one_arg_short(self):
        node = bindings.Node()

        with pytest.raises(TypeError) as exc:
            node.get_child()
        assert str(
            exc.value
        ) == "get_child() missing 1 required positional argument: 'idx'"

    def test_call_too_few_args(self):
        node = bindings.Node()

        with pytest.raises(TypeError) as exc:
            node.move_child()
        assert str(
            exc.value
        ) == "move_child() missing 2 required positional arguments: 'child_node' and 'to_position'"

    def test_call_with_defaults_and_too_few_args(self):
        node = bindings.Node()

        with pytest.raises(TypeError) as exc:
            node.add_child()
        assert str(
            exc.value
        ) == "add_child() missing 1 required positional argument: 'node'"

    def test_call_too_many_args(self):
        node = bindings.Node()

        with pytest.raises(TypeError) as exc:
            node.get_child(1, 2)
        assert str(
            exc.value
        ) == "get_child() takes 1 positional argument but 2 were given"

    def test_call_with_default_and_too_many_args(self):
        node = bindings.Node()

        with pytest.raises(TypeError) as exc:
            node.add_child(1, 2, 3)
        assert str(
            exc.value
        ) == "add_child() takes from 1 to 2 positional arguments but 3 were given"

    def test_call_with_defaults(self):
        node = bindings.Node()
        child = bindings.Node()
        # signature: void add_child(Node node, bool legible_unique_name=false)
        node.add_child(child)

        # legible_unique_name is False by default, check name is not human-redable
        children_names = [x.name for x in node.get_children()]
        assert children_names == ["@@2"]

    @pytest.mark.xfail(reason="not supported yet")
    def test_call_with_kwargs(self):
        node = bindings.Node()
        child = bindings.Node()
        new_child = bindings.Node()

        node.add_child(child, legible_unique_name=True)
        # Check name is readable
        children_names = [x.name for x in node.get_children()]
        assert children_names == ["Node"]

        # Kwargs are passed out of order
        node.add_child_below_node(
            legible_unique_name=True, child_node=child, node=new_child
        )
        # Check names are still readable
        children_names = [x.name for x in node.get_children()]
        assert children_names == ["Node", "Node1"]
