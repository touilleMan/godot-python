from godot import exposed, export

from pynode import PyNode


@exposed
class PySubNode(PyNode):
    _sub_ready_called = False
    _overloaded_by_child_prop_value = None

    def _ready(self):
        super()._ready()
        self._sub_ready_called = True

    def is_sub_ready_called(self):
        return self._sub_ready_called

    def overloaded_by_child_meth(self, attr):
        return f"sub:{attr}"

    @export(str, default="default")
    @property
    def overloaded_by_child_prop(self):
        return self._overloaded_by_child_prop_value

    @overloaded_by_child_prop.setter
    def overloaded_by_child_prop(self, value):
        self._overloaded_by_child_prop_value = f"sub:{value}"
