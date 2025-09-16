cimport cython
from cpython.ref cimport Py_INCREF, Py_DECREF, PyObject  # Needed for @godot_extension_class decorator

from .hazmat.gdextension_interface cimport *
from .hazmat.gdapi cimport *
from .hazmat cimport gdptrs
from .builtins cimport *
from .classes cimport _load_class, _load_singleton, _cleanup_loaded_classes_and_singletons, BaseGDObject

#
# Extensions definition
#

include "_lang_resource_format_loader.pxi"
include "_lang_resource_format_saver.pxi"
include "_lang_script_language.pxi"
include "_lang_script.pxi"
include "_lang_script_instance.pxi"
include "_lang_tags.pxi"


#
# Early init: Register `PythonScriptLanguage`/`PythonScript`/`PythonResourceFormat(Saver|Loader)` classes in Godot
#


cdef _early_register_classes():
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


cdef _early_unregister_classes():
    PythonResourceFormatSaver._PythonResourceFormatSaver__godot_extension_unregister_class()
    PythonResourceFormatLoader._PythonResourceFormatLoader__godot_extension_unregister_class()
    PythonScript._PythonScript__godot_extension_unregister_class()
    PythonScriptLanguage._PythonScriptLanguage__godot_extension_unregister_class()


#
# Late init: instantiate `PythonScriptLanguage` & friends and plug them into Godot
#


cdef _late_plug_language():
    print("[DEBUG] plug_language()", flush=True)

    _plug_language()
    _plug_resource_format_loader()
    _plug_resource_format_saver()


cdef _late_unplug_language():
    print("[DEBUG] unplug_language()", flush=True)

    _unplug_language()
    _unplug_resource_format_loader()
    _unplug_resource_format_saver()


cdef PythonScriptLanguage _python_script_language = None
cdef PythonResourceFormatLoader _python_resource_format_loader = None
cdef PythonResourceFormatSaver _python_resource_format_saver = None


# Plug as `Engine.register_script_language(PythonScriptLanguage())`
cdef _plug_language():
    global _python_script_language
    cdef GDExtensionObjectPtr engine
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args
    cdef StringName gdname_engine
    cdef StringName gdname_register_script_language
    cdef gd_int_t ret

    if _python_script_language is not None:
        return

    # Create the instance of `PythonScriptLanguage` class...

    _python_script_language = PythonScriptLanguage.__new__(PythonScriptLanguage)

    # ... and actually register Python into Godot \o/

    gdname_engine = StringName("Engine")
    gdname_register_script_language = StringName("register_script_language")
    engine = gdptrs.gdptr_global_get_singleton(&gdname_engine._gd_data)
    if engine == NULL:
        print("Failed to register Python into Godot: failed to retreive `Engine` singleton", flush=True)
        return

    bind = gdptrs.gdptr_classdb_get_method_bind(
        &gdname_engine._gd_data,
        &gdname_register_script_language._gd_data,
        1850254898,
    )
    if bind == NULL:
        _python_script_language = None
        print("Failed to register Python into Godot: failed to retreive `Engine::register_script_language`", flush=True)
        return

    args = [&_python_script_language._gd_ptr]
    gdptrs.gdptr_object_method_bind_ptrcall(
        bind,
        engine,
        args,
        &ret,
    )
    if ret != Error.OK:
        _python_script_language = None
        print(f"Failed to register Python into Godot: `Engine::register_script_language` returned error {ret}", flush=True)
        return


