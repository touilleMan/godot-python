from godot import exposed, export
from godot.bindings import Node2D


@exposed
class MyExportedCls(Node2D):
    initialized = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._python_prop = None

    def _ready(self):
        self.initialized = True

    def python_method(self, attr):
        return attr

    @export(int)
    @property
    def python_getter(self):
        return self._python_prop

    @python_getter.setter
    def python_getter(self, value):
        self._python_prop = value
