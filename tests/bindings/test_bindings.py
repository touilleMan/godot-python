import pytest

from godot import Vector3
from godot import bindings


def test_free_node():
    v = bindings.Node.new()
    v.free()
    # `check_memory_leak` auto fixture will do the bookkeeping


def test_expose_contains_constant():
    assert "OK" in dir(bindings)
    assert bindings.OK is not None


def test_expose_contains_class():
    assert "Node" in dir(bindings)
    assert bindings.Node is not None


def test_call_one_arg_short(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.get_child()
    assert (
        str(exc.value)
        == "get_child() takes exactly one argument (0 given)"
    )

def test_call_too_few_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.move_child()
    assert (
        str(exc.value)
        == "move_child() takes exactly 2 positional arguments (0 given)"
    )

def test_call_with_defaults_and_too_few_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.add_child()
    assert (
        str(exc.value)
        == "add_child() takes exactly 2 positional arguments (0 given)"
    )

def test_call_too_many_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.get_child(1, 2)
    assert (
        str(exc.value) == "get_child() takes exactly one argument (2 given)"
    )

def test_call_with_default_and_too_many_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.add_child(1, 2, 3)
    assert (
        str(exc.value)
        == "add_child() takes exactly 2 positional arguments (3 given)"
    )


@pytest.mark.xfail(reason="TODO: support defaults")
def test_call_with_defaults(generate_obj):
    node = generate_obj(bindings.Node)
    child = generate_obj(bindings.Node)
    # signature: void add_child(Node node, bool legible_unique_name=false)
    node.add_child(child)

    # legible_unique_name is False by default, check name is not human-redable
    children_names = [x.name for x in node.get_children()]
    assert children_names == ["@@2"]

# @pytest.mark.xfail(reason="not supported yet")
# def test_call_with_kwargs(generate_obj):
#     node = generate_obj(bindings.Node)
#     child = generate_obj(bindings.Node)
#     new_child = generate_obj(bindings.Node)

#     node.add_child(child, legible_unique_name=True)
#     # Check name is readable
#     children_names = [x.name for x in node.get_children()]
#     assert children_names == ["Node"]

#     # Kwargs are passed out of order
#     node.add_child_below_node(
#         legible_unique_name=True, child_node=child, node=new_child
#     )
#     # Check names are still readable
#     children_names = [x.name for x in node.get_children()]
#     assert children_names == ["Node", "Node1"]
