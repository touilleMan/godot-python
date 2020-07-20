from godot import exposed, export, EditorPlugin
from godot import *

from .python_export import PythonExport


BASE_RES = str(ProjectSettings.localize_path(__file__)).rsplit("/", 1)[0]
PYTHON_EXPORT_RES = ResourceLoader.load(f"{BASE_RES}/python_export.tscn")


@exposed(tool=True)
class Plugin(EditorPlugin):
    def _enter_tree(self):
        print("INIT export plugin")
        # Initialization of the plugin goes here
        self.plugin = PYTHON_EXPORT_RES.instance()
        self.add_export_plugin(self.plugin)
        print("INIT DONE")

    def _exit_tree(self):
        print("DESTROY export plugin")
        # Clean-up of the plugin goes here
        self.remove_export_plugin(self.plugin)
        self.plugin.queue_free()
        self.plugin = None

    def _ready(self):
        pass
