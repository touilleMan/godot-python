# cython: language_level=3


def initialize(level):
    print("MY initialize", level, flush=True)


def deinitialize(level):
    print("MY deinitialize", level, flush=True)
