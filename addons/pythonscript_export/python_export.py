import sys
import code
from godot import exposed, EditorExportPlugin


@exposed(tool=True)
class PythonExport(EditorExportPlugin):
    def _export_begin(features, is_debug, path, flags):
        print("=======> _export_begin", features, is_debug, path, flags)

    def _export_end():
        print("=======> _export_end")
