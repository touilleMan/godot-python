cimport cython
from cpython.ref cimport Py_INCREF, Py_DECREF
from libc.string cimport strcmp
from libc.stdlib cimport malloc, free

from godot.hazmat.gdextension_interface cimport *
from godot.hazmat.gdapi cimport *


@cython.final
cdef class ExtensionClassSpec:
    cdef bytes class_name
    cdef bytes parent_class_name
    cdef list specs_protected_from_gc


@cython.final
cdef class ExtensionClassMethodSpec:
    cdef bytes class_name
    cdef bytes method_name
    cdef bint is_staticmethod
    cdef bytes return_type
    cdef list arguments_type  # list of (<name>, <type>)


cdef inline list _get_extension_gc_protector() noexcept:
    import godot.hazmat
    return godot.hazmat.__dict__.setdefault("__extension_gc_protector", [])


cdef inline void unregister_extension_class(bytes class_name) noexcept:
    cdef gd_string_name_t gd_class_name
    pythonscript_gdstringname_new(&gd_class_name, <char*>class_name)
    pythonscript_gdextension.classdb_unregister_extension_class(
        pythonscript_gdextension_library,
        &gd_class_name,
    )
    gd_string_name_del(&gd_class_name)

    # Note we cannot free the spec given we don't know if the unregister operation has succeeded
    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged

cdef inline void _extension_class_to_string(GDExtensionClassInstancePtr p_instance, GDExtensionBool *r_is_valid, GDExtensionStringPtr p_out) noexcept with gil:
    cdef ExtensionClassSpec spec = <ExtensionClassSpec>p_instance
    (<gd_string_t*>p_out)[0] = gd_string_from_pybytes(spec.class_name)
    r_is_valid[0] = True


cdef inline void register_extension_class_creation(
    bytes class_name,
    bytes parent_class_name,
    GDExtensionClassCreateInstance create_instance_func,
    GDExtensionClassFreeInstance free_instance_func,
) noexcept:
    cdef ExtensionClassSpec spec = ExtensionClassSpec()
    spec.class_name = class_name
    spec.parent_class_name = parent_class_name
    spec.specs_protected_from_gc = []

    cdef list specs_list = _get_extension_gc_protector()
    specs_list.append(spec)

    cdef GDExtensionClassCreationInfo info
    info.set_func = NULL  # GDExtensionClassSet
    info.get_func = NULL  # GDExtensionClassGet
    info.get_property_list_func = NULL  # GDExtensionClassGetPropertyList
    info.free_property_list_func = NULL  # GDExtensionClassFreePropertyList
    info.property_can_revert_func = NULL # GDExtensionClassPropertyCanRevert
    info.property_get_revert_func = NULL # GDExtensionClassPropertyGetRevert
    info.notification_func = NULL  # GDExtensionClassNotification
    info.to_string_func = &_extension_class_to_string  # GDExtensionClassToString
    info.reference_func = NULL  # GDExtensionClassReference
    info.unreference_func = NULL  # GDExtensionClassUnreference
    info.create_instance_func = create_instance_func
    info.free_instance_func = free_instance_func
    info.get_virtual_func = NULL  # GDExtensionClassGetVirtual
    info.get_rid_func = NULL  # GDExtensionClassGetRID
    # Don't increment refcount given we rely on gc protector
    info.class_userdata = <void*>spec  # void*

    cdef gd_string_name_t gdname
    cdef gd_string_name_t gdname_parent
    pythonscript_gdstringname_new(&gdname, <char*>class_name)
    pythonscript_gdstringname_new(&gdname_parent, <char*>parent_class_name)
    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged
    pythonscript_gdextension.classdb_register_extension_class(
        pythonscript_gdextension_library,
        &gdname,
        &gdname_parent,
        &info,
    )
    gd_string_name_del(&gdname)
    gd_string_name_del(&gdname_parent)


cdef inline GDExtensionVariantType _extension_class_method_get_argument_type(void* p_method_userdata, int32_t p_argument) noexcept with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata

    if p_argument == -1:
        return _type_name_to_gdnative_variant_type(spec.return_type)
    else:
        return _type_name_to_gdnative_variant_type(spec.arguments_type[p_argument][1])


