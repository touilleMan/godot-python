from godot import exposed, export, Node2D


@exposed
class MyExportedCls(Node2D):
    initialized = False
    _python_prop = None

    def _ready(self):
        self.initialized = True

    def python_method(self, attr):
        return attr

    python_prop_static = export(str)

    @export(int, default=42)
    @property
    def python_prop(self):
        return self._python_prop

    @python_prop.setter
    def python_prop(self, value):
        self._python_prop = value
