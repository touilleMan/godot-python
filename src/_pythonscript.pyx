# `_pythonscript` module contains all the callbacks needed to expose Python
# as a language to Godot (see pythonscript.c for more on this).
# Hence there is no point of importing this module from Python given it
# only expose C functions.
# Beside this module depend on the `godot.hazmat` module so it would be a bad
# idea to make the `godot` module depend on it...

cimport cython
from cpython.ref cimport Py_INCREF, Py_DECREF, PyObject  # Needed for @godot_extension_class decorator
from godot.hazmat.gdextension_interface cimport *
from godot.hazmat.gdapi cimport *
from godot.hazmat.extension_class cimport *
from godot.builtins cimport *
from godot.classes cimport _load_class, _load_singleton

include "_pythonscript_editor.pxi"
include "_pythonscript_extension_class_language.pxi"
include "_pythonscript_extension_class_script.pxi"
# include "_godot_profiling.pxi"
# include "_godot_script.pxi"
# include "_godot_instance.pxi"
# include "_godot_io.pxi"

# from godot.hazmat.gdnative_api_struct cimport (
#     godot_gdnative_init_options,
#     godot_pluginscript_language_data,
# )
# from godot.hazmat.internal cimport set_pythonscript_verbose, get_pythonscript_verbose

# def _setup_config_entry(name, default_value):
#     gdname = GDString(name)
#     if not ProjectSettings.has_setting(gdname):
#         ProjectSettings.set_setting(gdname, default_value)
#     ProjectSettings.set_initial_value(gdname, default_value)
#     # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
#     return ProjectSettings.get_setting(gdname)

# include "_pythonscript_script.pxi"
# include "_pythonscript_instance.pxi"


cdef PythonScriptLanguage _pythons_script_language = None


cdef api GDExtensionObjectPtr _pythonscript_create_instance(
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


cdef _testbench():
    # Test builtins
    v = Vector2i(66, -77)
    assert v.x == 66
    assert v.y == -77
    # Set property
    v.x = 42
    assert v.x == 42
    # Access property
    v0 = v.ZERO
    assert v0.x == 0
    assert v0.y == 0
    assert v0 == v.ZERO
    v0.x = 1
    assert v0 != v.ZERO
    # Access method with no params
    assert isinstance(v.angle(), int)
    # Access method with params
    assert isinstance(v.dot(v), int)
    # Access method with no return value
    c = Color()
    assert c.set_r8(0xAABBCCDD) is None

    # Test classes
    OS = _load_singleton("OS")

    # print(repr(OS), dir(OS))
    print('OS.low_processor_usage_mode', OS.low_processor_usage_mode)
    # print('OS.get_cache_dir()', OS.get_cache_dir())
    # print('OS.can_use_threads()', OS.can_use_threads())
    OS.low_processor_usage_mode = True
    print('OS.low_processor_usage_mode == True', OS.low_processor_usage_mode)
    # print('OS.set_environment("foo", "bar")', OS.set_environment("foo", "bar"))
    # print('OS.get_environment("foo")', OS.get_environment("foo"))


cdef api void _pythonscript_late_init() with gil:
    global _pythons_script_language
    cdef GDExtensionObjectPtr singleton
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionTypePtr[1] args
    cdef StringName gdname_engine
    cdef StringName gdname_register_script_language
    # _testbench()

    # 2) Create an instance of `PythonScriptLanguage` class
    if _pythons_script_language is None:

        _pythons_script_language = PythonScriptLanguage.__new__(PythonScriptLanguage)

        # 3) Actually register Python into Godot \o/
        gdname_engine = StringName("Engine")
        gdname_register_script_language = StringName("register_script_language")
        singleton = pythonscript_gdextension.global_get_singleton(&gdname_engine._gd_data)
        bind = pythonscript_gdextension.classdb_get_method_bind(
            &gdname_engine._gd_data,
            &gdname_register_script_language._gd_data,
            1327703655,
        )
        args = [_pythons_script_language._gd_ptr]
        pythonscript_gdextension.object_method_bind_ptrcall(
            bind,
            singleton,
            # Cast on args is required given autopxd2 incorrectly removes the const
            # attributes when converting gdextension_interface.c to .pxd
            <const void * const*>args,
            NULL,
        )

    import sys
    from godot._version import __version__ as pythonscript_version

    cooked_sys_version = '.'.join(map(str, sys.version_info))
    print(f"Pythonscript {pythonscript_version} (CPython {cooked_sys_version})")
    print(f"PYTHONPATH: {sys.path}")


cdef api void _pythonscript_early_init() with gil:
    # Here is how we register Python into Godot:
    #
    # GDExtension API allows us to register "extension classes", those will be seen from
    # Godot as a regular class (e.g. you could hack into Godot code, remove the KinematicBody
    # class, create an extension that implement KinematicBody, and you platformer project would
    # run just fine).
    #
    # To implement a language in Godot you must create a class inheriting `LanguageExtension` and
    # register into the `LanguageServer`. This is what is done within Godot to implement GDScript.
    #
    # So we register a `PythonLanguage` extension class than inherits `ScriptLanguageExtension`
    # (the latter being just a proxy to `LanguageExtension`) and call `Engine.register_script_language`
    # (which is a simple wrapper given `LanguageServer` is private within Godot) by passing it
    # an instance of our brand new `PythonLanguage`.
    #
    # see: https://docs.godotengine.org/en/latest/classes/class_scriptlanguageextension.html

    # 1) Register `PythonScript` class into Godot
    PythonScriptLanguage.__godot_extension_register_class()
    PythonScript.__godot_extension_register_class()


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
    # TODO: unregister the language once https://github.com/godotengine/godot/pull/67155 is merged

    if _pythons_script_language is not None:
        # Cannot unregister the class given it is in use, and cannot stop using
        # the instance given...
        return

    # /!\ When this function is called, the Python interpreter is fully operational
    # and might be running user-created threads doing concurrent stuff.
    # That will continue until `godot_gdnative_terminate` is called (which is
    # responsible for the actual teardown of the interpreter).

    PythonScript.__godot_extension_unregister_class()
    PythonScriptLanguage.__godot_extension_unregister_class()
