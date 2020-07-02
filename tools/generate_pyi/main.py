from os import getcwd
from godot import exposed, Node, OS, bindings, builtins


@exposed
class Main(Node):
    def _ready(self):
        out = "godot_pyi"
        print(f"Generating {getcwd()}/{out}")
        try:
            from mypy.stubgen import generate_stubs, parse_options

            options = parse_options(["-p", "godot.bindings", "-o", out])
            generate_stubs(options)
        except BaseException as exc:
            import traceback

            traceback.print_exc()
            OS.set_exit_code(1)
        # Exit godot
        self.get_tree().quit()