cdef void _unplug_language():
    global _python_script_language
    cdef StringName gdname_engine
    cdef StringName gdname_unregister_script_language
    cdef GDExtensionObjectPtr engine
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args
    cdef gd_int_t ret

    if _python_script_language is None:
        return

    # 1) Unregister the language

    gdname_engine = StringName("Engine")
    gdname_unregister_script_language = StringName("unregister_script_language")
    engine = gdptrs.gdptr_global_get_singleton(&gdname_engine._gd_data)
    if engine == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `Engine` singleton", flush=True)
        return

    bind = gdptrs.gdptr_classdb_get_method_bind(
        &gdname_engine._gd_data,
        &gdname_unregister_script_language._gd_data,
        1850254898,
    )
    if bind == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `Engine::unregister_script_language`", flush=True)
        return

    args = [&_python_script_language._gd_ptr]
    gdptrs.gdptr_object_method_bind_ptrcall(
        bind,
        engine,
        args,
        &ret,
    )
    if ret != Error.OK:
        print(f"Failed to unregister Python from Godot: `Engine::unregister_script_language` returned error {ret}", flush=True)
        return

    # 2) Free the language instance

    gdptrs.gdptr_object_destroy(
        _python_script_language._gd_ptr,
    )

    # At this point `_python_script_language._gd_ptr` is no longer a valid pointer
    # however this is fine since we are clearing the reference to it right now (so
    # nobody is going to use it anymore) and `_gd_ptr` field is simply ignored during
    # garbage collection.

    # 3) Finally clear reference on the language instance Python bindings

    _python_script_language = None


# Plug as `ResourceLoader.add_resource_format_loader(PythonResourceFormatLoader())`
cdef void _plug_resource_format_loader():
    global _python_resource_format_loader
    cdef GDExtensionObjectPtr resource_loader
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[2] args
    cdef StringName gdname_resource_loader
    cdef StringName gdname_add_resource_format_loader
    cdef gd_bool_t param_at_front = False

    if _python_resource_format_loader is not None:
        return

    # Create the instance of `PythonResourceFormatLoader` class...

    _python_resource_format_loader = PythonResourceFormatLoader.__new__(PythonResourceFormatLoader)

    # ... and actually register it into Godot \o/

    gdname_resource_loader = StringName("ResourceLoader")
    gdname_add_resource_format_loader = StringName("add_resource_format_loader")
    resource_loader = gdptrs.gdptr_global_get_singleton(&gdname_resource_loader._gd_data)
    if resource_loader == NULL:
        print("Failed to register Python into Godot: failed to retreive `ResourceLoader` singleton", flush=True)
        return

    bind = gdptrs.gdptr_classdb_get_method_bind(
        &gdname_resource_loader._gd_data,
        &gdname_add_resource_format_loader._gd_data,
        2896595483,
    )
    if bind == NULL:
        _python_resource_format_loader = None
        print("Failed to register Python into Godot: failed to retreive `ResourceLoader::add_resource_format_loader`", flush=True)
        return

    args = [&_python_resource_format_loader._gd_ptr, &param_at_front]
    gdptrs.gdptr_object_method_bind_ptrcall(
        bind,
        resource_loader,
        args,
        NULL,
    )


cdef void _unplug_resource_format_loader():
    global _python_resource_format_loader
    cdef StringName gdname_resource_loader
    cdef StringName gdname_remove_resource_format_loader
    cdef GDExtensionObjectPtr resource_loader
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args

    if _python_resource_format_loader is None:
        return

    # 1) Unregister from Godot

    gdname_resource_loader = StringName("ResourceLoader")
    gdname_remove_resource_format_loader = StringName("remove_resource_format_loader")
    resource_loader = gdptrs.gdptr_global_get_singleton(&gdname_resource_loader._gd_data)
    if resource_loader == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceLoader` singleton", flush=True)
        return

    bind = gdptrs.gdptr_classdb_get_method_bind(
        &gdname_resource_loader._gd_data,
        &gdname_remove_resource_format_loader._gd_data,
        405397102,
    )
    if bind == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceLoader::remove_resource_format_loader`", flush=True)
        return

    args = [&_python_resource_format_loader._gd_ptr]
    gdptrs.gdptr_object_method_bind_ptrcall(
        bind,
        resource_loader,
        args,
        NULL,
    )

    # At this point `_python_resource_format_loader._gd_ptr` is no longer a valid pointer
    # (`ResourceLoader::remove_resource_format_loader` has destroyed it), however this is
    # fine since we are clearing the reference to `_python_resource_format_loader` right
    # now (so nobody is going to use it anymore) and `_gd_ptr` field is simply ignored
    # during garbage collection.

    # 2) Finally clear reference on the language instance Python bindings

    _python_resource_format_loader = None


