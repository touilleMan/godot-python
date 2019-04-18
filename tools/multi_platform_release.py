#! /usr/bin/env python3

"""
Build system is designed to created a build targetting a single platform.
This script aims at bundle together multiple builds to generate a final
multi-platform release.
"""

import argparse
from datetime import datetime
import os
import shutil
from urllib.request import urlretrieve
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor


BASEDIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = "https://github.com/touilleMan/godot-python/releases/download"
DEFAULT_BACKEND = "cpython"
DEFAULT_PLATFORMS_PER_BACKEND = {
    "cpython": ["osx-64", "windows-32", "windows-64", "x11-64"],
    "pypy": ["osx-64", "windows-32", "x11-64"],
}


def fetch_build(src, version, target):
    build_zipname = "godot-python-%s-%s.zip" % (version, target)
    if src.startswith("http://") or src.startswith("https://"):
        cache_file = build_zipname
        if not os.path.exists(cache_file):
            url = "%s/%s/%s" % (src, version, build_zipname)
            urlretrieve(
                url,
                filename=build_zipname,
                reporthook=lambda *args: print(".", end="", flush=True),
            )
        return ZipFile(cache_file)

    else:
        return ZipFile("%s/%s" % (src, build_zipname))


def extract_build(target, zipobj, dst):
    build_dst = "%s/pythonscript/%s" % (dst, target)
    extract_tmp = "%s-tmp" % build_dst
    zipobj.extractall(extract_tmp)
    shutil.move("%s/pythonscript" % extract_tmp, build_dst)
    shutil.rmtree(extract_tmp)
    return zipobj


def pipeline_executor(target, version, src, dst):

    print("%s - fetch build..." % target)
    zipbuild = fetch_build(src, version, target)

    print("%s - extract build..." % target)
    extract_build(target, zipbuild, dst)


def orchestrator(targets, version, src, dst, buildzip):
    futures = []
    with ThreadPoolExecutor() as executor:
        for target in targets:
            futures.append(
                executor.submit(pipeline_executor, target, version, src, dst)
            )
    for future in futures:
        if not future.cancelled():
            future.result()  # Raise exception if any

    print("add bonuses...")
    shutil.copy(
        "%s/../misc/release_pythonscript.gdnlib" % BASEDIR,
        "%s/pythonscript.gdnlib" % dst,
    )
    shutil.copy("%s/../misc/release_LICENSE.txt" % BASEDIR, "%s/LICENSE.txt" % dst)
    with open("%s/../misc/release_README.txt" % BASEDIR) as fd:
        readme = fd.read().format(
            version=version, date=datetime.utcnow().strftime("%Y-%m-%d")
        )
    with open("%s/README.txt" % dst, "w") as fd:
        fd.write(readme)

    if buildzip:
        print("zipping result...")
        shutil.make_archive(dst, "zip", dst)


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--backend", "-b", choices=("cpython", "pypy"), default=DEFAULT_BACKEND
    )
    parser.add_argument("--platforms", "-p", nargs="+")
    parser.add_argument("--src", default=DEFAULT_SRC)
    parser.add_argument("--no-zip", action="store_true")
    parser.add_argument("version")
    args = parser.parse_args()

    dst = "pythonscript-%s" % args.version
    try:
        shutil.os.mkdir(dst)
        shutil.os.mkdir("%s/pythonscript" % dst)
    except Exception:
        pass
    platforms = args.platforms or DEFAULT_PLATFORMS_PER_BACKEND[args.backend]
    targets = ["%s-%s" % (p, args.backend) for p in platforms]
    orchestrator(targets, args.version, args.src, dst, not args.no_zip)


if __name__ == "__main__":
    main()
