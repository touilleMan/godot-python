from godot import gddataclass, classes


@gddataclass(init=False)
class DummyExposedTarget(classes.Node):
    """Python class registered with Godot, used as the callee in the exposed-class benchmark.

    Provides a single `tick()` method that is callable from both GDScript and Python,
    going through Godot's virtual-call dispatch in both cases.
    """

    _counter: int

    def __init__(self):
        super().__init__()
        self._counter = 0

    def tick(self) -> int:
        self._counter += 1
        return self._counter
