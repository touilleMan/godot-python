import unittest
import sys

from godot import exposed
from godot.bindings import Node


@exposed
class Node(Node):

    def _ready(self):
        # TODO: use `OS.set_exit_code` when available here
        # os.listdir is not available, so list test modules by hand
        test_mods = (
            'test_vector2',
            'test_dynamic_bindings',
        )
        # Run tests here
        for mod in test_mods:
            print('\t=== Tests %s ===' % mod)
            try:
                unittest.main(mod)
            except Exception as exc:
                sys.print_exception(exc)
                break
        # Exit godot
        self.get_tree().quit()
