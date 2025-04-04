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
from godot.classes cimport _load_class, _load_singleton, _cleanup_loaded_classes_and_singletons

include "_pythonscript_editor.pxi"
include "_pythonscript_extension_class_language.pxi"
include "_pythonscript_extension_class_script.pxi"
include "_pythonscript_extension_resource_format_loader.pxi"
include "_pythonscript_extension_resource_format_saver.pxi"
# include "_godot_profiling.pxi"
# include "_godot_script.pxi"
# include "_godot_instance.pxi"
# include "_godot_io.pxi"

# from godot.hazmat.gdnative_api_struct cimport (
#     godot_gdnative_init_options,
#     godot_pluginscript_language_data,
# )
# from godot.hazmat.internal cimport set_pythonscript_verbose, get_pythonscript_verbose

def _setup_config_entry(name: str, default_value: object):
    # Cannot use `None` as config value since it is used in Godot to erase
    # custom project settings.
    # see https://docs.godotengine.org/en/stable/classes/class_projectsettings.html#class-projectsettings-method-set-setting
    assert default_value is not None

    ProjectSettings = _load_singleton("ProjectSettings")
    gdname = GDString(name)

    if not ProjectSettings.has_setting(gdname):
        ProjectSettings.set_setting(gdname, default_value)

    ProjectSettings.set_initial_value(gdname, default_value)
    ProjectSettings.set_restart_if_changed(gdname, True)

    return ProjectSettings.get_setting(gdname)

# include "_pythonscript_script.pxi"
# include "_pythonscript_instance.pxi"


cdef PythonScriptLanguage _pythons_script_language = None
cdef PythonResourceFormatLoader _python_resource_format_loader = None
cdef PythonResourceFormatSaver _python_resource_format_saver = None


cdef public GDExtensionObjectPtr _pythonscript_create_instance(
    void *p_userdata
) noexcept with gil:
    return NULL


cdef public void _pythonscript_free_instance(
    void *p_userdata, GDExtensionClassInstancePtr p_instance
) noexcept with gil:
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


# Early init: register `PythonScriptLanguage` & `PythonScript` classes in Godot
cdef void _register_pythonscript_classes():
    # Here is how we register Python into Godot:
    #
    # GDExtension API allows us to register "extension classes", those will be seen from
    # Godot as a regular class (e.g. you could hack into Godot code, remove the KinematicBody
    # class, create an extension that implement `KinematicBody`, and your platformer project would
    # run just fine).
    #
    # To implement a language in Godot you must create a class inheriting `LanguageExtension` and
    # register into the `LanguageServer`. This is what is done within Godot to implement `GDScript`.
    #
    # So we register a `PythonLanguage` extension class than inherits `ScriptLanguageExtension`
    # (the latter being just a proxy to `LanguageExtension`) and call `Engine.register_script_language`
    # (which is a simple wrapper given `LanguageServer` is private within Godot) with an instance
    # of our brand new `PythonLanguage` as parameter.
    #
    # see: https://docs.godotengine.org/en/latest/classes/class_scriptlanguageextension.html

    # See `scripts/gdextension_cython_preprocessor.py` for the detail of
    # `__godot_extension_register_class`'s implementation.

    PythonScriptLanguage._PythonScriptLanguage__godot_extension_register_class()
    PythonScript._PythonScript__godot_extension_register_class()
    PythonResourceFormatLoader._PythonResourceFormatLoader__godot_extension_register_class()
    PythonResourceFormatSaver._PythonResourceFormatSaver__godot_extension_register_class()


cdef void _unregister_pythonscript_classes():
    PythonResourceFormatSaver._PythonResourceFormatSaver__godot_extension_unregister_class()
    PythonResourceFormatLoader._PythonResourceFormatLoader__godot_extension_unregister_class()
    PythonScript._PythonScript__godot_extension_unregister_class()
    PythonScriptLanguage._PythonScriptLanguage__godot_extension_unregister_class()


