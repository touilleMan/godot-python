import argparse
from pathlib import Path
import shutil
import json


def load_config(python_distrib: Path) -> dict:
    conf = json.loads((python_distrib / "PYTHON.json").read_text())
    assert conf["version"] == "7"
    assert conf["libpython_link_mode"] == "shared"
    return conf


def install_linux(conf: dict, output: Path, input: Path, compressed_stdlib: bool) -> None:
    assert conf["target_triple"] in ("x86_64-unknown-linux-gnu", "x86-unknown-linux-gnu")
    major, minor = conf["python_major_minor_version"].split(".")

    shutil.copytree(input / "install", output, symlinks=True)
    shutil.copytree(input / "licenses", output / "licenses", symlinks=True)

    shutil.rmtree(output / "share")

    # Remove static library stuff
    config = conf["python_stdlib_platform_config"]
    assert config.startswith("install/lib/")
    config = output / config[len("install/") :]
    assert config.exists()
    shutil.rmtree(config)
    (output / f"lib/libpython{major}.{minor}.a").unlink()  # Remove symlink

    stdlib_path = output / f"lib/python{major}.{minor}"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(stdlib_path / "test")

    # Also remove __pycache__ & .pyc stuff
    for pycache in stdlib_path.glob("**/__pycache__"):
        shutil.rmtree(pycache)

    # Make sure site-packages is empty to avoid including pip (ensurepip should be used instead)
    shutil.rmtree(stdlib_path / "site-packages")

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        tmp_stdlib_path = output / f"lib/tmp_python{major}.{minor}"
        shutil.move(stdlib_path, tmp_stdlib_path)
        stdlib_path.mkdir()
        shutil.move(tmp_stdlib_path / "lib-dynload", stdlib_path / "lib-dynload")
        shutil.make_archive(
            base_name=str(output / f"lib/python{major}{minor}"),
            format="zip",
            root_dir=tmp_stdlib_path,
        )
        shutil.rmtree(tmp_stdlib_path)
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python failed to find it home...
        (stdlib_path / "os.py").touch()

    (stdlib_path / "site-packages").mkdir()


def install_windows(conf: dict, output: Path, input: Path, compressed_stdlib: bool) -> None:
    assert conf["target_triple"] in ("x86_64-pc-windows-msvc", "x86-pc-windows-msvc")
    major, minor = conf["python_major_minor_version"].split(".")

    shutil.copytree(input / "install", output, symlinks=True)
    shutil.copytree(input / "licenses", output / "licenses", symlinks=True)

    stdlib_path = output / "Lib"

    # Remove tests lib (pretty big and basically useless)
    shutil.rmtree(stdlib_path / "test")

    # Remove .pdb debug symbols
    for pdbfile in (output / "DLLs").glob("*.pdb"):
        pdbfile.unlink()

    # Also remove __pycache__ & .pyc stuff
    for pycache in stdlib_path.glob("**/__pycache__"):
        shutil.rmtree(pycache)

    # Make sure site-packages is empty to avoid including pip (ensurepip should be used instead)
    shutil.rmtree(stdlib_path / "site-packages")

    # Zip the stdlib to save plenty of space \o/
    if compressed_stdlib:
        shutil.make_archive(
            base_name=str(output / f"python{major}{minor}"),
            format="zip",
            root_dir=stdlib_path,
        )
        shutil.rmtree(stdlib_path)
        stdlib_path.mkdir()
        # Oddly enough, os.py must be present (even if empty !) otherwise
        # Python failed to find it home...
        (stdlib_path / "os.py").touch()

    (stdlib_path / "site-packages").mkdir()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--python-distrib", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--compressed-stdlib", action=argparse.BooleanOptionalAction, required=True)
    args = parser.parse_args()

    config = load_config(args.python_distrib)
    if config["python_platform_tag"].startswith("linux"):
        install_linux(
            conf=config,
            output_dir=args.output_dir,
            python_distrib=args.python_distrib,
            compressed_stdlib=args.compressed_stdlib,
        )
    elif config["python_platform_tag"].startswith("win"):
        install_windows(
            conf=config,
            output_dir=args.output_dir,
            python_distrib=args.python_distrib,
            compressed_stdlib=args.compressed_stdlib,
        )
    else:
        raise RuntimeError(f"Unsupported Python platform tag: `{config['python_platform_tag']}`")
