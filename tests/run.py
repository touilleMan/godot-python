#! /usr/bin/env python

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


DEFAULT_GODOT_BINARY_VERSION = "4.0.0-beta10"


BASEDIR = Path(__file__).resolve().parent
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NO_COLOR = "\033[0m"


GodotBinaryVersion = Tuple[str, str, str, str]
GodotBinaryPlatform = str


def parse_godot_binary_hint(
    godot_binary_hint: str,
) -> Union[Path, Tuple[GodotBinaryPlatform, GodotBinaryVersion]]:
    try:
        godot_binary_path = Path(godot_binary_hint).resolve()
        if godot_binary_path.is_file():
            return godot_binary_path
    except OSError:
        pass

    try:
        build_machine, raw_version = godot_binary_hint.split(":")
    except ValueError:
        build_machine = ""
        raw_version = godot_binary_hint
    raw_version = raw_version or DEFAULT_GODOT_BINARY_VERSION
    build_machine = build_machine or platform.machine()

    build_platform = f"{platform.system()}-{build_machine}".lower()
    godot_build_platform = {
        "linux-x86_64": "linux.x86_64",
        "linux-x64": "linux.x86_64",
        "linux-amd64": "linux.x86_64",
        "linux-x86": "linux.x86_32",
        "windows-x86_64": "win64",
        "windows-x64": "win64",
        "windows-amd64": "win64",
        "windows-x86": "win32",
        "darwin-x86_64": "macos.universal",
        "darwin-x64": "macos.universal",
        "darwin-amd64": "macos.universal",
    }.get(build_platform)
    if not godot_build_platform:
        raise RuntimeError(
            f"Don't know how to download a Godot binary for your platform `{build_platform}`"
        )

    # Provided value is version information with format <major>.<minor>.<patch>[-<extra>]
    match = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-(\w+))?$", raw_version)
    if match:
        major, minor, patch, extra = match.groups()
    else:
        raise ValueError(
            f"`{raw_version}` is neither an existing file nor a valid <major>.<minor>.<patch>[-<extra>] Godot version format"
        )
    return godot_build_platform, (major, minor, patch, extra or "stable")


def fetch_godot_binary(
    build_dir: Path, godot_platform: GodotBinaryPlatform, version: GodotBinaryVersion
) -> Path:
    major, minor, patch, extra = version
    strversion = f"{major}.{minor}.{patch}" if patch != "0" else f"{major}.{minor}"
    binary_name = f"Godot_v{strversion}-{extra}_{godot_platform}"
    if godot_platform.startswith("win"):
        binary_name += ".exe"
    if extra == "stable":
        url = f"https://downloads.tuxfamily.org/godotengine/{strversion}/{binary_name}.zip"
    else:
        url = f"https://downloads.tuxfamily.org/godotengine/{strversion}/{extra}/{binary_name}.zip"

    if godot_platform.startswith("osx"):
        zippath = "Godot.app/Contents/MacOS/Godot"
    else:
        zippath = binary_name
    binary_path = build_dir / binary_name

    if not binary_path.exists():
        print(f"Downloading {url}...", flush=True)
        buff = BytesIO()
        with urlopen(url) as rep:
            if not os.isatty(sys.stdout.fileno()):
                buff.write(rep.read())
            else:
                length = int(rep.headers.get("Content-Length"))
                # Poor's man progress bar
                while True:
                    if buff.write(rep.read(2**20)) == 0:
                        break
                    print(
                        f"{buff.tell()//2**20}Mo/{length//2**20}Mo",
                        flush=True,
                        end="\r",
                    )
                print("", flush=True)
        zipfile = ZipFile(buff)
        if zippath not in zipfile.namelist():
            raise RuntimeError(f"Archive doesn't contain {zippath}")

        print(f"Decompressing {binary_path}...", flush=True)
        binary_path.write_bytes(zipfile.open(zippath).read())
        if platform.system() != "Windows":
            os.chmod(binary_path, 0o755)

    return binary_path


def collect_tests() -> List[Path]:
    return [item for item in BASEDIR.iterdir() if (item / "project.godot").exists()]


def install_distrib(build_dir: Path, distrib_subdir: str) -> Path:
    distrib_workdir = build_dir / distrib_subdir
    print(f"{YELLOW}Generate distrib for tests {distrib_workdir}{NO_COLOR}", flush=True)
    cmd = [
        "meson",
        "install",
        "-C",
        str(build_dir),
        "--only-changed",  # Prevent from copying Python distrib over and over
        "--destdir",
        distrib_subdir,
    ]
    print(" ".join(cmd), flush=True)
    subprocess.check_call(cmd)

    for platform_dir in (distrib_workdir / "addons/pythonscript").iterdir():
        if "windows" in platform_dir.name.lower():
            python_path = platform_dir / "python.exe"
            break
        elif "linux" in platform_dir.name.lower():
            python_path = platform_dir / "bin/python3"
            break
        elif "macos" in platform_dir.name.lower():
            python_path = platform_dir / "bin/python3"
            break

    # We also have to install Cython to compile the projects
    if (
        subprocess.run(
            [str(python_path), "-m", "cython", "--version"], capture_output=True
        ).returncode
        != 0
    ):
        cmd = [str(python_path), "-m", "ensurepip"]
        print(" ".join(cmd), flush=True)
        subprocess.check_call(cmd)
        cmd = [str(python_path), "-m", "pip", "install", "cython"]
        print(" ".join(cmd), flush=True)
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

        _winapi.CreateJunction(str(src.resolve()), str(dst.resolve()))  # type: ignore[attr-defined]

    else:
        os.symlink(str(src.resolve()), str(dst.resolve()))


