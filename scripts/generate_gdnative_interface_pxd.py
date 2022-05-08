#! /usr/bin/env python3

import argparse
from pathlib import Path
from autopxd import translate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert gdnative_interface.h into Cython .pxd")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )
    args = parser.parse_args()

    pxd = translate(
        code=args.input.read_text(encoding="utf8"),
        hdrname="godot/gdnative_interface.h",
        debug=args.debug,
    )
    # wchar_t&size_t are missing
    pxd = "from libc.stddef cimport wchar_t, size_t\n" + pxd

    args.output.write_text(pxd, encoding="utf8")
