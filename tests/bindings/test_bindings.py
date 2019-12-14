import pytest

from godot.bindings import Node


def test_free_node():
    v = Node()
    v.free()
    # check_memory_leak auto fixture will do the bookkeeping
