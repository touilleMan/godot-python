from typing import Tuple
from urllib.request import urlopen
from pathlib import Path
import shutil
import json
import tarfile
from zstandard import ZstdDecompressor

import isengard


isg = isengard.get_parent()


PREBUILDS_BASE_URL = "https://github.com/indygreg/python-build-standalone/releases/download"
PLATFORM_TO_PREBUILDS = {
    "3.9.7": {
        "linux-x86_64": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-x86_64-unknown-linux-gnu-pgo+lto-20211017T1616.tar.zst",
        "windows-x86": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-i686-pc-windows-msvc-shared-pgo-20211017T1616.tar.zst",
        "windows-x86_64": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-x86_64-pc-windows-msvc-shared-pgo-20211017T1616.tar.zst",
        "osx-x86_64": f"{PREBUILDS_BASE_URL}/20211017/cpython-3.9.7-x86_64-apple-darwin-pgo+lto-20211017T1616.tar.zst",
    }
}


@isg.lazy_config
def cpython_prebuild_url(host_platform: str, host_cpython_version: str) -> str:
    per_platform = PLATFORM_TO_PREBUILDS.get(host_cpython_version)
    if not per_platform:
        raise RuntimeError(
            f"Unsupported CPython version `{host_cpython_version}`, valid values are: {', '.join(PLATFORM_TO_PREBUILDS.keys())}"
        )
    prebuild_url = per_platform.get(host_platform)
    if not prebuild_url:
        raise RuntimeError(f"No CPython prebuild for host_platform `{host_platform}`")
    return prebuild_url


@isg.lazy_config
def cpython_prebuild_archive_path(build_platform_dir: Path, cpython_prebuild_url: str) -> str:
    _, name = cpython_prebuild_url.rsplit("/", 1)
    return build_platform_dir / name


@isg.lazy_config
def libpython_config(
    host_cpython_version: str,
    host_platform: str,
    cc_is_msvc: bool,
    build_platform_dir: Path,
) -> str:
    basedir = build_platform_dir / "cpython_prebuild"

    major, minor, _ = host_cpython_version.split(".")
    if host_platform.startswith("windows"):
        python_header_dir = basedir / "python/install/include"
        python_lib_dir = basedir / "python/install/libs"
        python_lib = f"python{major}{minor}"
    else:
        python_header_dir = basedir / f"python/install/include/python{major}.{minor}"
        python_lib_dir = basedir / "python/install/lib"
        python_lib = f"python{major}.{minor}"

    if cc_is_msvc:
        cflags = (f"/I{python_header_dir}",)
        linkflags = (f"/LIBPATH:{python_lib_dir}", f"{python_lib}.lib")
    else:
        cflags = (f"-I{python_header_dir}",)
        linkflags = (f"-L{python_lib_dir}", f"-l{python_lib}")

    return (cflags, linkflags)


@isg.lazy_config
def libpython_cflags(python_config: Tuple[Tuple[str, ...], Tuple[str, ...]]) -> Tuple[str, ...]:
    return python_config[0]


@isg.lazy_config
def libpython_linkflags(python_config: Tuple[Tuple[str, ...], Tuple[str, ...]]) -> Tuple[str, ...]:
    return python_config[1]


@isg.rule(output="{cpython_prebuild_archive_path}#")
def download_cpython_prebuild_archive(output: Path, cpython_prebuild_url: str) -> None:
    print(f"Downloading {cpython_prebuild_url}...")
    with urlopen(cpython_prebuild_url) as infd:
        with open(output, "bw") as outfd:
            outfd.write(infd.read())


@isg.rule(
    output="{build_platform_dir}/cpython_prebuild/",
    input="{cpython_prebuild_archive_path}#",
)
def extract_cpython_prebuild_archive(
    output: Path,
    input: Path,
    host_cpython_version: str,
    host_platform: str,
    cc_is_msvc: bool,
) -> None:
    print(f"Extracting {input}...")
    with open(input, "rb") as fh:
        dctx = ZstdDecompressor()
        with dctx.stream_reader(fh) as reader:
            with tarfile.open(mode="r|", fileobj=reader) as tf:
                tf.extractall(output)


### Generate custom build from the prebuild ###


