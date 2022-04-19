import sys
import ctypes
from code import InteractiveConsole
from collections import deque
from threading import Thread, Lock, Event
from queue import SimpleQueue

from _godot import StdoutStderrCaptureToGodot, StdinCapture
from godot import exposed, export, ResourceLoader, VBoxContainer

from .plugin import BASE_RES


FONT = ResourceLoader.load(f"{BASE_RES}/hack_regular.tres")


class StdoutStderrCaptureToBufferAndPassthrough(StdoutStderrCaptureToGodot):
    def __init__(self):
        super().__init__()
        self._buffer = ""

    def _write(self, buff):
        # _write always executed with _lock taken
        super()._write(buff)
        self._buffer += buff

    def read_buffer(self):
        with self._lock:
            buffer = self._buffer
            self._buffer = ""
            return buffer


class StdinCaptureToBuffer(StdinCapture):
    def __init__(self):
        super().__init__()
        self._lock = Lock()
        self._has_data = Event()
        self._buffer = ""
        self._closed = False

    def _read(self, size=-1):
        if self._closed:
            raise EOFError

        if size < 0 or size > len(self._buffer):
            data = self._buffer
            self._buffer = ""
        else:
            data = self._buffer[:size]
            self._buffer = self._buffer[size:]

        if not self._buffer:
            self._has_data.clear()

        return data

    def read(self, size=-1):
        while True:
            self._has_data.wait()
            with self._lock:
                # Check if a concurrent readinto has already processed the data
                if not self._has_data.is_set():
                    continue

                return self._read(size)

    def readline(size=-1):
        while True:
            self._has_data.wait()
            with self._lock:
                # Check if a concurrent readinto has already processed the data
                if not self._has_data.is_set():
                    continue

                if size < 0:
                    size = len(self._buffer)
                try:
                    size = min(size, self._buffer.index("\n") + 1)
                except ValueError:
                    # \n not in self._buffer
                    pass
                return self._read(size)

    def write(self, buffer):
        if not buffer:
            return
        with self._lock:
            self._has_data.set()
            self._buffer += buffer

    def close(self):
        self._closed = True
        # Ensure read is waken up so it can raise EOFError
        self._has_data.set()


class InteractiveConsoleInREPL(InteractiveConsole):
    def __init__(self, repl_write, repl_read):
        super().__init__(locals={"__name__": "__console__", "__doc__": None})
        # Default write/raw_input relies on stderr/stdin, overwrite them
        # to only talk with the REPL
        self.write = repl_write
        # Note overwritting `InteractiveConsole.raw_input` doesn't prevent
        # from user code directly calling `input` (for instance when typing
        # `help()` which makes use of a pager).
        self.repl_read = repl_read
        self.thread = None

    def raw_input(self, prompt):
        data = self.repl_read()
        # Print the command line in the ouput box, this is needed given
        # we have a separate input box that is cleared each time
        # the user hit enter (unlike regular terminal where input and output
        # are mixed together and enter only jumps to next line)
        self.write(f"{prompt}{data}")
        return data

    def start_in_thread(self):
        assert not self.thread
        self.thread = Thread(target=self.interact)
        self.thread.start()

    def send_keyboard_interrupt(self):
        # Inject a exception in the thread running the interpreter.
        # This is not 100% perfect given the thread checks for exception only
        # when it is actually running Python code so we cannot interrupt native
        # code (for instance calling `time.sleep` cannot be interrupted)
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            self.thread.ident, ctypes.py_object(KeyboardInterrupt)
        )


