# `_pythonscript` module contains all the callbacks needed to expose Python
# as a language to Godot (see pythonscript.c for more on this).
# Hence there is no point of importing this module from Python given it
# only expose C functions.
# Beside this module depend on the `godot.hazmat` module so it would be a bad
# idea to make the `godot` module depend on it...
include "_pythonscript_editor.pxi"
# include "_godot_profiling.pxi"
# include "_godot_script.pxi"
# include "_godot_instance.pxi"
# include "_godot_io.pxi"

# from godot.hazmat.gdnative_api_struct cimport (
#     godot_gdnative_init_options,
#     godot_pluginscript_language_data,
# )
# from godot.hazmat.internal cimport set_pythonscript_verbose, get_pythonscript_verbose
from godot.builtins cimport GDString, Vector2, pystr_to_gdstr, gdstr_to_pystr

# def _setup_config_entry(name, default_value):
#     gdname = GDString(name)
#     if not ProjectSettings.has_setting(gdname):
#         ProjectSettings.set_setting(gdname, default_value)
#     ProjectSettings.set_initial_value(gdname, default_value)
#     # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
#     return ProjectSettings.get_setting(gdname)

from godot.hazmat.gdnative_interface cimport *
from godot.hazmat.gdapi cimport *


# include "_pythonscript_script.pxi"
# include "_pythonscript_instance.pxi"

cdef api GDNativeObjectPtr _pythonscript_create_instance(
    void *p_userdata
) with gil:
    return NULL


cdef api void _pythonscript_free_instance(
    void *p_userdata, GDExtensionClassInstancePtr p_instance
) with gil:
    pass


# Global reference on the godot api, this is guaranteed to be defined before
# Python is initialized.
# This reference is used by all the Cython modules (hence why `_pythonscript`
# is the very first Python module that gets loaded.


cdef api void _pythonscript_initialize() with gil:
    import sys
    from godot._version import __version__ as pythonscript_version
    r = gdstr_to_pystr(<GDNativeStringPtr*>&pystr_to_gdstr("foo")._gd_data)
    if r == "foo":
        pythonscript_gdapi.print_error("ok", "<function>", "<file>", 0)
    else:
        pythonscript_gdapi.print_error("ko", "<function>", "<file>", 0)

    cooked_sys_version = '.'.join(map(str, sys.version_info))
    print(f"Pythonscript {pythonscript_version} (CPython {cooked_sys_version})")
    print(f"PYTHONPATH: {sys.path}")
    v = Vector2(66.8, -77.99)
    v.x = 42
    print("===========>", v.x, v.y)
    v0 = v.ZERO
    print("===========> ZERO: ", v0.x, v0.y)
    print("===========> v.angle(): ", v.angle())
    print("===========> v.direction_to(v0): ", v.direction_to(v0))
    # v2 = Vector2(v)
    # cdef C_Vector2 cv = vector2_abs(<C_Vector2*>&v._gd_data)
    # v2._gd_data.x = cv.x
    # v2._gd_data.y = cv.y
    # print("+++++++++++>", v2.x, v2.y)

    # Now register Python as language into Godot
    cdef GDNativeExtensionClassCreationInfo info
    info.set_func = NULL  # GDNativeExtensionClassSet
    info.get_func = NULL  # GDNativeExtensionClassGet
    info.get_property_list_func = NULL  # GDNativeExtensionClassGetPropertyList
    info.free_property_list_func = NULL  # GDNativeExtensionClassFreePropertyList
    info.notification_func = NULL  # GDNativeExtensionClassNotification
    info.to_string_func = NULL  # GDNativeExtensionClassToString
    info.reference_func = NULL  # GDNativeExtensionClassReference
    info.unreference_func = NULL  # GDNativeExtensionClassUnreference
    info.create_instance_func = &_pythonscript_create_instance
    info.free_instance_func = &_pythonscript_free_instance
    info.get_virtual_func = NULL  # GDNativeExtensionClassGetVirtual
    info.get_rid_func = NULL  # GDNativeExtensionClassGetRID
    info.class_userdata = NULL  # void*
    pythonscript_gdapi.classdb_register_extension_class(
        pythonscript_gdlibrary,
        "PythonScriptLanguageExtension",
        "ScriptLanguageExtension",
        &info,
    )

    # cdef GDNativeExtensionClassMethodInfo info
    # info.name = NULL  # char* name
    # info.method_userdata = NULL  # void* method_userdata
    # info.call_func = NULL  # GDNativeExtensionClassMethodCall call_func
    # info.ptrcall_func = NULL  # GDNativeExtensionClassMethodPtrCall ptrcall_func
    # info.method_flags = NULL  # uint32_t method_flags
    # info.argument_count = NULL  # uint32_t argument_count
    # info.has_return_value = NULL  # GDNativeBool has_return_value
    # info.get_argument_type_func = NULL  # GDNativeExtensionClassMethodGetArgumentType get_argument_type_func
    # info.get_argument_info_func = NULL  # GDNativeExtensionClassMethodGetArgumentInfo get_argument_info_func
    # info.get_argument_metadata_func = NULL  # GDNativeExtensionClassMethodGetArgumentMetadata get_argument_metadata_func
    # info.default_argument_count = NULL  # uint32_t default_argument_count
    # info.default_arguments = NULL  # GDNativeVariantPtr* default_arguments
    # pythonscript_gdapi.classdb_register_extension_class_method(
    #     pythonscript_gdlibrary,
    #     "PythonScriptLanguageExtension",
    #     &info,
    # )


    # # OS and ProjectSettings are singletons exposed as global python objects,
    # # hence there are not available from a cimport
    # from godot.bindings import OS, ProjectSettings

    # # Provide argv arguments
    # sys.argv = ["godot"] + [str(x) for x in OS.get_cmdline_args()]

    # # Update PYTHONPATH according to configuration
    # pythonpath = str(_setup_config_entry("python_script/path", "res://;res://lib"))
    # for p in pythonpath.split(";"):
    #     p = ProjectSettings.globalize_path(GDString(p))
    #     sys.path.insert(0, str(p))

    # # Redirect stdout/stderr to have it in the Godot editor console
    # if _setup_config_entry("python_script/io_streams_capture", True):
    #     # Note we don't have to remove the stream capture in `pythonscript_finish` given
    #     # Godot print API is available until after the Python interpreter is teardown
    #     install_io_streams_capture()

    # # Enable verbose output from pythonscript framework
    # if _setup_config_entry("python_script/verbose", False):
    #     set_pythonscript_verbose(True)

    # # Finally proudly print banner ;-)
    # if _setup_config_entry("python_script/print_startup_info", True):
    #     cooked_sys_version = '.'.join(map(str, sys.version_info))
    #     print(f"Pythonscript {pythonscript_version} (CPython {cooked_sys_version})")

    # if get_pythonscript_verbose():
    #     print(f"PYTHONPATH: {sys.path}")


cdef api void _pythonscript_deinitialize() with gil:
    # /!\ When this function is called, the Python interpreter is fully operational
    # and might be running user-created threads doing concurrent stuff.
    # That will continue until `godot_gdnative_terminate` is called (which is
    # responsible for the actual teardown of the interpreter).
    pass
