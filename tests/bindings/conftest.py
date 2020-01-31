import pytest

from godot import OS, Node, Reference


__global_objs = []


def generate_global_obj(type):
    obj = type.new()
    __global_objs.append(obj)
    return obj


@pytest.fixture(scope="session", autouse=True)
def cleanup_global_objs():
    yield
    for obj in __global_objs:
        obj.free()


@pytest.fixture()
def generate_obj(check_memory_leak):
    # Make this fixture depend on `check_memory_leak` to ensure it will
    # check for memory leak after our own teardown

    objs = []

    def _generate_obj(type):
        obj = type.new()
        objs.append(obj)
        return obj

    yield _generate_obj

    # Node must be removed from the scenetree to avoid segfault on free
    for obj in objs:
        if isinstance(obj, Node):
            parent = obj.get_parent()
            if parent:
                parent.remove_child(obj)

    while objs:
        # Pop values to trigger gc for Reference instances
        obj = objs.pop()
        if not isinstance(obj, Reference):
            obj.free()


@pytest.fixture
def current_node():
    # `conftest.py` is imported weirdly by pytest so we cannot just put a
    # global variable in it and set it from `Main._ready`
    from main import get_current_node

    return get_current_node()


@pytest.fixture(autouse=True)
def check_memory_leak(request):
    if request.node.get_marker("ignore_leaks"):
        yield
    else:
        dynamic_mem_start = OS.get_dynamic_memory_usage()
        static_mem_start = OS.get_static_memory_usage()

        yield

        static_mem_end = OS.get_static_memory_usage()
        dynamic_mem_end = OS.get_dynamic_memory_usage()

        static_leak = static_mem_end - static_mem_start
        dynamic_leak = dynamic_mem_end - dynamic_mem_start
        assert static_leak == 0
        assert dynamic_leak == 0
