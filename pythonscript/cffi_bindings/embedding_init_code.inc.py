import inspect
import traceback
from pythonscriptcffi import ffi, lib


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
    import sys
    from godot.bindings import ProjectSettings, OS

    # Setup default value
    pythonpath_config_field = "python_script/path"
    pythonpath_default_value = "res://;res://lib"
    if not ProjectSettings.has(pythonpath_config_field):
        ProjectSettings.set(pythonpath_config_field, pythonpath_default_value)
    ProjectSettings.set_initial_value(pythonpath_config_field, pythonpath_default_value)
    # TODO: `set_builtin_order` is not exposed by gdnative... but is it useful ?
    pythonpath = ProjectSettings.get(pythonpath_config_field)

    sys.argv = ["godot"] + OS.get_cmdline_args()
    for p in pythonpath.split(';'):
        p = ProjectSettings.globalize_path(p)
        sys.path.append(p)

    print('sys.path: %s' % sys.path)


@ffi.def_extern()
def pybind_get_template_source_code(class_name, base_class_name, r_src):
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
    lib.godot_string_new_unicode_data(r_src, src, -1)


#### Language editor ####

@ffi.def_extern()
def pybind_add_global_constant(name, value):
    name = godot_string_to_pyobj(name)
    value = variant_to_pyobj(value)
    globals()[name] = value

@ffi.def_extern()
def pybind_debug_get_error():
    return godot_string_from_pyobj("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_line(level):
    return 1


@ffi.def_extern()
def pybind_debug_get_stack_level_function(level):
    return godot_string_from_pyobj("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_source(level):
    return godot_string_from_pyobj("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_locals(level, locals, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_get_stack_level_members(level, members, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_get_globals(locals, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_parse_stack_level_expression(level, expression, max_subitems, max_depth):
    return godot_string_from_pyobj("Nothing")[0]


@ffi.def_extern()
def pybind_profiling_start():
    pass


@ffi.def_extern()
def pybind_profiling_stop():
    pass


@ffi.def_extern()
def pybind_profiling_get_accumulated_data(info_arr, info_max):
    return 1


@ffi.def_extern()
def pybind_profiling_get_frame_data(info_arr, info_max):
    return 1



@ffi.def_extern()
def pybind_frame():
    pass


def _build_script_manifest(cls):
    from godot.bindings import Dictionary, Array

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
    manifest.data_handle = connect_handle(cls)
    lib.godot_string_new_unicode_data(ffi.addressof(manifest.name), cls.__name__, -1)
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
def pybind_script_init(path, source, r_error):
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
        cls = get_exposed_class_per_module(modname)
    except:
        r_error[0] = lib.GODOT_ERR_PARSE_ERROR
        raise
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
        print('[GD->PY] Set %s to %s (%s)' % (name, pyval, p_value))
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
    methname = godot_string_to_pyobj(p_method)
    try:
        meth = getattr(instance, methname)
    except AttributeError:
        r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
        # TODO: Keep this object cached instead of recreating everytime
        return pyobj_to_variant(None)[0]

    print('[GD->PY] Calling %s on %s ==> %s' % (methname, instance, meth))
    pyargs = [variant_to_pyobj(p_args[i]) for i in range(p_argcount)]
    try:
        pyret = meth(*pyargs)
        ret = pyobj_to_variant(pyret)
        r_error.error = lib.GODOT_CALL_ERROR_CALL_OK
        print('[GD->PY] result: %s (%s)' % (pyret, ret[0]))
        return ret[0]
    except NotImplementedError:
        print('[GD->PY] not implemented !')
        r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
    except TypeError:
        traceback.print_exc()
        # TODO: handle errors here
        r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_ARGUMENT
        r_error.argument = 1
        r_error.expected = lib.GODOT_VARIANT_TYPE_NIL
    # Something bad occured, return an default None variant
    # TODO: Keep this object cached instead of recreating everytime
    return pyobj_to_variant(None)[0]
