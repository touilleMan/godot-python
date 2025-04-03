cdef gd_string_name_t gdname_scriptextension
cdef gd_string_name_t gdname_pythonscript


# godot_extension: class(parent="ScriptExtension")
@cython.final
cdef class PythonScript:
    cdef gd_object_t _gd_ptr

    def __cinit__(self):
        self._gd_ptr = pythonscript_gdextension.classdb_construct_object(&gdname_scriptextension)
        pythonscript_gdextension.object_set_instance(self._gd_ptr, &gdname_pythonscript, <PyObject*>self)

    # godot_extension: register_class_hook()
    @staticmethod
    cdef inline void _register_class_hook():
        global gdname_scriptextension, gdname_pythonscript
        gdname_scriptextension = gd_string_name_from_unchecked_pystr("ScriptExtension")
        gdname_pythonscript = gd_string_name_from_unchecked_pystr("PythonScript")

    # godot_extension: unregister_class_hook()
    @staticmethod
    cdef inline void _unregister_class_hook():
        global gdname_scriptextension, gdname_pythonscript
        gd_string_name_del(&gdname_scriptextension)
        gd_string_name_del(&gdname_pythonscript)

    # godot_extension: generate_code()

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _can_instantiate(self):
        spy_log("CALLED PythonScript::_can_instantiate")
        # TODO
        return False

    # godot_extension: method(virtual=True)
    cdef gd_bool_t _editor_can_reload_from_file(self):
        spy_log("CALLED PythonScript::_editor_can_reload_from_file")
        # TODO
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_object_t _get_base_script(self):
        spy_log("CALLED PythonScript::_get_base_script")
        # TODO
        # Retuns Script
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_constants(self):
        spy_log("CALLED PythonScript::_get_constants")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_documentation(self):
        spy_log("CALLED PythonScript::_get_documentation")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_name_t _get_instance_base_type(self):
        spy_log("CALLED PythonScript::_get_instance_base_type")
        # TODO
        cdef gd_string_name_t ret = gd_string_name_from_pybytes(b"")
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_object_t _get_language(self):
        spy_log("CALLED PythonScript::_get_language")
        # TODO
        # Returns ScriptLanguage
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _get_member_line(self, gd_string_name_t member):
        spy_log("CALLED PythonScript::_get_member_line")
        # TODO
        gd_string_name_del(&member)
        return 0

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_name_t _get_members(self):
        spy_log("CALLED PythonScript::_get_members")
        # TODO
        cdef gd_string_name_t ret = gd_string_name_from_pybytes(b"")
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_method_info(self, gd_string_name_t method):
        spy_log("CALLED PythonScript::_get_method_info")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_name_del(&method)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _get_property_default_value(self, gd_string_name_t property):
        spy_log("CALLED PythonScript::_get_property_default_value")
        # TODO
        cdef gd_variant_t ret = gd_variant_new()
        gd_string_name_del(&property)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_variant_t _get_rpc_config(self):
        spy_log("CALLED PythonScript::_get_rpc_config")
        # TODO
        cdef gd_variant_t ret = gd_variant_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_script_method_list(self):
        spy_log("CALLED PythonScript::_get_script_method_list")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_script_property_list(self):
        spy_log("CALLED PythonScript::_get_script_property_list")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_script_signal_list(self):
        spy_log("CALLED PythonScript::_get_script_signal_list")
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_source_code(self):
        spy_log("CALLED PythonScript::_get_source_code")
        # TODO
        cdef gd_string_t ret = gd_string_from_pybytes(b"")
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_method(self, gd_string_name_t method):
        spy_log("CALLED PythonScript::_has_method")
        # TODO
        gd_string_name_del(&method)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_property_default_value(self, gd_string_name_t property):
        spy_log("CALLED PythonScript::_has_property_default_value")
        # TODO
        gd_string_name_del(&property)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_script_signal(self, gd_string_name_t signal):
        spy_log("CALLED PythonScript::_has_script_signal")
        # TODO
        gd_string_name_del(&signal)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_source_code(self):
        spy_log("CALLED PythonScript::_has_source_code")
        # TODO
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _inherits_script(self, gd_object_t script):
        spy_log("CALLED PythonScript::_inherits_script")
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef void* _instance_create(self, gd_object_t for_object):
        spy_log("CALLED PythonScript::_instance_create")
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return NULL

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _instance_has(self, gd_object_t object):
        spy_log("CALLED PythonScript::_instance_has")
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_placeholder_fallback_enabled(self):
        spy_log("CALLED PythonScript::_is_placeholder_fallback_enabled")
        # TODO
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_tool(self):
        spy_log("CALLED PythonScript::_is_tool")
        # TODO
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_valid(self):
        spy_log("CALLED PythonScript::_is_valid")
        # TODO
        return False

    # godot_extension: method(virtual=True)
    cdef void _placeholder_erased(self, void* placeholder):
        spy_log("CALLED PythonScript::_placeholder_erased")
        # TODO
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef void* _placeholder_instance_create(self, gd_object_t for_object):
        spy_log("CALLED PythonScript::_placeholder_instance_create")
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        pass

    # godot_extension: method(virtual=True)
    cdef gd_int_t _reload(self, gd_bool_t keep_state):
        spy_log("CALLED PythonScript::_reload")
        # TODO
        return Error.FAILED

    # godot_extension: method(virtual=True)
    cdef void _set_source_code(self, gd_string_t code):
        spy_log("CALLED PythonScript::_set_source_code")
        # TODO
        gd_string_del(&code)

    # godot_extension: method(virtual=True)
    cdef void _update_exports(self):
        spy_log("CALLED PythonScript::_update_exports")
        # TODO
        pass
