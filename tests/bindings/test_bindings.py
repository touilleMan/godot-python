import pytest

import godot
from godot import Vector3, Object, Node, Node2D, OK


def test_free_node():
    v = Node.new()
    v.free()
    # `check_memory_leak` auto fixture will do the bookkeeping


def test_expose_contains_constant():
    assert "OK" in dir(godot)
    assert OK is not None


def test_expose_contains_class():
    assert "Node" in dir(godot)
    assert Node is not None


def test_expose_contains_builtins():
    assert "Vector3" in dir(godot)
    assert Vector3 is not None


def test_call_one_arg_short(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.get_child()
    assert str(exc.value) == "get_child() takes exactly one argument (0 given)"


def test_call_too_few_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.move_child()
    assert (
        str(exc.value) == "move_child() takes exactly 2 positional arguments (0 given)"
    )


def test_call_with_defaults_and_too_few_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.add_child()
    assert (
        str(exc.value) == "add_child() takes at least 1 positional argument (0 given)"
    )


def test_call_none_in_base_type_args(current_node):
    with pytest.raises(TypeError) as exc:
        # signature: def get_child(self, godot_int idx)
        current_node.get_child(None)
    assert str(exc.value) == "an integer is required"


def test_call_none_in_builtin_args(current_node):
    with pytest.raises(TypeError) as exc:
        # signature: def get_node(self, NodePath path not None)
        current_node.get_node(None)
    assert str(exc.value) == "Invalid value None, must be str or NodePath"


def test_call_none_in_bindings_args(current_node):
    with pytest.raises(TypeError) as exc:
        # signature: def get_path_to(self, Node node not None)
        current_node.get_path_to(None)
    assert (
        str(exc.value)
        == "Argument 'node' has incorrect type (expected godot.bindings.Node, got NoneType)"
    )


def test_call_too_many_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.get_child(1, 2)
    assert str(exc.value) == "get_child() takes exactly one argument (2 given)"


def test_call_with_default_and_too_many_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.add_child(1, 2, 3)
    assert (
        str(exc.value) == "add_child() takes at most 2 positional arguments (3 given)"
    )


def test_call_with_defaults(generate_obj):
    node = generate_obj(Node)
    child = generate_obj(Node)
    # signature: void add_child(Node node, bool legible_unique_name=false)
    node.add_child(child)

    # legible_unique_name is False by default, check name is not human-redable
    children_names = [str(x.name) for x in node.get_children()]
    assert children_names == ["@@2"]


def test_call_with_kwargs(generate_obj):
    node = generate_obj(Node)
    child = generate_obj(Node)
    new_child = generate_obj(Node)

    node.add_child(child, legible_unique_name=True)
    # Check name is readable
    children_names = [str(x.name) for x in node.get_children()]
    assert children_names == ["Node"]

    # Kwargs are passed out of order
    node.add_child_below_node(legible_unique_name=True, child_node=new_child, node=node)
    # Check names are still readable
    children_names = [str(x.name) for x in node.get_children()]
    assert children_names == ["Node", "Node2"]


def test_inheritance(generate_obj):
    node = generate_obj(Node)
    node2d = generate_obj(Node2D)
    isinstance(node, Object)
    isinstance(node2d, Object)
    isinstance(node2d, Node)
