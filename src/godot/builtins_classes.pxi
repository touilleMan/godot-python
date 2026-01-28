# This file is included by `builtins.pxd.j2`

from enum import IntEnum
import inspect
from types import UnionType
import dataclasses


##############################################################################
#                          Instance Binding Callbacks                        #
##############################################################################


# These callbacks are used with object_get/set_instance_binding to associate
# Python objects with Godot objects. This allows us to retrieve the original
# Python object when a Godot object pointer is returned to us.

cdef void* _instance_binding_create_callback(
    void* p_token,
    void* p_instance
) noexcept nogil:
    # This callback is called when object_get_instance_binding is called on an
    # object that doesn't have a binding yet. We return NULL to indicate no
    # binding should be created automatically (we only set bindings explicitly
    # for Python extension class instances).
    return NULL


cdef void _instance_binding_free_callback(
    void* p_token,
    void* p_instance,
    void* p_binding
) noexcept with gil:
    # This callback is called when the Godot object is destroyed.
    # We don't need to do anything here since the Python object's ref is
    # managed by the extension class callbacks (_extension_class_free_instance).
    pass


cdef gdextension_interface.GDExtensionBool _instance_binding_reference_callback(
    void* p_token,
    void* p_binding,
    gdextension_interface.GDExtensionBool p_reference
) noexcept nogil:
    # This callback is called when a RefCounted object's reference count changes.
    # Return True to indicate we don't prevent the reference count from being decremented.
    return True


# Global instance binding callbacks structure
cdef gdextension_interface.GDExtensionInstanceBindingCallbacks _instance_binding_callbacks
_instance_binding_callbacks.create_callback = _instance_binding_create_callback
_instance_binding_callbacks.free_callback = _instance_binding_free_callback
_instance_binding_callbacks.reference_callback = _instance_binding_reference_callback


##############################################################################
#                                BaseGDObject                                #
##############################################################################


# BaseGDObject is the parent class of all Godot classes
# Note it is defined here instead of in `classes.pyx` to avoid recursive import


cdef class BaseGDObject:
    _gdpy_godot_class_name = None
    # Class attribute overwritten by child class that declares an actual Python
    # class (and not just a binding to expose an existing Godot class to Python).
    _gdpy_custom_class_name = None

    def __init__(self):
        print(f"[DEBUG] {type(self).__name__}.__init__()", flush=True)
        cdef BaseGDObject obj = <BaseGDObject>self
        obj._gd_ptr = gdptrs.gdptr_classdb_construct_object(
            &(<StringName>type(obj)._gdpy_godot_class_name)._gd_data
        )
        cdef object _gdpy_custom_class_name = type(obj)._gdpy_custom_class_name
        if _gdpy_custom_class_name is not None:
            gdptrs.gdptr_object_set_instance(
                obj._gd_ptr,
                &(<StringName>_gdpy_custom_class_name)._gd_data,
                <PyObject*>obj,
            )
            # Also set the instance binding so we can retrieve the Python object
            # from the Godot object pointer later (e.g. when Godot returns it to us)
            gdptrs.gdptr_object_set_instance_binding(
                obj._gd_ptr,
                gdptrs.gdptr_library,
                <PyObject*>obj,
                &_instance_binding_callbacks,
            )
            # Since we have registered this Python object into a Godot class instance, we must
            # make sure the Python object won't be destroyed before the Godot class instance.
            # Hence this manual refcount increase that will be decreased when Godot class
            # instance's `_del()` method is called.
            Py_INCREF(self)

    # Default `free`, is overwritten by `RefCounted` class to disable its behavior
    def free(self):
        print(f'[DEBUG] {type(self).__name__}.free()', flush=True)
        if type(self)._gdpy_custom_class_name is None:
            gdptrs.gdptr_object_destroy(self._gd_ptr)
            self._gd_ptr = NULL
        else:
            Py_DECREF(self)

    # Note `new` is not defined here since it needs the name of the class to instantiate.

    def __repr__(self):
        if not type(self)._gdpy_custom_class_name:
            return f"<{type(self).__name__} wrapper on 0x{<size_t>self._gd_ptr:x}>"
        else:
            return f"<{type(self).__name__} object at 0x{<size_t><PyObject>self:x}>"

    def __eq__(self, object other):
        try:
            return self._gd_ptr == (<BaseGDObject?>other)._gd_ptr
        except TypeError:
            return NotImplemented

    def _set_gd_ptr(self, ptr: int):
        # /!\ doing `<gd_object_t>ptr` would return the address of
        # the PyObject instead of casting its value !
        self._gd_ptr = <gd_object_t><size_t>ptr
        # Note if the object refcounted, we stole it from the caller given we
        # don't call `Reference.reference` here

    def _get_gd_ptr(self):
        return <size_t>self._gd_ptr

    @classmethod
    def _steal_from_ptr(cls, ptr: int):
        """
        `ptr` is not allowed to be NULL.
        Don't increase the refcount if the `ptr` points on a refcounted object
        (hence the "steal" in the name).
        """
        cdef BaseGDObject wrapper = cls.__new__(cls)
        wrapper._set_gd_ptr(ptr)
        return wrapper


#####################################################################
#                Godot classes exposed to Python                    #
#####################################################################


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

    cdef StringName gd_name = StringName(name)
    cdef gd_object_t gdobj = gdptrs.gdptr_global_get_singleton(&gd_name._gd_data)

    if gdobj == NULL:
        raise RuntimeError(f"Singleton `{name}` doesn't exist in Godot !")

    cdef object cls = _load_class(gd_name)
    cdef BaseGDObject singleton = <BaseGDObject>cls._steal_from_ptr(<size_t>gdobj)

    _loaded_singletons[name] = singleton
    return singleton


cdef inline object _property_getter(BaseGDObject obj, object name):
    return _object_call(obj._gd_ptr, StringName("get"), [name])


cdef inline void _property_setter(BaseGDObject obj, object name, object value):
    _object_call(obj._gd_ptr, StringName("set"), [name, value])


cdef inline object _meth_call(BaseGDObject obj, object name, object args):
    return _object_call(obj._gd_ptr, StringName("call"), [name, *args])


cdef inline object _build_class_from_spec(str name, StringName gd_name):
    # TODO: ClassDB won't be needed once method uses ptrcall
    # Load our good friend ClassDB
    cdef StringName gdname_classdb = StringName("ClassDB")
    cdef gd_object_t classdb = gdptrs.gdptr_global_get_singleton(&gdname_classdb._gd_data)

    from godot import _classes_api
    cdef list spec
    try:
        spec = getattr(_classes_api, name)
    except AttributeError:
        raise RuntimeError(f"Class `{name}` doesn't exist in Godot !")

    parent = spec[0]
    is_refcounted = spec[1]
    items_spec = iter(spec[2:])
    if parent:
        parent_cls = _load_class(StringName(parent))
        bases = (parent_cls, )
    else:
        bases = (BaseGDObject, )

    attrs = {"_gdpy_godot_class_name": gd_name}

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
                        return _object_call(classdb, StringName("class_call_static"), [gd_name, gd_method_name, *args])
                else:
                    def _meth(self, *args):
                        return _meth_call(self, gd_method_name, args)
                _meth.__name__ = method_name
                # Mark that this method is a wrapper over a Godot class's method,
                # this is useful to avoid infinite Godot->Python->Godot->... recursion.
                _meth.__gd_is_wrapper = True
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

    if name == "Object":
        # `Object` defines a `free`, but it doesn't work properly (instead we rely on `BaseGDObject.free`)
        attrs.pop("free", None)

    elif name == "RefCounted":

        def _gen():
            cdef StringName gdstr_unreference = StringName("unreference")

            def _del(self):
                print(f'[DEBUG] {type(self).__name__}.__del__()', flush=True)
                cdef BaseGDObject obj = <BaseGDObject>self
                if _object_call(obj._gd_ptr, gdstr_unreference, []):
                    gdptrs.gdptr_object_destroy(obj._gd_ptr)
                    obj._gd_ptr = NULL

            def _free(self):
                print(f'[DEBUG] {type(self).__name__}.free()', flush=True)
                raise RuntimeError("RefCounted Godot object, cannot be freed")

            return _del, _free

        attrs["__del__"], attrs["free"] = _gen()

    return type(name, bases, attrs)


