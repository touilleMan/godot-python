from pathlib import Path

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
        raise RuntimeError(f"Unsupported CPython version `{host_cpython_version}`, valid values are: {', '.join(PLATFORM_TO_PREBUILDS.keys())}")
    prebuild_url = per_platform.get(host_platform)
    if not prebuild_url:
        raise RuntimeError(f"No CPython prebuild for host_platform `{host_platform}`")
    return prebuild_url


@isg.rule(output="cpython_prebuild_archive@")
def download_cpython_prebuild_archive(
    output: isengard.VirtualTargetResolver, build_dir: Path, cpython_prebuild_url: str
) -> None:
    from urllib.request import urlopen

    _, name = cpython_prebuild_url.rsplit("/", 1)
    path = build_dir / name
    # TODO: should be handled by rule starter
    if not path.exists():
        print(f"Downloading {cpython_prebuild_url}...")
        with urlopen(cpython_prebuild_url) as infd:
            with open(path, "bw") as outfd:
                outfd.write(infd.read())
    output.resolve(path)


@isg.rule(output="{build_dir}/cpython_prebuild/", input="cpython_prebuild_archive@")
def extract_cpython_prebuild_archive(output: Path, input: Path) -> None:
    # TODO: should be handled by rule starter
    if output.exists():
        return

    import tarfile
    from zstandard import ZstdDecompressor

    print(f"Extracting {input}...")
    with open(input, "rb") as fh:
        dctx = ZstdDecompressor()
        with dctx.stream_reader(fh) as reader:
            with tarfile.open(mode="r|", fileobj=reader) as tf:
                tf.extractall(output)


@isg.rule(output="python_headers_dir@", input="{build_dir}/cpython_prebuild/")
def define_python_headers_dir(output: isengard.VirtualTargetResolver, input: Path, host_cpython_version: str) -> None:
    major, minor, _ = host_cpython_version.split('.')
    output.resolve(input / f"python/install/include/python{major}.{minor}")


@isg.rule(output="python_lib_dir@", input="{build_dir}/cpython_prebuild/")
def define_python_lib_dir(output: isengard.VirtualTargetResolver, input: Path) -> None:
    output.resolve(input / "python/install/lib")


### Generate custom build from the prebuild ###


@isg.rule(output="{build_dir}/cpython_build/", input="{build_dir}/cpython_prebuild/")
def generate_cpython_build(
    output: Path, input: Path, host_cpython_version: str, cpython_compressed_stdlib: bool, host_platform: str
):
    # TODO: should be handled by rule starter
    if output.exists():
        return

    global _generate_cpython_build_linux, _generate_cpython_build_windows
    import json

    prebuild = input / "python"
    build = output

    conf = json.loads((prebuild / "PYTHON.json").read_text())
    assert conf["version"] == "5"
    assert conf["libpython_link_mode"] == "shared"
    breakpoint()
    if host_platform.startswith("linux"):
        _generate_cpython_build_linux(conf, build, prebuild, host_cpython_version, cpython_compressed_stdlib)
    elif host_platform.startswith("windows"):
        _generate_cpython_build_windows(
            conf, build, prebuild, host_cpython_version, cpython_compressed_stdlib
        )
    else:
        raise RuntimeError(
            f"Don't know how to build for host_platform `{host_platform}`"
        )


def _generate_cpython_build_linux(
    conf: dict, build: Path, prebuild: Path, host_cpython_version: str, compressed_stdlib: bool
) -> None:
    import shutil

    assert conf["target_triple"] in ("x86_64-unknown-linux-gnu", "x86-unknown-linux-gnu")
    major, minor, _ = host_cpython_version.split('.')

    shutil.copytree(str(prebuild / "install"), str(build), symlinks=True)
    shutil.copytree(str(prebuild / "licenses"), str(build / "licenses"), symlinks=True)

    shutil.rmtree(str(build / "share"))

    # Remove static library stuff
    config = conf["python_stdlib_platform_config"]
    assert config.startswith("install/lib/")
    config = build / config[len("install/") :]
    assert config.exists()
    shutil.rmtree(str(config))

    stdlib_path = build / f"lib/python{major}.{minor}"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(str(stdlib_path / "test"))

    # Also remove __pycache__ & .pyc stuff
    for pycache in stdlib_path.glob("**/__pycache__"):
        shutil.rmtree(str(pycache))

    # Make sure site-packages is empty to avoid including pip (ensurepip should be used instead)
    shutil.rmtree(str(stdlib_path / "site-packages"))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        tmp_stdlib_path = build / f"lib/tmp_python{major}.{minor}"
        shutil.move(str(stdlib_path), str(tmp_stdlib_path))
        stdlib_path.mkdir()
        shutil.move(
            str(tmp_stdlib_path / "lib-dynload"), str(stdlib_path / "lib-dynload")
        )
        shutil.make_archive(
            base_name=str(build / f"lib/python{major}{minor}"),
            format="zip",
            root_dir=str(tmp_stdlib_path),
        )
        shutil.rmtree(str(tmp_stdlib_path))
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python failed to find it home...
        (stdlib_path / "os.py").touch()

    (stdlib_path / "site-packages").mkdir()


def _generate_cpython_build_windows(
    conf: dict, build: Path, prebuild: Path, host_cpython_version: str, compressed_stdlib: bool
) -> None:
    import shutil

    assert conf["target_triple"] in ("x86_64-pc-windows-msvc", "x86-pc-windows-msvc")
    major, minor, _ = host_cpython_version.split('.')

    shutil.copytree(str(prebuild / "install"), str(build), symlinks=True)
    shutil.copytree(str(prebuild / "licenses"), str(build / "licenses"), symlinks=True)

    stdlib_path = build / "Lib"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(str(stdlib_path / "test"))

    # Remove .pdb debug symbols
    for pdbfile in (build / "DLLs").glob("*.pdb"):
        pdbfile.unlink()

    # Also remove __pycache__ & .pyc stuff
    for pycache in stdlib_path.glob("**/__pycache__"):
        shutil.rmtree(str(pycache))

    # Make sure site-packages is empty to avoid including pip (ensurepip should be used instead)
    shutil.rmtree(str(stdlib_path / "site-packages"))

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        shutil.make_archive(
            base_name=str(build / f"python{major}{minor}"), format="zip", root_dir=str(stdlib_path)
        )
        shutil.rmtree(str(stdlib_path))
        stdlib_path.mkdir()
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python failed to find it home...
        (stdlib_path / "os.py").touch()

    (stdlib_path / "site-packages").mkdir()