cdef void _customize_config():
    import sys
    ProjectSettings = _load_singleton("ProjectSettings")
    OS = _load_singleton("OS")

    # Provide argv arguments

    args = OS.get_cmdline_args()
    sys.argv = ["godot"]
    # TODO: iteration on `PackedStringArray` not supported yet !
    for i in range(args.size()):
        sys.argv.append(str(args[i]))

    # # Redirect stdout/stderr to have it in the Godot editor console
    # if _setup_config_entry("python/io_streams_capture", True):
    #     # Note we don't have to remove the stream capture in `pythonscript_finish` given
    #     # Godot print API is available until after the Python interpreter is teardown
    #     install_io_streams_capture()

    # # Enable verbose output from pythonscript framework
    # if _setup_config_entry("python/verbose", False):
    #     set_pythonscript_verbose(True)

    # Update PYTHONPATH according to configuration
    pythonpath = str(_setup_config_entry("python/path", "res://;res://lib"))
    for p in pythonpath.split(";"):
        p = ProjectSettings.globalize_path(GDString(p))
        sys.path.insert(0, str(p))


cdef object _initialize_callback = None
cdef object _initialize_callback_hook(int p_level):
    global _initialize_callback

    if _initialize_callback is None:
        config = _setup_config_entry("python/initialize_callback", "")

        if not isinstance(config, GDString):
            raise ValueError("Invalid value for config `python/initialize_callback`: expected a string in format `<module>:<function>`")

        if config.is_empty():
            _initialize_callback = lambda _level: None  # Dummy callback

        else:
            try:
                module, function = str(config).split(":")
            except ValueError:
                raise ValueError("Invalid value for config `python/initialize_callback`: expected a string in format `<module>:<function>`") from None

            import importlib
            try:
                module = importlib.import_module(module)
            except ModuleNotFoundError:
                raise ValueError(f"Invalid value for config `python/initialize_callback`: cannot load module `{module}`")
            try:
                _initialize_callback = getattr(module, function)
            except AttributeError:
                raise ValueError(f"Invalid value for config `python/initialize_callback`: module `{module}` has no attribute `{function}`")

    try:
        _initialize_callback(p_level)
    except Exception as exc:
        raise ValueError(f"Invalid value for config `python/initialize_callback`: callback `{module}:{function}` call has failed") from exc


cdef object _deinitialize_callback = None
cdef object _deinitialize_callback_hook(int p_level):
    global _deinitialize_callback

    if _deinitialize_callback is None:
        config = _setup_config_entry("python/deinitialize_callback", "")

        if not isinstance(config, GDString):
            raise ValueError("Invalid value for config `python/deinitialize_callback`: expected a string in format `<module>:<function>`")

        if config.is_empty():
            _deinitialize_callback = lambda _level: None  # Dummy callback

        else:
            try:
                module, function = str(config).split(":")
            except ValueError:
                raise ValueError("Invalid value for config `python/deinitialize_callback`: expected a string in format `<module>:<function>`")

            import importlib
            try:
                module = importlib.import_module(module)
            except ModuleNotFoundError:
                raise ValueError(f"Invalid value for config `python/deinitialize_callback`: cannot load module `{module}`")
            try:
                _deinitialize_callback = getattr(module, function)
            except AttributeError:
                raise ValueError(f"Invalid value for config `python/deinitialize_callback`: module `{module}` has no attribute `{function}`")

    try:
        _deinitialize_callback(p_level)
    except Exception as exc:
        raise ValueError(f"Invalid value for config `python/deinitialize_callback`: callback `{module}:{function}` call has failed") from exc


