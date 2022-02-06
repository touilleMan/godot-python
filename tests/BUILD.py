from typing import Tuple
from pathlib import Path
import subprocess
import isengard


isg = isengard.get_parent()


def symlink(src: Path, trg: Path):
    try:
        import _winapi

        _winapi.CreateJunction(str(src), str(trg))
    except Exception:
        import os

        os.symlink(str(src), str(trg))


def rule_install_extension_in_test_dir(test_name: str) -> str:
    @isg.rule(
        output=f"{test_name}/addons#",
        inputs=[f"{test_name}/", "{build_dir}/dist/"],
    )
    def symlink_addons(
        output: Path,
        inputs: Tuple[Path, Path],
    ) -> None:
        _, dist_path = inputs
        # TODO: remove me
        if output.exists():
            return
        symlink(dist_path / "addons", output)

    @isg.rule(
        output=f"{test_name}/lib#",
        inputs=[
            f"{test_name}/",
            "_lib_vendors/",
        ],
    )
    def symlink_lib_vendors(
        output: Path,
        inputs: Tuple[Path, Path],
    ) -> None:
        _, lib_vendors_path = inputs
        # TODO: remove me
        if output.exists():
            return
        symlink(lib_vendors_path, output)

    @isg.rule(
        outputs=[f"run_{test_name}@", f"tests/{test_name}@"],
        inputs=["godot_binary@", f"{test_name}/", f"{test_name}/addons#", f"{test_name}/lib#"],
    )
    def run_test(
        outputs: Tuple[isengard.VirtualTargetResolver, isengard.VirtualTargetResolver],
        inputs: Tuple[Path, Path, Path],
        debugger: str,
        pytest_args: Tuple[str],
        godot_args: Tuple[str],
        headless: bool,
    ) -> None:
        godot_binary, test_path, *_ = inputs

        if debugger:
            cmd_prefix = [debugger, "-ex", "r", "--args"]
        else:
            cmd_prefix = []

        if pytest_args:
            cmd_suffix = [f"--pytest={arg}" for arg in pytest_args]
        else:
            cmd_suffix = []

        if headless:
            cmd_suffix.append("--no-window")

        cmd = [*cmd_prefix, str(godot_binary), *godot_args, "--path", str(test_path), *cmd_suffix]
        print(" ".join(cmd))
        subprocess.check_call(cmd)

    return f"tests/{test_name}@"


tests = [rule_install_extension_in_test_dir("helloworld")]


@isg.rule(output="tests@", inputs=tests)
def run_all_tests(output, inputs):
    pass
