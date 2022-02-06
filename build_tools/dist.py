from typing import List
from pathlib import Path
import shutil

import isengard


isg = isengard.get_parent()


@isg.rule(
    output="{build_dir}/dist/",
    # TODO: support globbing in inputs
    # inputs=["{build_dir}/dist/**"],
    inputs=["{build_dir}/dist/pythonscript.gdextension", "{build_dir}/dist/addons/"],
)
def dist(
    output: Path,
    inputs: List[Path],
) -> None:
    pass


# TODO: support simple copy metarule
@isg.rule(
    output="{build_dir}/dist/pythonscript.gdextension",
    input="../misc/release_pythonscript.gdextension",
)
def dist_gdextension(
    output: Path,
    input: Path,
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy(input, output)


@isg.rule(
    output="{build_dir}/dist/addons/",
    inputs=["{build_pythonscript_dir}/pytonscript.so"],
)
def dist_addons(
    output: Path,
    inputs: List[Path],
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy(inputs[0], output)
