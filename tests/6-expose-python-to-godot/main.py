from godot import exposed
from godot.classes import Node


@exposed
class Main(Node):
    def _ready(self):
        self.get_tree().quit()
