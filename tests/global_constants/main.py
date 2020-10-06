import traceback

from godot import exposed, Node, OS


@exposed
class Main(Node):
    def check_accessor_ok(self, name):
        node = self.get_node(name)
        if not node:
            print(f"Cannot retrieve node `{name}`")
            return False
        print(f"Node {name}, outcome: {node.outcome}")
        if str(node.outcome) != "ok":
            print(f"Node `{name}` had bad outcome `{node.outcome}`")
            return False
        return True

    def check_global_ok(self, name):
        path = f"/root/{name}"
        node = self.get_node(path)
        if not node:
            print(f"Cannot retrieve node `{path}`")
            return False
        accessors = {str(x) for x in node.accessors}
        if accessors != {"Python", "GDScript"}:
            print(f"Node `{name}` hasn't been correctly visited: {accessors}")
            return False
        return True

    def _ready(self):
        ok = True
        # Children _ready should have been called before us
        try:
            ok &= self.check_accessor_ok("access_from_gdscript")
            ok &= self.check_accessor_ok("access_from_python")
            ok &= self.check_global_ok("global_gd")
            ok &= self.check_global_ok("global_py")
        except Exception as exc:
            print("Unexpected error !")
            traceback.print_exc()
            ok = False

        if not ok:
            OS.set_exit_code(1)
        # Exit godot
        self.get_tree().quit()
