from .hazmat cimport gdapi, gdptrs, gdextension_interface
from .hazmat.gdtypes cimport *
from .builtins cimport *

from enum import IntEnum


def __getattr__(name: str):
    try:
        return _load_class(name)
    except RuntimeError:
        raise AttributeError


cdef class BaseGDObject:
    def free(self):
        gdptrs.gdptr_object_destroy(self._gd_ptr)
        self._gd_ptr = NULL

    def __init__(self):
        raise RuntimeError(
            f"Use `new()` method to instantiate non-refcounted Godot object (and don't forget to free it !)"
        )

    @classmethod
    def new(cls):
        cdef gd_string_name_t name = gdapi.gd_string_name_from_unchecked_pystr(cls.__name__)
        cdef BaseGDObject obj = cls.__new__(cls)
        obj._gd_ptr = gdptrs.gdptr_classdb_construct_object(&name)
        return obj

    def __repr__(self):
        return f"<{type(self).__name__} wrapper on 0x{<size_t>self._gd_ptr:x}>"

    def __eq__(self, object other):
        try:
            return self._gd_ptr == (<BaseGDObject?>other)._gd_ptr
        except TypeError:
            return NotImplemented

    def _set_gd_ptr(self, ptr: int):
        # /!\ doing `<gd_object_t>ptr` would return the address of
        # the PyObject instead of casting its value !
        self._gd_ptr = <gd_object_t><size_t>ptr
        # Note if the object is a reference, we stole it from the caller given we
        # don't call `Reference.reference` here

    def _get_gd_ptr(self):
        return <size_t>self._gd_ptr

    @classmethod
    def _from_ptr(cls, ptr: int):
        cdef BaseGDObject wrapper = cls.__new__(cls)
        wrapper._set_gd_ptr(ptr)
        return wrapper


cdef object _loaded_singletons = {}
cdef object _loaded_classes = {}


cdef void _cleanup_loaded_classes_and_singletons():
    _loaded_singletons.clear()
    _loaded_classes.clear()


cpdef BaseGDObject _load_singleton(str name):
    try:
        return <BaseGDObject>_loaded_singletons[name]
    except KeyError:
        pass

    cdef object cls = _load_class(name)
    cdef gd_string_name_t gdname = gdapi.gd_string_name_from_unchecked_pystr(name)
    cdef gd_object_t gdobj = gdptrs.gdptr_global_get_singleton(&gdname)
    gdapi.gd_string_name_del(&gdname)

    if gdobj == NULL:
        raise RuntimeError(f"Singleton `{name}` doesn't exist in Godot !")

    cdef BaseGDObject singleton = <BaseGDObject>cls._from_ptr(<size_t>gdobj)

    _loaded_singletons[name] = singleton
    return singleton


cdef inline object _property_getter(BaseGDObject obj, object name):
    return _object_call(obj._gd_ptr, "get", [name])


cdef inline void _property_setter(BaseGDObject obj, object name, object value):
    _object_call(obj._gd_ptr, "set", [name, value])


cdef inline object _meth_call(BaseGDObject obj, object name, object args):
    return _object_call(obj._gd_ptr, "call", [name, *args])


cdef object _load_class(str name):
    try:
        return _loaded_classes[name]
    except KeyError:
        pass

    from godot import _classes_api
    try:
        spec = getattr(_classes_api, name)
    except AttributeError:
        raise RuntimeError(f"Class `{name}` doesn't exist in Godot !")

    # TODO: ClassDB won't be needed once method uses ptrcall
    # Load our good friend ClassDB
    cdef StringName gdname_classdb = StringName("ClassDB")
    cdef gd_object_t classdb = gdptrs.gdptr_global_get_singleton(&gdname_classdb._gd_data)

    gd_name = StringName(name)
    parent = spec[0]
    items_spec = iter(spec[1:])
    if parent:
        parent_cls = _load_class(parent)
        bases = (parent_cls, )
    else:
        bases = (BaseGDObject, )

    attrs = {}

    if name == "RefCounted":
        @classmethod
        def _new(cls):
            raise RuntimeError(f"RefCounted Godot object must be created with `{ cls.__name__ }()`")

        attrs["new"] = _new

        def _del(self):
            cdef BaseGDObject obj = <BaseGDObject>self
            if _object_call(obj._gd_ptr, "unreference", []):
                gdptrs.gdptr_object_destroy(obj._gd_ptr)
                obj._gd_ptr = NULL

        attrs["__del__"] = _del

        def _free(self):
            raise RuntimeError("RefCounted Godot object cannot be freed")

        attrs["free"] = _free

        def _init(self):
            cdef gd_string_name_t name = gdapi.gd_string_name_from_unchecked_pystr(type(self).__name__)
            (<BaseGDObject>self)._gd_ptr = gdptrs.gdptr_classdb_construct_object(&name)

        attrs["__init__"] = _init

    while True:
        try:
            tag = next(items_spec)
        except StopIteration:
            break

        if tag == _classes_api._tag_constant:
            constant_name = next(items_spec)
            constant_value = next(items_spec)
            attrs[constant_name] = constant_value

        elif tag == _classes_api._tag_enum:
            enum_name = next(items_spec)
            enum_items_count = next(items_spec)
            enum_items_cooked = {}
            for _ in range(enum_items_count):
                enum_item_name = next(items_spec)
                enum_item_value = next(items_spec)
                enum_items_cooked[enum_item_name] = enum_item_value
            attrs[enum_name] = IntEnum(enum_name, enum_items_cooked)

        elif tag == _classes_api._tag_property:
            def _gen(
                prop_name,
                _prop_type,
                _prop_getter,
                _prop_setter,
                _prop_index,
            ):
                gd_prop_name = StringName(prop_name)
                # TODO: ptrcall on getter/setter
                @property
                def _property(self):
                    return _property_getter(self, gd_prop_name)
                @_property.setter
                def _property(self, value):
                    _property_setter(self, gd_prop_name, value)
                _property.fget.__name__ = prop_name
                _property.fset.__name__ = prop_name
                return _property

            prop_name = next(items_spec)
            attrs[prop_name] = _gen(
                prop_name,
                next(items_spec),
                next(items_spec),
                next(items_spec),
                next(items_spec),
            )

        elif tag == _classes_api._tag_signal:
            def _gen(
                signal_name,
                signal_arguments_count,
            ):
                gd_signal_name = StringName(signal_name)
                for _ in range(signal_arguments_count):
                    _arg_name = next(items_spec)
                    _arg_type = next(items_spec)
                    _arg_default_value = next(items_spec)
                # TODO: arguments support !
                @property
                def _signal(self):
                    return Signal(self, gd_signal_name)
                return _signal

            signal_name = next(items_spec)
            attrs[signal_name] = _gen(
                signal_name,
                next(items_spec),
            )

        elif tag == _classes_api._tag_method:
            def _gen(
                method_name,
                _method_hash,
                method_flags,
                _method_return_type,
                method_arguments_count,
            ):
                gd_method_name = StringName(method_name)
                for _ in range(method_arguments_count):
                    _arg_name = next(items_spec)
                    _arg_type = next(items_spec)
                    _arg_default_value = next(items_spec)
                # TODO: ptr call !
                # TODO: JIT compilation !
                if method_flags & _classes_api._tag_method_flag_is_static:
                    @staticmethod
                    def _meth(*args):
                        ret = _object_call(classdb, "class_call_static", [gd_name, gd_method_name, *args])
                        return ret
                else:
                    def _meth(self, *args):
                        ret = _meth_call(self, gd_method_name, args)
                        return ret
                _meth.__name__ = method_name
                return _meth

            method_name = next(items_spec)
            attrs[method_name] = _gen(
                method_name,
                next(items_spec),
                next(items_spec),
                next(items_spec),
                next(items_spec),
            )

        else:
            assert False, tag

    # `Object` defines a `free`, but it doesn't work properly (instead we rely on `BaseGDObject.free`)
    attrs.pop("free", None)

    cdef object klass = type(name, bases, attrs)

    _loaded_classes[name] = klass
    return klass


