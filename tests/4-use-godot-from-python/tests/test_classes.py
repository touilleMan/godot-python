from enum import Enum
import clodotest
from clodotest import assert_eq, assert_isinstance, assert_issubclass

import godot


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


def test_method():
    clodotest.skip("TODO")


def test_property():
    clodotest.skip("TODO")


def test_signal():
    clodotest.skip("TODO")


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
    assert_eq(Node.ProcessMode.PROCESS_MODE_WHEN_PAUSED.value, 2)
    # Defined in the parent
    assert_eq(Node.ConnectFlags.CONNECT_ONE_SHOT.value, 4)
