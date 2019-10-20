from .gdnative_api_struct cimport (
    godot_gdnative_api_struct,
    godot_gdnative_init_options,
    godot_gdnative_core_api_struct,
    godot_gdnative_core_1_1_api_struct,
    godot_gdnative_core_1_2_api_struct,
    godot_gdnative_ext_nativescript_api_struct,
    godot_gdnative_ext_pluginscript_api_struct,
    godot_gdnative_ext_android_api_struct,
    godot_gdnative_ext_arvr_api_struct,
    godot_pluginscript_language_data,
    GDNATIVE_EXT_NATIVESCRIPT,
    GDNATIVE_EXT_PLUGINSCRIPT,
    GDNATIVE_EXT_ANDROID,
    GDNATIVE_EXT_ARVR,
)


cdef const godot_gdnative_core_api_struct *gdapi
cdef const godot_gdnative_core_1_1_api_struct *gdapi11
cdef const godot_gdnative_core_1_2_api_struct *gdapi12
cdef const godot_gdnative_ext_nativescript_api_struct *gdapi_ext_nativescript
cdef const godot_gdnative_ext_pluginscript_api_struct *gdapi_ext_pluginscript
cdef const godot_gdnative_ext_android_api_struct *gdapi_ext_android
cdef const godot_gdnative_ext_arvr_api_struct *gdapi_ext_arvr


cdef void _register_gdapi(const godot_gdnative_init_options *options):
    global gdapi
    global gdapi11
    global gdapi12
    global gdapi_ext_nativescript
    global gdapi_ext_pluginscript
    global gdapi_ext_android
    global gdapi_ext_arvr

    gdapi = <const godot_gdnative_core_api_struct *>options.api_struct
    gdapi11 = NULL
    gdapi12 = NULL
    if gdapi.next:
        gdapi11 = <const godot_gdnative_core_1_1_api_struct *>gdapi.next
        if gdapi11.next:
            gdapi12 = <const godot_gdnative_core_1_2_api_struct *>gdapi11.next

    cdef const godot_gdnative_api_struct *ext
    for i in range(gdapi.num_extensions):
        ext = gdapi.extensions[i]
        if ext.type == GDNATIVE_EXT_NATIVESCRIPT:
            gdapi_ext_nativescript = <const godot_gdnative_ext_nativescript_api_struct *>ext;
        elif ext.type == GDNATIVE_EXT_PLUGINSCRIPT:
            gdapi_ext_pluginscript = <const godot_gdnative_ext_pluginscript_api_struct *>ext;
        elif ext.type == GDNATIVE_EXT_ANDROID:
            gdapi_ext_android = <const godot_gdnative_ext_android_api_struct *>ext;
        elif ext.type == GDNATIVE_EXT_ARVR:
            gdapi_ext_arvr = <const godot_gdnative_ext_arvr_api_struct *>ext;
        else:
            print(f"Pythonscript: Unknown extension type `{ext.type}`")
