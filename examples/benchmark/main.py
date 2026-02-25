from godot.builtins import register_python_extension_class


def initialize(level: int):
    """Called by Godot-Python during initialization."""
    if level != 2:  # GDEXTENSION_INITIALIZATION_SCENE
        return

    from logic.dummy_builtins_python import DummyBuiltinsPython
    from logic.dummy_classes_python import DummyClassesPython
    from logic.dummy_exposed_target import DummyExposedTarget
    from logic.dummy_exposed_python_caller import DummyExposedPythonCaller

    register_python_extension_class(DummyBuiltinsPython)
    register_python_extension_class(DummyClassesPython)
    register_python_extension_class(DummyExposedTarget)
    register_python_extension_class(DummyExposedPythonCaller)
