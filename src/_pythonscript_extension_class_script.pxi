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
        pass

    # godot_extension: method()
    cdef gd_bool_t _editor_can_reload_from_file(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_object_t _get_base_script(self):
        # Retuns Script
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_constants(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_documentation(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_name_t _get_instance_base_type(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_object_t _get_language(self):
        # Returns ScriptLanguage
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _get_member_line(self, gd_string_name_t member):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_name_t _get_members(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_method_info(self, gd_string_name_t method):
        pass

    # godot_extension: method(const=True)
    cdef gd_variant_t _get_property_default_value(self, gd_string_name_t property):
        pass

    # godot_extension: method(const=True)
    cdef gd_variant_t _get_rpc_config(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_script_method_list(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_script_property_list(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_script_signal_list(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _get_source_code(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_method(self, gd_string_name_t method):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_property_default_value(self, gd_string_name_t property):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_script_signal(self, gd_string_name_t signal):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_source_code(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _inherits_script(self, gd_object_t script):
        pass

    # godot_extension: method(const=True)
    cdef void* _instance_create(self, gd_object_t for_object):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _instance_has(self, gd_object_t object):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_placeholder_fallback_enabled(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_tool(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_valid(self):
        pass

    # godot_extension: method()
    cdef void _placeholder_erased(self, void* placeholder):
        pass

    # godot_extension: method(const=True)
    cdef void* _placeholder_instance_create(self, gd_object_t for_object):
        pass

    # godot_extension: method()
    cdef gd_int_t _reload(self, gd_bool_t keep_state):
        # Retuns Error
        pass

    # godot_extension: method()
    cdef void _set_source_code(self, gd_string_t code):
        pass

    # godot_extension: method()
    cdef void _update_exports(self):
        pass
