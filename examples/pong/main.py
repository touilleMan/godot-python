from godot.builtins import register_python_extension_class


def initialize(level: int):
    """Called by Godot-Python during initialization."""
    if level != 2:  # GDEXTENSION_INITIALIZATION_SCENE
        return

    # TODO: replace by a collect&register helper
    from logic.ball import Ball
    from logic.ceiling_floor import CeilingFloor
    from logic.paddle import Paddle
    from logic.wall import Wall

    register_python_extension_class(Ball)
    register_python_extension_class(CeilingFloor)
    register_python_extension_class(Paddle)
    register_python_extension_class(Wall)
