import os
import sys
import gc

from pythonscriptcffi import ffi

from godot import __version__
from godot.hazmat.base import destroy_exposed_classes
from godot.hazmat.io import enable_capture_io_streams
from godot.hazmat.ffi.script import enable_pythonscript_verbose
from godot.hazmat.gc_protector import protect_from_gc
from godot.bindings import OS, ProjectSettings


def connect_handle(obj):
    handle = obj.__dict__.get("_cffi_handle")
    if not handle:
        handle = ffi.new_handle(obj)
        obj._cffi_handle = handle
    return handle


def _setup_config_entry(name, default_value):
    if not ProjectSettings.has_setting(name):
        ProjectSettings.set_setting(name, default_value)
    ProjectSettings.set_initial_value(name, default_value)
    # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
    return ProjectSettings.get_setting(name)


@ffi.def_extern()
def pybind_init():
    # Make sure Python starts in the game directory
    os.chdir(ProjectSettings.globalize_path("res://"))

    # Pass argv arguments
    sys.argv = ["godot"] + list(OS.get_cmdline_args())

    # Update PYTHONPATH according to configuration
    pythonpath = _setup_config_entry("python_script/path", "res://;res://lib")
    for p in pythonpath.split(";"):
        p = ProjectSettings.globalize_path(p)
        sys.path.append(p)

    # Redirect stdout/stderr to have it in the Godot editor console
    if _setup_config_entry("python_script/io_streams_capture", True):
        enable_capture_io_streams()

    # Enable verbose output from pythonscript framework
    if _setup_config_entry("python_script/verbose", False):
        enable_pythonscript_verbose()

    # Finally display informative stuff ;-)
    if _setup_config_entry("python_script/print_startup_info", True):
        print("Pythonscript version: %s" % __version__)
        print(
            "Pythonscript backend: %s %s"
            % (sys.implementation.name, sys.version.replace("\n", " "))
        )
        print("PYTHONPATH: %s" % sys.path)

    return ffi.NULL


@ffi.def_extern()
def pybind_finish(handle):
    # Release Godot objects referenced by python wrappers
    protect_from_gc.clear()
    destroy_exposed_classes()
    gc.collect()
