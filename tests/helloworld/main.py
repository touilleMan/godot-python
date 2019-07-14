from godot import exposed
from godot.bindings import Node, OS


@exposed
class Main(Node):
    def _ready(self):
        # Exit godot
        OS.set_exit_code(0)
        self.get_tree().quit()
