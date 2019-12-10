# This test is in it own file to protect other tests from the `import *` side effects
from godot.bindings import *

# Class with trailing underscore are provided on star import
from godot.bindings import _OS, _ProjectSettings


def test_starimport():
    assert issubclass(Node, Object)
    assert isinstance(OS, _OS)
    assert isinstance(ProjectSettings, _ProjectSettings)
