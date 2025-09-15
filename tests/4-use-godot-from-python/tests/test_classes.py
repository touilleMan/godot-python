from enum import Enum
import clodotest
from clodotest import assert_eq, assert_ne, assert_isinstance, assert_issubclass

import godot


def test_eq_operator():
    from godot.classes import Node

    node1 = Node.new()
    node2 = Node.new()
    try:
        assert_ne(node1, None)
        assert_ne(node1, 42)

        node1.name = "node1"
        node2.name = "node2"

        assert_ne(node1, node2)
        assert_eq(node1, node1)

        node1.add_child(node2)
        node2b = node1.get_child(0)
        assert_eq(node2, node2b)

    finally:
        node2.free()
        node1.free()


def test_bad_meth_to_create_non_refcounted_object():
    from godot.classes import Node2D

    with clodotest.raises(RuntimeError) as raised:
        Node2D()
    assert_eq(
        str(raised.exc),
        "Use `new()` method to instantiate non-refcounted Godot object (and don't forget to free it !)",
    )


def test_bad_meth_to_create_refcounted_object():
    from godot.classes import Image

    with clodotest.raises(RuntimeError) as raised:
        Image.new()

    assert_eq(str(raised.exc), "RefCounted Godot object must be created with `Image()`")


def test_create_refcounted_object():
    from godot.classes import Image, Resource, Object

    img = Image()
    assert_isinstance(img, Image)
    assert_isinstance(img, Resource)
    assert_isinstance(img, Object)
    # Property
    assert_isinstance(img.data, godot.GDDictionary)
    # Method
    assert_eq(img.is_empty(), True)
    # Method from parent class
    assert_isinstance(img.is_built_in(), bool)  # Defined in `Resource`
    assert_isinstance(img.to_string(), godot.GDString)  # Defined in `Object`


def test_create_non_refcounted_object():
    from godot.classes import Node2D, Node, Object

    node = Node2D.new()
    try:
        assert_isinstance(node, Node2D)
        assert_isinstance(node, Node)
        assert_isinstance(node, Object)
        # Property
        assert_isinstance(node.global_rotation, float)
        # Method
        assert node.rotate(42.42) is None
        # Method from parent class
        assert_isinstance(node.is_processing(), bool)  # Defined in `Node`
        assert_isinstance(node.to_string(), godot.GDString)  # Defined in `Object`

    finally:
        node.free()


@clodotest.parametrize(
    "kind",
    [
        "normal_with_return_value",
        "normal_with_param",
        "normal_with_named_param",
        "inherited",
        "const",
        "virtual",
        "static",
        "vararg",
    ],
)
def test_method(kind: str):
    from godot.classes import Node, JSON

    node = Node.new()
    try:
        match kind:
            case "normal_with_return_value":
                assert_isinstance(node.get_tree_string(), godot.GDString)
                assert_eq(node.find_child("dummy"), None)  # Return None or `Node` instance
                node2 = Node.new()
                try:
                    node2.name = "child"
                    node.add_child(node2)
                    assert_eq(node.get_child(0), node2)
                finally:
                    node2.free()

            case "normal_with_param":
                assert_isinstance(node.is_ancestor_of(node), bool)

            case "normal_with_named_param":
                clodotest.skip(reason="TODO: named param not supported yet")
                assert_isinstance(node.is_ancestor_of(node=node), bool)

            case "inherited":
                # `get_class` is defined in `Object`
                assert_isinstance(node.get_class(), godot.GDString)

            case "const":
                assert_isinstance(node.get_children(), godot.GDArray)

            case "virtual":
                clodotest.skip(reason="TODO: find a virtual method overwritten by a subclass ?")

            case "static":
                assert_isinstance(JSON.stringify(42), godot.GDString)

            case "vararg":
                assert_isinstance(node.call("is_ancestor_of", node), bool)

            case unknown:
                assert False, unknown

    finally:
        node.free()


@clodotest.parametrize(
    "kind",
    [
        "scalar",
        "enum",
        "class",
    ],
)
def test_property(kind: str):
    from godot.classes import Node

    node = Node.new()
    try:
        match kind:
            case "scalar":
                assert_eq(node.name, godot.StringName(""))

                node.name = godot.StringName("foo")
                assert_eq(node.name, godot.StringName("foo"))

                node.name = "bar"
                assert_eq(node.name, godot.StringName("bar"))

            case "enum":
                clodotest.skip(
                    reason="TODO: enum currently return `int` instead of `Enum` instance"
                )
                assert_eq(
                    node.physics_interpolation_mode,
                    node.PhysicsInterpolationMode.PHYSICS_INTERPOLATION_MODE_INHERIT,
                )
                node.physics_interpolation_mode = (
                    node.PhysicsInterpolationMode.PHYSICS_INTERPOLATION_MODE_ON
                )
                assert_eq(
                    node.physics_interpolation_mode,
                    node.PhysicsInterpolationMode.PHYSICS_INTERPOLATION_MODE_ON,
                )

            case "class":
                node2 = Node.new()
                assert_eq(node2.owner, None)
                try:
                    node.add_child(node2)
                    assert_eq(node2.owner, None)
                    node2.owner = node
                    assert_eq(node2.owner, node)
                finally:
                    node2.free()

            case unknown:
                assert False, unknown
    finally:
        node.free()
    clodotest.skip("TODO")


@clodotest.xfail(reason="TODO: Signal constructor from object + signal name is not implemented")
def test_signal():
    from godot.classes import Node

    node = Node.new()
    node2 = Node.new()
    try:
        assert_isinstance(node.ready, godot.Signal)
        assert_eq(node.ready, node.ready)
        assert_ne(node.ready, node.replacing_by)

        # TODO: Connect a callable and emit the signal

    finally:
        node2.free()
        node.free()


def test_constant():
    from godot.classes import Node

    # Defined in the class
    assert_eq(Node.NOTIFICATION_ENTER_TREE, 10)
    # Defined in the parent
    assert_eq(Node.NOTIFICATION_PREDELETE, 1)


def test_enum():
    from godot.classes import Node

    # Defined in the class
    assert_issubclass(Node.ProcessMode, Enum)
    assert_eq(Node.ProcessMode.WHEN_PAUSED.value, 2)
    assert not hasattr(Node.ProcessMode, "PROCESS_MODE_WHEN_PAUSED")
    # Defined in the parent
    assert_eq(Node.ConnectFlags.ONE_SHOT.value, 4)
