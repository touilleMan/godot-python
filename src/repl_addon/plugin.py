from godot import exposed, EditorPlugin, ProjectSettings, ResourceLoader


BASE_RES = str(ProjectSettings.localize_path(__file__)).rsplit("/", 1)[0]
PYTHON_REPL_RES = ResourceLoader.load(f"{BASE_RES}/python_repl.tscn")


@exposed(tool=True)
class plugin(EditorPlugin):
    def _enter_tree(self):
        # Initialization of the plugin goes here
        self.repl = PYTHON_REPL_RES.instance()
        self.repl_button = self.add_control_to_bottom_panel(self.repl, "Python REPL")

    def _exit_tree(self):
        # Clean-up of the plugin goes here
        self.remove_control_from_bottom_panel(self.repl)
        self.repl.queue_free()
        self.repl = None
