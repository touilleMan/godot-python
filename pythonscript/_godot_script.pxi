# cython: c_string_type=unicode, c_string_encoding=utf8

import importlib

from cpython.ref cimport PyObject

from godot._hazmat.gdnative_api_struct cimport (
    godot_pluginscript_language_data,
    godot_string,
    godot_bool,
    godot_array,
    godot_pool_string_array,
    godot_object,
    godot_variant,
    godot_error,
    godot_string_name,
    godot_pluginscript_script_data,
    godot_pluginscript_script_manifest,
    GODOT_OK,
    GODOT_ERR_UNAVAILABLE,
    GODOT_ERR_FILE_BAD_PATH,
    GODOT_ERR_PARSE_ERROR,
    GODOT_METHOD_FLAG_FROM_SCRIPT,
    GODOT_METHOD_RPC_MODE_DISABLED,
)
from godot._hazmat.gdapi cimport pythonscript_gdapi10 as gdapi10
from godot._hazmat.conversion cimport (
    godot_string_to_pyobj,
    pyobj_to_godot_string,
    pyobj_to_godot_string_name,
    pytype_to_godot_type,
)
from godot._hazmat.internal cimport (
    get_pythonscript_verbose,
    get_exposed_class,
    set_exposed_class,
    destroy_exposed_class,
)
from godot.bindings cimport _initialize_bindings, Object
from godot.builtins cimport Array, Dictionary

import inspect
import traceback

from godot.tags import ExportedField, SignalField


cdef inline godot_pluginscript_script_manifest _build_empty_script_manifest():
    cdef godot_pluginscript_script_manifest manifest
    manifest.data = NULL
    gdapi10.godot_string_name_new_data(&manifest.name, "")
    manifest.is_tool = False
    gdapi10.godot_string_name_new_data(&manifest.base, "")
    gdapi10.godot_dictionary_new(&manifest.member_lines)
    gdapi10.godot_array_new(&manifest.methods)
    gdapi10.godot_array_new(&manifest.signals)
    gdapi10.godot_array_new(&manifest.properties)
    return manifest


cdef Dictionary _build_signal_info(object signal):
    cdef Dictionary methinfo = Dictionary()
    methinfo["name"] = signal.name
    # Dummy data, only name is important here
    methinfo["args"] = Array()
    methinfo["default_args"] = Array()
    methinfo["return"] = None
    methinfo["flags"] = GODOT_METHOD_FLAG_FROM_SCRIPT
    return methinfo


cdef Dictionary _build_method_info(object meth, object methname):
    cdef Dictionary methinfo = Dictionary()
    spec = inspect.getfullargspec(meth)
    methinfo["name"] = methname
    # TODO: Handle classmethod/staticmethod
    methinfo["args"] = Array(spec.args)
    methinfo["default_args"] = Array()  # TODO
    # TODO: use annotation to determine return type ?
    methinfo["return"] = None
    methinfo["flags"] = GODOT_METHOD_FLAG_FROM_SCRIPT
    methinfo["rpc_mode"] = getattr(
        meth, "__rpc", GODOT_METHOD_RPC_MODE_DISABLED
    )
    return methinfo


cdef Dictionary _build_property_info(object prop):
    cdef Dictionary propinfo = Dictionary()
    propinfo["name"] = prop.name
    propinfo["type"] = pytype_to_godot_type(prop.type)
    propinfo["hint"] = prop.hint
    propinfo["hint_string"] = prop.hint_string
    propinfo["usage"] = prop.usage
    propinfo["default_value"] = prop.default
    propinfo["rset_mode"] = prop.rpc
    return propinfo

cdef inline object is_method(object meth):
    if inspect.isfunction(meth):
        return True

    if 'cython_function' in type(meth).__name__:
        return True

    return False

