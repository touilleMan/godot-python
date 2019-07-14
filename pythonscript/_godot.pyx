include "_godot_editor.pxi"
include "_godot_profiling.pxi"
include "_godot_script.pxi"
include "_godot_instance.pxi"

from godot.gdnative_api_struct cimport (
    godot_gdnative_api_struct,
    godot_gdnative_init_options,
    godot_gdnative_core_api_struct,
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
cdef const godot_gdnative_ext_nativescript_api_struct *gdapi_ext_nativescript
cdef const godot_gdnative_ext_pluginscript_api_struct *gdapi_ext_pluginscript
cdef const godot_gdnative_ext_android_api_struct *gdapi_ext_android
cdef const godot_gdnative_ext_arvr_api_struct *gdapi_ext_arvr


cdef api void pythonscript_register_gdapi(const godot_gdnative_init_options *options):
    global gdapi
    global gdapi_ext_nativescript
    global gdapi_ext_pluginscript
    global gdapi_ext_android
    global gdapi_ext_arvr

    gdapi = <const godot_gdnative_core_api_struct *>options.api_struct
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


cdef api void pythonscript_print_banner():
    import sys
    import godot
    cooked_sys_version = sys.version.replace("\n", "")
    print(f"Pythonscript {godot.__version__} CPython {cooked_sys_version}")


cdef api godot_pluginscript_language_data *pythonscript_init():
    return NULL


cdef api void pythonscript_finish(godot_pluginscript_language_data *data):
    return
