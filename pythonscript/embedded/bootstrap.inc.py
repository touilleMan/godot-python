import os
import sys
import gc
import inspect
import traceback
from pythonscriptcffi import ffi, lib

from godot import __version__, get_exposed_class_per_module
from godot.hazmat.base import destroy_exposed_classes, BaseObject
from godot.hazmat.profiler import Profiler
from godot.hazmat.tools import (
    godot_string_to_pyobj,
    godot_string_from_pyobj,
    godot_string_from_pyobj_for_ffi_return,
    py_to_gd_type,
    variant_to_pyobj,
    pyobj_to_variant,
)
from godot.bindings import PoolStringArray, Dictionary, Array, ProjectSettings, OS


# Protect python objects passed to C from beeing garbage collected
class ProtectFromGC:
    def __init__(self):
        self._data = {}

    def register(self, value):
        self._data[id(value)] = value

    def unregister(self, value):
        del self._data[id(value)]

    def unregister_by_id(self, id):
        del self._data[id]

    def clear(self):
        self._data.clear()


protect_from_gc = ProtectFromGC()


def connect_handle(obj):
    handle = obj.__dict__.get('_cffi_handle')
    if not handle:
        handle = ffi.new_handle(obj)
        obj._cffi_handle = handle
    return handle


#### Language ####


@ffi.def_extern()
def pybind_init():
    # Make sure Python starts in the game directory
    os.chdir(ProjectSettings.globalize_path('res://'))
    # Setup default value
    pythonpath_config_field = "python_script/path"
    pythonpath_default_value = "res://;res://lib"
    if not ProjectSettings.has_setting(pythonpath_config_field):
        ProjectSettings.set_setting(pythonpath_config_field, pythonpath_default_value)
    ProjectSettings.set_initial_value(pythonpath_config_field, pythonpath_default_value)
    # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
    pythonpath = ProjectSettings.get_setting(pythonpath_config_field)

    sys.argv = ["godot"] + OS.get_cmdline_args()
    for p in pythonpath.split(';'):
        p = ProjectSettings.globalize_path(p)
        sys.path.append(p)

    print('Pythonscript version: %s' % __version__)
    print('Pythonscript backend: %s %s' %
        (sys.implementation.name, sys.version.replace('\n', ' ')))
    print('PYTHONPATH: %s' % sys.path)

    return ffi.NULL


@ffi.def_extern()
def pybind_finish(handle):
    # Release Godot objects referenced by python wrappers
    protect_from_gc.clear()
    destroy_exposed_classes()
    gc.collect()


#### Language editor ####


@ffi.def_extern()
def pybind_get_template_source_code(handle, class_name, base_class_name):
    print('==================================>>>TEMPLATE')
    class_name = godot_string_to_pyobj(class_name) or "MyExportedCls"
    base_class_name = godot_string_to_pyobj(base_class_name)
    src = """from godot import exposed, export
from godot.bindings import *


@exposed
class %s(%s):

    # member variables here, example:
    a = export(int)
    b = export(str, default='foo')

    def _ready(self):
        \"\"\"
        Called every time the node is added to the scene.
        Initialization here.
        \"\"\"
        pass
""" % (class_name, base_class_name)
    return godot_string_from_pyobj_for_ffi_return(src)[0]


@ffi.def_extern()
def pybind_validate(handle, script, r_line_error, r_col_error, test_error, path, r_functions):
    return 1


@ffi.def_extern()
def pybind_find_function(handle, function, code):
    pass


@ffi.def_extern()
def pybind_make_function(handle, class_, name, args):
    args = PoolStringArray.build_from_gdobj(args, steal=True)
    name = godot_string_to_pyobj(name)
    src = ['def %s(' % name]
    src.append(', '.join([arg.split(':', 1)[0] for arg in args]))
    src.append('):\n    pass')
    return ''.join(src)


@ffi.def_extern()
def pybind_complete_code(handle, p_code, p_base_path, p_owner, r_options, r_force, r_call_hint):
    return lib.GODOT_OK


@ffi.def_extern()
def pybind_auto_indent_code(handle, code, from_line, to_line):
    try:
        import autopep8
    except ImportError:
        print("[Pythonscript] Auto indent requires module `autopep8`, "
              "install it with `pip install autopep8`")
    pycode = godot_string_to_pyobj(code).splitlines()
    before = '\n'.join(pycode[:from_line])
    to_fix = '\n'.join(pycode[from_line:to_line])
    after = '\n'.join(pycode[to_line:])
    fixed = autopep8.fix_code(to_fix)
    final_code = '\n'.join((before, fixed, after))
    # TODO: modify code instead of replace it when binding on godot_string
    # operation is available
    lib.godot_string_destroy(code)
    lib.godot_string_new_unicode_data(code, final_code, len(final_code))