@isg.rule(
    output="{build_platform_dir}/cpython_distrib/", input="{build_platform_dir}/cpython_prebuild/"
)
def generate_cpython_distrib(
    output: Path,
    input: Path,
    host_cpython_version: str,
    cpython_compressed_stdlib: bool,
    host_platform: str,
):
    global _generate_cpython_distrib_linux, _generate_cpython_distrib_windows

    prebuild = input / "python"
    distrib = output

    conf = json.loads((prebuild / "PYTHON.json").read_text())
    assert conf["version"] == "7"
    assert conf["libpython_link_mode"] == "shared"
    if host_platform.startswith("linux"):
        _generate_cpython_distrib_linux(
            conf, distrib, prebuild, host_cpython_version, cpython_compressed_stdlib
        )
    elif host_platform.startswith("windows"):
        _generate_cpython_distrib_windows(
            conf, distrib, prebuild, host_cpython_version, cpython_compressed_stdlib
        )
    else:
        raise RuntimeError(f"Don't know how to build for host_platform `{host_platform}`")


def _generate_cpython_distrib_linux(
    conf: dict, distrib: Path, prebuild: Path, host_cpython_version: str, compressed_stdlib: bool
) -> None:
    assert conf["target_triple"] in ("x86_64-unknown-linux-gnu", "x86-unknown-linux-gnu")
    major, minor, _ = host_cpython_version.split(".")

    shutil.copytree(str(prebuild / "install"), str(distrib), symlinks=True)
    shutil.copytree(str(prebuild / "licenses"), str(distrib / "licenses"), symlinks=True)

    shutil.rmtree(str(distrib / "share"))

    # Remove static library stuff
    config = conf["python_stdlib_platform_config"]
    assert config.startswith("install/lib/")
    config = distrib / config[len("install/") :]
    assert config.exists()
    shutil.rmtree(str(config))
    (distrib / f"lib/libpython{major}.{minor}.a").unlink()  # Remove symlink

    stdlib_path = distrib / f"lib/python{major}.{minor}"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(str(stdlib_path / "test"))

    # Also remove __pycache__ & .pyc stuff
    for pycache in stdlib_path.glob("**/__pycache__"):
        shutil.rmtree(str(pycache))

    # Make sure site-packages is empty to avoid including pip (ensurepip should be used instead)
    shutil.rmtree(str(stdlib_path / "site-packages"))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        tmp_stdlib_path = distrib / f"lib/tmp_python{major}.{minor}"
        shutil.move(str(stdlib_path), str(tmp_stdlib_path))
        stdlib_path.mkdir()
        shutil.move(str(tmp_stdlib_path / "lib-dynload"), str(stdlib_path / "lib-dynload"))
        shutil.make_archive(
            base_name=str(distrib / f"lib/python{major}{minor}"),
            format="zip",
            root_dir=str(tmp_stdlib_path),
        )
        shutil.rmtree(str(tmp_stdlib_path))
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python failed to find it home...
        (stdlib_path / "os.py").touch()

    (stdlib_path / "site-packages").mkdir()


def _generate_cpython_distrib_windows(
    conf: dict, distrib: Path, prebuild: Path, host_cpython_version: str, compressed_stdlib: bool
) -> None:
    assert conf["target_triple"] in ("x86_64-pc-windows-msvc", "x86-pc-windows-msvc")
    major, minor, _ = host_cpython_version.split(".")

    shutil.copytree(str(prebuild / "install"), str(distrib), symlinks=True)
    shutil.copytree(str(prebuild / "licenses"), str(distrib / "licenses"), symlinks=True)

    stdlib_path = distrib / "Lib"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(str(stdlib_path / "test"))

    # Remove .pdb debug symbols
    for pdbfile in (distrib / "DLLs").glob("*.pdb"):
        pdbfile.unlink()

    # Also remove __pycache__ & .pyc stuff
    for pycache in stdlib_path.glob("**/__pycache__"):
        shutil.rmtree(str(pycache))

    # Make sure site-packages is empty to avoid including pip (ensurepip should be used instead)
    shutil.rmtree(str(stdlib_path / "site-packages"))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        shutil.make_archive(
            base_name=str(distrib / f"python{major}{minor}"),
            format="zip",
            root_dir=str(stdlib_path),
        )
        shutil.rmtree(str(stdlib_path))
        stdlib_path.mkdir()
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python failed to find it home...
        (stdlib_path / "os.py").touch()

    (stdlib_path / "site-packages").mkdir()
