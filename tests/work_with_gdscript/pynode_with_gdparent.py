from godot import exposed
from godot.bindings import ResourceLoader


GDNode = ResourceLoader.load("res://gdnode.gd", "", False)


@exposed
class PyNodeWithGDParent(GDNode):
    pass