cdef inline void _extension_class_method_get_argument_info(void* p_method_userdata, int32_t p_argument, GDExtensionPropertyInfo* r_info) noexcept with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata
    cdef bytes arg_name
    cdef bytes type_name

    if p_argument == -1:
        r_info.type = _type_name_to_gdnative_variant_type(spec.return_type)
        r_info.name = malloc(sizeof(gd_string_name_t))
        (<gd_string_name_t*>r_info.name)[0] = gd_string_name_from_pybytes(b"")
    else:
        arg_name, type_name = spec.arguments_type[p_argument]
        r_info.type = _type_name_to_gdnative_variant_type(type_name)
        r_info.name = malloc(sizeof(gd_string_name_t))
        (<gd_string_name_t*>r_info.name)[0] = gd_string_name_from_pybytes(arg_name)

    r_info.class_name = malloc(sizeof(gd_string_name_t))
    (<gd_string_name_t*>r_info.class_name)[0] = gd_string_name_from_pybytes(spec.class_name)

    # TODO: finish that !
    r_info.hint = PROPERTY_HINT_NONE
    r_info.hint_string = malloc(sizeof(gd_string_t))
    (<gd_string_t*>r_info.hint_string)[0] = gd_string_from_pybytes(b"")
    r_info.usage = PROPERTY_USAGE_DEFAULT


cdef inline void _extension_class_method_empty_argument_info(GDExtensionPropertyInfo* r_info) noexcept with gil:
    r_info.type = GDEXTENSION_VARIANT_TYPE_NIL
    r_info.name = malloc(sizeof(gd_string_name_t))
    (<gd_string_name_t*>r_info.name)[0] = gd_string_name_from_pybytes(b"")
    r_info.class_name = malloc(sizeof(gd_string_name_t))
    (<gd_string_name_t*>r_info.class_name)[0] = gd_string_name_from_pybytes(b"")
    r_info.hint = PROPERTY_HINT_NONE
    r_info.hint_string = malloc(sizeof(gd_string_t))
    (<gd_string_t*>r_info.hint_string)[0] = gd_string_from_pybytes(b"")
    r_info.usage = PROPERTY_USAGE_DEFAULT


cdef inline GDExtensionVariantType _type_name_to_gdnative_variant_type(bytes type_name) noexcept:
    if type_name is None:
        return GDEXTENSION_VARIANT_TYPE_NIL
    elif type_name in (b"void", b"gd_variant_t", b"gd_object_t") or type_name.endswith(b"*"):
        # Nil variant type both means "no type" and "type is a pointer"
        return GDEXTENSION_VARIANT_TYPE_NIL
    elif type_name == b"gd_bool_t":
        return GDEXTENSION_VARIANT_TYPE_BOOL
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
        return GDEXTENSION_VARIANT_TYPE_INT
    elif type_name in (b"gd_float_t", b"float", b"double"):
        return GDEXTENSION_VARIANT_TYPE_FLOAT
    elif type_name == b"gd_string_t":
        return GDEXTENSION_VARIANT_TYPE_STRING
    elif type_name == b"gd_vector2_t":
        return GDEXTENSION_VARIANT_TYPE_VECTOR2
    elif type_name == b"gd_vector2i_t":
        return GDEXTENSION_VARIANT_TYPE_VECTOR2I
    elif type_name == b"gd_rect2_t":
        return GDEXTENSION_VARIANT_TYPE_RECT2
    elif type_name == b"gd_rect2i_t":
        return GDEXTENSION_VARIANT_TYPE_RECT2I
    elif type_name == b"gd_vector3_t":
        return GDEXTENSION_VARIANT_TYPE_VECTOR3
    elif type_name == b"gd_vector3i_t":
        return GDEXTENSION_VARIANT_TYPE_VECTOR3I
    elif type_name == b"gd_transform2d_t":
        return GDEXTENSION_VARIANT_TYPE_TRANSFORM2D
    elif type_name == b"gd_vector4_t":
        return GDEXTENSION_VARIANT_TYPE_VECTOR4
    elif type_name == b"gd_vector4i_t":
        return GDEXTENSION_VARIANT_TYPE_VECTOR4I
    elif type_name == b"gd_plane_t":
        return GDEXTENSION_VARIANT_TYPE_PLANE
    elif type_name == b"gd_quaternion_t":
        return GDEXTENSION_VARIANT_TYPE_QUATERNION
    elif type_name == b"gd_aabb_t":
        return GDEXTENSION_VARIANT_TYPE_AABB
    elif type_name == b"gd_basis_t":
        return GDEXTENSION_VARIANT_TYPE_BASIS
    elif type_name == b"gd_transform3d_t":
        return GDEXTENSION_VARIANT_TYPE_TRANSFORM3D
    elif type_name == b"gd_projection_t":
        return GDEXTENSION_VARIANT_TYPE_PROJECTION
    elif type_name == b"gd_color_t":
        return GDEXTENSION_VARIANT_TYPE_COLOR
    elif type_name == b"gd_string_name_t":
        return GDEXTENSION_VARIANT_TYPE_STRING_NAME
    elif type_name == b"gd_node_path_t":
        return GDEXTENSION_VARIANT_TYPE_NODE_PATH
    elif type_name == b"gd_rid_t":
        return GDEXTENSION_VARIANT_TYPE_RID
    elif type_name == b"gd_object_t":
        return GDEXTENSION_VARIANT_TYPE_OBJECT
    elif type_name == b"gd_callable_t":
        return GDEXTENSION_VARIANT_TYPE_CALLABLE
    elif type_name == b"gd_signal_t":
        return GDEXTENSION_VARIANT_TYPE_SIGNAL
    elif type_name == b"gd_dictionary_t":
        return GDEXTENSION_VARIANT_TYPE_DICTIONARY
    elif type_name == b"gd_array_t":
        return GDEXTENSION_VARIANT_TYPE_ARRAY
    elif type_name == b"gd_packed_byte_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_BYTE_ARRAY
    elif type_name == b"gd_packed_int32_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_INT32_ARRAY
    elif type_name == b"gd_packed_int64_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_INT64_ARRAY
    elif type_name == b"gd_packed_float32_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_FLOAT32_ARRAY
    elif type_name == b"gd_packed_float64_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_FLOAT64_ARRAY
    elif type_name == b"gd_packed_string_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_STRING_ARRAY
    elif type_name == b"gd_packed_vector2_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_VECTOR2_ARRAY
    elif type_name == b"gd_packed_vector3_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_VECTOR3_ARRAY
    elif type_name == b"gd_packed_color_array_t":
        return GDEXTENSION_VARIANT_TYPE_PACKED_COLOR_ARRAY
    else:
        # TODO: better error !
        print(f"Pythonscript extension class registration: Unknown type_name `{type_name}`")
        return GDEXTENSION_VARIANT_TYPE_NIL