cdef godot_pluginscript_script_manifest _build_script_manifest(object cls):
    cdef godot_pluginscript_script_manifest manifest
    # No need to increase refcount here given `cls` is guaranteed to be kept
    # until we call `destroy_exposed_class`
    manifest.data = <PyObject*>cls
    pyobj_to_godot_string_name(cls.__name__, &manifest.name)
    manifest.is_tool = cls.__tool
    gdapi10.godot_dictionary_new(&manifest.member_lines)

    if cls.__bases__:
        # Only one Godot parent class (checked at class definition time)
        godot_parent_class = next(
            (b for b in cls.__bases__ if issubclass(b, Object))
        )
        if not godot_parent_class.__dict__.get("__exposed_python_class"):
            base = godot_parent_class.__name__
        else:
            # Pluginscript wants us to return the parent as a path
            base = f"res://{godot_parent_class.__module__.replace('.', '/')}.py"
        pyobj_to_godot_string_name(base, &manifest.base)

    methods = Array()
    signals = Array()
    properties = Array()
    for k, v in cls.__exported.items():
        if isinstance(v, ExportedField):
            properties.append(_build_property_info(v))
        elif isinstance(v, SignalField):
            signals.append(_build_signal_info(v))
        else:
            assert is_method(v)
            methods.append(_build_method_info(v, k))
    gdapi10.godot_array_new_copy(&manifest.methods, &methods._gd_data)
    gdapi10.godot_array_new_copy(&manifest.signals, &signals._gd_data)
    gdapi10.godot_array_new_copy(&manifest.properties, &properties._gd_data)

    return manifest


cdef api godot_pluginscript_script_manifest pythonscript_script_init(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_path,
    const godot_string *p_source,
    godot_error *r_error
) with gil:
    # Godot class&singleton are not all available at Pythonscript bootstrap.
    # Hence we wait until the Pythonscript start being actually used (i.e. until
    # the first Python script is loaded) before initializing the bindings.
    _initialize_bindings()

    cdef object path = godot_string_to_pyobj(p_path)
    if get_pythonscript_verbose():
        print(f"Loading python script from {path}")

    if not path.startswith("res://") or not path.rsplit(".", 1)[-1] in (
        "py",
        "pyc",
        "pyo",
        "pyd",
    ):
        print(
            f"Bad python script path `{path}`, must starts by `res://` and ends with `.py/pyc/pyo/pyd`"
        )
        r_error[0] = GODOT_ERR_FILE_BAD_PATH
        return _build_empty_script_manifest()

    # TODO: possible bug if res:// is not part of PYTHONPATH
    # Remove `res://`, `.py` and replace / by .
    modname = path[6:].rsplit(".", 1)[0].replace("/", ".")

    is_reload = modname in sys.modules
    if is_reload:
        # Reloading is done in two steps: remove the exported class,
        # then do module reloading through importlib.
        cls = get_exposed_class(modname)

        # If the module has no exported class, it has no real connection with
        # Godot and doesn't need to be reloaded
        if cls:
            if get_pythonscript_verbose():
                print(f"Reloading python script from {path} ({modname})")
            destroy_exposed_class(cls)
            importlib.reload(sys.modules[modname])

    try:
        importlib.import_module(modname)  # Force lazy loading of the module
        cls = get_exposed_class(modname)

    except BaseException:
        # If we are here it could be because the file doesn't exists
        # or (more possibly) the file content is not valid python (or
        # doesn't provide an exposed class)
        print(
            f"Got exception loading {path} ({modname}): {traceback.format_exc()}"
        )
        r_error[0] = GODOT_ERR_PARSE_ERROR
        return _build_empty_script_manifest()

    if cls is None:
        print(
            f"Cannot load {path} ({modname}) because it doesn't expose any class to Godot"
        )
        r_error[0] = GODOT_ERR_PARSE_ERROR
        return _build_empty_script_manifest()

    if is_reload:
        # During reloading, Godot calls the new class init before the old class finish (so
        # `pythonscript_script_finish` is going to be called after this function returns).
        # Hence we must manually increase the refcount to prevent finish to remove
        # the class.
        # Apparently multiple PluginScript instances can exist at the same time for the same script.
        set_exposed_class(cls)

    r_error[0] = GODOT_OK
    return _build_script_manifest(cls)


cdef api void pythonscript_script_finish(
    godot_pluginscript_script_data *p_data
) with gil:
    cdef object cls = <object>p_data
    if get_pythonscript_verbose():
        # Using print here will cause a crash on editor/game shutdown
        sys.__stdout__.write(f"Destroying python script {cls.__name__}\n")
    destroy_exposed_class(cls)
