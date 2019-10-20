# cython: c_string_type=unicode, c_string_encoding=utf8

from godot.gdnative_api_struct cimport (
    godot_pluginscript_language_data,
    godot_pluginscript_profiling_data,
)
from godot.hazmat cimport gdapi


cdef api void pythonscript_profiling_start(
    godot_pluginscript_language_data *p_data
):
    pass


cdef api void pythonscript_profiling_stop(
    godot_pluginscript_language_data *p_data
):
    pass


cdef api int pythonscript_profiling_get_accumulated_data(
    godot_pluginscript_language_data *p_data,
    godot_pluginscript_profiling_data *r_info,
    int p_info_max
):
    pass


cdef api int pythonscript_profiling_get_frame_data(
    godot_pluginscript_language_data *p_data,
    godot_pluginscript_profiling_data *r_info,
    int p_info_max
):
    pass


cdef api void pythonscript_profiling_frame(
    godot_pluginscript_language_data *p_data
):
    pass
