#! /usr/bin/env python3

import os
import sys
import re
import platform
from typing import List, Tuple, Union, Sequence
import argparse
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


BASEDIR = Path(__file__).resolve().parent


GodotBinaryVersion = Tuple[str, str, str, str]


def parse_godot_binary_hint(godot_binary_hint: str) -> Union[Path, GodotBinaryVersion]:
    godot_binary_path = Path(godot_binary_hint).resolve()
    if godot_binary_path.exists():
        return godot_binary_path

    # Provided value is version information with format <major>.<minor>.<patch>[-<extra>]
    match = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-(\w+))?$", godot_binary_hint)
    if match:
        major, minor, patch, extra = match.groups()
    else:
        raise ValueError(
            f"`{godot_binary_hint}` is neither an existing file nor a valid <major>.<minor>.<patch>[-<extra>] Godot version format"
        )
    return (major, minor, patch, extra or "stable")


def fetch_godot_binary(build_dir: Path, version: GodotBinaryVersion) -> Path:
    build_platform = f"{platform.system()}-{platform.machine()}".lower()
    godot_build_platform = {
        "linux-x86_64": "linux.64",
        "linux-x86": "linux.32",
        "windows-x86_64": "win64",
        "windows-x86": "win32",
        "osx-x86_64": "osx.universal",
    }.get(build_platform)
    if not godot_build_platform:
        raise RuntimeError(
            f"Don't know how to download a Godot binary for your platform `{platform}`"
        )

    major, minor, patch, extra = version
    strversion = f"{major}.{minor}.{patch}" if patch != "0" else f"{major}.{minor}"
    binary_name = f"Godot_v{strversion}-{extra}_{godot_build_platform}"
    if extra == "stable":
        url = f"https://downloads.tuxfamily.org/godotengine/{strversion}/Godot_v{strversion}-{extra}_{godot_build_platform}.zip"
    else:
        url = f"https://downloads.tuxfamily.org/godotengine/{strversion}/{extra}/Godot_v{strversion}-{extra}_{godot_build_platform}.zip"

    if godot_build_platform.startswith("osx"):
        zippath = "Godot.app/Contents/MacOS/Godot"
    else:
        zippath = binary_name
    binary_path = build_dir / binary_name

    if not binary_path.exists():
        print(f"Downloading {url}...")
        with urlopen(url) as rep:
            zipfile = ZipFile(BytesIO(rep.read()))
        if zippath not in zipfile.namelist():
            raise RuntimeError(f"Archive doesn't contain {zippath}")

        print(f"Decompressing {binary_path}...")
        binary_path.write_bytes(zipfile.open(zippath).read())
        if platform.system() != "Windows":
            os.chmod(binary_path, 0o755)

    return binary_path


def collect_tests() -> List[Path]:
    return [item for item in BASEDIR.iterdir() if (item / "project.godot").exists()]


def install_distrib(build_dir: Path, distrib_subdir: str) -> Path:
    distrib_workdir = build_dir / distrib_subdir
    print(f"### Generate distrib for tests {distrib_workdir}")
    cmd = [
        "meson",
        "install",
        "-C",
        str(build_dir),
        "--only-changed",  # Prevent from copying Python distrib over and over
        "--destdir",
        distrib_subdir,
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd)
    return distrib_workdir


def symlink(src: Path, dst: Path) -> None:
    if platform.system() == "Windows":
        import _winapi

        _winapi.CreateJunction(str(src.resolve()), str(dst.resolve()))

    else:
        os.symlink(str(src.resolve()), str(dst.resolve()))


def create_test_workdir(test_dir: Path, distrib_workdir: Path, test_workdir: Path) -> None:
    print(f"### Create&populate test workdir in {test_workdir}")
    shutil.copytree(test_dir, test_workdir, dirs_exist_ok=True)
    symlink(distrib_workdir / "addons", test_workdir / "addons")
    shutil.copy(distrib_workdir / "pythonscript.gdextension", test_workdir)


def run_test(test_workdir: Path, godot_binary: Path, extra_args: Sequence[str]) -> None:
    print(f"### Running test in workdir {test_workdir}")
    cmd = [str(godot_binary.resolve()), "--path", str(test_workdir.resolve()), *extra_args]
    print(" ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tests", nargs="*", help="Filter the tests to run")
    parser.add_argument(
        "--build-dir", type=Path, required=True, help="Build directory as configured in meson"
    )
    parser.add_argument(
        "--godot-binary",
        required=True,
        type=parse_godot_binary_hint,
        help="Path to Godot binary to use, or version of Godot to download and use",
    )

    try:
        options_separator = sys.argv.index("--")
    except ValueError:
        options_separator = len(sys.argv)

    args = parser.parse_args(sys.argv[1:options_separator])
    godot_extra_args = sys.argv[options_separator:]

    if args.tests:
        tests_dirs = [x for x in collect_tests() if x.name in args.tests]
    else:
        tests_dirs = collect_tests()

    build_dir = args.build_dir.resolve()

    if isinstance(args.godot_binary, Path):
        godot_binary_path = args.godot_binary
    else:
        godot_binary_path = fetch_godot_binary(build_dir, args.godot_binary)

    # Install the distrib, it is common to each test and kept between run to save time
    distrib_workdir = install_distrib(build_dir, "common_tests_install_distrib")

    # On the other hand we use a temporary directory for the test code (given there
    # is not much data, and Godot may write in this directory during the test) with
    # symlinks on the distrib
    for test_dir in tests_dirs:
        with TemporaryDirectory(prefix="godot-python-test") as raw_test_workdir:
            test_workdir = Path(raw_test_workdir)
            create_test_workdir(
                test_dir=test_dir, distrib_workdir=distrib_workdir, test_workdir=test_workdir
            )
            run_test(test_workdir, godot_binary_path, godot_extra_args)
