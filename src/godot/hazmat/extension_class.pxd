cimport cython
from cpython.ref cimport Py_INCREF, Py_DECREF
from libc.string cimport strcmp

from godot.hazmat.gdnative_interface cimport *
from godot.hazmat.gdapi cimport *


@cython.final
cdef class ExtensionClassSpec:
    cdef bytes class_name
    cdef bytes parent_class_name
    cdef list specs_protected_from_gc


@cython.final
cdef class ExtensionClassMethodSpec:
    cdef bytes class_name
    cdef bytes meth_name
    cdef bint is_staticmethod
    cdef bytes return_type
    cdef list arguments_type  # List[Tuple[bytes, bytes]]


cdef inline list _get_extension_gc_protector():
    import godot.hazmat
    return godot.hazmat.__dict__.setdefault("__extension_gc_protector", [])


cdef inline void unregister_extension_class(bytes class_name):
    # TODO: Don't know why, but class_name&parent_class_name are both str instead of bytes...
    # (this is worst than that: the type is str, but cannot calling encode on it raise a
    # `type object 'bytes' has no attribute 'encode'` error...)
    class_name = str(class_name).encode("utf8")

    pythonscript_gdnative_interface.classdb_unregister_extension_class(
        pythonscript_gdnative_library,
        class_name,
    )

    # Note we cannot free the spec given we don't know if the unregister operation has succeeded
    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged


cdef inline void _extension_class_to_string(GDExtensionClassInstancePtr p_instance, GDNativeStringPtr p_out) with gil:
    cdef ExtensionClassSpec spec = <ExtensionClassSpec>p_instance
    pythonscript_gdnative_interface.string_new_with_utf8_chars(p_out, spec.class_name)


cdef inline void register_extension_class_creation(
    bytes class_name,
    bytes parent_class_name,
    GDNativeExtensionClassCreateInstance create_instance_func,
    GDNativeExtensionClassFreeInstance free_instance_func,
):
    # TODO: Don't know why, but class_name&parent_class_name are both str instead of bytes...
    # (this is worst than that: the type is str, but cannot calling encode on it raise a
    # `type object 'bytes' has no attribute 'encode'` error...)
    class_name = str(class_name).encode("utf8")
    parent_class_name = str(parent_class_name).encode("utf8")

    cdef ExtensionClassSpec spec = ExtensionClassSpec(
        class_name=class_name,
        parent_class_name=parent_class_name,
        methods=[],
    )
    cdef list specs_list = _get_extension_gc_protector()
    specs_list.append(spec)

    cdef GDNativeExtensionClassCreationInfo info
    info.set_func = NULL  # GDNativeExtensionClassSet
    info.get_func = NULL  # GDNativeExtensionClassGet
    info.get_property_list_func = NULL  # GDNativeExtensionClassGetPropertyList
    info.free_property_list_func = NULL  # GDNativeExtensionClassFreePropertyList
    info.property_can_revert_func = NULL # GDNativeExtensionClassPropertyCanRevert
    info.property_get_revert_func = NULL # GDNativeExtensionClassPropertyGetRevert
    info.notification_func = NULL  # GDNativeExtensionClassNotification
    info.to_string_func = &_extension_class_to_string  # GDNativeExtensionClassToString
    info.reference_func = NULL  # GDNativeExtensionClassReference
    info.unreference_func = NULL  # GDNativeExtensionClassUnreference
    info.create_instance_func = create_instance_func
    info.free_instance_func = free_instance_func
    info.get_virtual_func = NULL  # GDNativeExtensionClassGetVirtual
    info.get_rid_func = NULL  # GDNativeExtensionClassGetRID
    # Don't increment refcount given we rely on gc protector
    info.class_userdata = <void*>spec  # void*

    pythonscript_gdnative_interface.classdb_register_extension_class(
        pythonscript_gdnative_library,
        class_name,
        parent_class_name,
        &info,
    )
    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged


cdef inline GDNativeVariantType _extension_class_method_get_argument_type(void* p_method_userdata, int32_t p_argument) with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata

    if p_argument == -1:
        return _type_name_to_gdnative_variant_type(spec.return_type)
    else:
        return _type_name_to_gdnative_variant_type(spec.arguments_type[p_argument][1])


