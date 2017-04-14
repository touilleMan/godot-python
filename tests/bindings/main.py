import pytest

from godot import exposed
from godot.bindings import Node, OS


@exposed
class Main(Node):

    def _ready(self):
        # Retrieve command line arguments passed through --pytest=...
        prefix = '--pytest='
        pytest_args = []
        for arg in OS.get_cmdline_args():
            if arg.startswith(prefix):
                pytest_args += arg[len(prefix):].split(',')
        # Run tests here
        if pytest.main(pytest_args):
            OS.set_exit_code(1)
        # Exit godot
        self.get_tree().quit()
