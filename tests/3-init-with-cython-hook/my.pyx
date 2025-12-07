# cython: language_level=3

from godot.builtins cimport *


def initialize(level):
    # Call builtin with Cython API
    cdef GDString gdstr = GDString("MY initialize {0}")
    print(gdstr.format(GDArray([<gd_int_t>level])), flush=True)


def deinitialize(level):
    # Call builtin with Python API
    gdstr = GDString("MY deinitialize {0}")
    print(gdstr.format(GDArray([level])), flush=True)
