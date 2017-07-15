# This test is in it own file to protect other tests from the `import *` side effects
from godot.bindings import *


def test_starimport():
	assert issubclass(Node, Object)
	assert isinstance(PhysicsServer, _PhysicsServer)
	assert isinstance(Engine, _Engine)
