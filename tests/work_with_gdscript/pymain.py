# TODO: - test GDScript static functions
#       - allow inheritance from GDScript class
import os
import pytest

from godot import exposed, Node, OS


root_node = None


@exposed
class PyMain(Node):
    def run_tests(self):
        global root_node
        root_node = self
        # Retrieve command line arguments passed through --pytest=...
        prefix = "--pytest="
        pytest_args = []
        for gdarg in OS.get_cmdline_args():
            arg = str(gdarg)
            if arg.startswith(prefix):
                pytest_args += arg[len(prefix) :].split(",")
        if all(arg.startswith("-") for arg in pytest_args):
            # Filter to avoid scanning `plugins` and `lib` directories
            pytest_args += [x for x in os.listdir() if x.startswith("test_")]
        # Run tests here
        print(f"running `pytest {' '.join(pytest_args)}`")
        return pytest.main(pytest_args)
