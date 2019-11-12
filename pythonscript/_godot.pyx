include "_godot_editor.pxi"
include "_godot_profiling.pxi"
include "_godot_script.pxi"
include "_godot_instance.pxi"

from godot.hazmat.gdnative_api_struct cimport (
    godot_gdnative_init_options,
    godot_pluginscript_language_data,
)


cdef api void pythonscript_print_banner():
    import sys
    import godot
    cooked_sys_version = '.'.join(map(str, sys.version_info))
    print(f"Pythonscript {godot.__version__} CPython {cooked_sys_version}")


cdef api godot_pluginscript_language_data *pythonscript_init():
    return NULL


cdef api void pythonscript_finish(godot_pluginscript_language_data *data):
    return
