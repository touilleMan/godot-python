import inspect
import traceback

from pythonscriptcffi import ffi, lib

from godot.hazmat.base import BaseObject, get_exposed_class_per_module
from godot.hazmat.gc_protector import connect_handle
from godot.hazmat.tools import (
    godot_string_to_pyobj,
    godot_string_from_pyobj,
    py_to_gd_type,
)
from godot.bindings import Dictionary, Array

# Set to True to show script loading progress; set by enable_pythonscript_verbose
verbose = False


def enable_pythonscript_verbose():
    """Enable verbose output from pythonscript startup"""
    verbose = True


def _build_script_manifest(cls):

    def _build_signal_info(signal):
        methinfo = Dictionary()
        methinfo["name"] = signal.name
        # Dummy data, only name is important here
        methinfo["args"] = Array()
        methinfo["default_args"] = Array()
        methinfo["return"] = None
        methinfo["flags"] = lib.METHOD_FLAG_FROM_SCRIPT
        return methinfo

    def _build_method_info(meth, methname):
        spec = inspect.getfullargspec(meth)
        methinfo = Dictionary()
        methinfo["name"] = methname
        # TODO: Handle classmethod/staticmethod
        methinfo["args"] = Array(spec.args)
        methinfo["default_args"] = Array()  # TODO
        # TODO: use annotation to determine return type ?
        methinfo["return"] = None
        methinfo["flags"] = lib.METHOD_FLAG_FROM_SCRIPT
        methinfo["rpc_mode"] = getattr(
            meth, "__rpc", lib.GODOT_METHOD_RPC_MODE_DISABLED
        )
        return methinfo

    def _build_property_info(prop):
        propinfo = Dictionary()
        propinfo["name"] = prop.name
        propinfo["type"] = py_to_gd_type(prop.type)
        propinfo["hint"] = prop.hint
        propinfo["hint_string"] = prop.hint_string
        propinfo["usage"] = prop.usage
        propinfo["default_value"] = prop.default
        propinfo["rset_mode"] = prop.rpc
        return propinfo

    manifest = ffi.new("godot_pluginscript_script_manifest*")
    manifest.data = connect_handle(cls)
    # TODO: should be able to use lib.godot_string_new_with_wide_string directly
    gdname = godot_string_from_pyobj(cls.__name__)
    lib.godot_string_name_new(ffi.addressof(manifest.name), gdname)
    if cls.__bases__:
        # Only one Godot parent class (checked at class definition time)
        godot_parent_class = next(
            (b for b in cls.__bases__ if issubclass(b, BaseObject))
        )
        if godot_parent_class.__dict__.get("__is_godot_native_class"):
            path = godot_parent_class.__name__
        else:
            # Pluginscript wants us to return the parent as a path
            path = "res://%s.py" % "/".join(cls.__bases__[0].__module__.split("."))
        gdbase = godot_string_from_pyobj(path)
        lib.godot_string_name_new(ffi.addressof(manifest.base), gdbase)
    manifest.is_tool = cls.__tool
    lib.godot_dictionary_new(ffi.addressof(manifest.member_lines))
    lib.godot_array_new(ffi.addressof(manifest.methods))
    methods = Array()
    # TODO: include inherited in exposed methods ? Expose Godot base class' ones ?
    # for methname in vars(cls):
    for methname in dir(cls):
        meth = getattr(cls, methname)
        if not inspect.isfunction(meth) or meth.__name__.startswith("__"):
            continue

        methinfo = _build_method_info(meth, methname)
        methods.append(methinfo)

    signals = Array()
    for signal in cls.__signals.values():
        signalinfo = _build_signal_info(signal)
        signals.append(signalinfo)

    properties = Array()
    for prop in cls.__exported.values():
        property_info = _build_property_info(prop)
        properties.append(property_info)

    lib.godot_array_new_copy(ffi.addressof(manifest.methods), methods._gd_ptr)
    lib.godot_array_new_copy(ffi.addressof(manifest.signals), signals._gd_ptr)
    lib.godot_array_new_copy(ffi.addressof(manifest.properties), properties._gd_ptr)
    return manifest


@ffi.def_extern()
def pybind_script_init(handle, path, source, r_error):
    path = godot_string_to_pyobj(path)
    if verbose:
        print("Loading python script from %s" % path)
    if (
        not path.startswith("res://")
        or not path.rsplit(".", 1)[-1] in ("py", "pyc", "pyo", "pyd")
    ):
        print(
            "Bad python script path `%s`, must starts by `res://` and ends with `.py/pyc/pyo/pyd`"
            % path
        )
        r_error[0] = lib.GODOT_ERR_FILE_BAD_PATH
        return ffi.NULL

    # TODO: possible bug if res:// is not part of PYTHONPATH
    # Remove `res://`, `.py` and replace / by .
    modname = path[6:].rsplit(".", 1)[0].replace("/", ".")
    try:
        __import__(modname)  # Force lazy loading of the module
        # TODO: make sure script reloading works
        cls = get_exposed_class_per_module(modname)
    except Exception:
        # If we are here it could be because the file doesn't exists
        # or (more possibly) the file content is not a valid python (or
        # miss an exposed class)
        print(
            "Got exception loading %s (%s): %s"
            % (path, modname, traceback.format_exc())
        )
        r_error[0] = lib.GODOT_ERR_PARSE_ERROR
        # Obliged to return the structure, but no need in init it
        return ffi.new("godot_pluginscript_script_manifest*")[0]

    r_error[0] = lib.GODOT_OK
    return _build_script_manifest(cls)[0]


@ffi.def_extern()
def pybind_script_finish(cls_handle):
    # TODO: unload the script
    pass
