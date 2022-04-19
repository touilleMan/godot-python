#! /usr/bin/env python3

"""
Build system is designed to created a build targetting a single platform.
This script aims at bundle together multiple builds to generate a final
multi-platform release.
"""

import json
from pathlib import Path
from urllib.request import urlopen

import argparse
import tarfile
from datetime import datetime
import os
import shutil
from urllib.request import urlretrieve
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor


API_REPO_URL = "https://api.github.com/repos/touilleMan/godot-python/releases"
PLATFORMS = ("x11-32", "x11-64", "osx-64", "windows-32", "windows-64")
MISC_DIR = Path(__file__).parent / "../misc"


def get_release_info(version=None):
    data = json.loads(urlopen(API_REPO_URL).read())
    if not version:
        release_info = data[0]
    else:
        tag_name = version if version.startswith("v") else f"v{version}"
        release_info = next(x for x in data if x["tag_name"] == tag_name)

    info = {
        "tag_name": release_info["tag_name"],
        "version": release_info["tag_name"][1:],
        "platforms": {},
    }

    for platform in PLATFORMS:
        asset = next((asset for asset in release_info["assets"] if platform in asset["name"]), None)
        if asset:
            info["platforms"][platform] = {
                "name": asset["name"],
                "url": asset["browser_download_url"],
            }
        else:
            print(f"Warning: release info for platform {platform} not found")

    return info


def pipeline_executor(dirs, release_info, platform_name):
    platform_info = release_info["platforms"][platform_name]
    release_archive = dirs["build"] / platform_info["name"]

    if not release_archive.exists():
        print(f"{platform_name} - Dowloading release")
        with urlopen(platform_info["url"]) as f:
            release_archive.write_bytes(f.read())

    if not (dirs["pythonscript"] / platform_name).exists():
        print(f"{platform_name} - Extracting release")
        if platform_info["name"].endswith(".zip"):
            zipobj = ZipFile(release_archive)
            # Only extract platform-specific stuff
            members = (
                x
                for x in zipobj.namelist()
                if x.startswith(f"addons/pythonscript/{platform_name}/")
            )
            zipobj.extractall(path=dirs["dist"], members=members)

        elif platform_info["name"].endswith(".tar.bz2"):
            tarobj = tarfile.open(release_archive)
            # Only extract platform-specific stuff
            members = (
                x for x in tarobj if x.name.startswith(f"./addons/pythonscript/{platform_name}/")
            )
            tarobj.extractall(path=dirs["dist"], members=members)

        else:
            raise RuntimeError(f"Unknown archive format for {release_archive}")


def orchestrator(dirs, release_info):
    futures = []
    with ThreadPoolExecutor() as executor:
        for platform_name in release_info["platforms"].keys():
            futures.append(executor.submit(pipeline_executor, dirs, release_info, platform_name))
    for future in futures:
        if not future.cancelled():
            future.result()  # Raise exception if any

    print("Add bonuses...")

    (dirs["pythonscript"] / ".gdignore").touch()
    license_txt = (MISC_DIR / "release_LICENSE.txt").read_text()
    for entry in ["dist", "pythonscript"]:
        (dirs[entry] / "LICENSE.txt").write_text(license_txt)
    (dirs["dist"] / "pythonscript.gdnlib").write_text(
        (MISC_DIR / "release_pythonscript.gdnlib").read_text()
    )
    (dirs["dist"] / "README.txt").write_text(
        (MISC_DIR / "release_README.txt")
        .read_text()
        .format(version=release_info["version"], date=datetime.utcnow().strftime("%Y-%m-%d"))
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=None)
    args = parser.parse_args()

    release_info = get_release_info(args.version)
    print(f"Release version: {release_info['version']}")

    build_dir = Path(f"pythonscript-assetlib-release-{release_info['version']}").resolve()
    dist_dir = build_dir / f"pythonscript-{release_info['version']}"
    addons_dir = dist_dir / "addons"
    pythonscript_dir = addons_dir / "pythonscript"

    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    addons_dir.mkdir(exist_ok=True)
    pythonscript_dir.mkdir(exist_ok=True)

    dirs = {
        "build": build_dir,
        "dist": dist_dir,
        "addons": addons_dir,
        "pythonscript": pythonscript_dir,
    }
    orchestrator(dirs, release_info)

    print(f"{dist_dir} is ready !")


if __name__ == "__main__":
    main()
