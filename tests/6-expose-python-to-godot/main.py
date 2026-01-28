from godot import register_python_extension_class


def initialize(level: int):
    """Called by Godot-Python during initialization."""
    if level != 2:  # GDEXTENSION_INITIALIZATION_SCENE
        return

    from node import MyPythonNode

    register_python_extension_class(MyPythonNode)
