from godot import exposed, export
from godot.bindings import Node2D, Object, Vector2


print('A', Vector2())
print('B', Vector2(1.122344))
print('C', Vector2(1, 2))

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
        print("Hello World !")
        print('OLD ROT:', self.get_rot())
        self.rotate(1.5)
        print('NEW ROT:', self.get_rot())
