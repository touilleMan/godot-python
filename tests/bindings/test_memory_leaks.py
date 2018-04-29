import pytest
from contextlib import contextmanager

from godot import bindings
from godot.bindings import OS


@contextmanager
def check_memory_leak():
    dynamic_mem_start = OS.get_dynamic_memory_usage()
    static_mem_start = OS.get_static_memory_usage()

    yield

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
    with check_memory_leak():

        v = bindings.Vector3()
        v.x = 42
        v.y


def test_dictionary_memory_leak():
    with check_memory_leak():

        v = bindings.Dictionary()
        v['foo'] = 42
        v.update({'a': 1, 'b': 2.0, 'c': 'three'})
        v['foo']
        [x for x in v]
        del v['a']


def test_array_memory_leak():
    with check_memory_leak():

        v = bindings.Array()
        v.append('x')
        v += [1, 2, 3]
        v[0]
        [x for x in v]


def test_pool_int_array_memory_leak():
    with check_memory_leak():

        v = bindings.PoolIntArray()
        v.append(42)
        v.resize(1000)
        v.pop()


def test_pool_string_array_memory_leak():
    with check_memory_leak():

        v = bindings.PoolStringArray()
        v.append("fooo")
        v.resize(1000)
        v.pop()


def test_object_memory_leak():
    with check_memory_leak():

        v = bindings.Node()
        v.free()
