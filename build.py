import re
import platform
from pathlib import Path
from typing import Callable, Optional, Tuple, FrozenSet
import argparse

import isengard

from build_tools.c import IsengardCMixin


class CustomizedIsengard(IsengardCMixin, isengard.Isengard):
    pass


isg = CustomizedIsengard(__file__, subdir_default_filename="BUILD.py")


# isg.subscript("build_tools/dist.py")
# isg.subscript("build_tools/godot_binary.py")
# isg.subscript("build_tools/python_distrib.py")
isg.subdir("pythonscript")
# isg.subdir("tests")


@isg.lazy_config
def cflags(cc_is_msvc: bool, build_type: str) -> FrozenSet[str]:
    if cc_is_msvc:
        args = ("/WX", "/W2")
    else:
        args = ["-Werror-implicit-function-declaration", "-fcolor-diagnostics", "-m64"]
        if build_type == "release":
            args += ("-O2", "-m64")
        else:
            assert build_type == "debug"
    return frozenset(args)


@isg.lazy_config
def linkflags(host_platform: str):
    return ("-m64",)


if __name__ == "__main__":

    def _parse_host_cypthon_version_argument(val):
        if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", val):
            raise ValueError(f"`{val}` doesn't respect the <major>.<minor>.<patch> version format")
        return val

    def _parse_godot_binary_argument(val):
        file = Path(val)
        if file.exists():
            return file
        # Provided value is version information with format <major>.<minor>.<patch>[-<extra>]
        match = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-(\w+))?$", val)
        if match:
            major, minor, patch, extra = match.groups()
        else:
            raise ValueError(
                f"`{val}` is neither an existing file nor a valid <major>.<minor>.<patch>[-<extra>] Godot version format"
            )
        return (major, minor, patch, extra or "stable")

    parser = argparse.ArgumentParser(description="Build the project")
    parser.add_argument("target")
    parser.add_argument(
        "--host-cpython-version",
        help="Version of CPython that will be shipped in the extension (default: 3.9.7)",
        default="3.9.7",
        type=_parse_host_cypthon_version_argument,
    )
    parser.add_argument(
        "--godot-binary",
        help="Path to Godot binary or version of Godot to use (default: 4.0.0-alpha1)",
        default="4.0.0-alpha1",
        type=_parse_godot_binary_argument,
    )
    parser.add_argument(
        "--godot-headers",
        help="Path to Godot headers directory",
        default="./godot_headers",
        type=lambda x: Path(x).resolve().absolute(),
    )
    parser.add_argument(
        "--dump-graph",
        help="Display dependency graph",
        action="store_true",
    )
    parser.add_argument(
        "--build-type",
        help="Build configuration: debug (default) or release",
        default="debug",
        choices=("debug", "release"),
    )
    parser.add_argument(
        "--build-dir",
        help="Path the build directory",
        default="build",
        type=lambda x: Path(x).resolve().absolute(),
    )
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    def get_build_platform():
        build_platform = ""

        # TODO: support Apple M1 ?

        system = platform.system()
        if system == "Linux":
            build_platform += "linux"
        elif system == "Windows":
            build_platform += "windows"
        elif system == "Darwin":
            build_platform += "osx"
        else:
            raise RuntimeError(f"Unsupported system {system}")

        machine = platform.machine()
        if machine in ("i386", "x86"):
            build_platform += "-x86"
        elif machine in ("AMD64", "x86_64"):
            build_platform += "-x86_64"
        else:
            raise RuntimeError(f"Unknown machine {machine}")

        return build_platform

    build_platform = get_build_platform()
    host_platform = build_platform  # No cross-compilation

    build_dir = args.build_dir
    build_platform_dir = build_dir / host_platform
    build_platform_dir.mkdir(parents=True, exist_ok=True)
    dist_dir = build_dir / "dist"

    isg.configure(
        build_platform=build_platform,
        host_platform=host_platform,
        build_type=args.build_type,
        build_dir=build_dir,
        build_platform_dir=build_platform_dir,
        dist_dir=dist_dir,
        dist_platform_dir=dist_dir / host_platform,
        godot_binary_hint=args.godot_binary,
        godot_headers=args.godot_headers,
        cpython_compressed_stdlib=True,
        host_cpython_version=args.host_cpython_version,
        godot_args=(),
        pytest_args=(),
        debugger="",
        headless=False,
        cython_flags=("-3", "--fast-fail"),
        cc_is_msvc=host_platform.startswith("windows"),
        cc="cl.exe" if host_platform.startswith("windows") else "clang",
        ld="link.exe" if host_platform.startswith("windows") else "clang",
    )

    if args.target == "targets":
        # TODO
        for raw, configured in isg.list_targets():
            # if isinstance(target, Path):
            #     target = target.relative_to(isg.rootdir)
            print(raw, configured)
    else:
        try:
            if args.dump_graph:
                print(isg.dump_graph(args.target, display_configured=True))
            isg.run(args.target)
        except isengard.IsengardError as exc:
            if args.debug:
                raise
            else:
                raise SystemExit(f"Run has failed: {exc}")
