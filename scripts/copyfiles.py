#! /usr/bin/env python3

import sys
import shutil


USAGE = "usage: copyfiles.py SRC1 SRC2 ... DST1 DST2 ..."


srcs_and_dsts = sys.argv[1:]
srcs = srcs_and_dsts[: len(srcs_and_dsts) // 2]
dsts = srcs_and_dsts[len(srcs_and_dsts) // 2 :]

if len(srcs) != len(dsts):
    raise SystemExit(USAGE)


for src, dst in zip(srcs, dsts):
    shutil.copyfile(src, dst)