cdef inline GDExtensionClassMethodArgumentMetadata _extension_class_method_get_argument_metadata(void* p_method_userdata, int32_t p_argument) noexcept with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata
    cdef bytes type_name
    if p_argument == -1:
        type_name = spec.return_type
    else:
        _, type_name = spec.arguments_type[p_argument]

    if type_name == b"uint8_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT8
    elif type_name == b"uint16_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT16
    elif type_name == b"uint32_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT32
    elif type_name == b"uint64_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_UINT64
    elif type_name == b"int8_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT8
    elif type_name == b"int16_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT16
    elif type_name == b"int32_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT32
    elif type_name == b"int64_t":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_INT_IS_INT64
    elif type_name == b"float":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_REAL_IS_FLOAT
    elif type_name == b"double":
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_REAL_IS_DOUBLE
    else:
        return GDEXTENSION_METHOD_ARGUMENT_METADATA_NONE


cdef inline void _method_call_func(
    void* p_method_userdata,
    GDExtensionClassInstancePtr p_instance,
    const GDExtensionConstVariantPtr* p_args,
    GDExtensionInt p_argument_count,
    GDExtensionVariantPtr r_return,
    GDExtensionCallError* r_error
) noexcept with gil:
    cdef ExtensionClassMethodSpec spec = <ExtensionClassMethodSpec>p_method_userdata
    # TODO: finish me !
    print(f"Pythonscript: `{spec.class_name.decode()}::{spec.method_name.decode()}` method call without ptrcall is not yet supported !!!")
    r_error[0].error = GDEXTENSION_CALL_ERROR_INVALID_METHOD
    r_error[0].argument = 0
    r_error[0].expected = 0


