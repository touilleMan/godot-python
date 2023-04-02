#! /usr/bin/env python

import os
import sys
import re
import platform
import shutil
from typing import Optional, Tuple
import subprocess
import argparse
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


GodotBinaryVersion = Tuple[str, str, str, str]
GodotBinaryPlatform = str


def log(*args, **kwargs):
    # Print logs to stderr given we will use stdout to return the path of Godot binary
    print(*args, **kwargs, file=sys.stderr)


def get_default_godot_version_from_meson(build_dir: Path) -> str:
    # Ultra lazy & fast json parsing ^^
    meson_build_options = build_dir / "meson-info/intro-buildoptions.json"
    version = (
        meson_build_options.read_text()
        .split('"name": "godot_version", "value": "', 1)[-1]
        .split('"', 1)[0]
    )
    assert version
    return version


def parse_raw_version(raw_version: str) -> GodotBinaryVersion:
    # Provided value is version information with format <major>.<minor>.<patch>[-<extra>]
    match = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-(\w+))?$", raw_version)
    if match:
        major, minor, patch, extra = match.groups()
    else:
        raise ValueError(
            f"`{raw_version}` is neither an existing file nor a valid <major>.<minor>.<patch>[-<extra>] Godot version format"
        )
    return (major, minor, patch, extra or "stable")


def parse_godot_binary_hint(
    godot_binary_hint: str,
) -> Tuple[GodotBinaryPlatform, Optional[GodotBinaryVersion]]:
    try:
        build_machine, raw_version = godot_binary_hint.split(":")
    except ValueError:
        build_machine = ""
        raw_version = godot_binary_hint

    # e.g. `build_machine == "x86"`
    build_machine = (build_machine or platform.machine()).lower()
    # e.g. `build_platform_prefix == "windows-"`
    build_platform_prefix = f"{platform.system()}-".lower()
    if build_machine.startswith(build_platform_prefix):
        build_platform = build_machine
    else:
        build_platform = build_platform_prefix + build_machine
    # e.g. `build_platform == "windows-x86"`

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

    # If version has not been provided, it will be determined later with `get_default_godot_version_from_meson()`
    version = parse_raw_version(raw_version) if raw_version else None
    return godot_build_platform, version


def fetch_godot_binary(
    build_dir: Path, godot_platform: GodotBinaryPlatform, version: Optional[GodotBinaryVersion]
) -> Path:
    if not version:
        version = parse_raw_version(get_default_godot_version_from_meson(build_dir))
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
        log(f"Downloading {url}...", flush=True)
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
                    log(
                        f"{buff.tell()//2**20}Mo/{length//2**20}Mo",
                        flush=True,
                        end="\r",
                    )
                log("", flush=True)
        zipfile = ZipFile(buff)
        if zippath not in zipfile.namelist():
            raise RuntimeError(f"Archive doesn't contain {zippath}")

        log(f"Decompressing {binary_path}...", flush=True)
        binary_path.write_bytes(zipfile.open(zippath).read())
        if platform.system() != "Windows":
            os.chmod(binary_path, 0o755)

    return binary_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "version",
        type=parse_godot_binary_hint,
        help="Version of Godot to download (e.g. `4.0.1`, `4.0.1-stable`, `linux-x86_64:4.0.1`)",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        required=True,
        help="Build directory as configured in meson",
    )
    parser.add_argument(
        "--generate-gdextension",
        action="store_true",
        help="Also generate gdextension_interface.h & extension_api.json",
    )
    args = parser.parse_args()

    godot_binary_path = fetch_godot_binary(args.build_dir, *args.version)

    if args.generate_gdextension:
        gdextension_dir = args.build_dir / "gdextension_api"
        gdextension_godot_dir = gdextension_dir / "godot"
        gdextension_godot_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                str(godot_binary_path.absolute()),
                "--headless",
                "--dump-extension-api",
                "--dump-gdextension-interface",
            ],
            stdout=sys.stderr,
            cwd=gdextension_dir,
            check=True,
        )
        shutil.move(
            src=gdextension_dir / "gdextension_interface.h",
            dst=gdextension_godot_dir / "gdextension_interface.h",
        )

    print(godot_binary_path.absolute())
