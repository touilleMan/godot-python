from godot import Node, exposed, export, Array


@exposed
class global_py(Node):

    accessors = export(Array, default=Array())
    type = export(str, default="Python")

    def set_accessed(self, name):
        self.accessors.append(name)
