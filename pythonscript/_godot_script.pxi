# cython: c_string_type=unicode, c_string_encoding=utf8

from godot.gdnative_api_struct cimport (
    godot_pluginscript_language_data,
    godot_string,
    godot_bool,
    godot_array,
    godot_pool_string_array,
    godot_object,
    godot_variant,
    godot_error,
    godot_pluginscript_script_data,
    godot_pluginscript_script_manifest
)
from _godot cimport gdapi


cdef api godot_pluginscript_script_manifest pythonscript_script_init(
	godot_pluginscript_language_data *p_data,
	const godot_string *p_path,
	const godot_string *p_source,
	godot_error *r_error
):
	pass


cdef api void pythonscript_script_finish(
	godot_pluginscript_script_data *p_data
):
	pass