cdef inline void register_extension_class_method(
    bytes class_name,
    bytes method_name,
    GDExtensionClassMethodPtrCall ptrcall_func,
    bint is_staticmethod,
    bytes return_type,
    list arguments_type
    # list default_arguments,
    # uint32_t argument_count,
) noexcept:
    # 1) Build & register spec

    cdef ExtensionClassMethodSpec method_spec = ExtensionClassMethodSpec()
    method_spec.class_name = class_name
    method_spec.method_name = method_name
    method_spec.is_staticmethod = is_staticmethod
    method_spec.return_type = return_type
    method_spec.arguments_type = arguments_type

    cdef list specs_list = _get_extension_gc_protector()
    specs_list.append(method_spec)

    # 2) Build the info struct (passed to Godot when registering the method)

    cdef GDExtensionClassMethodInfo info
    cdef gd_string_name_t gd_method_name = gd_string_name_from_pybytes(method_name)
    info.name = &gd_method_name
    info.method_userdata = <void*>method_spec  # void*
    info.call_func = _method_call_func  # GDExtensionClassMethodCall
    info.ptrcall_func = ptrcall_func  # GDExtensionClassMethodPtrCall
    # TODO: support other flags
    if is_staticmethod:
        info.method_flags = GDEXTENSION_METHOD_FLAG_STATIC
    else:
        info.method_flags = GDEXTENSION_METHOD_FLAG_NORMAL

    info.return_value_info = <GDExtensionPropertyInfo*>malloc(sizeof(GDExtensionPropertyInfo))
    if return_type == b"void":
        info.has_return_value = False  # gd_bool_t
        info.return_value_metadata = GDEXTENSION_METHOD_ARGUMENT_METADATA_NONE  # Dummy default
        _extension_class_method_empty_argument_info(info.return_value_info)  # Dummy default
    else:
        info.has_return_value = True  # gd_bool_t
        # TODO: refactor this hack based on the old GDExtension API
        _extension_class_method_get_argument_info(info.method_userdata, -1, info.return_value_info)  # GDExtensionPropertyInfo *
        info.return_value_metadata = _extension_class_method_get_argument_metadata(info.method_userdata, -1)  # GDExtensionClassMethodArgumentMetadata

    info.argument_count = <uint32_t>len(arguments_type)  # uint32_t

    if info.argument_count > 0:
        info.arguments_info = <GDExtensionPropertyInfo*>malloc(sizeof(GDExtensionPropertyInfo) * info.argument_count)
        info.arguments_metadata = <GDExtensionClassMethodArgumentMetadata*>malloc(sizeof(GDExtensionClassMethodArgumentMetadata) * info.argument_count)
    else:
        info.arguments_info = NULL  # GDExtensionPropertyInfo *
        info.arguments_metadata = NULL  # GDExtensionClassMethodArgumentMetadata *

    for i, _ in enumerate(arguments_type):
        # TODO: refactor this hack based on the old GDExtension API
        _extension_class_method_get_argument_info(info.method_userdata, i, &info.arguments_info[i])
        info.arguments_metadata[i] = _extension_class_method_get_argument_metadata(info.method_userdata, i)

    # TODO: support default arguments
    info.default_argument_count = 0  # uint32_t
    info.default_arguments = NULL  # GDExtensionVariantPtr*

    # 3) Actually register the method

    cdef gd_string_name_t gd_class_name = gd_string_name_from_pybytes(class_name)
    pythonscript_gdextension.classdb_register_extension_class_method(
        pythonscript_gdextension_library,
        &gd_class_name,
        &info,
    )
    gd_string_name_del(&gd_class_name)

    # 3) Free up the info struct

    gd_string_name_del(&gd_method_name)

    gd_string_name_del(<gd_string_name_t*>info.return_value_info.name)
    free(info.return_value_info.name)

    gd_string_name_del(<gd_string_name_t*>info.return_value_info.class_name)
    free(info.return_value_info.class_name)

    gd_string_del(<gd_string_t*>info.return_value_info.hint_string)
    free(info.return_value_info.hint_string)

    free(info.return_value_info)

    for i, _ in enumerate(arguments_type):
        gd_string_name_del(<gd_string_name_t*>info.arguments_info[i].name)
        free(info.arguments_info[i].name)

        gd_string_name_del(<gd_string_name_t*>info.arguments_info[i].class_name)
        free(info.arguments_info[i].class_name)

        gd_string_del(<gd_string_t*>info.arguments_info[i].hint_string)
        free(info.arguments_info[i].hint_string)

    if info.arguments_info != NULL:
        free(info.arguments_info)

    # TODO: free `info.default_arguments`

    # TODO: correct me once https://github.com/godotengine/godot/pull/67121 is merged
