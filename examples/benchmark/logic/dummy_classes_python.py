from godot import gddataclass, classes
from godot.singletons import Time, OS, Engine


@gddataclass(init=False)
class DummyClassesPython(classes.Node):
    """Python node stressing calls into Godot class methods.

    Each _process() call makes several calls on Godot singleton classes
    (Time, OS, Engine) and on Node instances obtained from the scene tree.

    This measures the round-trip cost of Python→Godot class method dispatch,
    i.e. the overhead of calling a bound method on a Godot Object from Python.
    """

    def _process(self, delta: float) -> None:
        # --- Godot singleton methods (Python → Godot class dispatch) ---
        _t_ms = Time.get_ticks_msec()
        _t_us = Time.get_ticks_usec()
        _os_name = OS.get_name()
        _fps = Engine.get_frames_per_second()
        _frames = Engine.get_process_frames()

        # --- Node tree traversal (Python → Godot Node method calls) ---
        root = self.get_tree().get_root()
        _root_name = root.get_name()
        _root_children = root.get_child_count()
        _parent = self.get_parent()
        _parent_name = _parent.get_name()