cpdef object _load_class(StringName gd_name):
    try:
        return _loaded_classes[gd_name]
    except KeyError:
        pass

    cdef object klass = _build_class_from_spec(str(gd_name), gd_name)

    _loaded_classes[gd_name] = klass
    return klass


cdef object _object_call(gd_object_t obj, StringName meth, list args):
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
    variant_args[0] = gdapi.gd_string_name_copy_into_variant(&meth._gd_data)

    for i, arg in enumerate(args, 1):
        variant_args[i] = ensure_is_gdany_and_borrow_ref(arg)

    gdptrs.gdptr_object_method_bind_call(
        Object_call,
        obj,
        <const gdextension_interface.GDExtensionConstVariantPtr*>&variant_args_ptrs,
        args_with_meth_len,
        &ret,
        &call_error,
    )

    for i in range(args_with_meth_len):
        gdapi.gd_variant_del(&variant_args[i])

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


#####################################################################
#            Python classes registered as Godot classes             #
#####################################################################


cdef gdextension_interface.GDExtensionObjectPtr _extension_class_create_instance(
    void *p_class_userdata,
    gdextension_interface.GDExtensionBool p_notify_postinitialize
) noexcept with gil:
    print("[DEBUG] _extension_class_create_instance", flush=True)

    # TODO: use `p_notify_postinitialize` ?

    cdef type cls = <type>p_class_userdata
    cdef BaseGDObject obj = cls()
    # TODO: Check the pointer is not NULL, as this might be the case if the parent class `__init__` hasn't been called...
    # TODO: Should we use `__cinit__` to make sure the end-user cannot prevent the init from being called ?
    return <void*>obj._gd_ptr


cdef void _extension_class_free_instance(
    void* p_class_userdata,
    gdextension_interface.GDExtensionClassInstancePtr p_instance
) noexcept with gil:
    print("[DEBUG] _extension_class_free_instance", flush=True)
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    Py_DECREF(obj)


cdef void _extension_class_to_string(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    gdextension_interface.GDExtensionBool *r_is_valid,
    gdextension_interface.GDExtensionStringPtr p_out
) noexcept with gil:
    print("[DEBUG] _extension_class_to_string", flush=True)
    cdef object klass = <object>p_instance
    (<gd_string_t*>p_out)[0] = gdapi.gd_string_from_pybytes(klass.__name__)
    r_is_valid[0] = True


cdef object _find_virtual_method_definition(object cls, str meth_name):
    """
    Look for a virtual method definition in the Godot class hierarchy.
    Returns a tuple of (return_type, [(arg_name, arg_type), ...]) or None if not found.
    """
    from godot import _classes_api

    # Walk up the class hierarchy looking for Godot classes
    cdef object current_cls = cls
    cdef object godot_class_name
    cdef str class_name_str
    cdef list spec
    cdef object result

    while current_cls is not None and issubclass(current_cls, BaseGDObject):
        # Get the Godot class name for this class
        godot_class_name = getattr(current_cls, '_gdpy_godot_class_name', None)
        if godot_class_name is None:
            # Move to parent class
            current_cls = _get_godot_parent_class(current_cls)
            continue

        # Get the class spec from _classes_api
        class_name_str = str(godot_class_name) if not isinstance(godot_class_name, str) else godot_class_name
        try:
            spec = getattr(_classes_api, class_name_str)
        except AttributeError:
            # Move to parent class
            current_cls = _get_godot_parent_class(current_cls)
            continue

        # Parse the spec looking for the virtual method
        result = _parse_spec_for_virtual_method(spec, meth_name, _classes_api)
        if result is not None:
            return result

        # Move to parent class
        current_cls = _get_godot_parent_class(current_cls)

    return None


cdef object _get_godot_parent_class(object cls):
    """Get the first parent class that is a BaseGDObject subclass."""
    for base in cls.__bases__:
        if base is not BaseGDObject and issubclass(base, BaseGDObject):
            return base
    return None


cdef object _parse_spec_for_virtual_method(list spec, str meth_name, object _classes_api):
    """Parse a class spec and return method definition if found."""
    items_spec = iter(spec[2:])  # Skip parent and is_refcounted

    while True:
        try:
            tag = next(items_spec)
        except StopIteration:
            break

        if tag == _classes_api._tag_constant:
            next(items_spec)  # constant_name
            next(items_spec)  # constant_value

        elif tag == _classes_api._tag_enum:
            next(items_spec)  # enum_name
            enum_items_count = next(items_spec)
            for _ in range(enum_items_count):
                next(items_spec)  # enum_item_name
                next(items_spec)  # enum_item_value

        elif tag == _classes_api._tag_property:
            next(items_spec)  # prop_name
            next(items_spec)  # prop_type
            next(items_spec)  # prop_getter
            next(items_spec)  # prop_setter
            next(items_spec)  # prop_index

        elif tag == _classes_api._tag_signal:
            next(items_spec)  # signal_name
            signal_arguments_count = next(items_spec)
            for _ in range(signal_arguments_count):
                next(items_spec)  # arg_name
                next(items_spec)  # arg_type
                next(items_spec)  # arg_default_value

        elif tag == _classes_api._tag_method:
            method_name = next(items_spec)
            method_hash = next(items_spec)
            method_flags = next(items_spec)
            method_return_type = next(items_spec)
            method_arguments_count = next(items_spec)

            # Read arguments
            args = []
            for _ in range(method_arguments_count):
                arg_name = next(items_spec)
                arg_type = next(items_spec)
                arg_default_value = next(items_spec)
                args.append((arg_name, arg_type))

            # Check if this is the virtual method we're looking for
            if method_name == meth_name and (method_flags & _classes_api._tag_method_flag_is_virtual):
                return (method_return_type, args)

    return None


