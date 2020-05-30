from godot import exposed, export, EditorPlugin
from godot import *


@exposed(tool=True)
class plugin(EditorPlugin):
    def _enter_tree(self):
        # Initialization of the plugin goes here
        self.repl = ResourceLoader.load("res://addons/pythonscript_repl/PythonREPL.tscn").instance()
        self.repl_button = self.add_control_to_bottom_panel(self.repl, "Python REPL")

    def _exit_tree(self):
        # Clean-up of the plugin goes here
        self.remove_control_from_bottom_panel(self.repl)
        self.repl.queue_free()
        self.repl = None

    def _ready(self):
        pass
