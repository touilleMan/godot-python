import sys
import code
from godot import exposed, export
from godot import *

from .plugin import BASE_RES


FONT = ResourceLoader.load(f"{BASE_RES}/hack_regular.tres")


@exposed(tool=True)
class PythonREPL(VBoxContainer):
    def _enter_tree(self):
        self.history = []
        self.selected_history = 0
        self.output_box = self.get_node("OutputBox")
        self.output_box.add_font_override("normal_font", FONT)
        self.output_box.add_font_override("mono_font", FONT)
        self.run_button = self.get_node("FooterContainer/RunButton")
        self.copy_button = self.get_node("HeaderContainer/CopyButton")
        self.copy_button.connect("pressed", self, "copy")
        self.clear_button = self.get_node("HeaderContainer/ClearButton")
        self.clear_button.connect("pressed", self, "clear")
        self.input_box = self.get_node("FooterContainer/InputBox")
        self.input_box.connect("text_entered", self, "execute")
        self.run_button.connect("pressed", self, "execute")
        self.interpreter_context = {"__name__": "__console__", "__doc__": None}
        self.interpreter = code.InteractiveConsole(self.interpreter_context)
        self.more = False
        if getattr(sys.stdout, "add_callback", None) is not None:
            sys.stdout.add_callback(self.output_line)
        # sys.stderr.add_callback(self.output_line)
        else:
            self.output_line("It seems IO Streams Capture is disabled.")
            self.output_line("In order to see the output of commands, go to:")
            self.output_line("Project > Project Settings > Python Script > Io Streams Capture")
            self.output_line("and enable Io Streams Capture.")

    def _exit_tree(self):
        self.cleanup()
    
    def cleanup(self):
        if getattr(sys.stdout, "remove_callback", None) is not None:
            sys.stdout.remove_callback(self.output_line)
    
    # make sure we disconnect the IO callback when game/editor is quiting
    def _notification(self, what):
        if what == Object.NOTIFICATION_PREDELETE or what == MainLoop.NOTIFICATION_WM_QUIT_REQUEST:
            self.cleanup()

    def _ready(self):
        pass

    def output_line(self, line):
        if not self.get_tree():
			return
        self.output_box.push_mono()
        self.output_box.add_text(line)
        self.output_box.newline()
        self.output_box.pop()

    def remove_last_line(self):
        self.output_box.remove_line(self.output_box.get_line_count() - 2)
        self.output_box.scroll_to_line(self.output_box.get_line_count() - 1)

    def execute(self, *args, **kwargs):
        string = self.input_box.get_text()
        # avoid adding multiple repeated entries to the command history
        if not (len(self.history) > 0 and self.history[-1] == string):
            self.history.append(string)
        self.selected_history = 0
        self.input_box.clear()
        linestart = "... " if self.more else ">>> "
        self.output_line(linestart + str(string))
        self.more = self.interpreter.push(str(string))

    def up_pressed(self):
        if len(self.history) >= abs(self.selected_history - 1):
            self.selected_history -= 1
            self.input_box.clear()
            self.input_box.set_text(self.history[self.selected_history])
        self.input_box.grab_focus()

    def down_pressed(self):
        if self.selected_history + 1 == 0:
            self.selected_history += 1
            self.input_box.clear()
        elif self.selected_history + 1 < 0:
            self.selected_history += 1
            self.input_box.clear()
            self.input_box.set_text(self.history[self.selected_history])

        self.input_box.grab_focus()

    def copy(self):
        pass

    def clear(self):
        self.output_box.clear()
