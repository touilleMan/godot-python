# `_godot` module contains all the callbacks needed by Godot's Pluginscript
# system to expose Python as a language to Godot (see pythonscript.c for
# more on this).
# Hence there is no point of importing this module from Python given it
# only expose C functions.
# Beside this module depend on the `godot.hazmat` module so it would be a bad
# idea to make the `godot` module depend on it...

include "_godot_editor.pxi"
include "_godot_profiling.pxi"
include "_godot_script.pxi"
include "_godot_instance.pxi"


from godot.hazmat.gdnative_api_struct cimport (
    godot_gdnative_init_options,
    godot_pluginscript_language_data,
)


cdef api godot_pluginscript_language_data *pythonscript_init():
	# Print banner
    import sys
    import godot
    cooked_sys_version = '.'.join(map(str, sys.version_info))
    print(f"Pythonscript {godot.__version__} CPython {cooked_sys_version}")
    return NULL


cdef api void pythonscript_finish(godot_pluginscript_language_data *data):
    return
