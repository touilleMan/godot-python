# Testing Godot-Python

Tests are divided on multiple stages:

- `0-gdscript`: Simple Godot project with only GDScript.
- `1-gdextension`: Godot project with a pure-C GDExtension.
- `2-init-with-python-hook`: Godot project loading Godot-Python as GDExtension, with a
  Python module (i.e. `my.py`) configured as initialization hook.
- `3-init-with-cython-hook`: Same as stage 2, but with a Cython module (i.e. `my.pyx`)
  configured as initialization hook.
- `4-use-godot-from-python`: 🚧 WIP 🚧
- `5-use-godot-from-cython`: 🚧 WIP 🚧
- `6-expose-python-to-godot`: 🚧 WIP 🚧
- `7-expose-cython-to-godot`: 🚧 WIP 🚧

Stages 0 & 1 don't involve Godot-Python at all and are only here to ensure the no prior
issues are present (e.g. bug in new Godot release, weird behavior on exotic platform...).

Stages 2&3 ensure Godot-Python initialize fine, and that we can run Python and Cython
modules from the CPython interpreter embedded in Godot.
