from pythonscriptcffi import ffi, lib


@ffi.def_extern()
def pybind_init_sys_path_and_argv(pythonpath, res_path, data_path):
    pythonpath = ffi.string(pythonpath)
    res_path = ffi.string(res_path)
    data_path = ffi.string(data_path)

    # TODO: handle argv
    import sys
    sys.argv = ['godot']

    for p in pythonpath.split(';'):
        if p.startswith("res://"):
            p = p.replace("res:/", res_path, 1)
        elif p.startswith("user://"):
            p = p.replace("user:/", data_path, 1)
        sys.path.append(p)

    print('PYTHON_PATH: %s' % sys.path)
    return True


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


@ffi.def_extern()
def pybind_load_exposed_class_per_module(modname):
    modname = ffi.string(modname)
    __import__(modname)  # Force lazy loading of the module
    cls = get_exposed_class_per_module(modname)
    return connect_handle(cls)


@ffi.def_extern()
def pybind_wrap_gdobj_with_class(cls_handle, gdobj):
    instance = ffi.from_handle(cls_handle)(gdobj)
    protect_from_gc.register(instance)
    return connect_handle(instance)


@ffi.def_extern()
def pybind_instanciate_from_classname(classname):
    cls = get_exposed_class_per_name(ffi.string(classname))
    instance = cls()
    protect_from_gc.register(instance)
    return connect_handle(instance)


@ffi.def_extern()
def pybind_release_instance(handle):
    instance = ffi.from_handle(handle)
    protect_from_gc.unregister(instance)


CALL_METH_OK = 0
CALL_METH_ERROR_INVALID_METHOD = 1
CALL_METH_ERROR_INVALID_ARGUMENT = 2
CALL_METH_ERROR_TOO_MANY_ARGUMENTS = 3
CALL_METH_ERROR_TOO_FEW_ARGUMENTS = 4
CALL_METH_ERROR_INSTANCE_IS_NULL = 5

CALL_METH_TYPE_NIL = 0 << 4
CALL_METH_TYPE_BOOL = 1 << 4
CALL_METH_TYPE_INT = 2 << 4
CALL_METH_TYPE_REAL = 3 << 4
CALL_METH_TYPE_STRING = 4 << 4
CALL_METH_TYPE_VECTOR2 = 5 << 4
CALL_METH_TYPE_RECT2 = 6 << 4
CALL_METH_TYPE_VECTOR3 = 7 << 4
CALL_METH_TYPE_TRANSFORM2D = 8 << 4
CALL_METH_TYPE_PLANE = 9 << 4
CALL_METH_TYPE_QUAT = 10 << 4
CALL_METH_TYPE_RECT3 = 11 << 4
CALL_METH_TYPE_BASIS = 12 << 4
CALL_METH_TYPE_TRANSFORM = 13 << 4
CALL_METH_TYPE_COLOR = 14 << 4
CALL_METH_TYPE_IMAGE = 15 << 4
CALL_METH_TYPE_NODE_PATH = 16 << 4
CALL_METH_TYPE__RID = 17 << 4
CALL_METH_TYPE_OBJECT = 18 << 4
CALL_METH_TYPE_INPUT_EVENT = 19 << 4
CALL_METH_TYPE_DICTIONARY = 20 << 4
CALL_METH_TYPE_ARRAY = 21 << 4
CALL_METH_TYPE_POOL_BYTE_ARRAY = 22 << 4
CALL_METH_TYPE_POOL_INT_ARRAY = 23 << 4
CALL_METH_TYPE_POOL_REAL_ARRAY = 24 << 4
CALL_METH_TYPE_POOL_STRING_ARRAY = 25 << 4
CALL_METH_TYPE_POOL_VECTOR2_ARRAY = 26 << 4
CALL_METH_TYPE_POOL_VECTOR3_ARRAY = 27 << 4
CALL_METH_TYPE_POOL_COLOR_ARRAY = 28 << 4


@ffi.def_extern()
def pybind_call_meth(handle, methname, args, argcount, ret, error):
    instance = ffi.from_handle(handle)
    meth = getattr(instance, ffi.string(methname))
    print('[GD->PY] Calling %s on %s (%s) ==> %s' % (ffi.string(methname), handle, instance, meth))
    pyargs = [variant_to_pyobj(args[i]) for i in range(argcount)]
    # error is an hacky int compressing Variant::CallError values
    try:
        pyret = meth(*pyargs)
        pyobj_to_variant(pyret, ret)
        error[0] = CALL_METH_OK
    except NotImplementedError:
        error[0] = CALL_METH_ERROR_INVALID_METHOD
    except TypeError as exc:
        print(exc)
        error[0] = 1 | CALL_METH_ERROR_INVALID_ARGUMENT | CALL_METH_TYPE_NIL
    # TODO: handle errors here


@ffi.def_extern()
def pybind_set_prop(handle, propname, val):
    instance = ffi.from_handle(handle)
    try:
        pyval = variant_to_pyobj(val)
        setattr(instance, ffi.string(propname), pyval)
        return True
    except Exception as exc:
        print(exc)
        return False


@ffi.def_extern()
def pybind_get_prop(handle, propname, ret):
    instance = ffi.from_handle(handle)
    try:
        pyret = getattr(instance, ffi.string(propname))
        pyobj_to_variant(pyret, ret)
        return True
    except Exception as exc:
        print(exc)
        return False


@ffi.def_extern()
def pybind_get_prop_type(handle, propname, prop_type):
    instance = ffi.from_handle(handle)
    prop = instance._exported.get(ffi.string(propname), None)
    if not prop:
        return False
    else:
        prop_type[0] = prop.gd_type
        return True


@ffi.def_extern()
def pybind_get_prop_default_value(handle, propname, r_val):
    cls_or_instance = ffi.from_handle(handle)
    prop = cls_or_instance._exported.get(ffi.string(propname), None)
    if not prop:
        return False
    pyobj_to_variant(prop.default, r_val)
    return True


@ffi.def_extern()
def pybind_get_prop_info(handle, propname, r_prop_info):
    cls_or_instance = ffi.from_handle(handle)
    prop = cls_or_instance._exported.get(ffi.string(propname), None)
    if not prop:
        return False
    r_prop_info.type = prop.gd_type
    r_prop_info.hint = prop.gd_hint
    r_prop_info.name = prop.gd_name[0]
    r_prop_info.hint_string = prop.gd_hint_string[0]
    r_prop_info.usage = prop.gd_usage
    return True


@ffi.def_extern()
def pybind_get_prop_list(handle):
    cls_or_instance = ffi.from_handle(handle)
    return cls_or_instance._exported_raw_list