# Late init: instantiate `PythonScriptLanguage`
cdef void _register_pythonscript_language():
    global _pythons_script_language
    cdef GDExtensionObjectPtr engine
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args
    cdef StringName gdname_engine
    cdef StringName gdname_register_script_language
    cdef gd_int_t ret

    if _pythons_script_language is not None:
        return

    # Create the instance of `PythonScriptLanguage` class...

    _pythons_script_language = PythonScriptLanguage.__new__(PythonScriptLanguage)

    # ... and actually register Python into Godot \o/

    gdname_engine = StringName("Engine")
    gdname_register_script_language = StringName("register_script_language")
    engine = pythonscript_gdextension.global_get_singleton(&gdname_engine._gd_data)
    if engine == NULL:
        print("Failed to register Python into Godot: failed to retreive `Engine` singleton", flush=True)
        return

    bind = pythonscript_gdextension.classdb_get_method_bind(
        &gdname_engine._gd_data,
        &gdname_register_script_language._gd_data,
        1850254898,
    )
    if bind == NULL:
        _pythons_script_language = None
        print("Failed to register Python into Godot: failed to retreive `Engine::register_script_language`", flush=True)
        return

    args = [&_pythons_script_language._gd_ptr]
    pythonscript_gdextension.object_method_bind_ptrcall(
        bind,
        engine,
        args,
        &ret,
    )
    if ret != Error.OK:
        _pythons_script_language = None
        print("Failed to register Python into Godot: `Engine::register_script_language` returned error {ret}", flush=True)
        return


cdef void _unregister_pythonscript_language():
    global _pythons_script_language
    cdef StringName gdname_engine
    cdef StringName gdname_unregister_script_language
    cdef GDExtensionObjectPtr engine
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args
    cdef gd_int_t ret

    if _pythons_script_language is None:
        return

    # 1) Unregister the language

    gdname_engine = StringName("Engine")
    gdname_unregister_script_language = StringName("unregister_script_language")
    engine = pythonscript_gdextension.global_get_singleton(&gdname_engine._gd_data)
    if engine == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `Engine` singleton", flush=True)
        return

    bind = pythonscript_gdextension.classdb_get_method_bind(
        &gdname_engine._gd_data,
        &gdname_unregister_script_language._gd_data,
        1850254898,
    )
    if bind == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `Engine::unregister_script_language`", flush=True)
        return

    args = [&_pythons_script_language._gd_ptr]
    pythonscript_gdextension.object_method_bind_ptrcall(
        bind,
        engine,
        args,
        &ret,
    )
    if ret != Error.OK:
        print(f"Failed to unregister Python from Godot: `Engine::unregister_script_language` returned error {ret}", flush=True)
        return

    # 2) Free the language instance

    pythonscript_gdextension.object_destroy(
        _pythons_script_language._gd_ptr,
    )

    # At this point `_pythons_script_language._gd_ptr` is no longer a valid pointer
    # however this is fine since we are clearing the reference to it right now (so
    # nobody is going to use it anymore) and `_gd_ptr` field is simply ignored during
    # garbage collection.

    # 3) Finally clear reference on the language instance Python bindings

    _pythons_script_language = None


# Late init: instantiate `PythonResourceFormatLoader`
cdef void _register_pythonscript_resource_format_loader():
    global _python_resource_format_loader
    cdef GDExtensionObjectPtr resource_loader
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[2] args
    cdef StringName gdname_resource_loader
    cdef StringName gdname_add_resource_format_loader
    cdef gd_bool_t param_at_front = False

    if _python_resource_format_loader is not None:
        return

    print("_register_pythonscript_resource_format_loader", flush=True)

    # Create the instance of `PythonResourceFormatLoader` class...

    _python_resource_format_loader = PythonResourceFormatLoader.__new__(PythonResourceFormatLoader)

    # ... and actually register it into Godot \o/

    gdname_resource_loader = StringName("ResourceLoader")
    gdname_add_resource_format_loader = StringName("add_resource_format_loader")
    resource_loader = pythonscript_gdextension.global_get_singleton(&gdname_resource_loader._gd_data)
    if resource_loader == NULL:
        print("Failed to register Python into Godot: failed to retreive `ResourceLoader` singleton", flush=True)
        return

    bind = pythonscript_gdextension.classdb_get_method_bind(
        &gdname_resource_loader._gd_data,
        &gdname_add_resource_format_loader._gd_data,
        2896595483,
    )
    if bind == NULL:
        _python_resource_format_loader = None
        print("Failed to register Python into Godot: failed to retreive `ResourceLoader::add_resource_format_loader`", flush=True)
        return

    args = [&_python_resource_format_loader._gd_ptr, &param_at_front]
    pythonscript_gdextension.object_method_bind_ptrcall(
        bind,
        resource_loader,
        args,
        NULL,
    )