# Plug as `ResourceSaver.add_resource_format_saver(PythonResourceFormatSaver())`
cdef void _plug_resource_format_saver():
    global _python_resource_format_saver
    cdef GDExtensionObjectPtr resource_saver
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[2] args
    cdef StringName gdname_resource_saver
    cdef StringName gdname_add_resource_format_saver
    cdef gd_bool_t param_at_front = False

    if _python_resource_format_saver is not None:
        return

    # Create the instance of `PythonResourceFormatSaver` class...

    _python_resource_format_saver = PythonResourceFormatSaver.__new__(PythonResourceFormatSaver)

    # ... and actually register it into Godot \o/

    gdname_resource_saver = StringName("ResourceSaver")
    gdname_add_resource_format_saver = StringName("add_resource_format_saver")
    resource_saver = gdptrs.gdptr_global_get_singleton(&gdname_resource_saver._gd_data)
    if resource_saver == NULL:
        print("Failed to register Python into Godot: failed to retreive `ResourceSaver` singleton", flush=True)
        return

    bind = gdptrs.gdptr_classdb_get_method_bind(
        &gdname_resource_saver._gd_data,
        &gdname_add_resource_format_saver._gd_data,
        362894272,
    )
    if bind == NULL:
        _python_resource_format_saver = None
        print("Failed to register Python into Godot: failed to retreive `ResourceSaver::add_resource_format_saver`", flush=True)
        return

    args = [&_python_resource_format_saver._gd_ptr, &param_at_front]
    gdptrs.gdptr_object_method_bind_ptrcall(
        bind,
        resource_saver,
        args,
        NULL,
    )


