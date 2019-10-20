include "_godot_editor.pxi"
include "_godot_profiling.pxi"
include "_godot_script.pxi"
include "_godot_instance.pxi"

from godot.gdnative_api_struct cimport (
    godot_gdnative_init_options,
    godot_pluginscript_language_data,
)
from _godot_gdapi cimport _register_gdapi


cdef api void pythonscript_register_gdapi(const godot_gdnative_init_options *options):
    _register_gdapi(options)


cdef api void pythonscript_print_banner():
    import sys
    print("import godot...")
    import godot
    print("done !")
    cooked_sys_version = '.'.join(map(str, sys.version_info))
    print(f"Pythonscript {godot.__version__} CPython {cooked_sys_version}")


cdef api godot_pluginscript_language_data *pythonscript_init():
    return NULL


cdef api void pythonscript_finish(godot_pluginscript_language_data *data):
    return
