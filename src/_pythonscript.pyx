# `_pythonscript` module contains all the callbacks needed to expose Python
# as a language to Godot (see pythonscript.c for more on this).
# Hence there is no point of importing this module from Python given it
# only expose C functions.
# Beside this module depend on the `godot.hazmat` module so it would be a bad
# idea to make the `godot` module depend on it...
# include "_godot_editor.pxi"
# include "_godot_profiling.pxi"
# include "_godot_script.pxi"
# include "_godot_instance.pxi"
# include "_godot_io.pxi"

# from godot._hazmat.gdnative_api_struct cimport (
#     godot_gdnative_init_options,
#     godot_pluginscript_language_data,
# )
# from godot._hazmat.internal cimport set_pythonscript_verbose, get_pythonscript_verbose
# from godot.builtins cimport GDString

# def _setup_config_entry(name, default_value):
#     gdname = GDString(name)
#     if not ProjectSettings.has_setting(gdname):
#         ProjectSettings.set_setting(gdname, default_value)
#     ProjectSettings.set_initial_value(gdname, default_value)
#     # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
#     return ProjectSettings.get_setting(gdname)

from godot._hazmat.gdnative_interface cimport (
    GDNativeInterface,
)



cdef extern from * nogil:
    # Global variables defined in _pythonscript.pyx
    # Given _pythonscript.pyx is always the very first module loaded, we are
    # guanteed `pythonscript_gdapi` symbol is always resolved
    """
    #ifdef _WIN32
    # define DLL_EXPORT __declspec(dllexport)
    # define DLL_IMPORT __declspec(dllimport)
    #else
    # define DLL_EXPORT
    # define DLL_IMPORT
    #endif

    #include <godot/gdnative_interface.h>
    DLL_EXPORT extern const GDNativeInterface *pythonscript_gdapi;
    """

# Global pointer on Godot API used by all Cython modules
# This is configured by `pythonscript.c` before any Python code is actually
# called, hence pythonscript_gdapi is guarantee to be valid from Cython point
# of view
cdef public const GDNativeInterface *pythonscript_gdapi = NULL  # Declared as `public` is it symbol is not mangled
cdef api _pythonscript_set_gdapi(const GDNativeInterface *gdapi):
    global pythonscript_gdapi
    pythonscript_gdapi = gdapi


# Global reference on the godot api, this is guaranteed to be defined before
# Python is initialized.
# This reference is used by all the Cython modules (hence why `_pythonscript`
# is the very first Python module that gets loaded.


cdef api void _pythonscript_initialize() with gil:
    pythonscript_gdapi.print_warning(
        "foooooooooooooooooooooooooooooooooooooooooo",
        "_pythonscript_initialize",
        "_pythonscript.pyx",
        0,
    )

    import sys
    print('#######################################', file=sys.stderr)
    from godot._version import __version__ as pythonscript_version

    cooked_sys_version = '.'.join(map(str, sys.version_info))
    print(f"Pythonscript {pythonscript_version} (CPython {cooked_sys_version})")
    print(f"PYTHONPATH: {sys.path}")


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
