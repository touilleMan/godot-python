import os
import pytest

from godot import exposed
from godot.bindings import Node, OS


@exposed
class Main(Node):

    def _ready(self):
        # Retrieve command line arguments passed through --pytest=...
        prefix = "--pytest="
        # Filter to avoid scanning `plugins` and `lib` directories
        pytest_args = [x for x in os.listdir() if x.startswith("test_")]
        for arg in OS.get_cmdline_args():
            if arg.startswith(prefix):
                pytest_args += arg[len(prefix):].split(",")
        # Run tests here
        if pytest.main(pytest_args):
            OS.set_exit_code(1)
        # Exit godot
        self.get_tree().quit()