def create_test_workdir(test_dir: Path, distrib_workdir: Path, test_workdir: Path) -> None:
    print(
        f"{YELLOW}{test_dir.name}: Create&populate test workdir in {test_workdir}{NO_COLOR}",
        flush=True,
    )
    shutil.copytree(test_dir, test_workdir, dirs_exist_ok=True)
    symlink(distrib_workdir / "addons", test_workdir / "addons")
    shutil.copy(distrib_workdir / "pythonscript.gdextension", test_workdir)
    # Godot headers are needed to compile Cython modules
    symlink(test_dir / "../../godot_headers", test_workdir / "godot_headers")

    build_script = test_workdir / "build.py"
    if build_script.exists():
        print(
            f"{YELLOW}{test_dir.name}: Running build script {build_script}{NO_COLOR}",
            flush=True,
        )
        cmd = [sys.executable, str(build_script)]
        print(" ".join(cmd), flush=True)
        subprocess.check_call(cmd)


def run_test(
    test_name: str, test_workdir: Path, godot_binary: Path, extra_args: Sequence[str]
) -> None:
    print(
        f"{YELLOW}{test_name}: Running test in workdir {test_workdir}{NO_COLOR}",
        flush=True,
    )
    cmd = [
        str(godot_binary.resolve()),
        "--path",
        str(test_workdir.resolve()),
        *extra_args,
    ]
    print(" ".join(cmd), flush=True)
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    total_output = b""
    while True:
        buff: bytes = res.stdout.read1()
        total_output += buff
        os.write(sys.stdout.fileno(), buff)
        try:
            res.wait(timeout=0.1)
            break
        except subprocess.TimeoutExpired:
            # Subprocess is still running
            pass
    if res.returncode != 0:
        raise SystemExit(f"{RED}{test_name}: Non-zero return code: {res.returncode}{NO_COLOR}")
    for line in total_output.splitlines():
        # See https://github.com/godotengine/godot/issues/66722
        if b"Message Id Number: 0 | Message Id Name: Loader Message" in line:
            continue
        if b"lavapipe is not a conformant vulkan implementation, testing use only." in line:
            continue
        lower_line = line.lower()
        if b"error" in lower_line or b"warning" in lower_line:
            raise SystemExit(
                f"{RED}{test_name}: stdout/stderr contains logs with error and/or warning ({line}){NO_COLOR}"
            )
    print(f"{GREEN}{test_name}: All good \\o/{NO_COLOR}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tests", nargs="*", help="Filter the tests to run", default=["helloworld"])
    parser.add_argument(
        "--build-dir",
        type=Path,
        required=True,
        help="Build directory as configured in meson",
    )
    parser.add_argument(
        "--test-dir",
        type=Path,
        help="Use an existing test dir instead of creating a temporary one",
    )
    parser.add_argument(
        "--godot-binary",
        type=parse_godot_binary_hint,
        default=DEFAULT_GODOT_BINARY_VERSION,
        help="Path to Godot binary to use, or version of Godot to download and use",
    )
    parser.add_argument(
        "--keep-test-dir",
        action="store_true",
        help="Don't remove the temporary directory used for the test",
    )
    parser.add_argument(
        "--only-refresh-common",
        action="store_true",
        help="Only update the addons build symlinked into all test projects",
    )

    try:
        options_separator = sys.argv.index("--")
    except ValueError:
        options_separator = len(sys.argv)

    args = parser.parse_args(sys.argv[1:options_separator])
    godot_extra_args = sys.argv[options_separator + 1 :]

    if args.tests:
        tests_dirs = [x for x in collect_tests() if x.name in args.tests]
        if not tests_dirs:
            raise SystemExit(
                f"No test selected, available tests: {[x.name for x in collect_tests()]}"
            )
    else:
        tests_dirs = collect_tests()

    build_dir = args.build_dir.resolve()

    if isinstance(args.godot_binary, Path):
        godot_binary_path = args.godot_binary
    else:
        godot_binary_path = fetch_godot_binary(build_dir, *args.godot_binary)

    # Install the distrib, it is common to each test and kept between run to save time
    distrib_workdir = install_distrib(build_dir, "common_tests_install_distrib")
    if args.only_refresh_common:
        raise SystemExit(0)

    @contextmanager
    def test_workdir_factory():
        if args.test_dir:
            yield args.test_dir
        else:
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
                test_dir=test_dir,
                distrib_workdir=distrib_workdir,
                test_workdir=test_workdir,
            )
            run_test(test_dir.name, test_workdir, godot_binary_path, godot_extra_args)
