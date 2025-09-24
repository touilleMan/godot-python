import clodotest
from pathlib import Path
import os


BASEDIR = Path(__file__).absolute().parent


def initialize(level: int):
    if level < 3:
        return
    assert level == 3

    clodotest.run_tests_with_argv(BASEDIR / "tests", os.environ.get("TEST_ARGV", "").split())
    # TODO: find a way to quit Godot with non-zero status code when the tests fail
