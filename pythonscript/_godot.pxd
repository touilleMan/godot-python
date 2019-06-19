from godot.gdnative_api_struct cimport (
    godot_gdnative_core_api_struct,
    godot_gdnative_ext_nativescript_api_struct,
    godot_gdnative_ext_pluginscript_api_struct,
    godot_gdnative_ext_android_api_struct,
    godot_gdnative_ext_arvr_api_struct,
)


cdef const godot_gdnative_core_api_struct *gdapi
cdef const godot_gdnative_ext_nativescript_api_struct *gdapi_ext_nativescript
cdef const godot_gdnative_ext_pluginscript_api_struct *gdapi_ext_pluginscript
cdef const godot_gdnative_ext_android_api_struct *gdapi_ext_android
cdef const godot_gdnative_ext_arvr_api_struct *gdapi_ext_arvr
