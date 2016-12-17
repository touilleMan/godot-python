from godot import exposed, export
from godot.bindings import Node2D, Object


print("rn ==>", Node2D, Object().get_instance_ID())


@exposed
class MyExportedCls(Node2D):

    # member variables here, example:
    a = export(int)
    b = export(str)

    def _ready(self):
        """
        Called every time the node is added to the scene.
        Initialization here.
        """
        pass
