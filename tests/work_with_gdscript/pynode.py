from godot import exposed, export, Node


@exposed
class PyNode(Node):
    _ready_called = False
    _overloaded_by_child_prop_value = None

    def _ready(self):
        self._ready_called = True

    def is_ready_called(self):
        return self._ready_called

    def meth(self, attr):
        return attr

    def overloaded_by_child_meth(self, attr):
        return attr

    @staticmethod
    def static_meth(attr):
        return f"static:{attr}"

    prop = export(int)

    @export(str, default="default")
    @property
    def overloaded_by_child_prop(self):
        return self._overloaded_by_child_prop_value

    @overloaded_by_child_prop.setter
    def overloaded_by_child_prop(self, value):
        self._overloaded_by_child_prop_value = value

    def print_tree(self):
        # Overloaded native method
        return """
  *
 ***
*****
  |
"""
