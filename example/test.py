from godot import exposed, export
# from godot.bindings import Node2D, Object, Vector2, KEY_F5, OS
from godot.bindings import Object


# v = Vector2(1, 2)
# print('Vector2.x', Vector2.x)
# print("Vector2.x.getter", Vector2.x.getter)
# print("Vector2().x", Vector2().x)
# print('BEFORE', v)
# v.x = 1.5
# print('AFTER', v)
# Vector2().x = 1
# p = property(lambda x: x.X)
# print(p, p.getter(T()))
# print(T.x, T.x.getter, T.x.getter(T()))
# print(Vector2.width, Vector2().width, Vector2.width is Vector2().width)
# print('W', dir(v.width), v.width.getter('a'))
# print('KEY_F5', KEY_F5)
# print('--->', OS.get_unix_time())


@exposed
class MyExportedCls(Object):

    # member variables here, example:
    a = export(int)
    b = export(str)

    def _ready(self):
        """
        Called every time the node is added to the scene.
        Initialization here.
        """
        print("Hello World !")
        print("Instance ID:", self.get_instance_ID())
        # print('OLD ROT:', self.get_rot())
        # self.rotate(1.5)
        # print('NEW ROT:', self.get_rot())
