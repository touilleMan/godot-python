from typing import Tuple
from pathlib import Path

import isengard


isg = isengard.get_parent()


### Godot binary (to run tests) ###


@isg.rule(output="godot_binary@")
def fetch_godot_binary(
    output: isengard.VirtualTargetResolver,
    build_platform_dir: Path,
    godot_binary_hint: Tuple[str, str, str, str],
    build_platform: str,
):
    import os
    from io import BytesIO
    from zipfile import ZipFile
    from urllib.request import urlopen

    last_binary_path = output.last_run_resolved
    assert last_binary_path is None or isinstance(last_binary_path, Path)

    godot_build_platform = {
        "linux-x86_64": "linux.64",
        "linux-x86": "linux.32",
        "windows-x86_64": "win64",
        "windows-x86": "win32",
        "osx-x86_64": "osx.universal",
    }.get(build_platform)
    if not godot_build_platform:
        raise RuntimeError(f"Godot doesn't seem to support platform `{build_platform}`")

    if isinstance(godot_binary_hint, Path):
        # Consider hint is pointing to an already existing binary
        binary_path = godot_binary_hint

    else:
        major, minor, patch, extra = godot_binary_hint
        version = f"{major}.{minor}.{patch}" if patch != "0" else f"{major}.{minor}"
        binary_name = f"Godot_v{version}-{extra}_{godot_build_platform}"
        if extra == "stable":
            url = f"https://downloads.tuxfamily.org/godotengine/{version}/Godot_v{version}-{extra}_{godot_build_platform}.zip"
        else:
            url = f"https://downloads.tuxfamily.org/godotengine/{version}/{extra}/Godot_v{version}-{extra}_{godot_build_platform}.zip"

        if build_platform[0] == "Darwin":
            zippath = "Godot.app/Contents/MacOS/Godot"
        else:
            zippath = binary_name
        binary_path = build_platform_dir / binary_name

        # TODO: properly handle `last_run_resolved`
        # if binary_path != last_binary_path or not last_binary_path.exists():
        if not binary_path.exists():
            print(f"Downloading {url}...")
            with urlopen(url) as rep:
                zipfile = ZipFile(BytesIO(rep.read()))
            if zippath not in zipfile.namelist():
                raise RuntimeError(f"Archive doesn't contain {zippath}")

            print(f"Decompressing {binary_path}...")
            binary_path.write_bytes(zipfile.open(zippath).read())
            if build_platform[0] != "Windows":
                os.chmod(binary_path, 0o755)

    output.resolve(binary_path)
