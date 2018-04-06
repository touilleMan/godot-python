"""
This module contains the autoloaded nodes. To do so it starts empty and
will be updated during Godot init phase by calls to
`godot.hazmat.editor.pybind_add_global_constant`.
Note the init of this module is done in two steps: first before any script
is loaded the constants' names are defined, then before any _ready is
called the constants' values are set.
"""
