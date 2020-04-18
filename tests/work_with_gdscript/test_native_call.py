# TODO:
#       - allow inheritance from GDScript class
#       - overload native method ?
import pytest

from godot import GDString, ResourceLoader, GDScript, PluginScript


def test_native_method(node):
    original_name = node.get_name()
    try:
        node.set_name("foo")
        name = node.get_name()
        assert name == GDString("foo")
    finally:
        node.set_name(original_name)


@pytest.mark.xfail
def test_overloaded_native_method(node, subnode):
    expected = """
  *
 ***
*****
  |
"""
    ret = node.print_tree()
    assert ret == expected
    ret = subnode.print_tree()
    assert ret == expected


def test_node_ready_called(node):
    assert node.is_ready_called()


def test_subnode_ready_called(subnode):
    assert subnode.is_ready_called()
    assert subnode.is_sub_ready_called()


def test_method_call(anynode):
    ret = anynode.meth("foo")
    assert ret == GDString("foo")


def test_overloaded_method_call(subnode):
    ret = subnode.overloaded_by_child_meth("foo")
    assert ret == GDString("sub:foo")


def test_property_without_default_value(anynode):
    value = anynode.prop
    assert value is None


def test_property(anynode):
    anynode.prop = 42
    value = anynode.prop
    assert value == 42


@pytest.mark.xfail(reason="default value seems to be only set in .tscn")
def test_overloaded_property_default_value(pynode, pysubnode):
    # Parent property
    value = pynode.overloaded_by_child_prop
    assert value == "default"
    # Overloaded property
    value = pysubnode.overloaded_by_child_prop
    assert value == "sub:default"


def test_overloaded_property(pynode, pysubnode):
    # Not supported by GDScript

    # Parent property
    pynode.overloaded_by_child_prop = "foo"
    value = pynode.overloaded_by_child_prop
    assert value == GDString("foo")

    # Overloaded property
    pysubnode.overloaded_by_child_prop = "foo"
    value = pysubnode.overloaded_by_child_prop
    assert value == GDString("sub:foo")


def test_static_method_call(node):
    value = node.static_meth("foo")
    assert value == GDString("static:foo")


@pytest.mark.parametrize(
    "path,expected_type", [("res://gdnode.gd", GDScript), ("res://pynode.py", PluginScript)]
)
def test_load_script(path, expected_type):
    script = ResourceLoader.load(path, "", False)
    try:
        assert isinstance(script, expected_type)
        assert script.can_instance()
    finally:
        script.free()
