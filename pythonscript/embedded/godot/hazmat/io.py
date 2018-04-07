import sys
import pdb
from io import RawIOBase

from pythonscriptcffi import lib

from godot.hazmat.tools import godot_string_from_pyobj


# TODO: really not optimized implementation...


class GodotIO(RawIOBase):

    def __init__(self, godot_func):
        self.buffer = ""
        self.godot_func = godot_func

    def write(self, b):
        self.buffer += b
        if "\n" in self.buffer:
            *to_print, self.buffer = self.buffer.split("\n")
            g_b = godot_string_from_pyobj("\n".join(to_print))
            self.godot_func(g_b)

    def flush(self):
        if self.buffer:
            g_b = godot_string_from_pyobj(self.buffer)
            self.godot_func(g_b)
            self.buffer = ""


godot_stdout_io = GodotIO(lib.godot_print)
# Note: godot_print_error takes 4 args: descr, func, file, line.
# So GodotIO.write/flush would need to call it like that.
# But we don't have func/file/line here.
# Also, python calls write() at fairly random points with substrings of
# the actual message, so trying to structure the output with
# godot_print_error doesn't work well. Just use godot_print for now.
godot_stderr_io = GodotIO(lib.godot_print)
vanilla_Pdb = pdb.Pdb


def enable_capture_io_streams():
    sys.stdout.flush()
    sys.stderr.flush()

    # if pdb.Pdb is not GodotIOStreamCaptureSwitchPdb:
    #     pdb.Pdb = GodotIOStreamCaptureSwitchPdb

    sys.stdout = godot_stdout_io
    sys.stderr = godot_stderr_io


# TODO: Godot always end it print with a '\n', which mess the `(pdb)` cursor
# the solution could be to create a special console (with input !) in the Godot
# editor...


def disable_capture_io_streams():
    sys.stdout.flush()
    sys.stderr.flush()

    # if pdb.Pbd is not vanilla_Pdb:
    #     pdb.Pdb = vanilla_Pdb

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


class GodotIOStreamCaptureSwitchPdb(pdb.Pdb):

    def __init__(self):
        super().__init__()
        disable_capture_io_streams()
