import sys
import builtins
import traceback
from io import RawIOBase
from godot._hazmat.conversion cimport (
    godot_string_to_pyobj,
    pyobj_to_godot_string,
    godot_variant_to_pyobj,
)
from godot._hazmat.gdnative_api_struct cimport (
    godot_string,
    godot_string_name,
    godot_bool,
    godot_array,
    godot_pool_string_array,
    godot_object,
    godot_variant,
    godot_variant_call_error,
    godot_method_rpc_mode,
    godot_pluginscript_script_data,
    godot_pluginscript_instance_data,
    godot_variant_call_error_error,
    godot_variant_type
)

class GodotIOStream(RawIOBase):

    def __init__(self, godot_print_func):
        self.buffer = ""
        self.godot_print_func = godot_print_func

    def write(self, b):
        self.buffer += b
        if "\n" in self.buffer:
            to_print, self.buffer = self.buffer.rsplit("\n", 1)
            self.godot_print_func(to_print)

    def flush(self):
        if self.buffer:
            self.godot_print_func(self.buffer)
            self.buffer = ""


class GodotIO:

    _godot_stdout_io = None
    _godot_stderr_io = None
    _builtin_print = None
    _traceback_print_exception = None

    @staticmethod
    def godot_print_pystr(pystr):
        """
            Receives a python string (pystr), convert to a godot string, and print using the godot print function.
        """
        cdef godot_string gdstr
        pyobj_to_godot_string(pystr, &gdstr)
        with nogil:
            gdapi10.godot_print(&gdstr)
            gdapi10.godot_string_destroy(&gdstr)
    
    @staticmethod
    def godot_print_error_pystr(pystr, lineno=None, filename=None, name=None):
        """
            Receives a python string (pystr), convert to char*, and print using the godot_print_error function.
            Also tries to get exception information such as, file name, line numer, method name, etc
            and pass that along to godot_print_error
        """

        # we are printing an error message, so we must avoid other errors at all costs,
        # otherwise the user may never see the error message printed, making debugging a living hell
        try:
            # don't try to get exception info if user provided the details.
            if lineno is None and filename is None and name is None:
                exc_info = sys.exc_info()
                tb = exc_info[2]
                if tb:
                    tblist = traceback.extract_tb(tb)
                    if len(tblist) > 0:
                        lineno = tblist[-1].lineno
                        filename = tblist[-1].filename
                        name = tblist[-1].name
        except:
            sys.__stderr__.write("Additional errors occured while printing:\n" + traceback.format_exc() + "\n")
        
        # default values in case we couldn't get exception info and user have not provided those
        pystr = pystr or ""
        lineno = lineno or 0
        filename = filename or "UNKNOWN"
        name = name or "UNKNOWN"

        pystr = pystr.encode('utf-8')
        name = name.encode('utf-8')
        filename = filename.encode('utf-8')

        cdef char * c_msg = pystr
        cdef char * c_name = name
        cdef char * c_filename = filename
        cdef int c_lineno = <int>lineno

        with nogil:
            gdapi10.godot_print_error(c_msg, c_name, c_filename, c_lineno)
    
    @staticmethod
    def print_override(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
        """
            We need to override the builtin print function to avoid multiple calls to stderr.write.
            e.g:
                print(a, b, c, file=sys.stderr)
                would cause 3 writes to be issued: write(a), write(b) and write(c).
                Since we are using godot_print_error, that would cause a very weird print to the console,
                so overriding print and making sure a single call to write is issued solves the problem.
        """
        if file == GodotIO.get_godot_stderr_io():
            msg = str(sep).join([str(obj) for obj in objects]) + str(end)
            GodotIO.godot_print_error_pystr(msg)
        else:
            GodotIO._builtin_print(*objects, sep=sep, end=end, file=file, flush=flush)
    
    @staticmethod
    def print_exception_override(etype, value, tb, limit=None, file=None, chain=True):
        # We override traceback.print_exception to avoid multiple calls to godot_print_error on newlines,
        # making the traceback look weird
        if file is None:
            file = sys.stderr
        trace = "\n"
        for line in traceback.TracebackException(type(value), value, tb, limit=limit).format(chain=chain):
            trace += str(line)
        GodotIO.godot_print_error_pystr(trace)
    
    @staticmethod
    def enable_capture_io_streams():
        # flush existing buffer
        sys.stdout.flush()
        sys.stderr.flush()

        # make stdout and stderr the custom iostream defined above
        sys.stdout = GodotIO.get_godot_stdout_io()
        sys.stderr = GodotIO.get_godot_stderr_io()

        # override python print function
        GodotIO._builtin_print = builtins.print
        builtins.print = GodotIO.print_override

        # override traceback.print_exception
        GodotIO._traceback_print_exception = traceback.print_exception
        traceback.print_exception = GodotIO.print_exception_override

    
    @staticmethod
    def get_godot_stdout_io():
        if not GodotIO._godot_stderr_io:
            GodotIO._godot_stderr_io = GodotIOStream(GodotIO.godot_print_pystr)
        return GodotIO._godot_stderr_io

    @staticmethod
    def get_godot_stderr_io():
        if not GodotIO._godot_stderr_io:
            GodotIO._godot_stderr_io = GodotIOStream(GodotIO.godot_print_error_pystr)
        return GodotIO._godot_stderr_io
