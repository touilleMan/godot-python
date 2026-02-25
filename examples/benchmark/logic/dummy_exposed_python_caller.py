from godot import gddataclass, classes


@gddataclass(init=False)
class DummyExposedPythonCaller(classes.Node):
    """Python node that calls tick() on a DummyExposedTarget from Python.

    Measures the cost of Python → GDExtension-registered-Python-class method dispatch.
    Each instance creates its own DummyExposedTarget child in _ready() and calls
    tick() on it every frame.
    """

    def _ready(self) -> None:
        from logic.dummy_exposed_target import DummyExposedTarget

        target = DummyExposedTarget()
        self.add_child(target)
        # Plain Python instance attribute — not a Godot property, no declaration needed.
        self._target = target

    def _process(self, delta: float) -> None:
        self._target.tick()