cdef object _convert_ptr_arg_to_python(const void* ptr, str type_str):
    """Convert a raw Godot pointer argument to a Python object based on type string."""
    # Handle Nil
    if type_str == "Nil":
        return None

    # Handle primitive types
    if type_str == "bool":
        return (<gdextension_interface.GDExtensionBool*>ptr)[0] != 0
    if type_str == "int":
        return (<int64_t*>ptr)[0]
    if type_str == "c:int":
        return (<int*>ptr)[0]
    if type_str == "c:float":
        return (<float*>ptr)[0]
    if type_str == "c:double":
        return (<double*>ptr)[0]

    # Handle meta types
    if type_str == "meta:int8":
        return (<int8_t*>ptr)[0]
    if type_str == "meta:int16":
        return (<int16_t*>ptr)[0]
    if type_str == "meta:int32":
        return (<int32_t*>ptr)[0]
    if type_str == "meta:int64":
        return (<int64_t*>ptr)[0]
    if type_str == "meta:uint8":
        return (<uint8_t*>ptr)[0]
    if type_str == "meta:uint16":
        return (<uint16_t*>ptr)[0]
    if type_str == "meta:uint32":
        return (<uint32_t*>ptr)[0]
    if type_str == "meta:uint64":
        return (<uint64_t*>ptr)[0]
    if type_str == "meta:float":
        return (<float*>ptr)[0]
    if type_str == "meta:double":
        return (<double*>ptr)[0]
    if type_str == "meta:char32":
        return (<int32_t*>ptr)[0]

    # Handle Godot builtins
    if type_str == "String":
        ret = GDString.__new__(GDString)
        (<GDString>ret)._gd_data = gdapi.gd_string_new_from_string(<gd_string_t*>ptr)
        return ret
    if type_str == "StringName":
        ret = StringName.__new__(StringName)
        (<StringName>ret)._gd_data = gdapi.gd_string_name_new_from_string_name(<gd_string_name_t*>ptr)
        return ret
    if type_str == "Vector2":
        ret = Vector2.__new__(Vector2)
        (<Vector2>ret)._gd_data = (<gd_vector2_t*>ptr)[0]
        return ret
    if type_str == "Vector2i":
        ret = Vector2i.__new__(Vector2i)
        (<Vector2i>ret)._gd_data = (<gd_vector2i_t*>ptr)[0]
        return ret
    if type_str == "Vector3":
        ret = Vector3.__new__(Vector3)
        (<Vector3>ret)._gd_data = (<gd_vector3_t*>ptr)[0]
        return ret
    if type_str == "Vector3i":
        ret = Vector3i.__new__(Vector3i)
        (<Vector3i>ret)._gd_data = (<gd_vector3i_t*>ptr)[0]
        return ret
    if type_str == "Vector4":
        ret = Vector4.__new__(Vector4)
        (<Vector4>ret)._gd_data = (<gd_vector4_t*>ptr)[0]
        return ret
    if type_str == "Vector4i":
        ret = Vector4i.__new__(Vector4i)
        (<Vector4i>ret)._gd_data = (<gd_vector4i_t*>ptr)[0]
        return ret
    if type_str == "Rect2":
        ret = Rect2.__new__(Rect2)
        (<Rect2>ret)._gd_data = (<gd_rect2_t*>ptr)[0]
        return ret
    if type_str == "Rect2i":
        ret = Rect2i.__new__(Rect2i)
        (<Rect2i>ret)._gd_data = (<gd_rect2i_t*>ptr)[0]
        return ret
    if type_str == "Transform2D":
        ret = Transform2D.__new__(Transform2D)
        (<Transform2D>ret)._gd_data = (<gd_transform2d_t*>ptr)[0]
        return ret
    if type_str == "Transform3D":
        ret = Transform3D.__new__(Transform3D)
        (<Transform3D>ret)._gd_data = (<gd_transform3d_t*>ptr)[0]
        return ret
    if type_str == "Plane":
        ret = Plane.__new__(Plane)
        (<Plane>ret)._gd_data = (<gd_plane_t*>ptr)[0]
        return ret
    if type_str == "Quaternion":
        ret = Quaternion.__new__(Quaternion)
        (<Quaternion>ret)._gd_data = (<gd_quaternion_t*>ptr)[0]
        return ret
    if type_str == "AABB":
        ret = AABB.__new__(AABB)
        (<AABB>ret)._gd_data = (<gd_aabb_t*>ptr)[0]
        return ret
    if type_str == "Basis":
        ret = Basis.__new__(Basis)
        (<Basis>ret)._gd_data = (<gd_basis_t*>ptr)[0]
        return ret
    if type_str == "Projection":
        ret = Projection.__new__(Projection)
        (<Projection>ret)._gd_data = (<gd_projection_t*>ptr)[0]
        return ret
    if type_str == "Color":
        ret = Color.__new__(Color)
        (<Color>ret)._gd_data = (<gd_color_t*>ptr)[0]
        return ret
    if type_str == "NodePath":
        ret = NodePath.__new__(NodePath)
        (<NodePath>ret)._gd_data = gdapi.gd_node_path_new_from_node_path(<gd_node_path_t*>ptr)
        return ret
    if type_str == "RID":
        ret = RID.__new__(RID)
        (<RID>ret)._gd_data = (<gd_rid_t*>ptr)[0]
        return ret
    if type_str == "Callable":
        ret = GDCallable.__new__(GDCallable)
        (<GDCallable>ret)._gd_data = gdapi.gd_callable_new_from_callable(<gd_callable_t*>ptr)
        return ret
    if type_str == "Signal":
        ret = Signal.__new__(Signal)
        (<Signal>ret)._gd_data = gdapi.gd_signal_new_from_signal(<gd_signal_t*>ptr)
        return ret
    if type_str == "Dictionary":
        ret = GDDictionary.__new__(GDDictionary)
        (<GDDictionary>ret)._gd_data = gdapi.gd_dictionary_new_from_dictionary(<gd_dictionary_t*>ptr)
        return ret
    if type_str == "Array":
        ret = GDArray.__new__(GDArray)
        (<GDArray>ret)._gd_data = gdapi.gd_array_new_from_array(<gd_array_t*>ptr)
        return ret
    if type_str == "PackedByteArray":
        ret = PackedByteArray.__new__(PackedByteArray)
        (<PackedByteArray>ret)._gd_data = gdapi.gd_packed_byte_array_new_from_packed_byte_array(<gd_packed_byte_array_t*>ptr)
        return ret
    if type_str == "PackedInt32Array":
        ret = PackedInt32Array.__new__(PackedInt32Array)
        (<PackedInt32Array>ret)._gd_data = gdapi.gd_packed_int32_array_new_from_packed_int32_array(<gd_packed_int32_array_t*>ptr)
        return ret
    if type_str == "PackedInt64Array":
        ret = PackedInt64Array.__new__(PackedInt64Array)
        (<PackedInt64Array>ret)._gd_data = gdapi.gd_packed_int64_array_new_from_packed_int64_array(<gd_packed_int64_array_t*>ptr)
        return ret
    if type_str == "PackedFloat32Array":
        ret = PackedFloat32Array.__new__(PackedFloat32Array)
        (<PackedFloat32Array>ret)._gd_data = gdapi.gd_packed_float32_array_new_from_packed_float32_array(<gd_packed_float32_array_t*>ptr)
        return ret
    if type_str == "PackedFloat64Array":
        ret = PackedFloat64Array.__new__(PackedFloat64Array)
        (<PackedFloat64Array>ret)._gd_data = gdapi.gd_packed_float64_array_new_from_packed_float64_array(<gd_packed_float64_array_t*>ptr)
        return ret
    if type_str == "PackedStringArray":
        ret = PackedStringArray.__new__(PackedStringArray)
        (<PackedStringArray>ret)._gd_data = gdapi.gd_packed_string_array_new_from_packed_string_array(<gd_packed_string_array_t*>ptr)
        return ret
    if type_str == "PackedVector2Array":
        ret = PackedVector2Array.__new__(PackedVector2Array)
        (<PackedVector2Array>ret)._gd_data = gdapi.gd_packed_vector2_array_new_from_packed_vector2_array(<gd_packed_vector2_array_t*>ptr)
        return ret
    if type_str == "PackedVector3Array":
        ret = PackedVector3Array.__new__(PackedVector3Array)
        (<PackedVector3Array>ret)._gd_data = gdapi.gd_packed_vector3_array_new_from_packed_vector3_array(<gd_packed_vector3_array_t*>ptr)
        return ret
    if type_str == "PackedColorArray":
        ret = PackedColorArray.__new__(PackedColorArray)
        (<PackedColorArray>ret)._gd_data = gdapi.gd_packed_color_array_new_from_packed_color_array(<gd_packed_color_array_t*>ptr)
        return ret
    if type_str == "PackedVector4Array":
        ret = PackedVector4Array.__new__(PackedVector4Array)
        (<PackedVector4Array>ret)._gd_data = gdapi.gd_packed_vector4_array_new_from_packed_vector4_array(<gd_packed_vector4_array_t*>ptr)
        return ret

    # Handle Object types (any Godot class) - passed as pointer to pointer
    return BaseGDObject.steal_cast_from_object((<gd_object_t*>ptr)[0])


