#! /usr/bin/env python3

from __future__ import annotations
import argparse
from pathlib import Path
import shutil


BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR / "../.."
TARGET_DIR = BASE_DIR / "src"


def copy_data(build_dir: Path) -> None:
    output_godot_dir = TARGET_DIR / "godot"
    output_godot_hazmat_dir = output_godot_dir / "hazmat"
    output_godot_hazmat_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy(ROOT_DIR / "src/gdpy_libgodot.pyx", TARGET_DIR)
    shutil.copy(build_dir / "src/gdpy_gdextension_ptrs.c", TARGET_DIR)

    shutil.copytree(build_dir / "gdextension_api", TARGET_DIR / "gdextension_api")

    src_godot_dir = ROOT_DIR / "src/godot"
    shutil.copy(src_godot_dir / "__init__.py", output_godot_dir)
    shutil.copy(src_godot_dir / "_lang.pyx", output_godot_dir)
    shutil.copy(src_godot_dir / "_lang_resource_format_loader.pxi", output_godot_dir)
    shutil.copy(src_godot_dir / "_lang_resource_format_saver.pxi", output_godot_dir)
    shutil.copy(src_godot_dir / "_lang_script_language.pxi", output_godot_dir)
    shutil.copy(src_godot_dir / "_lang_script.pxi", output_godot_dir)
    shutil.copy(src_godot_dir / "py.typed", output_godot_dir)
    shutil.copy(src_godot_dir / "singletons.py", output_godot_dir)

    build_src_godot_dir = build_dir / "src/godot"
    shutil.copy(build_src_godot_dir / "builtins.pyx", output_godot_dir)
    shutil.copy(build_src_godot_dir / "builtins.pyi", output_godot_dir)
    shutil.copy(build_src_godot_dir / "builtins.pxd", output_godot_dir)
    shutil.copy(build_src_godot_dir / "classes.pyx", output_godot_dir)
    shutil.copy(build_src_godot_dir / "classes.pyi", output_godot_dir)
    shutil.copy(build_src_godot_dir / "classes.pxd", output_godot_dir)
    shutil.copy(build_src_godot_dir / "_version.py", output_godot_dir)

    src_godot_hazmat_dir = src_godot_dir / "hazmat"
    shutil.copy(src_godot_hazmat_dir / "extension_class.pxd", output_godot_hazmat_dir)
    shutil.copy(src_godot_hazmat_dir / "extension_class.pyx", output_godot_hazmat_dir)
    shutil.copy(src_godot_hazmat_dir / "__init__.py", output_godot_hazmat_dir)

    build_src_godot_hazmat_dir = build_src_godot_dir / "hazmat"
    shutil.copy(build_src_godot_hazmat_dir / "gdapi.pxd", output_godot_hazmat_dir)
    shutil.copy(build_src_godot_hazmat_dir / "gdextension_interface.pxd", output_godot_hazmat_dir)
    shutil.copy(build_src_godot_hazmat_dir / "gdptrs.pxd", output_godot_hazmat_dir)
    shutil.copy(build_src_godot_hazmat_dir / "gdtypes.pxd", output_godot_hazmat_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Python project embedding LibGodot & Godot-Python bindings"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="BUILD_PATH",
        type=Path,
        default=BASE_DIR / "../build",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
    )

    args = parser.parse_args()

    if TARGET_DIR.exists():
        if args.force:
            shutil.rmtree(TARGET_DIR)
        else:
            raise RuntimeError(f"{TARGET_DIR} already exists, aborting")

    copy_data(build_dir=args.input)
