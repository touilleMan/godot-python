#! /usr/bin/env python3

import argparse
from pathlib import Path
import re
from urllib.request import urlopen
import shutil
import tarfile
import json
from compression import zstd, gzip


PREBUILDS_BASE_URL = "https://github.com/astral-sh/python-build-standalone/releases/download"
PLATFORM_TO_PREBUILDS = {
    "3.14.2": {
        "linux-x86_64": f"{PREBUILDS_BASE_URL}/20251205/cpython-3.14.2+20251205-x86_64_v3-unknown-linux-gnu-pgo+lto-full.tar.zst",
        "windows-x86": f"{PREBUILDS_BASE_URL}/20251205/cpython-3.14.2+20251205-i686-pc-windows-msvc-pgo-full.tar.zst",
        "windows-x86_64": f"{PREBUILDS_BASE_URL}/20251205/cpython-3.14.2+20251205-x86_64-pc-windows-msvc-pgo-full.tar.zst",
        "macos-x86_64": f"{PREBUILDS_BASE_URL}/20251205/cpython-3.14.2+20251205-x86_64-apple-darwin-pgo+lto-full.tar.zst",
    },
    "3.13.7": {
        "linux-x86_64": f"{PREBUILDS_BASE_URL}/20250902/cpython-3.13.7+20250902-x86_64_v3-unknown-linux-gnu-pgo+lto-full.tar.zst",
        "windows-x86": f"{PREBUILDS_BASE_URL}/20250902/cpython-3.13.7+20250902-i686-pc-windows-msvc-pgo-full.tar.zst",
        "windows-x86_64": f"{PREBUILDS_BASE_URL}/20250902/cpython-3.13.7+20250902-x86_64-pc-windows-msvc-pgo-full.tar.zst",
        "macos-x86_64": f"{PREBUILDS_BASE_URL}/20250902/cpython-3.13.7+20250902-x86_64-apple-darwin-pgo+lto-full.tar.zst",
    },
}


def fetch_prebuild(
    host_platform: str, cpython_version: str, workdir: Path, prebuild_dir: Path, force: bool
) -> None:
    try:
        per_platform = PLATFORM_TO_PREBUILDS[cpython_version]
    except KeyError:
        raise SystemExit(
            f"Unsupported CPython version `{cpython_version}`, valid values are: {', '.join(PLATFORM_TO_PREBUILDS.keys())}"
        )
    try:
        archive_url = per_platform[host_platform]
    except KeyError:
        raise SystemExit(f"No CPython prebuild for host_platform `{host_platform}`")

    archive_name = archive_url.rsplit("/", 1)[1]
    archive_path = workdir / archive_name
    if not archive_path.exists() or force:
        print(f"Downloading {archive_url} ...")
        tmp_archive_path = archive_path.parent / f"{archive_path.name}.tmp"
        with urlopen(archive_url) as rep:
            with open(tmp_archive_path, "bw") as outfd:
                length = int(rep.headers.get("Content-Length"))
                # Poor's man progress bar
                print(f"0Mo/{length // 2**20}Mo", flush=True, end="\r")
                while True:
                    if outfd.write(rep.read(2**20)) == 0:
                        break
                    print(f"{outfd.tell() // 2**20}Mo/{length // 2**20}Mo", flush=True, end="\r")

        shutil.move(tmp_archive_path, archive_path)

    if force and prebuild_dir.exists():
        shutil.rmtree(prebuild_dir)

    if not prebuild_dir.exists():
        print(f"Extracting {archive_path}...")

        def _tar_extract(reader):
            with tarfile.open(mode="r|", fileobj=reader) as tf:
                tf.extractall(prebuild_dir)

        if archive_path.suffix == ".gz":
            with gzip.open(archive_path, mode="rb") as reader:
                _tar_extract(reader)
        else:
            assert archive_path.suffix == ".zst"
            with open(archive_path, mode="rb") as fh:
                reader = zstd.ZstdFile(fh)
                _tar_extract(reader)


def load_config(prebuild_dir: Path) -> dict:
    conf = json.loads((prebuild_dir / "python/PYTHON.json").read_text())
    assert conf["version"] in (
        "7",
        "8",
    ), f"Unsupported PYTHON.json format version {conf['version']}"
    assert conf["libpython_link_mode"] == "shared"
    return conf