cdef object _object_call(gd_object_t obj, str meth, list args):
    cdef object pyret
    cdef gd_variant_t ret
    cdef gdextension_interface.GDExtensionCallError call_error

    cdef StringName gdname_object = StringName("Object")
    cdef StringName gdname_call = StringName("call")
    cdef gdextension_interface.GDExtensionMethodBindPtr Object_call = gdptrs.gdptr_classdb_get_method_bind(&gdname_object._gd_data, &gdname_call._gd_data, 3400424181)

    cdef gdextension_interface.GDExtensionInt args_with_meth_len = len(args) + 1
    # Currently the worst method takes 14 arguments, so this hack should be enough...
    if args_with_meth_len > 15:
        # TODO: handle this
        gdptrs.gdptr_print_error("Calling with more than 14 parameters is not supported (wtf are you calling ? :/)", "_object_call", "", 0, False)
        return None
    cdef gd_variant_t[15] variant_args
    cdef (gd_variant_t*)[15] variant_args_ptrs
    for i in range(args_with_meth_len):
        variant_args_ptrs[i] = &variant_args[i]

    # TODO: provide a helper for string name from Python str creation
    cdef gd_string_name_t meth_gdstrname = gdapi.gd_string_name_from_unchecked_pystr(meth)
    variant_args[0] = gdapi.gd_string_name_into_variant(&meth_gdstrname)
    # Note `gd_string_name_into_variant(&meth_gdstrname)` already calls `meth_gdstrname`'s destructor

    for i, arg in enumerate(args, 1):
        variant_args[i] = ensure_is_gdany_and_borrow_ref(arg)

    gdptrs.gdptr_object_method_bind_call(
        Object_call,
        obj,
        # Cast is required given autopxd2 incorrectly removes the const attributes
        # when converting gdextension_interface.c to .pxd
        <const void * const*>&variant_args_ptrs,
        args_with_meth_len,
        &ret,
        &call_error,
    )
    # In Godot the callee is responsible to destroy the provided parameters.
    # Hence we don't have to call `gd_variant_del()` on `variant_args`.
    if call_error.error == gdextension_interface.GDEXTENSION_CALL_OK:
        # Note `gd_variant_steal_into_pyobj(&ret)` already calls `ret`'s destructor
        return gd_variant_steal_into_pyobj(&ret)

    # TODO: improve ret error raised exception type ?
    elif call_error.error == gdextension_interface.GDEXTENSION_CALL_ERROR_INVALID_METHOD:
        raise RuntimeError(f"Error in Godot object method call: invalid method")

    elif call_error.error == gdextension_interface.GDEXTENSION_CALL_ERROR_INVALID_ARGUMENT:
        raise RuntimeError(f"Error in Godot object method call: invalid argument")

    elif (
        call_error.error == gdextension_interface.GDEXTENSION_CALL_ERROR_TOO_MANY_ARGUMENTS  or
        call_error.error == gdextension_interface.GDEXTENSION_CALL_ERROR_TOO_FEW_ARGUMENTS
    ):
        raise RuntimeError(f"Error in Godot object method call: expected {call_error.argument} arguments, got {call_error.expected}")

    elif call_error.error == gdextension_interface.GDEXTENSION_CALL_ERROR_INSTANCE_IS_NULL:
        raise RuntimeError(f"Error in Godot object method call: instance is null")

    else:
        raise RuntimeError(f"Unknown error in Godot object method call: Godot error code {call_error.error}")
