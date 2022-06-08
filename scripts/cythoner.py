#! /usr/bin/env python3

import os
import sys
from pathlib import Path
import shutil


USAGE = "usage: cythoner OUTPUT.c PRIVATE_DIR INPUT.pyx [INPUT.pxd ...]"
SRC_DIR = Path(__file__, "../../src/").resolve()
BUILD_DIR = Path(os.getcwd()).resolve()


if len(sys.argv) < 3:
    raise SystemExit(USAGE)


c_output, private_dir, pyx_src, *import_srcs = [Path(x).resolve() for x in sys.argv[1:]]
if not pyx_src.name.endswith(".pyx") or any(not src.name.endswith(".pxd") for src in import_srcs):
    raise SystemError(USAGE)


# Generate the import dir from the inputs (except the actual .pyx)
for src in import_srcs:
    src = src.resolve()
    if "#" in src.name:
        # Source is a generated pxd (see `src/meson.build`), it actual path
        # is encoded in it name
        *parents, name = src.name.split("#")
        parent_dir = private_dir / Path(*parents)
        tgt = parent_dir / name

    else:
        # Standard case: source is within src or build dir
        try:
            relative_path = src.relative_to(SRC_DIR)
        except ValueError:
            try:
                relative_path = src.relative_to(BUILD_DIR)
            except ValueError:
                raise SystemExit(f"Input {src} is not relative to src or build dirs")

        parent_dir = private_dir / relative_path.parent
        tgt = parent_dir / src.name

    parent_dir.mkdir(exist_ok=True, parents=True)
    # `__init__.py` are required so Cython consider the directory as a package,
    # however it content is never read so an empty file is good enough
    (parent_dir / "__init__.py").touch()
    shutil.copyfile(src, tgt)


sys.argv = [
    "cython",
    "-3",
    "--fast-fail",
    f"--include-dir={private_dir}",
    str(pyx_src),
    f"--output-file={c_output}",
]


# Starts Cython CLI
from Cython.Compiler.Main import setuptools_main

sys.exit(setuptools_main())
