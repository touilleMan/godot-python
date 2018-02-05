import sys

from godot.hazmat.lazy_bindings import LazyBindingsModule
from godot.hazmat.recursive import godot_bindings_module


godot_bindings_module.__class__ = LazyBindingsModule
godot_bindings_module.__init__(__name__)

sys.modules[__name__] = godot_bindings_module
