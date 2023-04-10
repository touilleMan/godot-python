# cython: language_level=3

from godot.hazmat.gdapi cimport *


def initialize(level):
    print("MY initialize", level)


def deinitialize(level):
    print("MY deinitialize", level)
