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
    if output.exists():  # TODO: remove me
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(input, output)


@isg.rule(
    output="{build_dir}/dist/addons/",
    inputs=["{build_pythonscript_dir}/pytonscript.so", "{build_platform_dir}/cpython_distrib/"],
)
def dist_addons(
    output: Path,
    inputs: List[Path],
    host_platform: str,
) -> None:
    if output.exists():  # TODO: remove me
        return
    pythonscript_so, cpython_distrib = inputs
    platform_output = output / "pythonscript" / host_platform
    platform_output.parent.mkdir(parents=True, exist_ok=True)
    # Put CPython distrib into the plaform dir and add pythonscript.so
    shutil.copytree(cpython_distrib, platform_output, symlinks=True)
    shutil.copy(pythonscript_so, platform_output)