def install_linux(
    conf: dict,
    build_dir: Path,
    prebuild_dir: Path,
    compressed_stdlib: bool,
    without_pyc: bool,
    without_ensurepip: bool,
    without_pip: bool,
) -> None:
    print(f"Create clean distribution {build_dir}...")

    # See https://gregoryszorc.com/docs/python-build-standalone/main/running.html#obtaining-distributions
    if not re.match(r"^x86_64(|_v2|_v3|_v4)-unknown-linux-(gnu|musl)$", conf["target_triple"]):
        raise RuntimeError(f"Unexpected target_triple `{conf['target_triple']}`")
    major, minor = map(int, conf["python_major_minor_version"].split("."))
    assert major == 3

    shutil.copytree(prebuild_dir / "python/install", build_dir, symlinks=True)
    shutil.copytree(prebuild_dir / "python/licenses", build_dir / "licenses", symlinks=True)

    shutil.rmtree(build_dir / "share")

    # Remove static library stuff
    config = conf["python_stdlib_platform_config"]
    assert config.startswith("install/lib/")
    config = build_dir / config[len("install/") :]
    assert config.exists()
    shutil.rmtree(config)
    (build_dir / f"lib/libpython{major}.{minor}.a").unlink()  # Remove symlink

    stdlib_path = build_dir / f"lib/python{major}.{minor}"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(stdlib_path / "test")

    # Also remove __pycache__ & .pyc stuff
    if without_pyc:
        for pycache in stdlib_path.glob("**/__pycache__"):
            shutil.rmtree(pycache)

    site_packages_path = stdlib_path / "site-packages"

    if without_ensurepip:
        shutil.rmtree(stdlib_path / "ensurepip")

    if without_pip:
        shutil.rmtree(site_packages_path / "pip")
        shutil.rmtree(next(site_packages_path.glob("pip-*.dist-info")))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        # TODO: support Zstandard with Python >= 3.15
        archive_format = "zip"

        tmp_stdlib_path = build_dir / f"lib/tmp_python{major}.{minor}"
        shutil.move(stdlib_path, tmp_stdlib_path)

        # `site-packages` is not stdlib, so it must be excluded from the archive
        stdlib_path.mkdir()
        shutil.move(tmp_stdlib_path / site_packages_path.name, site_packages_path)

        shutil.move(tmp_stdlib_path / "lib-dynload", stdlib_path / "lib-dynload")
        shutil.make_archive(
            base_name=str(build_dir / f"lib/python{major}{minor}"),
            format=archive_format,
            root_dir=tmp_stdlib_path,
        )
        shutil.rmtree(tmp_stdlib_path)
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python fails to find its home...
        (stdlib_path / "os.py").touch()

    assert site_packages_path.exists()


def install_macos(
    conf: dict,
    build_dir: Path,
    prebuild_dir: Path,
    compressed_stdlib: bool,
    without_pyc: bool,
    without_ensurepip: bool,
    without_pip: bool,
) -> None:
    print(f"Create clean distribution {build_dir}...")

    if conf["target_triple"] not in ("x86_64-apple-darwin",):
        raise RuntimeError(f"Unexpected target_triple `{conf['target_triple']}`")
    major, minor = map(int, conf["python_major_minor_version"].split("."))
    assert major == 3

    shutil.copytree(prebuild_dir / "python/install", build_dir, symlinks=True)
    shutil.copytree(prebuild_dir / "python/licenses", build_dir / "licenses", symlinks=True)

    shutil.rmtree(build_dir / "share")

    # Remove static library stuff
    config = conf["python_stdlib_platform_config"]
    assert config.startswith("install/lib/")
    config = build_dir / config[len("install/") :]
    assert config.exists()
    shutil.rmtree(config)
    (build_dir / f"lib/libpython{major}.{minor}.a").unlink()  # Remove symlink

    stdlib_path = build_dir / f"lib/python{major}.{minor}"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(stdlib_path / "test")

    # Also remove __pycache__ & .pyc stuff
    if without_pyc:
        for pycache in stdlib_path.glob("**/__pycache__"):
            shutil.rmtree(pycache)

    site_packages_path = stdlib_path / "site-packages"

    if without_ensurepip:
        shutil.rmtree(stdlib_path / "ensurepip")

    if without_pip:
        shutil.rmtree(site_packages_path / "pip")
        shutil.rmtree(next(site_packages_path.glob("pip-*.dist-info")))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        # TODO: support Zstandard with Python >= 3.15
        archive_format = "zip"

        tmp_stdlib_path = build_dir / f"lib/tmp_python{major}.{minor}"
        shutil.move(stdlib_path, tmp_stdlib_path)

        # `site-packages` is not stdlib, so it must be excluded from the archive
        stdlib_path.mkdir()
        shutil.move(tmp_stdlib_path / site_packages_path.name, site_packages_path)

        shutil.move(tmp_stdlib_path / "lib-dynload", stdlib_path / "lib-dynload")
        shutil.make_archive(
            base_name=str(build_dir / f"lib/python{major}{minor}"),
            format=archive_format,
            root_dir=tmp_stdlib_path,
        )
        shutil.rmtree(tmp_stdlib_path)
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python fails to find its home...
        (stdlib_path / "os.py").touch()

    assert site_packages_path.exists()


