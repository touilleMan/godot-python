# TODO: - test GDScript static functions
#       - allow inheritance from GDScript class
import pytest

from godot import exposed
from godot.bindings import Node, OS


root_node = None


@exposed
class PyMain(Node):

    def run_tests(self):
        global root_node
        root_node = self
        # Retrieve command line arguments passed through --pytest=...
        prefix = '--pytest='
        pytest_args = []
        for arg in OS.get_cmdline_args():
            if arg.startswith(prefix):
                pytest_args += arg[len(prefix):].split()
        # Run tests here
        return pytest.main(pytest_args)
