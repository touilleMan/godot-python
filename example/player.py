from godot import exposed, Node


@exposed
class Player(Node):
    def __init__(self, name="John"):
        self.name = name
