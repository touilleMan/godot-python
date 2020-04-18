import pytest

from godot import ResourceLoader

import pymain


assert pymain.root_node


@pytest.fixture
def root_node():
    return pymain.root_node


@pytest.fixture(
    params=[
        "/root/main/test/pynode",
        "/root/main/test/gdnode",
        "/root/main/test/pysubnode",
        "/root/main/test/gdsubnode",
    ]
)
def anynode(request, root_node):
    return root_node.get_node(request.param)


@pytest.fixture(params=["/root/main/test/pynode", "/root/main/test/gdnode"])
def node(request, root_node):
    return root_node.get_node(request.param)


@pytest.fixture(params=["/root/main/test/pysubnode", "/root/main/test/gdsubnode"])
def subnode(request, root_node):
    return root_node.get_node(request.param)


@pytest.fixture
def pynode(root_node):
    return root_node.get_node("/root/main/test/pynode")


@pytest.fixture
def pysubnode(root_node):
    return root_node.get_node("/root/main/test/pysubnode")


@pytest.fixture
def gdnode(root_node):
    return root_node.get_node("/root/main/test/gdnode")


@pytest.fixture
def gdsubnode(root_node):
    return root_node.get_node("/root/main/test/gdsubnode")


@pytest.fixture
def pynode_scene():
    return ResourceLoader.load("res://pynode.tscn", "", False)


@pytest.fixture
def pysubnode_scene():
    return ResourceLoader.load("res://pysubnode.tscn", "", False)


@pytest.fixture
def gdnode_scene():
    return ResourceLoader.load("res://gdnode.tscn", "", False)


@pytest.fixture
def gdsubnode_scene():
    return ResourceLoader.load("res://gdsubnode.tscn", "", False)
