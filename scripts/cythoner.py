#! /usr/bin/env python3

import os
import sys
from pathlib import Path
import shutil


USAGE = "usage: cythoner OUTPUT.c PRIVATE_DIR INPUT.pyx [INPUT.pxd, INPUT.pxi, ...] [--] [<cythonize args>]"
SRC_DIR = Path(__file__, "../../src/").resolve()
BUILD_SRC_DIR = Path(os.getcwd()).resolve() / "src"


try:
    args_separator = sys.argv.index("--")
    args = sys.argv[1:args_separator]
    extra_args = sys.argv[args_separator + 1 :]
except ValueError:
    args = sys.argv[1:]
    extra_args = []


if len(args) < 3:
    raise SystemExit(USAGE)


c_output, private_dir, pyx_src, *pxd_srcs = [Path(x).resolve() for x in args]
# `pxd_srcs` can also contains `.pxi` files given we handle them in a similar fashion
if not pyx_src.name.endswith(".pyx") or any(
    not src.name.endswith(".pxd") and not src.name.endswith(".pxi") for src in pxd_srcs
):
    raise SystemExit(USAGE)


def relative_path(path: Path) -> Path:
    try:
        return path.relative_to(SRC_DIR)
    except ValueError:
        try:
            return path.relative_to(BUILD_SRC_DIR)
        except ValueError:
            raise SystemExit(f"Input {path} is not relative to src or build dirs")


# Symlink is much better during development when hacking into compiled file
# is often needed, but it is not available on Windows
if sys.platform == "win32":

    def copy(src, tgt):
        shutil.copyfile(src, tgt)

else:

    def copy(src, tgt):
        try:
            os.unlink(tgt)
        except FileNotFoundError:
            pass
        os.symlink(src, tgt)


# Generate the import dir from the inputs (except the actual .pyx)
for pxd_src in pxd_srcs:
    pxd_src = pxd_src.resolve()
    if "#" in pxd_src.name:
        # Source is a generated pxd (see `src/meson.build`), it actual path
        # is encoded in it name
        *pxd_parents, pxd_name = pxd_src.name.split("#")
        pxd_parent_dir = private_dir / Path(*pxd_parents)
        pxd_tgt = pxd_parent_dir / pxd_name

    else:
        # Standard case: source is within src or build dir
        pxd_src_relative = relative_path(pxd_src)
        pxd_parent_dir = private_dir / pxd_src_relative.parent
        pxd_tgt = pxd_parent_dir / pxd_src.name

    pxd_parent_dir.mkdir(exist_ok=True, parents=True)
    while pxd_parent_dir != private_dir:
        # `__init__.py` are required so Cython consider the directory as a package,
        # however it content is never read so an empty file is good enough
        (pxd_parent_dir / "__init__.py").touch()
        pxd_parent_dir = pxd_parent_dir.parent
    copy(pxd_src, pxd_tgt)


# We need to copy the pyx file into the right directory to respect the package
# it belongs to
pyx_src_relative = relative_path(pyx_src)
pyx_parent_dir = private_dir / pyx_src_relative.parent
pyx_tgt = pyx_parent_dir / pyx_src.name
copy(pyx_src, pyx_tgt)


sys.argv = [
    "cython",
    "-3",
    "--fast-fail",
    f"--include-dir={private_dir}",
    str(pyx_tgt),
    f"--output-file={c_output}",
    *extra_args,
]


from cython_godot_extension_class_preprocessor import patch_cython_pipeline

patch_cython_pipeline()

# Starts Cython CLI
from Cython.Compiler.Main import setuptools_main

sys.exit(setuptools_main())
