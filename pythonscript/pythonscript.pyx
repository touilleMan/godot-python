# cython: language_level=3

from gdnative_api_struct cimport godot_gdnative_core_api_struct, godot_pluginscript_language_data

cdef godot_gdnative_core_api_struct gdapi

cdef api godot_pluginscript_language_data *pythonscript_init():
	return NULL

cdef api void pythonscript_finish(godot_pluginscript_language_data *data):
	return
