#! /usr/bin/env python3

import os
import sys
import re
import platform
from typing import List, Tuple, Union, Sequence
from contextlib import contextmanager
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
        "linux-x64": "linux.64",
        "linux-amd64": "linux.64",
        "linux-x86": "linux.32",
        "windows-x86_64": "win64",
        "windows-x64": "win64",
        "windows-amd64": "win64",
        "windows-x86": "win32",
        "darwin-x86_64": "osx.universal",
        "darwin-x64": "osx.universal",
        "darwin-amd64": "osx.universal",
    }.get(build_platform)
    if not godot_build_platform:
        raise RuntimeError(
            f"Don't know how to download a Godot binary for your platform `{build_platform}`"
        )

    major, minor, patch, extra = version
    strversion = f"{major}.{minor}.{patch}" if patch != "0" else f"{major}.{minor}"
    binary_name = f"Godot_v{strversion}-{extra}_{godot_build_platform}"
    if build_platform.startswith("windows"):
        binary_name += ".exe"
    if extra == "stable":
        url = f"https://downloads.tuxfamily.org/godotengine/{strversion}/{binary_name}.zip"
    else:
        url = f"https://downloads.tuxfamily.org/godotengine/{strversion}/{extra}/{binary_name}.zip"

    if godot_build_platform.startswith("osx"):
        zippath = "Godot.app/Contents/MacOS/Godot"
    else:
        zippath = binary_name
    binary_path = build_dir / binary_name

    if not binary_path.exists():
        print(f"Downloading {url}...")
        with urlopen(url) as rep:
            length = rep.headers.get("Content-Length")
            # Poor's man progress bar
            buff = BytesIO()
            while True:
                if buff.write(rep.read(2**20)) == 0:
                    break
                print(f"{buff.tell()}/{length}", flush=True, end="\r")
        print("", flush=True)
        zipfile = ZipFile(buff)
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
    # Python's `os.symlink` doesn't work on Windows...
    # Well it kind of work: you must use Python>=3.8 and have administrator privilege
    # or have "Developer Mode" enabled (wtf is that, I guess you have to do a Konami
    # code in 3D Pinball Space Cadet to enable it).
    # The funny thing is Windows also has a concept of "junction point" that are
    # basically symlink for folder (though not what Python uses in `os.symlink`,
    # even if this function contains a `target_is_directory` param only for Windows
    # that could have totally let you think junction point is used...).
    # But there is more ! Python actually has a junction point creation function,
    # though it is in a private module so we are not supposed to use it, but yolo ;-)
    if platform.system() == "Windows":
        import _winapi

        _winapi.CreateJunction(str(src.resolve()), str(dst.resolve()))

    else:
        os.symlink(str(src.resolve()), str(dst.resolve()))


def create_test_workdir(test_dir: Path, distrib_workdir: Path, test_workdir: Path) -> None:
    print(f"### {test_dir.name}: Create&populate test workdir in {test_workdir}")
    shutil.copytree(test_dir, test_workdir, dirs_exist_ok=True)
    symlink(distrib_workdir / "addons", test_workdir / "addons")
    shutil.copy(distrib_workdir / "pythonscript.gdextension", test_workdir)


def run_test(
    test_name: str, test_workdir: Path, godot_binary: Path, extra_args: Sequence[str]
) -> None:
    print(f"### {test_name}: Running test in workdir {test_workdir}")
    cmd = [str(godot_binary.resolve()), "--path", str(test_workdir.resolve()), *extra_args]
    print(" ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tests", nargs="*", help="Filter the tests to run", default=["helloworld"])
    parser.add_argument(
        "--build-dir", type=Path, required=True, help="Build directory as configured in meson"
    )
    parser.add_argument(
        "--godot-binary",
        type=parse_godot_binary_hint,
        default="4.0.0-alpha13",
        help="Path to Godot binary to use, or version of Godot to download and use",
    )
    parser.add_argument(
        "--keep-test-dir",
        action="store_true",
        help="Don't remove the temporary directory used for the test",
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

    @contextmanager
    def test_workdir_factory():
        temp_dir = TemporaryDirectory(prefix="godot-python-test-")
        try:
            yield Path(temp_dir.name)
        finally:
            if not args.keep_test_dir:
                temp_dir.cleanup()
            else:
                temp_dir._finalizer.detach()  # Avoid cleanup when temp_dir is garbage collected

    # On the other hand we use a temporary directory for the test code (given there
    # is not much data, and Godot may write in this directory during the test) with
    # symlinks on the distrib
    for test_dir in tests_dirs:
        with test_workdir_factory() as test_workdir:
            create_test_workdir(
                test_dir=test_dir, distrib_workdir=distrib_workdir, test_workdir=test_workdir
            )
            run_test(test_dir.name, test_workdir, godot_binary_path, godot_extra_args)
