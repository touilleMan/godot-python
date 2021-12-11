import pytest
from typing import List
from pathlib import Path

import isengard


@pytest.fixture
def isg(tmp_path):
    isg = isengard.Isengard(
        self_file=tmp_path / "build.py", db=tmp_path / ".isengard.sqlite"
    )

    @isg.rule(output="x.o", input="x.c")
    @isg.rule(output="y.o", input="y.c")
    @isg.rule(output="z.o", input="z.c")
    def compile_c(output: Path, input: Path, basedir: Path):
        isg.events.append(
            f"cc -c {input.relative_to(basedir)} -o {output.relative_to(basedir)}"
        )
        output.touch()

    @isg.rule(output="a.out", inputs=["x.o", "y.o"])
    def link_c(output: Path, inputs: List[Path], basedir: Path):
        isg.events.append(
            f"cc -c {input.relative_to(basedir)} -o {output.relative_to(basedir)}"
        )
        output.touch()

    isg.test_output = tmp_path / "a.out"
    isg.test_inputs = []
    for name in ["x.c", "y.c", "z.c"]:
        path = tmp_path / name
        isg.test_inputs.append(path)
        path.touch()
    (tmp_path / "build.py").touch()

    isg.test_events = []
    return isg
