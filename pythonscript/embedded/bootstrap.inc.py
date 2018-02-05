# Given file is included inside a cffi-generated C source file, pdb cannot
# display it at all. This is why it should not contain anything but imports.
from godot.hazmat.ffi import *  # noqa