cdef void _convert_python_to_ptr_ret(object pyobj, str type_str, void* r_ret):
    """Convert a Python return value to a raw Godot pointer based on type string."""
    # Handle Nil - nothing to write
    if type_str == "Nil":
        return

    # Handle primitive types
    if type_str == "bool":
        (<gdextension_interface.GDExtensionBool*>r_ret)[0] = 1 if pyobj else 0
        return
    if type_str == "int":
        (<int64_t*>r_ret)[0] = <int64_t>pyobj
        return
    if type_str == "c:int":
        (<int*>r_ret)[0] = <int>pyobj
        return
    if type_str == "c:float":
        (<float*>r_ret)[0] = <float>pyobj
        return
    if type_str == "c:double":
        (<double*>r_ret)[0] = <double>pyobj
        return

    # Handle meta types
    if type_str == "meta:int8":
        (<int8_t*>r_ret)[0] = <int8_t>pyobj
        return
    if type_str == "meta:int16":
        (<int16_t*>r_ret)[0] = <int16_t>pyobj
        return
    if type_str == "meta:int32":
        (<int32_t*>r_ret)[0] = <int32_t>pyobj
        return
    if type_str == "meta:int64":
        (<int64_t*>r_ret)[0] = <int64_t>pyobj
        return
    if type_str == "meta:uint8":
        (<uint8_t*>r_ret)[0] = <uint8_t>pyobj
        return
    if type_str == "meta:uint16":
        (<uint16_t*>r_ret)[0] = <uint16_t>pyobj
        return
    if type_str == "meta:uint32":
        (<uint32_t*>r_ret)[0] = <uint32_t>pyobj
        return
    if type_str == "meta:uint64":
        (<uint64_t*>r_ret)[0] = <uint64_t>pyobj
        return
    if type_str == "meta:float":
        (<float*>r_ret)[0] = <float>pyobj
        return
    if type_str == "meta:double":
        (<double*>r_ret)[0] = <double>pyobj
        return
    if type_str == "meta:char32":
        (<int32_t*>r_ret)[0] = <int32_t>pyobj
        return

    # Handle Godot builtins
    if type_str == "String":
        (<gd_string_t*>r_ret)[0] = gdapi.gd_string_new_from_string(&(<GDString>pyobj)._gd_data)
        return
    if type_str == "StringName":
        (<gd_string_name_t*>r_ret)[0] = gdapi.gd_string_name_new_from_string_name(&(<StringName>pyobj)._gd_data)
        return
    if type_str == "Vector2":
        (<gd_vector2_t*>r_ret)[0] = (<Vector2>pyobj)._gd_data
        return
    if type_str == "Vector2i":
        (<gd_vector2i_t*>r_ret)[0] = (<Vector2i>pyobj)._gd_data
        return
    if type_str == "Vector3":
        (<gd_vector3_t*>r_ret)[0] = (<Vector3>pyobj)._gd_data
        return
    if type_str == "Vector3i":
        (<gd_vector3i_t*>r_ret)[0] = (<Vector3i>pyobj)._gd_data
        return
    if type_str == "Vector4":
        (<gd_vector4_t*>r_ret)[0] = (<Vector4>pyobj)._gd_data
        return
    if type_str == "Vector4i":
        (<gd_vector4i_t*>r_ret)[0] = (<Vector4i>pyobj)._gd_data
        return
    if type_str == "Rect2":
        (<gd_rect2_t*>r_ret)[0] = (<Rect2>pyobj)._gd_data
        return
    if type_str == "Rect2i":
        (<gd_rect2i_t*>r_ret)[0] = (<Rect2i>pyobj)._gd_data
        return
    if type_str == "Transform2D":
        (<gd_transform2d_t*>r_ret)[0] = (<Transform2D>pyobj)._gd_data
        return
    if type_str == "Transform3D":
        (<gd_transform3d_t*>r_ret)[0] = (<Transform3D>pyobj)._gd_data
        return
    if type_str == "Plane":
        (<gd_plane_t*>r_ret)[0] = (<Plane>pyobj)._gd_data
        return
    if type_str == "Quaternion":
        (<gd_quaternion_t*>r_ret)[0] = (<Quaternion>pyobj)._gd_data
        return
    if type_str == "AABB":
        (<gd_aabb_t*>r_ret)[0] = (<AABB>pyobj)._gd_data
        return
    if type_str == "Basis":
        (<gd_basis_t*>r_ret)[0] = (<Basis>pyobj)._gd_data
        return
    if type_str == "Projection":
        (<gd_projection_t*>r_ret)[0] = (<Projection>pyobj)._gd_data
        return
    if type_str == "Color":
        (<gd_color_t*>r_ret)[0] = (<Color>pyobj)._gd_data
        return
    if type_str == "NodePath":
        (<gd_node_path_t*>r_ret)[0] = gdapi.gd_node_path_new_from_node_path(&(<NodePath>pyobj)._gd_data)
        return
    if type_str == "RID":
        (<gd_rid_t*>r_ret)[0] = (<RID>pyobj)._gd_data
        return
    if type_str == "Callable":
        (<gd_callable_t*>r_ret)[0] = gdapi.gd_callable_new_from_callable(&(<GDCallable>pyobj)._gd_data)
        return
    if type_str == "Signal":
        (<gd_signal_t*>r_ret)[0] = gdapi.gd_signal_new_from_signal(&(<Signal>pyobj)._gd_data)
        return
    if type_str == "Dictionary":
        (<gd_dictionary_t*>r_ret)[0] = gdapi.gd_dictionary_new_from_dictionary(&(<GDDictionary>pyobj)._gd_data)
        return
    if type_str == "Array":
        (<gd_array_t*>r_ret)[0] = gdapi.gd_array_new_from_array(&(<GDArray>pyobj)._gd_data)
        return
    if type_str == "PackedByteArray":
        (<gd_packed_byte_array_t*>r_ret)[0] = gdapi.gd_packed_byte_array_new_from_packed_byte_array(&(<PackedByteArray>pyobj)._gd_data)
        return
    if type_str == "PackedInt32Array":
        (<gd_packed_int32_array_t*>r_ret)[0] = gdapi.gd_packed_int32_array_new_from_packed_int32_array(&(<PackedInt32Array>pyobj)._gd_data)
        return
    if type_str == "PackedInt64Array":
        (<gd_packed_int64_array_t*>r_ret)[0] = gdapi.gd_packed_int64_array_new_from_packed_int64_array(&(<PackedInt64Array>pyobj)._gd_data)
        return
    if type_str == "PackedFloat32Array":
        (<gd_packed_float32_array_t*>r_ret)[0] = gdapi.gd_packed_float32_array_new_from_packed_float32_array(&(<PackedFloat32Array>pyobj)._gd_data)
        return
    if type_str == "PackedFloat64Array":
        (<gd_packed_float64_array_t*>r_ret)[0] = gdapi.gd_packed_float64_array_new_from_packed_float64_array(&(<PackedFloat64Array>pyobj)._gd_data)
        return
    if type_str == "PackedStringArray":
        (<gd_packed_string_array_t*>r_ret)[0] = gdapi.gd_packed_string_array_new_from_packed_string_array(&(<PackedStringArray>pyobj)._gd_data)
        return
    if type_str == "PackedVector2Array":
        (<gd_packed_vector2_array_t*>r_ret)[0] = gdapi.gd_packed_vector2_array_new_from_packed_vector2_array(&(<PackedVector2Array>pyobj)._gd_data)
        return
    if type_str == "PackedVector3Array":
        (<gd_packed_vector3_array_t*>r_ret)[0] = gdapi.gd_packed_vector3_array_new_from_packed_vector3_array(&(<PackedVector3Array>pyobj)._gd_data)
        return
    if type_str == "PackedColorArray":
        (<gd_packed_color_array_t*>r_ret)[0] = gdapi.gd_packed_color_array_new_from_packed_color_array(&(<PackedColorArray>pyobj)._gd_data)
        return
    if type_str == "PackedVector4Array":
        (<gd_packed_vector4_array_t*>r_ret)[0] = gdapi.gd_packed_vector4_array_new_from_packed_vector4_array(&(<PackedVector4Array>pyobj)._gd_data)
        return

    # Handle Object types - return pointer to the object
    if isinstance(pyobj, BaseGDObject):
        (<gd_object_t*>r_ret)[0] = (<BaseGDObject>pyobj)._gd_ptr
        return

    raise ValueError(f"Cannot convert Python object {pyobj!r} to Godot type {type_str}")


cdef void *_extension_class_get_virtual_with_data(
    void* p_class_userdata,
    gdextension_interface.GDExtensionConstStringNamePtr p_name,
    uint32_t p_hash  # TODO: use p_hash ?
) noexcept with gil:
    cdef object cls = <object>p_class_userdata
    cdef str meth_name = gdapi.gd_string_name_to_pystr(<gd_string_name_t*>p_name)

    # Don't use `getattr` here since it would also look into the parent class
    cdef object meth = cls.__dict__.get(meth_name, None)

    print(f"[DEBUG] _extension_class_get_virtual_with_data({cls!r}, {meth_name!r}) -> {meth!r}", flush=True)

    if meth is None:
        return NULL

    # Find the virtual method definition in the Godot class hierarchy
    cdef object meth_def = _find_virtual_method_definition(cls, meth_name)
    if meth_def is None:
        print(f"[WARNING] Virtual method {meth_name} not found in Godot class hierarchy for {cls}", flush=True)
        return NULL

    # Build a tuple of (method, method_definition) and return it
    # The tuple needs to be kept alive, so we INCREF it
    cdef tuple userdata = (meth, meth_def)
    Py_INCREF(userdata)

    return <void*>userdata