@exposed(tool=True)
class PythonREPL(VBoxContainer):
    __STREAMS_CAPTURE_INSTALLED = False

    def _enter_tree(self):
        self.__plugin_instantiated = False
        self.history = []
        self.selected_history = 0
        self.output_box = self.get_node("OutputBox")
        self.output_box.add_font_override("normal_font", FONT)
        self.output_box.add_font_override("mono_font", FONT)
        self.run_button = self.get_node("FooterContainer/RunButton")
        self.run_button.connect("pressed", self, "execute")
        self.clear_button = self.get_node("HeaderContainer/ClearButton")
        self.clear_button.connect("pressed", self, "clear")
        self.interrupt_button = self.get_node("HeaderContainer/KeyboardInterruptButton")
        self.interrupt_button.connect("pressed", self, "send_keyboard_interrupt")
        self.input_box = self.get_node("FooterContainer/InputBox")
        self.input_box.connect("text_entered", self, "execute")

        # Hijack stdout/stderr/stdin streams
        self.stdout_stderr_capture = StdoutStderrCaptureToBufferAndPassthrough()
        self.stdin_capture = StdinCaptureToBuffer()
        # Only overwrite streams if the scene has been created by the
        # pythonscript_repl plugin. This avoid concurrent streams patching
        # when the scene is opened from the editor (typically when we want
        # to edit the repl GUI)
        # TODO: find a way to differentiate plugin instantiated from other
        # instantiations instead of relying on "first instantiated is plugin"
        if not PythonREPL.__STREAMS_CAPTURE_INSTALLED:
            PythonREPL.__STREAMS_CAPTURE_INSTALLED = True
            self.__plugin_instantiated = True
            self.stdout_stderr_capture.install()
            self.stdin_capture.install()

        # Finally start the Python interpreter, it must be running it in own
        # thread given it does blocking reads on stdin
        self.interpreter = InteractiveConsoleInREPL(
            repl_write=self.write, repl_read=self.stdin_capture.read
        )
        self.interpreter.start_in_thread()

    def _exit_tree(self):
        # Closing our custom stdin stream should make `InteractiveConsole.interact`
        # return, hence finishing the interpreter thread
        self.stdin_capture.close()
        self.interpreter.thread.join()

        # Our custom stream capture must be removed before this node is destroyed,
        # otherwise segfault will occur on next print !
        if self.__plugin_instantiated:
            PythonREPL.__STREAMS_CAPTURE_INSTALLED = False
            self.stdout_stderr_capture.remove()
            self.stdin_capture.remove()

    def write(self, buffer):
        for line in buffer.splitlines():
            self.output_box.push_mono()
            self.output_box.add_text(line)
            self.output_box.newline()
            self.output_box.pop()

    def _process(self, delta):
        if not hasattr(self, "stdout_stderr_capture"):
            return
        # Display new lines
        self.write(self.stdout_stderr_capture.read_buffer())

    def remove_last_line(self):
        self.output_box.remove_line(self.output_box.get_line_count() - 2)
        self.output_box.scroll_to_line(self.output_box.get_line_count() - 1)

    def execute(self, *args, **kwargs):
        string = str(self.input_box.get_text())
        # Avoid adding multiple repeated entries to the command history
        if not (len(self.history) > 0 and self.history[-1] == string):
            self.history.append(string)
        self.selected_history = 0
        self.input_box.clear()
        # Send the line into stdin and let the interpret do the rest
        self.stdin_capture.write(string + "\n")

    def up_pressed(self):
        if len(self.history) >= abs(self.selected_history - 1):
            self.selected_history -= 1
            self.input_box.clear()
            val = str(self.history[self.selected_history])
            self.input_box.set_text(val)
            self.input_box.set_cursor_position(len(val))
        self.input_box.grab_focus()

    def down_pressed(self):
        if self.selected_history + 1 == 0:
            self.selected_history += 1
            self.input_box.clear()
        elif self.selected_history + 1 < 0:
            self.selected_history += 1
            self.input_box.clear()
            val = str(self.history[self.selected_history])
            self.input_box.set_text(val)
            self.input_box.set_cursor_position(len(val))
        self.input_box.grab_focus()

    def clear(self):
        self.output_box.clear()

    def send_keyboard_interrupt(self):
        self.interpreter.send_keyboard_interrupt()
