# `_godot` module contains all the callbacks needed by Godot's Pluginscript
# system to expose Python as a language to Godot (see pythonscript.c for
# more on this).
# Hence there is no point of importing this module from Python given it
# only expose C functions.
# Beside this module depend on the `godot.hazmat` module so it would be a bad
# idea to make the `godot` module depend on it...
include "_godot_editor.pxi"
include "_godot_profiling.pxi"
include "_godot_script.pxi"
include "_godot_instance.pxi"

from godot._hazmat.gdnative_api_struct cimport (
    godot_gdnative_init_options,
    godot_pluginscript_language_data,
)
from godot._hazmat.internal cimport set_pythonscript_verbose, get_pythonscript_verbose
from godot.builtins cimport GDString

import os
import sys

import godot
from godot.bindings import OS, ProjectSettings


def _setup_config_entry(name, default_value):
    gdname = GDString(name)
    if not ProjectSettings.has_setting(gdname):
        ProjectSettings.set_setting(gdname, default_value)
    ProjectSettings.set_initial_value(gdname, default_value)
    # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
    return ProjectSettings.get_setting(gdname)


cdef api godot_pluginscript_language_data *pythonscript_init():
    # Pass argv arguments
    sys.argv = ["godot"] + [str(x) for x in OS.get_cmdline_args()]

    # Update PYTHONPATH according to configuration
    pythonpath = str(_setup_config_entry("python_script/path", "res://;res://lib"))
    for p in pythonpath.split(";"):
        p = ProjectSettings.globalize_path(GDString(p))
        sys.path.append(str(p))

    # TODO
    # Redirect stdout/stderr to have it in the Godot editor console
    # if _setup_config_entry("python_script/io_streams_capture", True):
    #     enable_capture_io_streams()

    # Enable verbose output from pythonscript framework
    if _setup_config_entry("python_script/verbose", False):
        set_pythonscript_verbose(True)

    # Finally proudly print banner ;-)
    if _setup_config_entry("python_script/print_startup_info", True):
        cooked_sys_version = '.'.join(map(str, sys.version_info))
        print(f"Pythonscript {godot.__version__} (CPython {cooked_sys_version})")

    if get_pythonscript_verbose():
        print(f"PYTHONPATH: {sys.path}")

    return NULL


cdef api void pythonscript_finish(godot_pluginscript_language_data *data):
    return
