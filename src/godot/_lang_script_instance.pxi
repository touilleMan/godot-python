cdef inline GDExtensionScriptInstanceInfo3 generate_instance_info():
    cdef GDExtensionScriptInstanceInfo3 info

    info.set_func = _script_instance_set_func
    info.get_func = _script_instance_get_func
    info.get_property_list_func = _script_instance_get_property_list_func
    info.free_property_list_func = NULL  # _script_instance_free_property_list_func
    info.get_class_category_func = NULL  # _script_instance_get_class_category_func
    info.property_can_revert_func = NULL  # _script_instance_property_can_revert_func
    info.property_get_revert_func = NULL  # _script_instance_property_get_revert_func
    info.get_owner_func = NULL  # _script_instance_get_owner_func
    info.get_property_state_func = NULL  # _script_instance_get_property_state_func
    info.get_method_list_func = _script_instance_get_method_list_func
    info.free_method_list_func = NULL  # _script_instance_free_method_list_func
    info.get_property_type_func = NULL  # _script_instance_get_property_type_func
    info.validate_property_func = NULL  # _script_instance_validate_property_func
    info.has_method_func = NULL  # _script_instance_has_method_func
    info.get_method_argument_count_func = NULL  # _script_instance_get_method_argument_count_func
    info.call_func = _script_instance_call_func
    info.notification_func = NULL  # _script_instance_notification_func
    info.to_string_func = NULL  # _script_instance_to_string_func
    info.refcount_incremented_func = NULL  # _script_instance_refcount_incremented_func
    info.refcount_decremented_func = NULL  # _script_instance_refcount_decremented_func
    info.get_script_func = _script_instance_get_script_func
    info.is_placeholder_func = NULL  # _script_instance_is_placeholder_func
    info.set_fallback_func = NULL  # _script_instance_set_fallback_func
    info.get_fallback_func = NULL  # _script_instance_get_fallback_func
    info.get_language_func = NULL  # _script_instance_get_language_func
    info.free_func = _script_instance_free_func

    return info


cdef GDExtensionBool _script_instance_set_func(
    GDExtensionScriptInstanceDataPtr p_instance,
    GDExtensionConstStringNamePtr p_name,
    GDExtensionConstVariantPtr p_value,
) noexcept with gil:
    print(f"[DEBUG] CALLED _script_instance_set_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


cdef GDExtensionBool _script_instance_get_func(
    GDExtensionScriptInstanceDataPtr p_instance,
    GDExtensionConstStringNamePtr p_name,
    GDExtensionVariantPtr r_ret,
) noexcept with gil:
    print(f"[DEBUG] CALLED _script_instance_get_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


cdef const GDExtensionPropertyInfo* _script_instance_get_property_list_func(
    GDExtensionScriptInstanceDataPtr p_instance,
    uint32_t* r_count,
) noexcept with gil:
    print(f"[DEBUG] CALLED _script_instance_get_property_list_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef void _script_instance_free_property_list_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     const GDExtensionPropertyInfo* p_list,
#     uint32_t p_count,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_free_property_list_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_get_class_category_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionPropertyInfo* p_class_category,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_class_category_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_property_can_revert_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_property_can_revert_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_property_get_revert_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
#     GDExtensionVariantPtr r_ret,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_property_get_revert_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionObjectPtr _script_instance_get_owner_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_owner_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef void _script_instance_get_property_state_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionScriptInstancePropertyStateAdd p_add_func,
# void* p_userdata,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_property_state_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


cdef const GDExtensionMethodInfo* _script_instance_get_method_list_func(
    GDExtensionScriptInstanceDataPtr p_instance,
    uint32_t* r_count,
) noexcept with gil:
    print(f"[DEBUG] CALLED _script_instance_get_method_list_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef void _script_instance_free_method_list_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     const GDExtensionMethodInfo* p_list,
#     uint32_t p_count,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_free_method_list_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionVariantType _script_instance_get_property_type_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
#     GDExtensionBool* r_is_valid,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_property_type_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_validate_property_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionPropertyInfo* p_property,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_validate_property_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_has_method_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_has_method_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionInt _script_instance_get_method_argument_count_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
#     GDExtensionBool* r_is_valid,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_method_argument_count_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


cdef void _script_instance_call_func(
    GDExtensionScriptInstanceDataPtr p_self,
    GDExtensionConstStringNamePtr p_method,
    const GDExtensionConstVariantPtr* p_args,
    GDExtensionInt p_argument_count,
    GDExtensionVariantPtr r_return,
    GDExtensionCallError* r_error,
) noexcept with gil:
    cdef object method = gdapi.gd_string_name_to_pystr(<gd_string_name_t*>p_method)
    cdef list args = [gd_variant_steal_into_pyobj((<gd_variant_t**>p_args)[i]) for i in range(p_argument_count)]
    print(f"[DEBUG] CALLED _script_instance_call_func(self=<object 0x{<size_t>p_self:x}>, method={method!r}, args={args!r})", flush=True)
    cdef object meth
    cdef object ret
    cdef BaseGDObject self = <BaseGDObject>p_self
    # TODO: detect virtual method and avoid calling them here !

    try:
        method_fn = self.__class__.__dict__[str(method)]
    except KeyError as exc:
        r_error.error = GDExtensionCallErrorType.GDEXTENSION_CALL_ERROR_INVALID_METHOD
        print(f"[DEBUG] CALLED DONE _script_instance_call_func(...) -> ERROR {exc!r}", flush=True)
        return
    try:
        ret = method_fn(self, *args)
    except ValueError as exc:
        r_error.error = GDExtensionCallErrorType.GDEXTENSION_CALL_ERROR_INVALID_ARGUMENT
        print(f"[DEBUG] CALLED DONE _script_instance_call_func(...) -> ERROR {exc!r}", flush=True)
        return

    if not gd_variant_steal_from_pyobj(ret, <gd_variant_t*>r_return):
        print(f"Returned value {ret!r} cannot be converted to Godot Variant")
    print(f"[DEBUG] CALLED DONE _script_instance_call_func(...) -> {ret!r}", flush=True)


# cdef void _script_instance_notification_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     int32_t p_what,
#     GDExtensionBool p_reversed,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_notification_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef void _script_instance_to_string_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionBool* r_is_valid,
#     GDExtensionStringPtr r_out,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_to_string_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef void _script_instance_refcount_incremented_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_refcount_incremented_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_refcount_decremented_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_refcount_decremented_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


cdef GDExtensionObjectPtr _script_instance_get_script_func(
    GDExtensionScriptInstanceDataPtr p_instance,
) noexcept with gil:
    print(f"[DEBUG] CALLED _script_instance_get_script_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_is_placeholder_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_is_placeholder_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_set_fallback_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
#     GDExtensionConstVariantPtr p_value,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_set_fallback_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionBool _script_instance_get_fallback_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
#     GDExtensionConstStringNamePtr p_name,
#     GDExtensionVariantPtr r_ret,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_fallback_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


# cdef GDExtensionScriptLanguagePtr _script_instance_get_language_func(
#     GDExtensionScriptInstanceDataPtr p_instance,
# ) noexcept with gil:
#     print(f"[DEBUG] CALLED _script_instance_get_language_func(<object 0x{<size_t>p_instance:x}>)", flush=True)


cdef void _script_instance_free_func(
    GDExtensionScriptInstanceDataPtr p_instance,
) noexcept with gil:
    print(f"[DEBUG] CALLED _script_instance_free_func(<object 0x{<size_t>p_instance:x}>)", flush=True)
    Py_DECREF(<object>p_instance)
