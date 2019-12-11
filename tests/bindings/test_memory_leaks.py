import pytest

from godot import Vector3, Dictionary, Array, PoolIntArray, PoolStringArray
from godot.bindings import OS, Node


def check_memory_leak(fn):
    dynamic_mem_start = OS.get_dynamic_memory_usage()
    static_mem_start = OS.get_static_memory_usage()

    fn()

    static_mem_end = OS.get_static_memory_usage()
    dynamic_mem_end = OS.get_dynamic_memory_usage()

    static_leak = static_mem_end - static_mem_start
    dynamic_leak = dynamic_mem_end - dynamic_mem_start
    assert static_leak == 0
    assert dynamic_leak == 0


def test_base_static_memory_leak_check():
    # Make sure calling this monitoring function doesn't cause a memory
    # leak on it own
    static_mem = OS.get_static_memory_usage()
    static_mem2 = OS.get_static_memory_usage()

    static_leak = static_mem2 - static_mem
    assert static_leak == 0


def test_base_dynamic_memory_leak_check():
    # Make sure calling this monitoring function doesn't cause a memory
    # leak on it own
    dynamic_mem = OS.get_dynamic_memory_usage()
    dynamic_mem2 = OS.get_dynamic_memory_usage()

    dynamic_leak = dynamic_mem2 - dynamic_mem
    assert dynamic_leak == 0


def test_base_builtin_memory_leak():
    def fn():
        v = Vector3()
        v.x = 42
        v.y

    check_memory_leak(fn)


def test_dictionary_memory_leak():
    def fn():
        v = Dictionary()
        v["foo"] = OS
        v.update({"a": 1, "b": 2.0, "c": "three"})
        v["foo"]
        [x for x in v.items()]
        del v["a"]

    check_memory_leak(fn)


def test_array_memory_leak():
    def fn():
        v = Array()
        v.append("x")
        v += [1, 2, 3]
        v[0]
        [x for x in v]

    check_memory_leak(fn)


def test_pool_int_array_memory_leak():
    def fn():
        v = PoolIntArray()
        v.append(42)
        v.resize(1000)
        del v[0]
        del v[10]

    check_memory_leak(fn)


def test_pool_string_array_memory_leak():
    def fn():
        v = PoolStringArray()
        v.append("fooo")
        v.resize(1000)
        del v[0]
        del v[10]

    check_memory_leak(fn)


def test_object_memory_leak():
    def fn():
        v = Node()
        v.free()

    check_memory_leak(fn)
