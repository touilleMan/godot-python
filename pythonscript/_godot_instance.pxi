# cython: c_string_type=unicode, c_string_encoding=utf8

from libc.stddef cimport wchar_t

from godot.hazmat cimport gdapi
from godot.hazmat.gdnative_api_struct cimport (
    godot_string,
    godot_string_name,
    godot_bool,
    godot_array,
    godot_pool_string_array,
    godot_object,
    godot_variant,
    godot_variant_call_error,
    godot_method_rpc_mode,
    godot_pluginscript_script_data,
    godot_pluginscript_instance_data
)


cdef api godot_pluginscript_instance_data* pythonscript_instance_init(
    godot_pluginscript_script_data *p_data,
    godot_object *p_owner
):
    pass


cdef api void pythonscript_instance_finish(
    godot_pluginscript_instance_data *p_data
):
    pass


cdef api godot_bool pythonscript_instance_set_prop(
    godot_pluginscript_instance_data *p_data,
    const godot_string *p_name,
    const godot_variant *p_value
):
    pass


cdef api godot_bool pythonscript_instance_get_prop(
    godot_pluginscript_instance_data *p_data,
    const godot_string *p_name,
    godot_variant *r_ret
):
    pass


cdef api godot_variant pythonscript_instance_call_method(
    godot_pluginscript_instance_data *p_data,
    const godot_string_name *p_method,
    const godot_variant **p_args,
    int p_argcount,
    godot_variant_call_error *r_error
):
    pass


cdef api void pythonscript_instance_notification(
    godot_pluginscript_instance_data *p_data,
    int p_notification
):
    pass


cdef api godot_method_rpc_mode pythonscript_instance_get_rpc_mode(
    godot_pluginscript_instance_data *p_data,
    const godot_string *p_method
):
    pass


cdef api godot_method_rpc_mode pythonscript_instance_get_rset_mode(
    godot_pluginscript_instance_data *p_data,
    const godot_string *p_variable
):
    pass

# Useful ?

# cdef api void pythonscript_instance_refcount_incremented(
#     godot_pluginscript_instance_data *p_data
# ):
#     pass


# cdef api bool pythonscript_instance_refcount_decremented(
#     godot_pluginscript_instance_data *p_data
# ):
#     pass




# import godot


# cdef api void pythonscript_instance_init(cls_handle, gdobj):
#     instance = ffi.from_handle(cls_handle)(gdobj)
#     protect_from_gc.register(instance)
#     return connect_handle(instance)


# cdef api void pythonscript_instance_finish(instance_handle):
#     instance = ffi.from_handle(instance_handle)
#     protect_from_gc.unregister(instance)


# cdef api void pythonscript_instance_set_prop(instance_handle, p_name, p_value):
#     instance = ffi.from_handle(instance_handle)
#     try:
#         pyval = variant_to_pyobj(p_value)
#         name = godot_string_to_pyobj(p_name)
#         # print('[GD->PY] Set %s to %s (%s)' % (name, pyval, p_value))
#         setattr(instance, name, pyval)
#         return True

#     except Exception:
#         traceback.print_exc()
#         return False


# cdef api void pythonscript_instance_get_prop(instance_handle, p_name, r_ret):
#     instance = ffi.from_handle(instance_handle)
#     try:
#         name = godot_string_to_pyobj(p_name)
#         pyret = getattr(instance, name)
#         pyobj_to_variant(pyret, r_ret)
#         return True

#     except Exception:
#         traceback.print_exc()
#         return False


# cdef api void pythonscript_instance_notification(instance_handle, notification):
#     # Godot's notification should call all parent `_notification`
#     # methods (better not use `super()._notification` in those methods...)
#     instance = ffi.from_handle(instance_handle)
#     cls = type(instance)
#     # TODO: cache the methods to call ?
#     for parentcls in inspect.getmro(cls):
#         try:
#             parentcls.__dict__["_notification"](instance, notification)
#         except (KeyError, NotImplementedError):
#             pass


# cdef api void pythonscript_instance_call_method(handle, p_method, p_args, p_argcount, r_error):
#     instance = ffi.from_handle(handle)
#     # TODO: improve this by using a dict lookup using string_name
#     method = lib.godot_string_name_get_name(p_method)
#     methname = godot_string_to_pyobj(ffi.addressof(method))
#     lib.godot_string_destroy(ffi.addressof(method))
#     try:
#         meth = getattr(instance, methname)
#     except AttributeError:
#         r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
#         # TODO: Keep this object cached instead of recreating everytime
#         return pyobj_to_variant(None, for_ffi_return=True)[0]

#     # print('[GD->PY] Calling %s on %s ==> %s' % (methname, instance, meth))
#     pyargs = [variant_to_pyobj(p_args[i]) for i in range(p_argcount)]
#     try:
#         pyret = meth(*pyargs)
#         ret = pyobj_to_variant(pyret, for_ffi_return=True)
#         r_error.error = lib.GODOT_CALL_ERROR_CALL_OK
#         # print('[GD->PY] result: %s (%s)' % (pyret, ret[0]))
#         return ret[0]

#     except NotImplementedError:
#         # print('[GD->PY] not implemented !')
#         r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_METHOD
#     except TypeError:
#         traceback.print_exc()
#         # TODO: handle errors here
#         r_error.error = lib.GODOT_CALL_ERROR_CALL_ERROR_INVALID_ARGUMENT
#         r_error.argument = 1
#         r_error.expected = lib.GODOT_VARIANT_TYPE_NIL
#     # Something bad occured, return a default None variant
#     # TODO: Keep this object cached instead of recreating it everytime
#     return pyobj_to_variant(None, for_ffi_return=True)[0]
