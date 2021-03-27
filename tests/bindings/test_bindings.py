import pytest
from math import inf
from struct import unpack

import godot
from godot import (
    Vector3,
    GDString,
    NodePath,
    Object,
    Node,
    CanvasItem,
    Node2D,
    PluginScript,
    OpenSimplexNoise,
    OS,
    Error,
    OK,
    exposed,
)


@exposed
class virtualtestbedcls(Node):
    def _to_string(self):
        # Implemented for test_bindings::test_virtual_to_string_customize
        return GDString("<Main Node>")

    def _notification(self, what):
        on_notification = getattr(self, "on_notification", None)
        if on_notification:
            on_notification(what)


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
    assert str(exc.value) == "move_child() takes exactly 2 positional arguments (0 given)"


def test_call_with_defaults_and_too_few_args(current_node):
    with pytest.raises(TypeError) as exc:
        current_node.add_child()
    assert str(exc.value) == "add_child() takes at least 1 positional argument (0 given)"


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
    assert str(exc.value) == "add_child() takes at most 2 positional arguments (3 given)"


def test_call_with_defaults(generate_obj):
    node = generate_obj(Node)
    child = generate_obj(Node)
    # signature: void add_child(Node node, bool legible_unique_name=false)
    node.add_child(child)

    # legible_unique_name is False by default, check name is not human-redable
    children_names = [str(x.name) for x in node.get_children()]
    assert children_names == ["@@2"]


def test_call_returns_enum(generate_obj):
    node = generate_obj(Node)
    ret = node.connect("foo", node, "bar")
    assert isinstance(ret, Error)


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

    # CanvasItem is a direct subclass of Node
    canvas_item = generate_obj(CanvasItem)
    assert isinstance(node, Object)
    assert isinstance(canvas_item, Object)
    assert isinstance(canvas_item, Node)

    # TODO: headless server end up with a static memory leak
    # when instanciating a Node2D...
    if not OS.has_feature("Server"):
        # Node2D is a grand child subclass of Node
        node2d = generate_obj(Node2D)
        assert isinstance(node, Object)
        assert isinstance(node2d, Object)
        assert isinstance(node2d, Node)


def test_call_with_refcounted_return_value(current_node):
    script = current_node.get_script()
    assert isinstance(script, PluginScript)


def test_call_with_refcounted_param_value(generate_obj):
    node = generate_obj(Node)
    script = PluginScript()
    node.set_script(script)


def test_access_property(generate_obj):
    node = generate_obj(Node)
    path = NodePath("/foo/bar")
    node._import_path = path
    assert node._import_path == path


@pytest.mark.xfail(reason="Create Python class from Python not implemented yet")
def test_new_on_overloaded_class(generate_obj):
    node = generate_obj(virtualtestbedcls)
    # Make sure doing MyClass.new() doesn't return an instance of the
    # Godot class we inherit from
    assert isinstance(node, virtualtestbedcls)


@pytest.mark.xfail(reason="Create Python class from Python not implemented yet")
def test_virtual_call_overloaded_notification(generate_obj):
    node = generate_obj(virtualtestbedcls)

    notifications = []

    def _on_notification(what):
        notifications.append(what)

    node.on_notification = _on_notification
    try:
        node.notification(1)
        node.notification(2)
        node.notification(3)

    finally:
        node.on_notification = None

    assert notifications == [1, 2, 3]


@pytest.mark.xfail(reason="Pluginscript doesn't support _to_string overloading")
def test_virtual_to_string_customize(generate_obj):
    node = generate_obj(virtualtestbedcls)
    # Object.to_string() can be customized when defining _to_string()
    expected = GDString("<Main Node>")
    assert node._to_string() == expected
    assert node.to_string() == expected

    # Try to access undefined _to_string
    node = generate_obj(Node)
    with pytest.raises(AttributeError):
        node._to_string()


@pytest.fixture(params=["godot_class", "python_subclass"])
def node_for_access(request, current_node, generate_obj):
    if request.param == "godot_class":
        return generate_obj(Node)
    else:
        return current_node


@pytest.mark.xfail(reason="Current implement uses Object.callv which doesn't inform of the failure")
def test_virtual_call__to_string_not_customized(node_for_access):
    with pytest.raises(AttributeError):
        node_for_access._to_string()


@pytest.mark.xfail(reason="Current implement uses Object.callv which doesn't inform of the failure")
def test_virtual_call__notification_not_customized(node_for_access):
    with pytest.raises(AttributeError):
        node_for_access._notification(42)


def test_access_unknown_attribute(node_for_access):
    with pytest.raises(AttributeError):
        node_for_access.dummy


def test_call_unknown_method(node_for_access):
    with pytest.raises(AttributeError):
        node_for_access.dummy(42)


def test_create_refcounted_value():
    script1_ref1 = PluginScript()
    script2_ref1 = PluginScript()
    script1_ref2 = script1_ref1
    script2_ref2 = script2_ref1
    del script1_ref1


def test_late_initialized_bindings_and_float_param_ret():
    # OpenSimplexNoise is refcounted, so no need to create it with `generate_obj`
    obj = OpenSimplexNoise()

    # Float are tricky given they must be converted back and forth to double
    ret = obj.get_noise_1d(inf)
    assert ret == 0

    # Build a double number that cannot be reprented on a float
    double_only_number, = unpack("!d", b"\x11" * 8)
    ret = obj.get_noise_1d(double_only_number)
    assert ret == pytest.approx(-0.02726514)

    # Now try with better parameter to have a correct return value
    ret = obj.get_noise_3d(100, 200, 300)
    assert ret == pytest.approx(-0.10482934)


def test_bad_meth_to_create_non_refcounted_object():
    with pytest.raises(RuntimeError):
        Node()


def test_bad_meth_to_create_refcounted_object():
    with pytest.raises(RuntimeError):
        OpenSimplexNoise.new()
