from godot.builtins import GDString, GDArray


def initialize(level: int):
    gdstr = GDString("MY initialize {0}")
    print(gdstr.format(GDArray([level])), flush=True)


def deinitialize(level: int):
    print("MY deinitialize", level, flush=True)