cdef void _unregister_pythonscript_resource_format_loader():
    global _python_resource_format_loader
    cdef StringName gdname_resource_loader
    cdef StringName gdname_remove_resource_format_loader
    cdef GDExtensionObjectPtr resource_loader
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args

    if _python_resource_format_loader is None:
        return

    print("_unregister_pythonscript_resource_format_loader", flush=True)

    # 1) Unregister from Godot

    gdname_resource_loader = StringName("ResourceLoader")
    gdname_remove_resource_format_loader = StringName("remove_resource_format_loader")
    resource_loader = pythonscript_gdextension.global_get_singleton(&gdname_resource_loader._gd_data)
    if resource_loader == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceLoader` singleton", flush=True)
        return

    bind = pythonscript_gdextension.classdb_get_method_bind(
        &gdname_resource_loader._gd_data,
        &gdname_remove_resource_format_loader._gd_data,
        405397102,
    )
    if bind == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceLoader::remove_resource_format_loader`", flush=True)
        return

    args = [&_python_resource_format_loader._gd_ptr]
    pythonscript_gdextension.object_method_bind_ptrcall(
        bind,
        resource_loader,
        args,
        NULL,
    )

    # 2) Free the object instance

    pythonscript_gdextension.object_destroy(
        _python_resource_format_loader._gd_ptr,
    )

    # At this point `_python_resource_format_loader._gd_ptr` is no longer a valid pointer
    # however this is fine since we are clearing the reference to it right now (so
    # nobody is going to use it anymore) and `_gd_ptr` field is simply ignored during
    # garbage collection.

    # 3) Finally clear reference on the language instance Python bindings

    _python_resource_format_loader = None


# Late init: instantiate `PythonResourceFormatSaver`
cdef void _register_pythonscript_resource_format_saver():
    global _python_resource_format_saver
    cdef GDExtensionObjectPtr resource_saver
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[2] args
    cdef StringName gdname_resource_saver
    cdef StringName gdname_add_resource_format_saver
    cdef gd_bool_t param_at_front = False

    if _python_resource_format_saver is not None:
        return

    print("_register_pythonscript_resource_format_saver", flush=True)

    # Create the instance of `PythonResourceFormatSaver` class...

    _python_resource_format_saver = PythonResourceFormatSaver.__new__(PythonResourceFormatSaver)

    # ... and actually register it into Godot \o/

    gdname_resource_saver = StringName("ResourceSaver")
    gdname_add_resource_format_saver = StringName("add_resource_format_saver")
    resource_saver = pythonscript_gdextension.global_get_singleton(&gdname_resource_saver._gd_data)
    if resource_saver == NULL:
        print("Failed to register Python into Godot: failed to retreive `ResourceSaver` singleton", flush=True)
        return

    bind = pythonscript_gdextension.classdb_get_method_bind(
        &gdname_resource_saver._gd_data,
        &gdname_add_resource_format_saver._gd_data,
        362894272,
    )
    if bind == NULL:
        _python_resource_format_saver = None
        print("Failed to register Python into Godot: failed to retreive `ResourceSaver::add_resource_format_saver`", flush=True)
        return

    args = [&_python_resource_format_saver._gd_ptr, &param_at_front]
    pythonscript_gdextension.object_method_bind_ptrcall(
        bind,
        resource_saver,
        args,
        NULL,
    )


