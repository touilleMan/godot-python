import clodotest
from pathlib import Path


BASEDIR = Path(__file__).absolute().parent


def initialize(level: int):
    if level < 3:
        return
    assert level == 3

    clodotest.run_tests(path=BASEDIR / "tests", filter=None, stop_on_failure=True, quiet=True)
