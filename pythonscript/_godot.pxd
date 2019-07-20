from godot.gdnative_api_struct cimport (
    godot_gdnative_core_api_struct,
    godot_gdnative_core_1_1_api_struct,
    godot_gdnative_core_1_2_api_struct,
    godot_gdnative_ext_nativescript_api_struct,
    godot_gdnative_ext_pluginscript_api_struct,
    godot_gdnative_ext_android_api_struct,
    godot_gdnative_ext_arvr_api_struct,
)


cdef const godot_gdnative_core_api_struct *gdapi
cdef const godot_gdnative_core_1_1_api_struct *gdapi11
cdef const godot_gdnative_core_1_2_api_struct *gdapi12
cdef const godot_gdnative_ext_nativescript_api_struct *gdapi_ext_nativescript
cdef const godot_gdnative_ext_pluginscript_api_struct *gdapi_ext_pluginscript
cdef const godot_gdnative_ext_android_api_struct *gdapi_ext_android
cdef const godot_gdnative_ext_arvr_api_struct *gdapi_ext_arvr
