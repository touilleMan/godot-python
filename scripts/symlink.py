#! /usr/bin/env python3

import sys
import os


def symlink(src, dst):
    try:
        os.unlink(dst)
    except Exception:
        pass

    if sys.platform == "win32":
        try:
            import _winapi

            _winapi.CreateJunction(src, dst)
        except Exception as e:
            raise SystemExit(
                f"Can't do a NTFS junction as symlink fallback ({src} -> {dst})"
            ) from e

    else:
        try:
            os.symlink(src, dst)
        except Exception as e:
            raise SystemExit(f"Can't create symlink ({src} -> {dst})") from e


USAGE = "usage: symlink.py SRC1 SRC2 ... DST1 DST2 ..."


srcs_and_dsts = sys.argv[1:]
srcs = srcs_and_dsts[: len(srcs_and_dsts) // 2]
dsts = srcs_and_dsts[len(srcs_and_dsts) // 2 :]


if len(srcs) != len(dsts):
    raise SystemExit(USAGE)


for src, dst in zip(srcs, dsts):
    symlink(src, dst)
