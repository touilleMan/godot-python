# Testing Godot-Python

Tests are divided on multiple stages:

- `0-gdscript`: Simple Godot project with only GDScript.
- `1-gdextension`: Godot project with a pure-C GDExtension.
- `2-pythonscript-init`: Godot project loading Godot-Python as GDExtension.
- `3-pythonscript-cython-only`: 🚧 WIP 🚧 Godot project using Godot-Python to run Cython code.
- `4-pythonscript-python`: 🚧 WIP 🚧 Godot project using Godot-Python to run Python code.

Stages 0 & 1 don't involve Godot-Python at all and are only here to ensure the no prior
issues are present (e.g. bug in new Godot release, weird behavior on exotic platform...).
