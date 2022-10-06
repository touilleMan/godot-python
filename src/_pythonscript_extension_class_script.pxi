@godot_extension_class(parent="ScriptExtension")
@cython.final
cdef class PythonScript:

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _can_instantiate(self):
    #     pass

    # @godot_extension_class_method  # virtual
    # cdef gd_bool_t _editor_can_reload_from_file(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef Script _get_base_script(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_dictionary_t _get_constants(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_dictionary_t _get_documentation(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_string_name_t _get_instance_base_type(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef ScriptLanguage _get_language(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_int_t _get_member_line(self, gd_string_name_t member):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_string_name_t _get_members(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_dictionary_t _get_method_info(self, gd_string_name_t method):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef Variant _get_property_default_value(self, gd_string_name_t property):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef Variant _get_rpc_config(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_dictionary_t _get_script_method_list(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_dictionary_t _get_script_property_list(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_dictionary_t _get_script_signal_list(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_string_t _get_source_code(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _has_method(self, gd_string_name_t method):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _has_property_default_value(self, gd_string_name_t property):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _has_script_signal(self, gd_string_name_t signal):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _has_source_code(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _inherits_script(self, Script script):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef void* _instance_create(self, gd_object_t for_object):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _instance_has(self, gd_object_t object):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _is_placeholder_fallback_enabled(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _is_tool(self):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef gd_bool_t _is_valid(self):
    #     pass

    # @godot_extension_class_method  # virtual
    # cdef void _placeholder_erased(self, void* placeholder):
    #     pass

    # @godot_extension_class_method  # virtual const
    # cdef void* _placeholder_instance_create(self, gd_object_t for_object):
    #     pass

    # @godot_extension_class_method  # virtual
    # cdef Error _reload(self, gd_bool_t keep_state):
    #     pass

    # @godot_extension_class_method  # virtual
    # cdef void _set_source_code(self, gd_string_t code):
    #     pass

    @godot_extension_class_method  # virtual
    cdef void _update_exports(self):
        pass
