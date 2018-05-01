import pytest

from godot import bindings
from godot.bindings import OS


def check_memory_leak(fn):
    dynamic_mem_start = OS.get_dynamic_memory_usage()
    static_mem_start = OS.get_static_memory_usage()

    fn()

    # TODO: force garbage collection on pypy

    static_mem_end = OS.get_static_memory_usage()
    dynamic_mem_end = OS.get_dynamic_memory_usage()

    static_leak = static_mem_end - static_mem_start
    dynamic_leak = dynamic_mem_end - dynamic_mem_start
    assert not static_leak
    assert not dynamic_leak


def test_base_static_memory_leak_check():
    # Make sure calling this monitoring function doesn't cause a memory
    # leak on it own
    static_mem = OS.get_static_memory_usage()
    static_mem2 = OS.get_static_memory_usage()

    static_leak = static_mem2 - static_mem
    assert not static_leak


def test_base_dynamic_memory_leak_check():
    # Make sure calling this monitoring function doesn't cause a memory
    # leak on it own
    dynamic_mem = OS.get_dynamic_memory_usage()
    dynamic_mem2 = OS.get_dynamic_memory_usage()

    dynamic_leak = dynamic_mem2 - dynamic_mem
    assert not dynamic_leak


def test_base_builtin_memory_leak():

    def fn():
        v = bindings.Vector3()
        v.x = 42
        v.y

    check_memory_leak(fn)


def test_dictionary_memory_leak():

    def fn():
        v = bindings.Dictionary()
        v["foo"] = OS
        v.update({"a": 1, "b": 2.0, "c": "three"})
        v["foo"]
        [x for x in v.items()]
        del v["a"]

    check_memory_leak(fn)


def test_array_memory_leak():

    def fn():
        v = bindings.Array()
        v.append("x")
        v += [1, 2, 3]
        v[0]
        [x for x in v]

    check_memory_leak(fn)


def test_pool_int_array_memory_leak():

    def fn():
        v = bindings.PoolIntArray()
        v.append(42)
        v.resize(1000)
        v.pop()

    check_memory_leak(fn)


def test_pool_string_array_memory_leak():

    def fn():
        v = bindings.PoolStringArray()
        v.append("fooo")
        # v.resize(1000)  # TODO: when uncommenting this, the test pass...
        v.pop()

    check_memory_leak(fn)


def test_object_memory_leak():

    def fn():
        v = bindings.Node()
        v.free()

    check_memory_leak(fn)