cdef inline void _extension_class_method_get_argument_info(void* p_method_userdata, int32_t p_argument, GDNativePropertyInfo* r_info) with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata
    cdef bytes arg_name
    cdef bytes type_name

    if p_argument == -1:
        r_info.type = _type_name_to_gdnative_variant_type(spec.return_type)
        r_info.name = NULL
    else:
        arg_name, type_name = spec.arguments_type[p_argument]
        r_info.type = _type_name_to_gdnative_variant_type(type_name)
        r_info.name = arg_name

    # TODO: handle class name !
    r_info.class_name = b""

    # TODO: finish that !
    r_info.hint = PROPERTY_HINT_NONE
    r_info.hint_string = b""
    r_info.usage = PROPERTY_USAGE_DEFAULT


cdef inline GDNativeVariantType _type_name_to_gdnative_variant_type(bytes type_name):
    if type_name is None:
        return GDNATIVE_VARIANT_TYPE_NIL
    elif type_name in (b"void", b"gd_variant_t", b"gd_object_t"):
        return GDNATIVE_VARIANT_TYPE_NIL
    elif type_name == b"gd_bool_t":
        return GDNATIVE_VARIANT_TYPE_BOOL
    elif type_name in (
        b"gd_int_t",
        b"uint8_t",
        b"uint16_t",
        b"uint32_t",
        b"uint64_t",
        b"int8_t",
        b"int16_t",
        b"int32_t",
        b"int64_t",
    ):
        return GDNATIVE_VARIANT_TYPE_INT
    elif type_name in (b"gd_float_t", b"float", b"double"):
        return GDNATIVE_VARIANT_TYPE_FLOAT
    elif type_name == b"gd_string_t":
        return GDNATIVE_VARIANT_TYPE_STRING
    elif type_name == b"gd_vector2_t":
        return GDNATIVE_VARIANT_TYPE_VECTOR2
    elif type_name == b"gd_vector2i_t":
        return GDNATIVE_VARIANT_TYPE_VECTOR2I
    elif type_name == b"gd_rect2_t":
        return GDNATIVE_VARIANT_TYPE_RECT2
    elif type_name == b"gd_rect2i_t":
        return GDNATIVE_VARIANT_TYPE_RECT2I
    elif type_name == b"gd_vector3_t":
        return GDNATIVE_VARIANT_TYPE_VECTOR3
    elif type_name == b"gd_vector3i_t":
        return GDNATIVE_VARIANT_TYPE_VECTOR3I
    elif type_name == b"gd_transform2d_t":
        return GDNATIVE_VARIANT_TYPE_TRANSFORM2D
    elif type_name == b"gd_vector4_t":
        return GDNATIVE_VARIANT_TYPE_VECTOR4
    elif type_name == b"gd_vector4i_t":
        return GDNATIVE_VARIANT_TYPE_VECTOR4I
    elif type_name == b"gd_plane_t":
        return GDNATIVE_VARIANT_TYPE_PLANE
    elif type_name == b"gd_quaternion_t":
        return GDNATIVE_VARIANT_TYPE_QUATERNION
    elif type_name == b"gd_aabb_t":
        return GDNATIVE_VARIANT_TYPE_AABB
    elif type_name == b"gd_basis_t":
        return GDNATIVE_VARIANT_TYPE_BASIS
    elif type_name == b"gd_transform3d_t":
        return GDNATIVE_VARIANT_TYPE_TRANSFORM3D
    elif type_name == b"gd_projection_t":
        return GDNATIVE_VARIANT_TYPE_PROJECTION
    elif type_name == b"gd_color_t":
        return GDNATIVE_VARIANT_TYPE_COLOR
    elif type_name == b"gd_string_name_t":
        return GDNATIVE_VARIANT_TYPE_STRING_NAME
    elif type_name == b"gd_node_path_t":
        return GDNATIVE_VARIANT_TYPE_NODE_PATH
    elif type_name == b"gd_rid_t":
        return GDNATIVE_VARIANT_TYPE_RID
    elif type_name == b"gd_object_t":
        return GDNATIVE_VARIANT_TYPE_OBJECT
    elif type_name == b"gd_callable_t":
        return GDNATIVE_VARIANT_TYPE_CALLABLE
    elif type_name == b"gd_signal_t":
        return GDNATIVE_VARIANT_TYPE_SIGNAL
    elif type_name == b"gd_dictionary_t":
        return GDNATIVE_VARIANT_TYPE_DICTIONARY
    elif type_name == b"gd_array_t":
        return GDNATIVE_VARIANT_TYPE_ARRAY
    elif type_name == b"gd_packed_byte_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_BYTE_ARRAY
    elif type_name == b"gd_packed_int32_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_INT32_ARRAY
    elif type_name == b"gd_packed_int64_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_INT64_ARRAY
    elif type_name == b"gd_packed_float32_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_FLOAT32_ARRAY
    elif type_name == b"gd_packed_float64_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_FLOAT64_ARRAY
    elif type_name == b"gd_packed_string_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_STRING_ARRAY
    elif type_name == b"gd_packed_vector2_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_VECTOR2_ARRAY
    elif type_name == b"gd_packed_vector3_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_VECTOR3_ARRAY
    elif type_name == b"gd_packed_color_array_t":
        return GDNATIVE_VARIANT_TYPE_PACKED_COLOR_ARRAY
    else:
        # TODO: better error !
        print(f"Pythonscript extension class registration: Unknown type_name `{type_name}`")
        return GDNATIVE_VARIANT_TYPE_NIL


