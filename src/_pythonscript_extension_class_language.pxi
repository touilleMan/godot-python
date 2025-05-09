from godot.classes cimport ScriptLanguageExtensionProfilingInfo


cdef gd_string_name_t gdname_scriptlanguageextension
cdef gd_string_name_t gdname_pythonscriptlanguage


debug_spy = True
cdef spy_log(msg: str):
    if debug_spy:
        print(msg, flush=True)


# godot_extension: class(parent="ScriptLanguageExtension")
@cython.final
cdef class PythonScriptLanguage:
    cdef gd_object_t _gd_ptr

    def __cinit__(self):
        self._gd_ptr = pythonscript_gdextension.classdb_construct_object(&gdname_scriptlanguageextension)
        pythonscript_gdextension.object_set_instance(self._gd_ptr, &gdname_pythonscriptlanguage, <PyObject*>self)

    # godot_extension: register_class_hook()
    @staticmethod
    cdef inline void _register_class_hook():
        global gdname_scriptlanguageextension, gdname_pythonscriptlanguage
        gdname_scriptlanguageextension = gd_string_name_from_unchecked_pystr("ScriptLanguageExtension")
        gdname_pythonscriptlanguage = gd_string_name_from_unchecked_pystr("PythonScriptLanguage")

    # godot_extension: unregister_class_hook()
    @staticmethod
    cdef inline void _unregister_class_hook():
        global gdname_scriptlanguageextension, gdname_pythonscriptlanguage
        gd_string_name_del(&gdname_scriptlanguageextension)
        gd_string_name_del(&gdname_pythonscriptlanguage)

    # godot_extension: generate_code()

    # godot_extension: method(virtual=True)
    cdef void _add_global_constant(self, gd_string_name_t name, gd_variant_t value):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_add_global_constant")
        gd_string_name_del(&name)
        gd_variant_del(&value)

    # godot_extension: method(virtual=True)
    cdef void _add_named_global_constant(self, gd_string_name_t name, gd_variant_t value):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_add_named_global_constant")
        gd_string_name_del(&name)
        gd_variant_del(&value)

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _auto_indent_code(self, gd_string_t code, gd_int_t from_line, gd_int_t to_line):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_auto_indent_code")
        return code

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _can_inherit_from_file(self):
        spy_log("CALLED PythonScriptLanguage::_can_inherit_from_file")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _can_make_function(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_can_make_function")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _complete_code(self, gd_string_t code, gd_string_t path, gd_object_t owner):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_complete_code")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_del(&code)
        gd_string_del(&path)
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_object_t _create_script(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_create_script")

    # godot_extension: method(virtual=True)
    cdef gd_array_t _debug_get_current_stack_info(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_current_stack_info")
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _debug_get_error(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_error")
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True)
    cdef gd_dictionary_t _debug_get_globals(self, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_globals")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _debug_get_stack_level_count(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_count")
        return 0

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _debug_get_stack_level_function(self, gd_int_t level):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_function")
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True)
    cdef void* _debug_get_stack_level_instance(self, gd_int_t level):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_instance")
        return NULL

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _debug_get_stack_level_line(self, gd_int_t level):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_line")
        return 0

    # godot_extension: method(virtual=True)
    cdef gd_dictionary_t _debug_get_stack_level_locals(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_locals")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True)
    cdef gd_dictionary_t _debug_get_stack_level_members(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_members")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _debug_get_stack_level_source(self, gd_int_t level):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_get_stack_level_source")

    # godot_extension: method(virtual=True)
    cdef gd_string_t _debug_parse_stack_level_expression(self, gd_int_t level, gd_string_t expression, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_debug_parse_stack_level_expression")
        gd_string_del(&expression)
        gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _find_function(self, gd_string_t function, gd_string_t code):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_find_function")
        gd_string_del(&function)
        return -1

    # godot_extension: method(virtual=True)
    cdef void _finish(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_finish")

    # godot_extension: method(virtual=True)
    cdef void _frame(self):
        # TODO
        # spy_log("CALLED PythonScriptLanguage::_frame")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef gd_array_t _get_built_in_templates(self, gd_string_name_t object):
        # TODO
        spy_log("CALLED PythonScriptLanguage::")
        gd_string_name_del(&object)
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_comment_delimiters(self):
        spy_log("CALLED PythonScriptLanguage::_get_comment_delimiters")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"#"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_doc_comment_delimiters(self):
        spy_log("CALLED PythonScriptLanguage::_get_doc_comment_delimiters")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"##"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_extension(self):
        spy_log("CALLED PythonScriptLanguage::_get_extension")
        return gd_string_from_pybytes(b"py")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_global_class_name(self, gd_string_t path):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_get_global")
        gd_string_del(&path)
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_name(self):
        spy_log("CALLED PythonScriptLanguage::_get_name")
        return gd_string_from_pybytes(b"Python")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_array_t _get_public_annotations(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_get_public_constants")
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _get_public_constants(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_get_public_constants")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_array_t _get_public_functions(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::")
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        spy_log("CALLED PythonScriptLanguage::_get_recognized_extensions")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"py", b"pyc", b"pyo", b"pyd", b"pyi", b"pyx", b"pxd", b"pxi"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_reserved_words(self):
        spy_log("CALLED PythonScriptLanguage::_get_reserved_words")
        cdef gd_packed_string_array_t words = gd_packed_string_array_new()
        cdef gd_string_t word

        for py_word in (
            b"False",
            b"None",
            b"True",
            b"and",
            b"as",
            b"assert",
            b"break",
            b"class",
            b"continue",
            b"def",
            b"del",
            b"elif",
            b"else",
            b"except",
            b"finally",
            b"for",
            b"from",
            b"global",
            b"if",
            b"import",
            b"in",
            b"is",
            b"lambda",
            b"nonlocal",
            b"not",
            b"or",
            b"pass",
            b"raise",
            b"return",
            b"try",
            b"while",
            b"with",
            b"yield",
        ):
            word = gd_string_from_pybytes(py_word)
            gd_packed_string_array_append(&words, &word)
            gd_string_del(&word)

        return words

    # godot_extension: method(virtual=True, const=True)
    cdef gd_packed_string_array_t _get_string_delimiters(self):
        spy_log("CALLED PythonScriptLanguage::_get_string_delimiters")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"' '", b'" "', b'""" """', b"''' '''"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _get_type(self):
        spy_log("CALLED PythonScriptLanguage::_get_type")
        return gd_string_from_pybytes(b"Python")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _handles_global_class_type(self, gd_string_t type):
        spy_log("CALLED PythonScriptLanguage::_handles_global_class_type")
        # TODO: would be more efficient to precompute the type into a `gd_string_t`
        cdef gd_bool_t result = gd_string_to_pystr(&type) == "Python"
        gd_string_del(&type)
        return result

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _has_named_classes(self):
        spy_log("CALLED PythonScriptLanguage::_has_named_classes")
        return True

    # godot_extension: method(virtual=True)
    cdef void _init(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_init")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _is_control_flow_keyword(self, gd_string_t keyword):
        spy_log("CALLED PythonScriptLanguage::_is_control_flow_keyword")
        # TODO: would be more efficient to precompute the keywords into a `gd_packed_string_array_t`
        cdef gd_bool_t result = gd_string_to_pystr(&keyword) in (
            "break",
            "continue",
            "elif",
            "else",
            "for",
            "if",
            "match",
            "pass",
            "return",
            "when",
            "while",
        )
        gd_string_del(&keyword)
        return result

    # godot_extension: method(virtual=True)
    cdef gd_bool_t _is_using_templates(self):
        spy_log("CALLED PythonScriptLanguage::_is_using_templates")
        return True

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _lookup_code(self, gd_string_t code, gd_string_t symbol, gd_string_t path, gd_object_t owner):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_lookup_code")
        gd_string_del(&code)
        gd_string_del(&symbol)
        gd_string_del(&path)
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _make_function(self, gd_string_t class_name, gd_string_t function_name, gd_packed_string_array_t function_args):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_make_function")
        gd_string_del(&class_name)
        gd_string_del(&function_name)
        gd_packed_string_array_del(&function_args)
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_object_t _make_template(self, gd_string_t template, gd_string_t class_name, gd_string_t base_class_name):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_make_template")
        gd_string_del(&template)
        gd_string_del(&class_name)
        gd_string_del(&base_class_name)

    # godot_extension: method(virtual=True)
    cdef gd_int_t _open_in_external_editor(self, gd_object_t script, gd_int_t line, gd_int_t column):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_open_in_external_editor")
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return Error.ERR_UNAVAILABLE

    # godot_extension: method(virtual=True)
    cdef gd_bool_t _overrides_external_editor(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_overrides_external_editor")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_int_t _preferred_file_name_casing(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_preferred_file_name_casing")
        # Returns a `ScriptLanguage.ScriptNameCasing` enum
        return 0

    # godot_extension: method(virtual=True)
    cdef gd_int_t _profiling_get_accumulated_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_profiling_get_accumulated_data")
        return 0

    # godot_extension: method(virtual=True)
    cdef gd_int_t _profiling_get_frame_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_profiling_get_frame_data")
        return 0

    # godot_extension: method(virtual=True)
    cdef void _profiling_set_save_native_calls(self, gd_bool_t enable):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_profiling_set_save_native_calls")

    # godot_extension: method(virtual=True)
    cdef void _profiling_start(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_profiling_start")

    # godot_extension: method(virtual=True)
    cdef void _profiling_stop(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_profiling_stop")

    # godot_extension: method(virtual=True)
    cdef void _reload_all_scripts(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_reload_all_scripts")

    # godot_extension: method(virtual=True)
    cdef void _reload_scripts(self, gd_array_t scripts, gd_bool_t soft_reload):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_reload_scripts")
        gd_array_del(&scripts)

    # godot_extension: method(virtual=True)
    cdef void _reload_tool_script(self, gd_object_t script, gd_bool_t soft_reload):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_reload_tool_script")
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)

    # godot_extension: method(virtual=True)
    cdef void _remove_named_global_constant(self, gd_string_name_t name):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_remove_named_global_constant")
        gd_string_name_del(&name)

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _supports_builtin_mode(self):
        spy_log("CALLED PythonScriptLanguage::_supports_builtin_mode")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef gd_bool_t _supports_documentation(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_supports_documentation")
        return False

    # godot_extension: method(virtual=True)
    cdef void _thread_enter(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_thread_enter")

    # godot_extension: method(virtual=True)
    cdef void _thread_exit(self):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_thread_exit")

    # godot_extension: method(virtual=True, const=True)
    cdef gd_dictionary_t _validate(self, gd_string_t script, gd_string_t path, gd_bool_t validate_functions, gd_bool_t validate_errors, gd_bool_t validate_warnings, gd_bool_t validate_safe_lines):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_validate")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_del(&script)
        gd_string_del(&path)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef gd_string_t _validate_path(self, gd_string_t path):
        # TODO
        spy_log("CALLED PythonScriptLanguage::_validate_path")
        cdef gd_string_t ret = gd_string_from_pybytes(b"")
        gd_string_del(&path)
        return ret
