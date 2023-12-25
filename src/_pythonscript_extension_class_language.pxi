from godot.classes cimport ScriptLanguageExtensionProfilingInfo


cdef StringName gdname_scriptlanguageextension = StringName("ScriptLanguageExtension")
cdef StringName gdname_pythonscriptlanguage = StringName("PythonScriptLanguage")

# godot_extension: class(parent="ScriptLanguageExtension")
@cython.final
cdef class PythonScriptLanguage:
    cdef gd_object_t _gd_ptr

    def __cinit__(self):
        self._gd_ptr = pythonscript_gdextension.classdb_construct_object(&gdname_scriptlanguageextension._gd_data)
        pythonscript_gdextension.object_set_instance(self._gd_ptr, &gdname_pythonscriptlanguage._gd_data, <PyObject*>self)

    # godot_extension: generate_code()

    # editor

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _validate(self, gd_string_t script, gd_string_t path, gd_bool_t validate_functions, gd_bool_t validate_errors, gd_bool_t validate_warnings, gd_bool_t validate_safe_lines):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _validate_path(self, gd_string_t path):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _auto_indent_code(self, gd_string_t code, gd_int_t from_line, gd_int_t to_line):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _complete_code(self, gd_string_t code, gd_string_t path, gd_object_t owner):
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _find_function(self, gd_string_t class_name, gd_string_t function_name):
        pass

    # godot_extension: method()
    cdef gd_int_t _open_in_external_editor(self, gd_object_t script, gd_int_t line, gd_int_t column):
        # Returns Error
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _make_function(self, gd_string_t class_name, gd_string_t function_name, gd_packed_string_array_t function_args):
        pass

    # godot_extension: method(const=True)
    cdef gd_object_t _make_template(self, gd_string_t template, gd_string_t class_name, gd_string_t base_class_name):
        # Returns String
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _lookup_code(self, gd_string_t code, gd_string_t symbol, gd_string_t path, gd_object_t owner):
        pass

    # godot_extension: method()
    cdef gd_bool_t _overrides_external_editor(self):
        pass

    # debug

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_current_stack_info(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _debug_get_error(self):
        pass

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_globals(self, gd_int_t max_subitems, gd_int_t max_depth):
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _debug_get_stack_level_count(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _debug_get_stack_level_function(self, gd_int_t level):
        pass

    # godot_extension: method()
    cdef void* _debug_get_stack_level_instance(self, gd_int_t level):
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _debug_get_stack_level_line(self, gd_int_t level):
        pass

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_stack_level_locals(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        pass

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_stack_level_members(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        pass

    # godot_extension: method()
    cdef gd_string_t _debug_parse_stack_level_expression(self, gd_int_t level, gd_string_t expression, gd_int_t max_subitems, gd_int_t max_depth):
        pass

    # profiling

    # godot_extension: method()
    cdef gd_int_t _profiling_get_accumulated_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        pass

    # godot_extension: method()
    cdef gd_int_t _profiling_get_frame_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        pass

    # godot_extension: method()
    cdef void _profiling_start(self):
        pass

    # godot_extension: method()
    cdef void _profiling_stop(self):
        pass

    # spec

    # godot_extension: method(const=True)
    cdef gd_bool_t _can_inherit_from_file(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_comment_delimiters(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _get_extension(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _get_name(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_reserved_words(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_string_delimiters(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _get_type(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_named_classes(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_control_flow_keyword(self, gd_string_t keyword):
        pass

    # godot_extension: method()
    cdef gd_bool_t _is_using_templates(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _supports_builtin_mode(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _supports_documentation(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_built_in_templates(self, gd_string_name_t object):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_global_class_name(self, gd_string_t path):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_public_annotations(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_public_constants(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_public_functions(self):
        pass

    # runtime

    # godot_extension: method()
    cdef void _add_global_constant(self, gd_string_name_t name, gd_variant_t value):
        pass

    # godot_extension: method()
    cdef void _add_named_global_constant(self, gd_string_name_t name, gd_variant_t value):
        pass

    # godot_extension: method()
    cdef void _remove_named_global_constant(self, gd_string_name_t name):
        pass

    # godot_extension: method()
    cdef void _init(self):
        pass

    # godot_extension: method()
    cdef void _finish(self):
        pass

    # godot_extension: method()
    cdef void _frame(self):
        pass

    # godot_extension: method()
    cdef void* _alloc_instance_binding_data(self, gd_object_t obj):
        pass

    # godot_extension: method()
    cdef void _free_instance_binding_data(self, void* data):
        pass

    # godot_extension: method()
    cdef gd_bool_t _refcount_decremented_instance_binding(self, gd_object_t obj):
        pass

    # godot_extension: method()
    cdef void _refcount_incremented_instance_binding(self, gd_object_t obj):
        pass

    # godot_extension: method()
    cdef void _thread_enter(self):
        pass

    # godot_extension: method()
    cdef void _thread_exit(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_object_t _create_script(self):
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _handles_global_class_type(self, gd_string_t type):
        pass

    # godot_extension: method()
    cdef gd_int_t _execute_file(self, gd_string_t path):
        # Returns Error
        pass

    # godot_extension: method()
    cdef void _reload_all_scripts(self):
        pass

    # godot_extension: method()
    cdef void _reload_tool_script(self, gd_object_t script, gd_bool_t soft_reload):
        pass
