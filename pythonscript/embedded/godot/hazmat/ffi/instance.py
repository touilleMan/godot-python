import inspect
import traceback

from pythonscriptcffi import ffi, lib

from godot.hazmat.gc_protector import protect_from_gc, connect_handle
from godot.hazmat.tools import godot_string_to_pyobj, variant_to_pyobj, pyobj_to_variant


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
            parentcls.__dict__["_notification"](instance, notification)
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
        return pyobj_to_variant(None, for_ffi_return=True)[0]

    # print('[GD->PY] Calling %s on %s ==> %s' % (methname, instance, meth))
    pyargs = [variant_to_pyobj(p_args[i]) for i in range(p_argcount)]
    try:
        pyret = meth(*pyargs)
        ret = pyobj_to_variant(pyret, for_ffi_return=True)
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
    return pyobj_to_variant(None, for_ffi_return=True)[0]