cdef void _extension_class_call_virtual_with_data(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    gdextension_interface.GDExtensionConstStringNamePtr p_name,
    void* p_virtual_call_userdata,
    const gdextension_interface.GDExtensionConstTypePtr* p_args,
    gdextension_interface.GDExtensionTypePtr r_ret
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    cdef str meth_name = gdapi.gd_string_name_to_pystr(<gd_string_name_t*>p_name)

    # Retrieve the tuple of (method, method_definition)
    cdef tuple userdata = <tuple>p_virtual_call_userdata
    cdef object meth = userdata[0]
    cdef tuple meth_def = userdata[1]
    cdef str return_type = meth_def[0]
    cdef list args_def = meth_def[1]

    print(f"[DEBUG] _extension_class_call_virtual_with_data({obj!r}, {meth_name!r}, return={return_type}, args={args_def})", flush=True)

    # Convert the arguments from raw pointers to Python objects
    cdef list py_args = []
    cdef int i
    cdef str arg_type
    for i in range(len(args_def)):
        arg_type = args_def[i][1]
        py_args.append(_convert_ptr_arg_to_python(p_args[i], arg_type))

    # Call the Python method
    cdef object ret = meth(obj, *py_args)

    # Convert the return value back to Godot
    if r_ret != NULL and return_type != "Nil":
        _convert_python_to_ptr_ret(ret, return_type, r_ret)


# typedef const GDExtensionPropertyInfo *(*GDExtensionClassGetPropertyList)(GDExtensionClassInstancePtr p_instance, uint32_t *r_count);
cdef const gdextension_interface.GDExtensionPropertyInfo * _extension_class_get_property_list_func(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    uint32_t *r_count
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    print(f"[DEBUG] _extension_class_get_property_list_func({obj!r})", flush=True)

    # Get the property fields list from the class
    cdef object cls = type(obj)
    cdef list property_fields = getattr(cls, '_gdpy_property_fields', [])
    cdef uint32_t prop_count = len(property_fields)

    r_count[0] = prop_count

    if prop_count == 0:
        return NULL

    cdef gdextension_interface.GDExtensionPropertyInfo *properties = <gdextension_interface.GDExtensionPropertyInfo *>PyMem_Malloc(sizeof(gdextension_interface.GDExtensionPropertyInfo) * prop_count)

    # Iterate over all dataclass fields and create property info for each
    for i, (field_name, field_type) in enumerate(property_fields):
        properties[i].type = py_to_gd_type(field_type)
        properties[i].name = <gdextension_interface.GDExtensionStringNamePtr>PyMem_Malloc(sizeof(gd_string_name_t))
        (<gd_string_name_t*>properties[i].name)[0] = gdapi.gd_string_name_from_unchecked_pystr(field_name)
        properties[i].class_name = <gdextension_interface.GDExtensionStringNamePtr>PyMem_Malloc(sizeof(gd_string_name_t))
        if properties[i].type == gdextension_interface.GDEXTENSION_VARIANT_TYPE_OBJECT:
            (<gd_string_name_t*>properties[i].class_name)[0] = gdapi.gd_string_name_from_unchecked_pystr(field_type.__name__)
        else:
            (<gd_string_name_t*>properties[i].class_name)[0] = gdapi.gd_string_name_new()
        properties[i].hint = 0  # uint32_t, Bitfield of `PropertyHint` (defined in `extension_api.json`).
        properties[i].hint_string = <gdextension_interface.GDExtensionStringPtr>PyMem_Malloc(sizeof(gd_string_t))
        (<gd_string_t*>properties[i].hint_string)[0] = gdapi.gd_string_new()
        properties[i].usage = 6  # uint32_t, Bitfield of `PropertyUsageFlags` (defined in `extension_api.json`).

    return properties


# typedef void (*GDExtensionClassFreePropertyList2)(GDExtensionClassInstancePtr p_instance, const GDExtensionPropertyInfo *p_list, uint32_t p_count);
cdef void _extension_class_free_property_list_func(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    const gdextension_interface.GDExtensionPropertyInfo *p_list,
    uint32_t p_count
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    print(f"[DEBUG] _extension_class_free_property_list_func({obj!r})", flush=True)
    for i in range(p_count):
        PyMem_Free(p_list[i].name)
        PyMem_Free(p_list[i].class_name)
        PyMem_Free(p_list[i].hint_string)
    PyMem_Free(<gdextension_interface.GDExtensionPropertyInfo *>p_list)


# typedef GDExtensionBool (*GDExtensionClassGet)(GDExtensionClassInstancePtr p_instance, GDExtensionConstStringNamePtr p_name, GDExtensionVariantPtr r_ret);
cdef gdextension_interface.GDExtensionBool _extension_class_get(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    gdextension_interface.GDExtensionConstStringNamePtr p_name,
    gdextension_interface.GDExtensionVariantPtr r_ret,
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    cdef str name = gdapi.gd_string_name_to_pystr(<gd_string_name_t*>p_name)

    # Check if this attribute is a registered property field
    cdef object cls = type(obj)
    cdef list property_fields = getattr(cls, '_gdpy_property_fields', [])
    cdef bint is_property = False
    for field_name, field_type in property_fields:
        if field_name == name:
            is_property = True
            break

    if not is_property:
        return False

    print(f"[DEBUG] _extension_class_get({obj!r}, {name!r})", flush=True)
    cdef object ret
    try:
        ret = getattr(obj, name)
        if not gd_variant_copy_from_pyobj(ret, <gd_variant_t*>r_ret):
            raise ValueError(f"Attribute `{obj.__class__.__name__}.{name}` has returned a value that cannot be converted into a Godot type: `{ret}`")
            # TODO: should return False, so replace the exception by an error log ?
    except AttributeError:
        return False

    return True


# typedef GDExtensionBool (*GDExtensionClassSet)(GDExtensionClassInstancePtr p_instance, GDExtensionConstStringNamePtr p_name, GDExtensionConstVariantPtr p_value);
cdef gdextension_interface.GDExtensionBool _extension_class_set(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    gdextension_interface.GDExtensionConstStringNamePtr p_name,
    gdextension_interface.GDExtensionConstVariantPtr p_value,
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    cdef str name = gdapi.gd_string_name_to_pystr(<gd_string_name_t*>p_name)

    # Check if this attribute is a registered property field
    cdef object cls = type(obj)
    cdef list property_fields = getattr(cls, '_gdpy_property_fields', [])
    cdef bint is_property = False
    for field_name, field_type in property_fields:
        if field_name == name:
            is_property = True
            break

    if not is_property:
        return False

    print(f"[DEBUG] _extension_class_set({obj!r}, {name!r})", flush=True)

    cdef object value = gd_variant_steal_into_pyobj(<gd_variant_t*>p_value)
    setattr(obj, name, value)
    return True


cdef void _extension_class_notification2(
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    int32_t p_what,
    gdextension_interface.GDExtensionBool p_reversed
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    print(f"[DEBUG] _extension_class_notification2({obj!r}, {int(p_what)}, {bool(p_reversed)})", flush=True)
    cdef object callback
    try:
        # Note `Object._notification`, like all Object's virtual methods, is mentioned
        # in the Godot documentation but has no actual existance.
        callback = getattr(obj, "_notification")
    except AttributeError:
        print(f"[DEBUG] _extension_class_notification2({obj!r}) -> nocall", flush=True)
        return

    print(f"[DEBUG] _extension_class_notification2({obj!r}) -> call {callback!r}({int(p_what)}, {bool(p_reversed)})", flush=True)
    callback(int(p_what), bool(p_reversed))


# TODO: should hack typing info in a .pyi
class signal:
    """Godot signal declaration for Python extension classes.

    Usage:
        # Signal with no arguments
        my_signal = signal()

        # Signal with typed arguments (auto-generated names)
        my_signal = signal(int, str)

        # Signal with named arguments
        my_signal = signal(("count", int), ("name", str))
    """
    def __init__(self, *args):
        # Convert args to list of (name, type) tuples
        self._args = []
        for i, arg in enumerate(args):
            if isinstance(arg, tuple) and len(arg) == 2:
                # Named argument: ("arg_name", type)
                arg_name, arg_type = arg
                self._args.append((arg_name, arg_type))
            else:
                # Just a type, auto-generate name
                self._args.append((f"arg{i}", arg))


def register_python_extension_class(klass: type):
    cdef StringName gd_class_name = StringName(klass.__name__)
    klass._gdpy_custom_class_name = gd_class_name

    # 1) Register the class itself

    cdef gdextension_interface.GDExtensionClassCreationInfo4 info
    info.is_virtual = klass.__gdpy_is_virtual
    info.is_abstract = klass.__gdpy_is_abstract
    info.is_exposed = klass.__gdpy_is_exposed
    info.is_runtime = klass.__gdpy_is_runtime
    cdef gd_string_name_t icon_path
    if klass.__gdpy_icon_path is None:
        info.icon_path = NULL
    else:
        icon_path = gdapi.gd_string_name_from_utf8_and_len(<char*>klass.__gdpy_icon_path, len(klass.__gdpy_icon_path))
        info.icon_path = &icon_path
    info.icon_path = NULL  # GDExtensionConstStringPtr
    # `set/get` here are some kind of generic callbacks (like `__getattr__`),
    # instead we should bind a callback for each property
    info.set_func = _extension_class_set
    info.get_func = _extension_class_get
    info.get_property_list_func = _extension_class_get_property_list_func
    info.free_property_list_func = _extension_class_free_property_list_func
    info.property_can_revert_func = NULL  # GDExtensionClassPropertyCanRevert
    info.property_get_revert_func = NULL  # GDExtensionClassPropertyGetRevert
    info.validate_property_func = NULL  # GDExtensionClassValidateProperty
    # Notification is going to call the `_notification` method, so we can be smart here.
    # TODO: we need additional tests here regarding how inheritance works.
    #       Typically what happens if we subclass a Python class:
    #       - If both have a `_notification` method defined
    #       - If only the parent has a `_notification` method defined
    if "_notification" in klass.__dict__:
        info.notification_func = _extension_class_notification2
    else:
        info.notification_func = NULL
    info.to_string_func = &_extension_class_to_string  # GDExtensionClassToString
    info.reference_func = NULL  # GDExtensionClassReference
    info.unreference_func = NULL  # GDExtensionClassUnreference
    info.create_instance_func = _extension_class_create_instance
    info.free_instance_func = _extension_class_free_instance
    info.recreate_instance_func = NULL  # GDExtensionClassRecreateInstance
    # Queries a virtual function by name and returns a callback to invoke the requested virtual function.
    info.get_virtual_func = NULL
    # Paired with `call_virtual_with_data_func`, this is an alternative to `get_virtual_func` for extensions that
    # need or benefit from extra data when calling virtual functions.
    # Returns user data that will be passed to `call_virtual_with_data_func`.
    # Returning `NULL` from this function signals to Godot that the virtual function is not overridden.
    # Data returned from this function should be managed by the extension and must be valid until the extension is deinitialized.
    # You should supply either `get_virtual_func`, or `get_virtual_call_data_func` with `call_virtual_with_data_func`.
    info.get_virtual_call_data_func = _extension_class_get_virtual_with_data  # GDExtensionClassGetVirtualCallData2
    # Used to call virtual functions when `get_virtual_call_data_func` is not null.
    info.call_virtual_with_data_func = _extension_class_call_virtual_with_data  # GDExtensionClassCallVirtualWithData
    # TODO: GC protector is not currently in place!
    # Don't increment refcount given we rely on gc protector
    info.class_userdata = <void*>klass  # void*

    cdef object parent_godot_class = next((k for k in klass.__bases__ if issubclass(k, BaseGDObject)), None)
    if parent_godot_class is None:
        raise ValueError(f"Class {klass} must directly inherit a Godot class!")
    cdef gd_string_name_t gdname_parent = gdapi.gd_string_name_from_unchecked_pystr(parent_godot_class.__name__)
    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged
    gdptrs.gdptr_classdb_register_extension_class4(
        gdptrs.gdptr_library,
        &gd_class_name._gd_data,
        &gdname_parent,
        &info,
    )
    gdapi.gd_string_name_del(&gdname_parent)
    if info.icon_path != NULL:
        gdapi.gd_string_name_del(&icon_path)

    # 2) Collect methods, signals and `@property`-based properties

    cdef StringName gd_signal_name
    for attr_name in klass.__dict__.keys():
        if attr_name.startswith("__"):
            continue

        attr = object.__getattribute__(klass, attr_name)

        # IntEnum (exposed as integer constants)

        if isinstance(attr, type) and issubclass(attr, IntEnum):
            # Handle IntEnum subclasses - register each member as an integer constant
            # Must be before callable check since IntEnum subclasses are callable
            enum_name = attr.__name__
            for member_name, member_value in attr.__members__.items():
                _register_python_extension_class_integer_constant(
                    &gd_class_name._gd_data,
                    f"{enum_name}_{member_name}",
                    member_value.value,
                    enum_name
                )

        # Methods

        elif isinstance(attr, classmethod):
            attr = getattr(klass, attr_name)
            _register_python_extension_class_method(&gd_class_name._gd_data, attr_name, attr, True)

        elif isinstance(attr, staticmethod):
            attr = getattr(klass, attr_name)
            _register_python_extension_class_method(&gd_class_name._gd_data, attr_name, attr, True)

        elif callable(attr):  # Regular method (must be last since `staticmethod` & `IntEnum` are also callable!)
            _register_python_extension_class_method(&gd_class_name._gd_data, attr_name, attr, False)

        # Signal

        elif isinstance(attr, signal):
            # `signal` object is just a placeholder, replace it by the actual
            # property method that returns a bound signal instance.
            # Use a generator function to properly capture the signal name in closure
            def _gen_signal_property(signal_name):
                cdef StringName gd_signal_name = StringName(signal_name)
                @property
                def _signal_property(self):
                    return Signal(self, gd_signal_name)
                    # return _BoundSignal(self, gd_signal_name)
                _signal_property.__name__ = signal_name
                return _signal_property, gd_signal_name

            signal_prop, gd_signal_name = _gen_signal_property(attr_name)
            setattr(klass, attr_name, signal_prop)

            _register_python_extension_class_signal(&gd_class_name._gd_data, &gd_signal_name._gd_data, attr._args)

        # Property

        elif isinstance(attr, property):
            # Handle @property decorators
            prop_name = attr_name

            getter_name = f"__gd_get_{prop_name}"
            # Register the getter method
            _register_python_extension_class_method(
                &gd_class_name._gd_data,
                getter_name,
                attr.fget,
                False,
            )

            # Register the setter method if it exists
            setter_name = None
            if attr.fset is not None:
                setter_name = f"__gd_set_{prop_name}"
                _register_python_extension_class_method(
                    &gd_class_name._gd_data,
                    setter_name,
                    attr.fset,
                    False,
                )

            # Get type from the getter function's return annotation
            try:
                prop_type = attr.fget.__annotations__["return"]
            except (AttributeError, KeyError):
                # Unknown type, use Godot Variant type
                prop_type = type(None)  # `py_to_gd_type(type(None))` returns the Variant type

            # Register the property itself
            _register_python_extension_class_property(
                &gd_class_name._gd_data,
                prop_name,
                prop_type,
                getter_name,
                setter_name,
            )

    # 3) Collect attribute-based properties and constants

    # Collect dataclass fields that should be exposed as Godot properties or constants
    cdef list property_fields = []
    for field_name, field in klass.__dataclass_fields__.items():
        if field_name.startswith("__"):
            continue

        if getattr(field, "_field_type") == dataclasses._FIELD_CLASSVAR:
            # Handle ClassVar fields as constants
            # Get the actual value from the class
            constant_value = getattr(klass, field_name, None)
            # Godot only supports integer constant
            if isinstance(constant_value, int):
                _register_python_extension_class_integer_constant(
                    &gd_class_name._gd_data,
                    field_name,
                    constant_value
                )
            continue

        # Store field name and type for later use in get/set/get_property_list
        property_fields.append((field_name, field.type))

    # Store in class for access by extension class callbacks
    klass._gdpy_property_fields = property_fields

    # 4) Keep track of the registered class is needed for `gd_variant_steal_into_pyobj`

    _loaded_classes[klass.__name__] = klass


# cdef void _register_python_extension_class_property(gd_string_name_t *gd_class_name, str arg_name, type arg, str setter_name, object getter_name: str | None):
#     cdef gdextension_interface.GDExtensionPropertyInfo info
#     generate_property_info(&info, arg_name, arg)

#     gdptrs.gdptr_classdb_register_extension_class_property(
#         gdptrs.gdptr_library,
#         &gd_class_name,
#         &info,
#         p_setter,
#         p_getter,
#     )

#     free_property_info(&info)

# #     cdef gdextension_interface.GDExtensionClassLibraryPtr p_library
# #     cdef gdextension_interface.GDExtensionConstStringNamePtr p_class_name
# #     cdef const gdextension_interface.GDExtensionPropertyInfo *p_info
# #     cdef gdextension_interface.GDExtensionConstStringNamePtr p_setter
# #     cdef gdextension_interface.GDExtensionConstStringNamePtr p_gette



# cdef void _register_python_extension_class_property_group(gd_string_name_t *gd_class_name, group_name: str, prefix: str):
#     cdef gd_string_t gd_group_name = gdapi.gd_string_from_unchecked_pystr(group_name)
#     cdef gd_string_t gd_prefix = gdapi.gd_string_from_unchecked_pystr(prefix)

#     gdptrs.gdptr_classdb_register_extension_class_property_group(
#         gdptrs.gdptr_library,
#         gd_class_name,
#         &gd_group_name,
#         &gd_prefix
#     )

#     gdapi.gd_string_del(&gd_group_name)
#     gdapi.gd_string_del(&gd_prefix)


# cdef void _register_python_extension_class_property_sub_group(gd_string_name_t *gd_class_name, subgroup_name: str, prefix: str):
#     cdef gd_string_t gd_subgroup_name = gdapi.gd_string_from_unchecked_pystr(subgroup_name)
#     cdef gd_string_t gd_prefix = gdapi.gd_string_from_unchecked_pystr(prefix)

#     gdptrs.gdptr_classdb_register_extension_class_property_group(
#         gdptrs.gdptr_library,
#         gd_class_name,
#         &gd_subgroup_name,
#         &gd_prefix
#     )

#     gdapi.gd_string_del(&gd_subgroup_name)
#     gdapi.gd_string_del(&gd_prefix)


# typedef void (*GDExtensionClassMethodCall)(void *method_userdata, GDExtensionClassInstancePtr p_instance, const GDExtensionConstVariantPtr *p_args, GDExtensionInt p_argument_count, GDExtensionVariantPtr r_return, GDExtensionCallError *r_error);
cdef void _extension_class_method_call(
    void *method_userdata,
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    const gdextension_interface.GDExtensionConstVariantPtr *p_args,
    gdextension_interface.GDExtensionInt p_argument_count,
    gdextension_interface.GDExtensionVariantPtr r_return,
    gdextension_interface.GDExtensionCallError *r_error,
) noexcept with gil:
    cdef BaseGDObject obj = <BaseGDObject>p_instance
    cdef object method = <object>method_userdata

    # TODO: Better handle argument passing
    #       - Pre-compute the number and type of arguments?
    #       - Return GDEXTENSION_CALL_ERROR_TOO_(FEW|MANY)_ARGUMENTS errors?
    #       - Determine what value should be passed to argument/excepted fields?
    cdef list args = []
    for i in range(p_argument_count):
        args.append(gd_variant_steal_into_pyobj(<gd_variant_t*>p_args[i]))

    print(f"[DEBUG] _extension_class_method_call({method!r}, {obj!r}, *{args!r})", flush=True)

    try:
        gd_variant_copy_from_pyobj(method(obj, *args), <gd_variant_t*>r_return)
    except:
        r_error[0].type = gdextension_interface.GDEXTENSION_CALL_ERROR_INVALID_ARGUMENT
        r_error[0].argument = 0
        r_error[0].expected = 0
        raise


cdef void _extension_class_static_method_call(
    void *method_userdata,
    gdextension_interface.GDExtensionClassInstancePtr p_instance,
    const gdextension_interface.GDExtensionConstVariantPtr *p_args,
    gdextension_interface.GDExtensionInt p_argument_count,
    gdextension_interface.GDExtensionVariantPtr r_return,
    gdextension_interface.GDExtensionCallError *r_error,
) noexcept with gil:
    cdef object method = <object>method_userdata

    # TODO: Better handle argument passing
    #       - Pre-compute the number and type of arguments?
    #       - Return GDEXTENSION_CALL_ERROR_TOO_(FEW|MANY)_ARGUMENTS errors?
    #       - Determine what value should be passed to argument/excepted fields?
    cdef list args = []
    for i in range(p_argument_count):
        args.append(gd_variant_steal_into_pyobj(<gd_variant_t*>p_args[i]))

    print(f"[DEBUG] _extension_class_static_method_call({method!r}, *{args!r})", flush=True)

    try:
        gd_variant_copy_from_pyobj(method(*args), <gd_variant_t*>r_return)
    except:
        r_error[0].type = gdextension_interface.GDEXTENSION_CALL_ERROR_INVALID_ARGUMENT
        r_error[0].argument = 0
        r_error[0].expected = 0
        raise


# typedef void (*GDExtensionClassMethodValidatedCall)(void *method_userdata, GDExtensionClassInstancePtr p_instance, const GDExtensionConstVariantPtr *p_args, GDExtensionVariantPtr r_return);
# typedef void (*GDExtensionClassMethodPtrCall)(void *method_userdata, GDExtensionClassInstancePtr p_instance, const GDExtensionConstTypePtr *p_args, GDExtensionTypePtr r_ret);


cdef void _register_python_extension_class_method(gd_string_name_t *gd_class_name, str method_name, object method, bint is_static):
    print(f"[DEBUG] _register_python_extension_class_method({method!r}, static={is_static!r})", flush=True)
    cdef object signature = inspect.signature(method)
    cdef gd_string_name_t gd_method_name = gdapi.gd_string_name_from_unchecked_pystr(method_name)
    cdef gdextension_interface.GDExtensionPropertyInfo return_value
    cdef ssize_t parameters_offset

    cdef gdextension_interface.GDExtensionClassMethodInfo info
    info.name = &gd_method_name
    Py_INCREF(method)  # TODO: Don't forget to Py_DECREF when unregistering the class!
    info.method_userdata = <void*>method

    if is_static:
        info.call_func = _extension_class_static_method_call  # GDExtensionClassMethodCall
        info.method_flags = gdextension_interface.GDEXTENSION_METHOD_FLAG_STATIC  # Bitfield of `GDExtensionClassMethodFlags`
        info.argument_count = len(signature.parameters)
        parameters_offset = 0
    else:
        info.call_func = _extension_class_method_call  # GDExtensionClassMethodCall
        info.method_flags = gdextension_interface.GDEXTENSION_METHOD_FLAG_NORMAL  # Bitfield of `GDExtensionClassMethodFlags`
        parameters_offset = 1  # Ignore self argument
        if len(signature.parameters) != 0:
            info.argument_count = len(signature.parameters) - 1  # Ignore self argument
        else:
            # The method is not supposed to lack the `self` argument, however this
            # might be the case if has been poorly written!
            # In such case we want to avoid ending up with `argument_count == 2**32-1`
            # (which unsurprizingly leads to a segfault) , and instead let the user
            # discovers his mistake by himself whenever he will actually call the
            # method (as it is the Python way ^^).
            info.argument_count = 0

    # TODO: GDExtensionClassMethodPtrCall ptrcall_func;

    if signature.return_annotation is None:
        info.has_return_value = False
    else:
        info.has_return_value = True
        generate_property_info(
            &return_value,
            "",
            # If the return type is missing we consider anything is possible (i.e.
            # a Godot Variant is to be returned).
            # Note `GDExtensionVariantType` has no value to specify the whole variant:
            # `GDEXTENSION_VARIANT_TYPE_NIL` is to be used insead, hence why `type(None)`
            # is passed here).
            type(None) if signature.return_annotation is signature.empty else signature.return_annotation
        )
        info.return_value_info = &return_value  # GDExtensionPropertyInfo*
        # TODO: handle metadata
        info.return_value_metadata = gdextension_interface.GDEXTENSION_METHOD_ARGUMENT_METADATA_NONE  # GDExtensionClassMethodArgumentMetadata

    if info.argument_count != 0:

        # Arguments: `arguments_info` and `arguments_metadata` are array of size `argument_count`.
        # Name and hint information for the argument can be omitted in release builds. Class name should always be present if it applies.
        info.arguments_info = <gdextension_interface.GDExtensionPropertyInfo*>PyMem_Malloc(
            sizeof(gdextension_interface.GDExtensionPropertyInfo) * info.argument_count
        )
        info.arguments_metadata = <gdextension_interface.GDExtensionClassMethodArgumentMetadata*>PyMem_Malloc(
            sizeof(gdextension_interface.GDExtensionClassMethodArgumentMetadata) * info.argument_count
        )

        for i, param in enumerate(signature.parameters.values()):
            if i == 0 and not is_static:  # Ignore self
                continue
            generate_property_info(&info.arguments_info[i - parameters_offset], param.name, param.annotation)
            # TODO: handle metadata
            info.arguments_metadata[i - parameters_offset] = gdextension_interface.GDEXTENSION_METHOD_ARGUMENT_METADATA_NONE  # GDExtensionClassMethodArgumentMetadata

    else:
        info.arguments_info = NULL
        info.arguments_metadata = NULL

    if method.__defaults__ is None:
        info.default_argument_count = 0
        info.default_arguments = NULL  # GDExtensionVariantPtr*
    else:
        info.default_argument_count = len(method.__defaults__)
        info.default_arguments = <gdextension_interface.GDExtensionVariantPtr*>PyMem_Malloc(
            sizeof(gdextension_interface.GDExtensionVariantPtr) * info.default_argument_count
        )
        info.default_arguments[0] = <gdextension_interface.GDExtensionVariantPtr>PyMem_Malloc(sizeof(gd_variant_t) * info.default_argument_count)
        for i in range(info.default_argument_count):
            info.default_arguments[i] = (info.default_arguments[0]) + <ssize_t>i
            gd_variant_copy_from_pyobj(method.__defaults__[i], <gd_variant_t*>info.default_arguments[i])

    gdptrs.gdptr_classdb_register_extension_class_method(
        gdptrs.gdptr_library,
        gd_class_name,
        &info,
    )

    if info.argument_count != 0:
        for i in range(info.argument_count):
            free_property_info(&info.arguments_info[i])
        PyMem_Free(info.arguments_info)
        PyMem_Free(info.arguments_metadata)
    if info.default_arguments != NULL:
        for i in range(info.default_argument_count):
            gdapi.gd_variant_del(<gd_variant_t*>info.default_arguments[i])
        PyMem_Free(info.default_arguments[0])
        PyMem_Free(info.default_arguments)
    gdapi.gd_string_name_del(&gd_method_name)


cdef void _register_python_extension_class_signal(gd_string_name_t *gd_class_name, gd_string_name_t *gd_signal_name, list args):
    cdef gdextension_interface.GDExtensionInt argument_count = len(args)
    cdef gdextension_interface.GDExtensionPropertyInfo *arguments_info = NULL

    if argument_count > 0:
        arguments_info = <gdextension_interface.GDExtensionPropertyInfo *>PyMem_Malloc(
            sizeof(gdextension_interface.GDExtensionPropertyInfo) * argument_count
        )
        for i, (arg_name, arg) in enumerate(args):
            generate_property_info(&arguments_info[i], arg_name, arg)

    gdptrs.gdptr_classdb_register_extension_class_signal(
        gdptrs.gdptr_library,
        gd_class_name,
        gd_signal_name,
        arguments_info,
        argument_count,
    )

    if argument_count > 0:
        for i in range(argument_count):
            free_property_info(&arguments_info[i])
        PyMem_Free(arguments_info)


cdef void generate_property_info(gdextension_interface.GDExtensionPropertyInfo *info, str name, object pytype):
    if isinstance(pytype, UnionType):
        info.type = gdextension_interface.GDEXTENSION_VARIANT_TYPE_NIL  # `Nil` stands for "any Variant" here
    else:
        info.type = py_to_gd_type(pytype)  # GDExtensionVariantType
    info.name = <gdextension_interface.GDExtensionStringNamePtr*>PyMem_Malloc(sizeof(gdextension_interface.GDExtensionStringNamePtr))
    (<gd_string_name_t*>info.name)[0] = gdapi.gd_string_name_from_unchecked_pystr(name)
    info.class_name = <gdextension_interface.GDExtensionStringNamePtr*>PyMem_Malloc(sizeof(gdextension_interface.GDExtensionStringNamePtr))
    if info.type == gdextension_interface.GDEXTENSION_VARIANT_TYPE_OBJECT:
        (<gd_string_name_t*>info.class_name)[0] = gdapi.gd_string_name_from_unchecked_pystr(pytype.__name__)
    else:
        (<gd_string_name_t*>info.class_name)[0] = gdapi.gd_string_name_new()
    # TODO: Handle property hint!
    info.hint = gdapi.PROPERTY_HINT_NONE  # uint32_t, Bitfield of `PropertyHint` (defined in `extension_api.json`).
    info.hint_string = <gdextension_interface.GDExtensionStringPtr*>PyMem_Malloc(sizeof(gdextension_interface.GDExtensionStringPtr))
    (<gd_string_t*>info.hint_string)[0] = gdapi.gd_string_new()
    # TODO: is usage needed when property struct is used type return value & parameters ?
    info.usage = gdapi.PROPERTY_USAGE_NONE  # uint32_t, Bitfield of `PropertyUsageFlags` (defined in `extension_api.json`).


cdef void free_property_info(gdextension_interface.GDExtensionPropertyInfo *info):
    PyMem_Free(info.name)
    PyMem_Free(info.class_name)
    PyMem_Free(info.hint_string)


cdef void _register_python_extension_class_property(
    gd_string_name_t *gd_class_name,
    str prop_name,
    type prop_type,
    str getter_name,
    object setter_name
):
    """Register a Python property as a Godot property.

    Args:
        gd_class_name: The Godot class name
        prop_name: The property name
        getter_func: The getter function (to extract type information)
        getter_name: Name of the registered getter method
        setter_name: Name of the registered setter method (or None for read-only)
    """
    cdef gdextension_interface.GDExtensionPropertyInfo info
    cdef gd_string_name_t gd_getter_name = gdapi.gd_string_name_from_unchecked_pystr(getter_name)
    cdef gd_string_name_t gd_setter_name
    if setter_name is not None:
        gd_setter_name = gdapi.gd_string_name_from_unchecked_pystr(setter_name)
    else:
        # Read-only property (empty setter name)
        gd_setter_name = gdapi.gd_string_name_new()

    generate_property_info(&info, prop_name, prop_type)
    gdptrs.gdptr_classdb_register_extension_class_property(
        gdptrs.gdptr_library,
        gd_class_name,
        &info,
        &gd_setter_name,
        &gd_getter_name
    )

    gdapi.gd_string_name_del(&gd_setter_name)
    gdapi.gd_string_name_del(&gd_getter_name)
    free_property_info(&info)


cdef void _register_python_extension_class_integer_constant(gd_string_name_t *gd_class_name, str constant_name, int constant_value, str enum_name=None):
    """Register an integer constant for a Python extension class.

    Args:
        gd_class_name: The Godot class name
        constant_name: The constant name (for enums, should be ENUM_MEMBER format)
        constant_value: The integer value
        enum_name: Optional enum name for grouping constants
    """
    cdef gd_string_name_t gd_constant_name = gdapi.gd_string_name_from_unchecked_pystr(constant_name)
    cdef gd_string_name_t gd_enum_name

    if enum_name is not None:
        gd_enum_name = gdapi.gd_string_name_from_unchecked_pystr(enum_name)
    else:
        gd_enum_name = gdapi.gd_string_name_new()  # Empty for standalone constants

    gdptrs.gdptr_classdb_register_extension_class_integer_constant(
        gdptrs.gdptr_library,
        gd_class_name,
        &gd_enum_name,
        &gd_constant_name,
        constant_value,
        False  # is_bitfield
    )

    gdapi.gd_string_name_del(&gd_constant_name)
    gdapi.gd_string_name_del(&gd_enum_name)
