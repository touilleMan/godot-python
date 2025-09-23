from godot import exposed
from godot.classes import Node


@exposed
class Main(Node):
    def _ready(self):
        print("Python: _ready entered", flush=True)
        self.get_tree().quit()
        print("Python: _ready done", flush=True)