@ffi.def_extern()
def pybind_add_global_constant(handle, name, value):
    name = godot_string_to_pyobj(name)
    value = variant_to_pyobj(value)
    globals()[name] = value


@ffi.def_extern()
def pybind_debug_get_error(handle):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_line(handle, level):
    return 1


@ffi.def_extern()
def pybind_debug_get_stack_level_function(handle, level):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_source(handle, level):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_locals(handle, level, locals, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_get_stack_level_members(handle, level, members, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_get_globals(handle, locals, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_parse_stack_level_expression(handle, level, expression, max_subitems, max_depth):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


def _build_script_manifest(cls):

    def _build_signal_info(signal):
        methinfo = Dictionary()
        methinfo['name'] = signal.name
        # Dummy data, only name is important here
        methinfo['args'] = Array()
        methinfo['default_args'] = Array()
        methinfo['return'] = None
        methinfo['flags'] = lib.METHOD_FLAG_FROM_SCRIPT
        return methinfo

    def _build_method_info(meth, methname):
        spec = inspect.getfullargspec(meth)
        methinfo = Dictionary()
        methinfo['name'] = methname
        # TODO: Handle classmethod/staticmethod
        methinfo['args'] = Array(spec.args)
        methinfo['default_args'] = Array()  # TODO
        # TODO: use annotation to determine return type ?
        methinfo['return'] = None
        methinfo['flags'] = lib.METHOD_FLAG_FROM_SCRIPT
        methinfo['rpc_mode'] = getattr(meth, '__rpc', lib.GODOT_METHOD_RPC_MODE_DISABLED)
        return methinfo

    def _build_property_info(prop):
        propinfo = Dictionary()
        propinfo['name'] = prop.name
        propinfo['type'] = py_to_gd_type(prop.type)
        propinfo['hint'] = prop.hint
        propinfo['hint_string'] = prop.hint_string
        propinfo['usage'] = prop.usage
        propinfo['default_value'] = prop.default
        propinfo['rset_mode'] = prop.rpc
        return propinfo

    manifest = ffi.new('godot_pluginscript_script_manifest*')
    manifest.data = connect_handle(cls)
    # TODO: should be able to use lib.godot_string_new_with_wide_string directly
    gdname = godot_string_from_pyobj(cls.__name__)
    lib.godot_string_name_new(ffi.addressof(manifest.name), gdname)
    if cls.__bases__:
        # Only one Godot parent class (checked at class definition time)
        godot_parent_class = next((b for b in cls.__bases__ if issubclass(b, BaseObject)))
        if godot_parent_class.__dict__.get('__is_godot_native_class'):
            path = godot_parent_class.__name__
        else:
            # Pluginscript wants us to return the parent as a path
            path = 'res://%s.py' % '/'.join(cls.__bases__[0].__module__.split('.'))
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
        if not inspect.isfunction(meth) or meth.__name__.startswith('__'):
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
    if not path.startswith('res://') or not path.rsplit('.', 1)[-1] in ('py', 'pyc', 'pyo', 'pyd'):
        print("Bad python script path `%s`, must starts by `res://` and ends with `.py/pyc/pyo/pyd`" % path)
        r_error[0] = lib.GODOT_ERR_FILE_BAD_PATH
        return ffi.NULL
    # TODO: possible bug if res:// is not part of PYTHONPATH
    # Remove `res://`, `.py` and replace / by .
    modname = path[6:].rsplit('.', 1)[0].replace('/', '.')
    try:
        __import__(modname)  # Force lazy loading of the module
        # TODO: make sure script reloading works
        cls = get_exposed_class_per_module(modname)
    except Exception:
        # If we are here it could be because the file doesn't exists
        # or (more possibly) the file content is not a valid python (or
        # miss an exposed class)
        traceback.print_exc()
        r_error[0] = lib.GODOT_ERR_PARSE_ERROR
        # Obliged to return the structure, but no need in init it
        return ffi.new('godot_pluginscript_script_manifest*')[0]
    r_error[0] = lib.GODOT_OK
    return _build_script_manifest(cls)[0]


@ffi.def_extern()
def pybind_script_finish(cls_handle):
    # TODO: unload the script
    pass


@ffi.def_extern()
def pybind_instance_init(cls_handle, gdobj):
    instance = ffi.from_handle(cls_handle)(gdobj)
    protect_from_gc.register(instance)
    return connect_handle(instance)


@ffi.def_extern()
def pybind_instance_finish(instance_handle):
    instance = ffi.from_handle(instance_handle)
    protect_from_gc.unregister(instance)


@ffi.def_extern()
def pybind_instance_set_prop(instance_handle, p_name, p_value):
    instance = ffi.from_handle(instance_handle)
    try:
        pyval = variant_to_pyobj(p_value)
        name = godot_string_to_pyobj(p_name)
        # print('[GD->PY] Set %s to %s (%s)' % (name, pyval, p_value))
        setattr(instance, name, pyval)
        return True
    except Exception:
        traceback.print_exc()
        return False


@ffi.def_extern()
def pybind_instance_get_prop(instance_handle, p_name, r_ret):
    instance = ffi.from_handle(instance_handle)
    try:
        name = godot_string_to_pyobj(p_name)
        pyret = getattr(instance, name)
        pyobj_to_variant(pyret, r_ret)
        return True
    except Exception:
        traceback.print_exc()
        return False


@ffi.def_extern()
def pybind_instance_notification(instance_handle, notification):
    # Godot's notification should call all parent `_notification`
    # methods (better not use `super()._notification` in those methods...)
    instance = ffi.from_handle(instance_handle)
    cls = type(instance)
    # TODO: cache the methods to call ?
    for parentcls in inspect.getmro(cls):
        try:
            parentcls.__dict__['_notification'](instance, notification)
        except (KeyError, NotImplementedError):
            pass


@ffi.def_extern()
def pybind_instance_call_method(handle, p_method, p_args, p_argcount, r_error):
    instance = ffi.from_handle(handle)
    # TODO: improve this by using a dict lookup using string_name
    method = lib.godot_string_name_get_name(p_method)
    methname = godot_string_to_pyobj(ffi.addressof(method))
    lib.godot_string_destroy(ffi.addressof(method))
    try:
        meth = getattr(instance, methname)
    except AttributeError:
        r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
        # TODO: Keep this object cached instead of recreating everytime
        return pyobj_to_variant(None)[0]

    # print('[GD->PY] Calling %s on %s ==> %s' % (methname, instance, meth))
    pyargs = [variant_to_pyobj(p_args[i]) for i in range(p_argcount)]
    try:
        pyret = meth(*pyargs)
        ret = pyobj_to_variant(pyret)
        r_error.error = lib.GODOT_CALL_ERROR_CALL_OK
        # print('[GD->PY] result: %s (%s)' % (pyret, ret[0]))
        return ret[0]
    except NotImplementedError:
        # print('[GD->PY] not implemented !')
        r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
    except TypeError:
        traceback.print_exc()
        # TODO: handle errors here
        r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_ARGUMENT
        r_error.argument = 1
        r_error.expected = lib.GODOT_VARIANT_TYPE_NIL
    # Something bad occured, return a default None variant
    # TODO: Keep this object cached instead of recreating it everytime
    return pyobj_to_variant(None)[0]


### Profiler ###


profiler = Profiler()


@ffi.def_extern()
def pybind_profiling_start(handle):
    profiler.reset()
    profiler.enabled = True
    sys.setprofile(profiler.get_profilefunc())


@ffi.def_extern()
def pybind_profiling_stop(handle):
    profiler.enabled = False
    sys.setprofile(None)


@ffi.def_extern()
def pybind_profiling_get_accumulated_data(handle, info, info_max):
    print('get_frame_accumulated_data')
    info = Dictionary.build_from_gdobj(info, steal=True)
    # Sort function to make sure we can display the most consuming ones
    sorted_and_limited = sorted(profiler.per_meth_profiling.items(),
                                key=lambda x: -x[1].self_time)[:info_max]
    for signature, profile in sorted_and_limited:
        info[signature] = Dictionary(
            call_count=profile.call_count,
            total_time=int(profile.total_time * 1e6),
            self_time=int(profile.self_time * 1e6)
        )
    return len(sorted_and_limited)


@ffi.def_extern()
def pybind_profiling_get_frame_data(handle, info, info_max):
    print('get_frame_data')
    # Sort function to make sure we can display the most consuming ones
    sorted_and_limited = sorted(profiler.per_meth_profiling.items(),
                                key=lambda x: -x[1].last_frame_self_time)[:info_max]
    for i, item in enumerate(sorted_and_limited):
        signature, profile = item
        # TODO: should be able to use lib.godot_string_new_with_wide_string directly
        lib.godot_string_name_new(ffi.addressof(info[i].signature), godot_string_from_pyobj(signature))
        info[i].call_count = profile.last_frame_call_count
        info[i].total_time = int(profile.last_frame_total_time * 1e6)
        info[i].self_time = int(profile.last_frame_self_time * 1e6)
    return len(sorted_and_limited)


@ffi.def_extern()
def pybind_profiling_frame(handle):
    if profiler.enabled:
        profiler.next_frame()