cdef void _unplug_resource_format_saver():
    global _python_resource_format_saver
    cdef StringName gdname_resource_saver
    cdef StringName gdname_remove_resource_format_saver
    cdef GDExtensionObjectPtr resource_saver
    cdef GDExtensionMethodBindPtr bind
    cdef GDExtensionConstTypePtr[1] args

    if _python_resource_format_saver is None:
        return

    # 1) Unregister from Godot

    gdname_resource_saver = StringName("ResourceSaver")
    gdname_remove_resource_format_saver = StringName("remove_resource_format_saver")
    resource_saver = gdptrs.gdptr_global_get_singleton(&gdname_resource_saver._gd_data)
    if resource_saver == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceSaver` singleton", flush=True)
        return

    bind = gdptrs.gdptr_classdb_get_method_bind(
        &gdname_resource_saver._gd_data,
        &gdname_remove_resource_format_saver._gd_data,
        3373026878,
    )
    if bind == NULL:
        print("Failed to unregister Python from Godot: failed to retreive `ResourceSaver::remove_resource_format_saver`", flush=True)
        return

    args = [&_python_resource_format_saver._gd_ptr]
    gdptrs.gdptr_object_method_bind_ptrcall(
        bind,
        resource_saver,
        args,
        NULL,
    )

    # At this point `_python_resource_format_saver._gd_ptr` is no longer a valid pointer
    # (`ResourceSaver::remove_resource_format_saver` has destroyed it), however this is
    # fine since we are clearing the reference to `_python_resource_format_saver` right
    # now (so nobody is going to use it anymore) and `_gd_ptr` field is simply ignored
    # during garbage collection.

    # 2) Finally clear reference on the language instance Python bindings

    _python_resource_format_saver = None


#
# Godot project settings helpers
#


cdef object _setup_project_settings_entry(name: str, default_value: object):
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


cdef void _apply_python_config_from_project_settings():
    import sys
    cdef BaseGDObject ProjectSettings = <BaseGDObject>_load_singleton("ProjectSettings")

    # # Redirect stdout/stderr to have it in the Godot editor console
    # if _setup_project_settings_entry("python/io_streams_capture", True):
    #     # Note we don't have to remove the stream capture in `gdpy_finish` given
    #     # Godot print API is available until after the Python interpreter is teardown
    #     install_io_streams_capture()

    # # Enable verbose output from Godot-Python framework
    # if _setup_project_settings_entry("python/verbose", False):
    #     set_gdpy_verbose(True)

    # Update PYTHONPATH according to configuration
    pythonpath = str(_setup_project_settings_entry("python/path", "res://;res://lib"))
    for p in pythonpath.split(";"):
        p = ProjectSettings.globalize_path(GDString(p))
        sys.path.insert(0, str(p))


#
# Project initial/deinitialize callbacks
#


cdef object _initialize_callback = None
cdef object _initialize_callback_hook(int p_level):
    global _initialize_callback
    cdef GDString config

    if _initialize_callback is None:
        try:
            config = <GDString?>_setup_project_settings_entry("python/initialize_callback", "")
        except TypeError as exc:
            raise ValueError("Invalid value for config `python/initialize_callback`: expected a string in format `<module>:<function>`") from exc

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
    cdef GDString config

    if _deinitialize_callback is None:
        try:
            config = <GDString?>_setup_project_settings_entry("python/deinitialize_callback", "")
        except TypeError as exc:
            raise ValueError("Invalid value for config `python/deinitialize_callback`: expected a string in format `<module>:<function>`") from exc

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


cdef void _print_banner():
    import sys

    if _setup_project_settings_entry("python/print_startup_info", True):
        from godot._version import __version__ as gdpy_version
        cooked_sys_version = '.'.join(map(str, sys.version_info))
        print(f"Godot-Python {gdpy_version} (CPython {cooked_sys_version})", flush=True)

    if _setup_project_settings_entry("python/verbose", True):
        print(f"PYTHONPATH: {sys.path}", flush=True)


cdef void _gdpy_initialize(int p_level) noexcept with gil:
    cdef BaseGDObject OS
    cdef PackedStringArray args

    if p_level == GDEXTENSION_INITIALIZATION_SERVERS:
        _early_register_classes()

    # Language registration must be done at `GDEXTENSION_INITIALIZATION_SERVERS` level which
    # is too early to have have everything we need for (e.g. `ClassDB` & `OS` singletons).
    # So we have to do another init step at `GDEXTENSION_INITIALIZATION_SCENE` level.
    if p_level == GDEXTENSION_INITIALIZATION_SCENE:
        import sys

        # When CPython is embedded into Godot, `sys.argv` is not initialized (and
        # hence `sys.argv == [""]`). In such case, now is the time to configure it.
        if len(sys.argv) == 1 and sys.argv[0] == "":
            OS = <BaseGDObject>_load_singleton("OS")
            args = <PackedStringArray?>OS.get_cmdline_args()
            sys.argv = ["godot"]
            for arg in args:
                sys.argv.append(str(arg))

        _apply_python_config_from_project_settings()

        _late_plug_language()

        # Finally proudly print banner ;-)
        _print_banner()

    if p_level >= GDEXTENSION_INITIALIZATION_SCENE:
        _initialize_callback_hook(p_level)


cdef void _gdpy_deinitialize(int p_level) noexcept with gil:
    # /!\ When this function is called, the Python interpreter is fully operational
    # and might be running user-created threads doing concurrent stuff.
    # That will continue until `godot_gdnative_terminate` is called (which is
    # responsible for the actual teardown of the interpreter).

    if p_level >= GDEXTENSION_INITIALIZATION_SCENE:
        _deinitialize_callback_hook(p_level)

    if p_level == GDEXTENSION_INITIALIZATION_SCENE:
        _late_unplug_language()

    if p_level == GDEXTENSION_INITIALIZATION_SERVERS:

        # Unregister Python classes from Godot's classDB

        _early_unregister_classes()

        _cleanup_loaded_classes_and_singletons()

        # TODO: needed ?
        # gc_protector = _get_extension_gc_protector()
        # print('!!!!!!!! gc_protector', repr(gc_protector))
        # gc_protector.clear()


# Given how simple those functions are, we don't want to bother with C header
# include and linkage considerations. Instead we just expose their function
# pointers as Python objects that will be fetch using the C Python API.
gdpy_initialize_function_ptr = <size_t>_gdpy_initialize
gdpy_deinitialize_function_ptr = <size_t>_gdpy_deinitialize