def install_windows(
    conf: dict,
    build_dir: Path,
    prebuild_dir: Path,
    compressed_stdlib: bool,
    without_pyc: bool,
    without_ensurepip: bool,
    without_pip: bool,
) -> None:
    print(f"Create clean distribution {build_dir}...")

    if conf["target_triple"] not in ("x86_64-pc-windows-msvc", "i686-pc-windows-msvc"):
        raise RuntimeError(f"Unexpected target_triple `{conf['target_triple']}`")
    major, minor = map(int, conf["python_major_minor_version"].split("."))
    assert major == 3

    shutil.copytree(prebuild_dir / "python/install", build_dir, symlinks=True)
    shutil.copytree(prebuild_dir / "python/licenses", build_dir / "licenses", symlinks=True)

    stdlib_path = build_dir / "Lib"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(stdlib_path / "test")

    # Remove .pdb debug symbols
    for pdbfile in (build_dir / "DLLs").glob("*.pdb"):
        pdbfile.unlink()

    # Also remove __pycache__ & .pyc stuff
    if without_pyc:
        for pycache in stdlib_path.glob("**/__pycache__"):
            shutil.rmtree(pycache)

    site_packages_path = stdlib_path / "site-packages"

    if without_ensurepip:
        shutil.rmtree(stdlib_path / "ensurepip")

    if without_pip:
        shutil.rmtree(site_packages_path / "pip")
        shutil.rmtree(next(site_packages_path.glob("pip-*.dist-info")))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        # TODO: support Zstandard with Python >= 3.15
        archive_format = "zip"

        tmp_stdlib_path = build_dir / "tmp_Lib"
        shutil.move(stdlib_path, tmp_stdlib_path)

        # `site-packages` is not stdlib, so it must be excluded from the archive
        stdlib_path.mkdir()
        shutil.move(tmp_stdlib_path / site_packages_path.name, site_packages_path)

        shutil.make_archive(
            base_name=str(build_dir / f"python{major}{minor}"),
            format=archive_format,
            root_dir=tmp_stdlib_path,
        )
        shutil.rmtree(tmp_stdlib_path)
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python fails to find its home...
        (stdlib_path / "os.py").touch()

    assert site_packages_path.exists()


def build_distrib(
    build_dir: Path,
    prebuild_dir: Path,
    force: bool,
    compressed_stdlib: bool,
    without_pyc: bool,
    without_ensurepip: bool,
    without_pip: bool,
) -> None:
    # Config may have change, so must clean previous prebuild
    if build_dir.exists():
        if force:
            shutil.rmtree(build_dir)
        else:
            return

    config = load_config(prebuild_dir)
    if config["python_platform_tag"].startswith("linux"):
        install_linux(
            conf=config,
            build_dir=build_dir,
            prebuild_dir=prebuild_dir,
            compressed_stdlib=compressed_stdlib,
            without_pyc=without_pyc,
            without_ensurepip=without_ensurepip,
            without_pip=without_pip,
        )
    elif config["python_platform_tag"].startswith("win"):
        install_windows(
            conf=config,
            build_dir=build_dir,
            prebuild_dir=prebuild_dir,
            compressed_stdlib=compressed_stdlib,
            without_pyc=without_pyc,
            without_ensurepip=without_ensurepip,
            without_pip=without_pip,
        )
    elif config["python_platform_tag"].startswith("macosx"):
        install_macos(
            conf=config,
            build_dir=build_dir,
            prebuild_dir=prebuild_dir,
            compressed_stdlib=compressed_stdlib,
            without_pyc=without_pyc,
            without_ensurepip=without_ensurepip,
            without_pip=without_pip,
        )
    else:
        raise RuntimeError(f"Unsupported Python platform tag: `{config['python_platform_tag']}`")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("fetch_prebuild", "build_distrib", "all"), default="all")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--host-platform", required=True)
    parser.add_argument("--cpython-version", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--compressed-stdlib", action="store_true")
    parser.add_argument("--without-pyc", action="store_true")
    parser.add_argument("--without-ensurepip", action="store_true")
    parser.add_argument("--without-pip", action="store_true")

    args = parser.parse_args()

    workdir = args.output_dir
    prebuild_dir = workdir / f"python_prebuild-{args.cpython_version}-{args.host_platform}"
    build_dir = workdir / "python_distrib"

    if args.action in ("all", "fetch_prebuild"):
        fetch_prebuild(
            host_platform=args.host_platform,
            cpython_version=args.cpython_version,
            workdir=workdir,
            prebuild_dir=prebuild_dir,
            force=args.force,
        )

    if args.action in ("all", "build_distrib"):
        build_distrib(
            prebuild_dir=prebuild_dir,
            build_dir=build_dir,
            force=args.force,
            compressed_stdlib=args.compressed_stdlib,
            without_pyc=args.without_pyc,
            without_ensurepip=args.without_ensurepip,
            without_pip=args.without_pip,
        )
