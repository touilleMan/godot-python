cdef StringName gdname_scriptextension = StringName("ScriptExtension")
cdef StringName gdname_pythonscript = StringName("PythonScript")

# godot_extension: class(parent="ScriptExtension")
@cython.final
cdef class PythonScript:
    cdef gd_object_t _gd_ptr

    def __cinit__(self):
        self._gd_ptr = pythonscript_gdextension.classdb_construct_object(&gdname_scriptextension._gd_data)
        pythonscript_gdextension.object_set_instance(self._gd_ptr, &gdname_pythonscript._gd_data, <PyObject*>self)

    # godot_extension: generate_code()

    # godot_extension: method(const=True)
    cdef gd_bool_t _can_instantiate(self):
        # TODO
        return False

    # godot_extension: method()
    cdef gd_bool_t _editor_can_reload_from_file(self):
        # TODO
        return False

    # godot_extension: method(const=True)
    cdef gd_object_t _get_base_script(self):
        # TODO
        # Retuns Script
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_constants(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_documentation(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_string_name_t _get_instance_base_type(self):
        # TODO
        cdef gd_string_name_t ret = gd_string_name_from_pybytes(b"")
        return ret

    # godot_extension: method(const=True)
    cdef gd_object_t _get_language(self):
        # TODO
        # Returns ScriptLanguage
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _get_member_line(self, gd_string_name_t member):
        # TODO
        gd_string_name_del(&member)
        return 0

    # godot_extension: method(const=True)
    cdef gd_string_name_t _get_members(self):
        # TODO
        cdef gd_string_name_t ret = gd_string_name_from_pybytes(b"")
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_method_info(self, gd_string_name_t method):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_name_del(&method)
        return ret

    # godot_extension: method(const=True)
    cdef gd_variant_t _get_property_default_value(self, gd_string_name_t property):
        # TODO
        cdef gd_variant_t ret = gd_variant_new()
        gd_string_name_del(&property)
        return ret

    # godot_extension: method(const=True)
    cdef gd_variant_t _get_rpc_config(self):
        # TODO
        cdef gd_variant_t ret = gd_variant_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_script_method_list(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_script_property_list(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_script_signal_list(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_string_t _get_source_code(self):
        # TODO
        cdef gd_string_t ret = gd_string_from_pybytes(b"")
        return ret

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_method(self, gd_string_name_t method):
        # TODO
        gd_string_name_del(&method)
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_property_default_value(self, gd_string_name_t property):
        # TODO
        gd_string_name_del(&property)
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_script_signal(self, gd_string_name_t signal):
        # TODO
        gd_string_name_del(&signal)
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_source_code(self):
        # TODO
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _inherits_script(self, gd_object_t script):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return False

    # godot_extension: method(const=True)
    cdef void* _instance_create(self, gd_object_t for_object):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return NULL

    # godot_extension: method(const=True)
    cdef gd_bool_t _instance_has(self, gd_object_t object):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_placeholder_fallback_enabled(self):
        # TODO
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_tool(self):
        # TODO
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_valid(self):
        # TODO
        return False

    # godot_extension: method()
    cdef void _placeholder_erased(self, void* placeholder):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef void* _placeholder_instance_create(self, gd_object_t for_object):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        pass

    # godot_extension: method()
    cdef gd_int_t _reload(self, gd_bool_t keep_state):
        # TODO
        return Error.FAILED

    # godot_extension: method()
    cdef void _set_source_code(self, gd_string_t code):
        # TODO
        gd_string_del(&code)

    # godot_extension: method()
    cdef void _update_exports(self):
        # TODO
        pass