cdef void _unregister_pythonscript_resource_format_saver():
    global _python_resource_format_saver
    cdef StringName gdname_resource_saver
    cdef StringName gdname_remove_resource_format_saver
    cdef GDExtensionObjectPtr resource_saver
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args

    if _python_resource_format_saver is None:
        return

    print("_unregister_pythonscript_resource_format_saver", flush=True)

    # 1) Unregister from Godot

    gdname_resource_saver = StringName("ResourceSaver")
    gdname_remove_resource_format_saver = StringName("remove_resource_format_saver")
    resource_saver = pythonscript_gdextension.global_get_singleton(&gdname_resource_saver._gd_data)
    if resource_saver == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceSaver` singleton", flush=True)
        return

    bind = pythonscript_gdextension.classdb_get_method_bind(
        &gdname_resource_saver._gd_data,
        &gdname_remove_resource_format_saver._gd_data,
        3373026878,
    )
    if bind == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceSaver::remove_resource_format_saver`", flush=True)
        return

    args = [&_python_resource_format_saver._gd_ptr]
    pythonscript_gdextension.object_method_bind_ptrcall(
        bind,
        resource_saver,
        args,
        NULL,
    )

    # 2) Free the object instance

    pythonscript_gdextension.object_destroy(
        _python_resource_format_saver._gd_ptr,
    )

    # At this point `_python_resource_format_saver._gd_ptr` is no longer a valid pointer
    # however this is fine since we are clearing the reference to it right now (so
    # nobody is going to use it anymore) and `_gd_ptr` field is simply ignored during
    # garbage collection.

    # 3) Finally clear reference on the language instance Python bindings

    _python_resource_format_saver = None


cdef void _print_banner():
    import sys

    if _setup_config_entry("python/print_startup_info", True):
        from godot._version import __version__ as pythonscript_version
        cooked_sys_version = '.'.join(map(str, sys.version_info))
        print(f"Pythonscript {pythonscript_version} (CPython {cooked_sys_version})", flush=True)

    if _setup_config_entry("python/verbose", True):
        print(f"PYTHONPATH: {sys.path}", flush=True)


cdef public void _pythonscript_initialize(int p_level) noexcept with gil:
    if p_level == GDEXTENSION_INITIALIZATION_SERVERS:
        _register_pythonscript_classes()

    # Language registration must be done at `GDEXTENSION_INITIALIZATION_SERVERS` level which
    # is too early to have have everything we need for (e.g. `ClassDB` & `OS` singletons).
    # So we have to do another init step at `GDEXTENSION_INITIALIZATION_SCENE` level.
    if p_level == GDEXTENSION_INITIALIZATION_SCENE:
        _customize_config()
        _register_pythonscript_language()
        _register_pythonscript_resource_format_loader()
        _register_pythonscript_resource_format_saver()
        # Finally proudly print banner ;-)
        _print_banner()

    if p_level >= GDEXTENSION_INITIALIZATION_SCENE:
        _initialize_callback_hook(p_level)


cdef public void _pythonscript_deinitialize(int p_level) noexcept with gil:
    global _pythons_script_language

    # /!\ When this function is called, the Python interpreter is fully operational
    # and might be running user-created threads doing concurrent stuff.
    # That will continue until `godot_gdnative_terminate` is called (which is
    # responsible for the actual teardown of the interpreter).

    if p_level >= GDEXTENSION_INITIALIZATION_SCENE:
        _deinitialize_callback_hook(p_level)

    if p_level == GDEXTENSION_INITIALIZATION_SCENE and _pythons_script_language is not None:
        _unregister_pythonscript_resource_format_saver()
        _unregister_pythonscript_resource_format_loader()
        _unregister_pythonscript_language()

    if p_level == GDEXTENSION_INITIALIZATION_SERVERS:

        # Unregister Python classes from Godot's classDB

        _unregister_pythonscript_classes()
        _cleanup_loaded_classes_and_singletons()

        # TODO: needed ?
        # gc_protector = _get_extension_gc_protector()
        # print('!!!!!!!! gc_protector', repr(gc_protector))
        # gc_protector.clear()
