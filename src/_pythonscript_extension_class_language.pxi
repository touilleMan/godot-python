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
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_del(&script)
        gd_string_del(&path)
        return ret

    # godot_extension: method(const=True)
    cdef gd_string_t _validate_path(self, gd_string_t path):
        # TODO
        cdef gd_string_t ret = gd_string_from_pybytes(b"")
        gd_string_del(&path)
        return ret

    # godot_extension: method(const=True)
    cdef gd_string_t _auto_indent_code(self, gd_string_t code, gd_int_t from_line, gd_int_t to_line):
        # TODO
        cdef gd_string_t ret = gd_string_from_pybytes(b"")
        gd_string_del(&code)
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _complete_code(self, gd_string_t code, gd_string_t path, gd_object_t owner):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_del(&code)
        gd_string_del(&path)
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return ret

    # godot_extension: method(const=True)
    cdef gd_int_t _find_function(self, gd_string_t class_name, gd_string_t function_name):
        # TODO
        gd_string_del(&class_name)
        gd_string_del(&function_name)
        return -1

    # godot_extension: method()
    cdef gd_int_t _open_in_external_editor(self, gd_object_t script, gd_int_t line, gd_int_t column):
        # TODO
        return Error.ERR_UNAVAILABLE

    # godot_extension: method(const=True)
    cdef gd_string_t _make_function(self, gd_string_t class_name, gd_string_t function_name, gd_packed_string_array_t function_args):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_object_t _make_template(self, gd_string_t template, gd_string_t class_name, gd_string_t base_class_name):
        # TODO
        # Returns String
        pass

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _lookup_code(self, gd_string_t code, gd_string_t symbol, gd_string_t path, gd_object_t owner):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_bool_t _overrides_external_editor(self):
        # TODO
        pass

    # debug

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_current_stack_info(self):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _debug_get_error(self):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_globals(self, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _debug_get_stack_level_count(self):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_string_t _debug_get_stack_level_function(self, gd_int_t level):
        # TODO
        pass

    # godot_extension: method()
    cdef void* _debug_get_stack_level_instance(self, gd_int_t level):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_int_t _debug_get_stack_level_line(self, gd_int_t level):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_stack_level_locals(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_dictionary_t _debug_get_stack_level_members(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_string_t _debug_parse_stack_level_expression(self, gd_int_t level, gd_string_t expression, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        pass

    # profiling

    # godot_extension: method()
    cdef gd_int_t _profiling_get_accumulated_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_int_t _profiling_get_frame_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        # TODO
        pass

    # godot_extension: method()
    cdef void _profiling_start(self):
        # TODO
        pass

    # godot_extension: method()
    cdef void _profiling_stop(self):
        # TODO
        pass

    # spec

    # godot_extension: method(const=True)
    cdef gd_bool_t _can_inherit_from_file(self):
        return False

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_comment_delimiters(self):
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"#"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_doc_comment_delimiters(self):
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"##"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(const=True)
    cdef gd_string_t _get_extension(self):
        return gd_string_from_pybytes(b"py")

    # godot_extension: method(const=True)
    cdef gd_string_t _get_name(self):
        return gd_string_from_pybytes(b"Python")

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_recognized_extensions(self):
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"py", b"pyc", b"pyo", b"pyd", b"pyi", b"pyx", b"pxd", b"pxi"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_reserved_words(self):
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

    # godot_extension: method(const=True)
    cdef gd_packed_string_array_t _get_string_delimiters(self):
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"' '", b'" "', b'""" """', b"''' '''"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(const=True)
    cdef gd_string_t _get_type(self):
        return gd_string_from_pybytes(b"Python")

    # godot_extension: method(const=True)
    cdef gd_bool_t _has_named_classes(self):
        return True

    # godot_extension: method(const=True)
    cdef gd_bool_t _is_control_flow_keyword(self, gd_string_t keyword):
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

    # godot_extension: method()
    cdef gd_bool_t _is_using_templates(self):
        return True

    # godot_extension: method(const=True)
    cdef gd_bool_t _supports_builtin_mode(self):
        return False

    # godot_extension: method(const=True)
    cdef gd_bool_t _supports_documentation(self):
        # TODO: support documentation
        return False

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_built_in_templates(self, gd_string_name_t object):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_name_del(&object)
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_global_class_name(self, gd_string_t path):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_public_annotations(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_public_constants(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(const=True)
    cdef gd_dictionary_t _get_public_functions(self):
        # TODO
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # runtime

    # godot_extension: method()
    cdef void _add_global_constant(self, gd_string_name_t name, gd_variant_t value):
        # TODO
        gd_string_name_del(&name)
        gd_variant_del(&value)

    # godot_extension: method()
    cdef void _add_named_global_constant(self, gd_string_name_t name, gd_variant_t value):
        # TODO
        gd_string_name_del(&name)
        gd_variant_del(&value)

    # godot_extension: method()
    cdef void _remove_named_global_constant(self, gd_string_name_t name):
        # TODO
        gd_string_name_del(&name)

    # godot_extension: method()
    cdef void _init(self):
        # TODO
        pass

    # godot_extension: method()
    cdef void _finish(self):
        # TODO
        pass

    # godot_extension: method()
    cdef void _frame(self):
        # TODO
        pass

    # godot_extension: method()
    cdef void* _alloc_instance_binding_data(self, gd_object_t obj):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        pass

    # godot_extension: method()
    cdef void _free_instance_binding_data(self, void* data):
        # TODO
        pass

    # godot_extension: method()
    cdef gd_bool_t _refcount_decremented_instance_binding(self, gd_object_t obj):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        pass

    # godot_extension: method()
    cdef void _refcount_incremented_instance_binding(self, gd_object_t obj):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        pass

    # godot_extension: method()
    cdef void _thread_enter(self):
        # TODO
        pass

    # godot_extension: method()
    cdef void _thread_exit(self):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_object_t _create_script(self):
        # TODO
        pass

    # godot_extension: method(const=True)
    cdef gd_bool_t _handles_global_class_type(self, gd_string_t type):
        # TODO: would be more efficient to precompute the type into a `gd_string_t`
        cdef gd_bool_t result = gd_string_to_pystr(&type) == "Python"
        gd_string_del(&type)
        return result

    # godot_extension: method()
    cdef gd_int_t _execute_file(self, gd_string_t path):
        # TODO
        gd_string_del(&path)
        return Error.FAILED

    # godot_extension: method()
    cdef void _reload_all_scripts(self):
        # TODO
        pass

    # godot_extension: method()
    cdef void _reload_tool_script(self, gd_object_t script, gd_bool_t soft_reload):
        # TODO
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        pass