cdef inline GDNativeExtensionClassMethodArgumentMetadata _extension_class_method_get_argument_metadata(void* p_method_userdata, int32_t p_argument) with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata
    cdef bytes type_name
    if p_argument == -1:
        type_name = spec.return_type
    else:
        _, type_name = spec.arguments_type[p_argument]

    if type_name == b"uint8_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT8
    elif type_name == b"uint16_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT16
    elif type_name == b"uint32_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT32
    elif type_name == b"uint64_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT64
    elif type_name == b"int8_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT8
    elif type_name == b"int16_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT16
    elif type_name == b"int32_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT32
    elif type_name == b"int64_t":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT64
    elif type_name == b"float":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_REAL_IS_FLOAT
    elif type_name == b"double":
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_REAL_IS_DOUBLE
    else:
        return GDNATIVE_EXTENSION_METHOD_ARGUMENT_METADATA_NONE


cdef inline void _method_call_func(
    void* p_method_userdata,
    GDExtensionClassInstancePtr p_instance,
    GDNativeVariantPtr* p_args,
    GDNativeInt p_argument_count,
    GDNativeVariantPtr r_return,
    GDNativeCallError* r_error
) with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata
    # TODO: finish me !
    print(f"Pythonscript: `{spec.class_name.decode()}::{spec.method_name.decode()}` method call without ptrcall is not yet supported !!!")
    r_error[0].error = GDNATIVE_CALL_ERROR_INVALID_METHOD
    r_error[0].argument = 0
    r_error[0].expected = 0


cdef inline void register_extension_class_method(
    bytes class_name,
    bytes method_name,
    GDNativeExtensionClassMethodPtrCall ptrcall_func,
    bint is_staticmethod,
    bytes return_type,
    list arguments_type
    # list default_arguments,
    # uint32_t argument_count,
):
    # TODO: Don't know why, but class_name&parent_class_name are both str instead of bytes...
    # (this is worst than that: the type is str, but cannot calling encode on it raise a
    # `type object 'bytes' has no attribute 'encode'` error...)
    class_name = str(class_name).encode("utf8")
    method_name = str(method_name).encode("utf8")

    cdef ExtensionClassMethodSpec method_spec = ExtensionClassMethodSpec(
        class_name=class_name,
        method_name=method_name,
        is_staticmethod=is_staticmethod,
        return_type=return_type,
        arguments_type=arguments_type,
    )
    cdef list specs_list = _get_extension_gc_protector()
    specs_list.append(method_spec)

    cdef GDNativeExtensionClassMethodInfo info
    info.name = method_name
    info.method_userdata = <void*>method_spec  # void*
    info.call_func = _method_call_func  # GDNativeExtensionClassMethodCall
    info.ptrcall_func = ptrcall_func  # GDNativeExtensionClassMethodPtrCall
    # TODO: support other flags
    if is_staticmethod:
        info.method_flags = GDNATIVE_EXTENSION_METHOD_FLAG_STATIC
    else:
        info.method_flags = GDNATIVE_EXTENSION_METHOD_FLAG_NORMAL
    info.argument_count = len(arguments_type)  # uint32_t
    info.has_return_value = return_type == b"void"  # gd_bool_t
    info.get_argument_type_func = _extension_class_method_get_argument_type  # GDNativeExtensionClassMethodGetArgumentType
    info.get_argument_info_func = _extension_class_method_get_argument_info  # GDNativeExtensionClassMethodGetArgumentInfo
    info.get_argument_metadata_func = _extension_class_method_get_argument_metadata  # GDNativeExtensionClassMethodGetArgumentMetadata
    # TODO: support default arguments
    info.default_argument_count = 0  # uint32_t
    info.default_arguments = NULL  # GDNativeVariantPtr*
    pythonscript_gdnative_interface.classdb_register_extension_class_method(
        pythonscript_gdnative_library,
        class_name,
        &info,
    )
    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged
