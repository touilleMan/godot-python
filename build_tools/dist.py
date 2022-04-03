from typing import List, Tuple
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
    # inputs=["{build_pythonscript_dir}/pythonscript.so", "{build_platform_dir}/cpython_distrib/"],
    inputs=[
        "pythonscript_lib@",
        "underscore_pythonscript_lib@",
        "{build_platform_dir}/cpython_distrib/",
        "{rootdir}/pythonscript/godot/",
    ],
)
def dist_addons(
    output: Path,
    inputs: Tuple[isengard.VirtualTargetResolver, isengard.VirtualTargetResolver, Path],
    host_platform: str,
) -> None:
    *libs_items, cpython_distrib, godot_py = inputs
    platform_output = output / "pythonscript" / host_platform
    if not platform_output.exists():  # TODO: remove me
        platform_output.parent.mkdir(parents=True, exist_ok=True)
        # Put CPython distrib into the plaform dir and add pythonscript.so
        shutil.copytree(cpython_distrib, platform_output, symlinks=True)
    for lib_items in libs_items:
        for item in lib_items:
            shutil.copy(item, platform_output)
    # Copy .py files
    # TODO: make this cleaner !
    godot_dir = platform_output / "Lib/site-packages/godot"
    godot_dir.mkdir(parents=True, exist_ok=True)
    for py in godot_py.glob("*.py"):
        if py.name == "BUILD.py":
            continue
        shutil.copy(py, godot_dir)
