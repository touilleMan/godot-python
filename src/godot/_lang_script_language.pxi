from .classes cimport ScriptLanguageExtensionProfilingInfo


debug_spy = True
cdef spy_log(msg: str):
    if debug_spy:
        print(f"[DEBUG] {msg}", flush=True)


# godot_extension: class(parent="ScriptLanguageExtension")
@cython.final
cdef class PythonScriptLanguage:
    cdef gd_object_t _gd_ptr

    # godot_extension: method(virtual=True)
    cdef inline void _add_global_constant(self, gd_string_name_t name, gd_variant_t value):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_add_global_constant(name={gdapi.gd_string_name_to_pystr(&name)!r}, value={value!r})")
        gd_string_name_del(&name)
        gd_variant_del(&value)

    # godot_extension: method(virtual=True)
    cdef inline void _add_named_global_constant(self, gd_string_name_t name, gd_variant_t value):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_add_named_global_constant(name={gdapi.gd_string_name_to_pystr(&name)!r}, value={value!r})")
        gd_string_name_del(&name)
        gd_variant_del(&value)

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _auto_indent_code(self, gd_string_t code, gd_int_t from_line, gd_int_t to_line):
        spy_log(f"CALLED PythonScriptLanguage::_auto_indent_code(code={gdapi.gd_string_to_pystr(&code)!r}, from_line={from_line}, to_line={to_line})")
        # For now, just return the code as-is since proper Python auto-indentation
        # would require a full Python parser. This could be enhanced later.
        return code

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _can_inherit_from_file(self):
        spy_log(f"CALLED PythonScriptLanguage::_can_inherit_from_file()")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _can_make_function(self):
        spy_log(f"CALLED PythonScriptLanguage::_can_make_function()")
        return True

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_dictionary_t _complete_code(self, gd_string_t code, gd_string_t path, gd_object_t owner):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_complete_code(code={gdapi.gd_string_to_pystr(&code)!r}, path={gdapi.gd_string_to_pystr(&path)!r}, owner=<object 0x{<size_t>owner:x}>)")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_del(&code)
        gd_string_del(&path)
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_object_t _create_script(self):
        spy_log(f"CALLED PythonScriptLanguage::_create_script()")
        cdef PythonScript script = PythonScript()
        return script._gd_ptr

    # godot_extension: method(virtual=True)
    cdef inline gd_array_t _debug_get_current_stack_info(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_current_stack_info()")
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _debug_get_error(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_error()")
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True)
    cdef inline gd_dictionary_t _debug_get_globals(self, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_globals(max_subitems={max_subitems}, max_depth={max_depth})")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_int_t _debug_get_stack_level_count(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_count()")
        return 0

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _debug_get_stack_level_function(self, gd_int_t level):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_function(level={level})")
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True)
    cdef inline void* _debug_get_stack_level_instance(self, gd_int_t level):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_instance(level={level})")
        return NULL

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_int_t _debug_get_stack_level_line(self, gd_int_t level):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_line(level={level})")
        return 0

    # godot_extension: method(virtual=True)
    cdef inline gd_dictionary_t _debug_get_stack_level_locals(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_locals(level={level}, max_subitems={max_subitems}, max_depth={max_depth})")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True)
    cdef inline gd_dictionary_t _debug_get_stack_level_members(self, gd_int_t level, gd_int_t max_subitems, gd_int_t max_depth):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_members(level={level}, max_subitems={max_subitems}, max_depth={max_depth})")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _debug_get_stack_level_source(self, gd_int_t level):
        spy_log(f"CALLED PythonScriptLanguage::_debug_get_stack_level_source(level={level})")
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True)
    cdef inline gd_string_t _debug_parse_stack_level_expression(self, gd_int_t level, gd_string_t expression, gd_int_t max_subitems, gd_int_t max_depth):
        spy_log(f"CALLED PythonScriptLanguage::_debug_parse_stack_level_expression(level={level}, expression={gdapi.gd_string_to_pystr(&expression)!r}, max_subitems={max_subitems}, max_depth={max_depth})")
        gd_string_del(&expression)
        return gd_string_from_pybytes(b"")

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_int_t _find_function(self, gd_string_t function, gd_string_t code):
        spy_log(f"CALLED PythonScriptLanguage::_find_function(function={gdapi.gd_string_to_pystr(&function)!r}, code={gdapi.gd_string_to_pystr(&code)!r})")
        cdef object py_function = gdapi.gd_string_to_pystr(&function)
        cdef object py_code = gdapi.gd_string_to_pystr(&code)
        gd_string_del(&function)
        gd_string_del(&code)

        # Simple search for function definition
        try:
            lines = py_code.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith(f'def {py_function}('):
                    return i
        except:
            pass

        return -1

    # godot_extension: method(virtual=True)
    cdef inline void _finish(self):
        spy_log(f"CALLED PythonScriptLanguage::_finish()")
        # Clean up any Python script language resources
        # This is where we could clean up global Python environment

    # godot_extension: method(virtual=True)
    cdef inline void _frame(self):
        # This function is a noop, but must still be provided since Godot calls
        # it for every frame no matter what
        # spy_log(f"CALLED PythonScriptLanguage::_frame()")
        pass

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_array_t _get_built_in_templates(self, gd_string_name_t object):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::(object={gdapi.gd_string_name_to_pystr(&object)!r})")
        gd_string_name_del(&object)
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_packed_string_array_t _get_comment_delimiters(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_comment_delimiters()")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"#"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_meth_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_packed_string_array_t _get_doc_comment_delimiters(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_doc_comment_delimiters()")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"##"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_meth_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _get_extension(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_extension()")
        return gd_string_from_pybytes(b"py")

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_dictionary_t _get_global_class_name(self, gd_string_t path):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_get_global(path={gdapi.gd_string_to_pystr(&path)!r})")
        gd_string_del(&path)
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _get_name(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_name()")
        return gd_string_from_pybytes(b"Python")

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_array_t _get_public_annotations(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_get_public_constants()")
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_dictionary_t _get_public_constants(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_get_public_constants()")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_array_t _get_public_functions(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::()")
        cdef gd_array_t ret = gd_array_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_packed_string_array_t _get_recognized_extensions(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_recognized_extensions()")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"py", b"pyc", b"pyo", b"pyd", b"pyi", b"pyx", b"pxd", b"pxi"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_meth_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_packed_string_array_t _get_reserved_words(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_reserved_words()")
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
            gd_packed_string_array_meth_append(&words, &word)
            gd_string_del(&word)

        return words

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_packed_string_array_t _get_string_delimiters(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_string_delimiters()")
        cdef gd_packed_string_array_t extensions = gd_packed_string_array_new()
        cdef gd_string_t extension

        for py_extension in (b"' '", b'" "', b'""" """', b"''' '''"):
            extension = gd_string_from_pybytes(py_extension)
            gd_packed_string_array_meth_append(&extensions, &extension)
            gd_string_del(&extension)

        return extensions

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _get_type(self):
        spy_log(f"CALLED PythonScriptLanguage::_get_type()")
        return gd_string_from_pybytes(b"Python")

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _handles_global_class_type(self, gd_string_t type):
        spy_log(f"CALLED PythonScriptLanguage::_handles_global_class_type(type={gdapi.gd_string_to_pystr(&type)!r})")
        # TODO: would be more efficient to precompute the type into a `gd_string_t`
        cdef gd_bool_t result = gdapi.gd_string_to_pystr(&type) == "Python"
        gd_string_del(&type)
        return result

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _has_named_classes(self):
        spy_log(f"CALLED PythonScriptLanguage::_has_named_classes()")
        return True

    # godot_extension: method(virtual=True)
    cdef inline void _init(self):
        spy_log(f"CALLED PythonScriptLanguage::_init()")
        # Initialize the Python script language
        # This is where we could set up any global Python environment needed

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _is_control_flow_keyword(self, gd_string_t keyword):
        spy_log(f"CALLED PythonScriptLanguage::_is_control_flow_keyword(keyword={gdapi.gd_string_to_pystr(&keyword)!r})")
        # TODO: use `string_operator_index_const` here !
        # This method seems to only be called right after `_get_reserved_words`
        # TODO: would be more efficient to precompute the keywords into a `gd_packed_string_array_t`
        cdef gd_bool_t result = gdapi.gd_string_to_pystr(&keyword) in (
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
    cdef inline gd_bool_t _is_using_templates(self):
        spy_log(f"CALLED PythonScriptLanguage::_is_using_templates()")
        return True

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_dictionary_t _lookup_code(self, gd_string_t code, gd_string_t symbol, gd_string_t path, gd_object_t owner):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_lookup_code(code={gdapi.gd_string_to_pystr(&code)!r}, symbol={gdapi.gd_string_to_pystr(&symbol)!r}, path={gdapi.gd_string_to_pystr(&path)!r}, owner=<object 0x{<size_t>owner:x}>)")
        gd_string_del(&code)
        gd_string_del(&symbol)
        gd_string_del(&path)
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        cdef gd_dictionary_t ret = gd_dictionary_new()
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _make_function(self, gd_string_t class_name, gd_string_t function_name, gd_packed_string_array_t function_args):
        spy_log(f"CALLED PythonScriptLanguage::_make_function(class_name={gdapi.gd_string_to_pystr(&class_name)!r}, function_name={gdapi.gd_string_to_pystr(&function_name)!r}, function_args={function_args!r})")
        cdef object py_class_name = gdapi.gd_string_to_pystr(&class_name)
        cdef object py_function_name = gdapi.gd_string_to_pystr(&function_name)
        gd_string_del(&class_name)
        gd_string_del(&function_name)

        # Convert function arguments
        cdef object args = []
        cdef gd_int_t arg_count = gd_packed_string_array_meth_size(&function_args)
        cdef gd_string_t arg_str
        cdef gd_int_t i
        for i in range(arg_count):
            arg_str = gd_packed_string_array_indexed_getter(&function_args, i)
            args.append(gdapi.gd_string_to_pystr(&arg_str))
            gd_string_del(&arg_str)
        gd_packed_string_array_del(&function_args)

        # Create function signature
        cdef object arg_list = ', '.join(['self'] + args) if args else 'self'
        cdef object function_template = f"\ndef {py_function_name}({arg_list}):\n    pass\n"

        return gd_string_from_unchecked_pystr(function_template)

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_object_t _make_template(self, gd_string_t template, gd_string_t class_name, gd_string_t base_class_name):
        spy_log(f"CALLED PythonScriptLanguage::_make_template(template={gdapi.gd_string_to_pystr(&template)!r}, class_name={gdapi.gd_string_to_pystr(&class_name)!r}, base_class_name={gdapi.gd_string_to_pystr(&base_class_name)!r})")
        cdef object py_template = gdapi.gd_string_to_pystr(&template)
        cdef object py_class_name = gdapi.gd_string_to_pystr(&class_name)
        cdef object py_base_class_name = gdapi.gd_string_to_pystr(&base_class_name)
        gd_string_del(&template)
        gd_string_del(&class_name)
        gd_string_del(&base_class_name)

        # Create a basic Python script template
        cdef object source_template = f'''extends {py_base_class_name}
# {py_class_name}

class {py_class_name}({py_base_class_name}):
    def _init(self):
        pass

    def _ready(self):
        pass
'''

        # Create a new PythonScript with the template
        cdef PythonScript script = PythonScript()
        cdef gd_string_t gd_source = gd_string_from_unchecked_pystr(source_template)
        script._set_source_code(gd_source)
        gd_string_del(&gd_source)

        return script._gd_ptr

    # godot_extension: method(virtual=True)
    cdef inline gd_int_t _open_in_external_editor(self, gd_object_t script, gd_int_t line, gd_int_t column):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_open_in_external_editor(script=<object 0x{<size_t>script:x}>, line={line}, column={column})")
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)
        return Error.ERR_UNAVAILABLE

    # godot_extension: method(virtual=True)
    cdef inline gd_bool_t _overrides_external_editor(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_overrides_external_editor()")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_int_t _preferred_file_name_casing(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_preferred_file_name_casing()")
        # Returns a `ScriptLanguage.ScriptNameCasing` enum
        return 0

    # godot_extension: method(virtual=True)
    cdef inline gd_int_t _profiling_get_accumulated_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_profiling_get_accumulated_data(info_array=<opaque ptr>, info_max={info_max})")
        return 0

    # godot_extension: method(virtual=True)
    cdef inline gd_int_t _profiling_get_frame_data(self, ScriptLanguageExtensionProfilingInfo* info_array, gd_int_t info_max):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_profiling_get_frame_data(info_array=<opaque ptr>, info_max={info_max})")
        return 0

    # godot_extension: method(virtual=True)
    cdef inline void _profiling_set_save_native_calls(self, gd_bool_t enable):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_profiling_set_save_native_calls(enable={enable})")

    # godot_extension: method(virtual=True)
    cdef inline void _profiling_start(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_profiling_start()")

    # godot_extension: method(virtual=True)
    cdef inline void _profiling_stop(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_profiling_stop()")

    # godot_extension: method(virtual=True)
    cdef inline void _reload_all_scripts(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_reload_all_scripts()")

    # godot_extension: method(virtual=True)
    cdef inline void _reload_scripts(self, gd_array_t scripts, gd_bool_t soft_reload):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_reload_scripts(scripts={scripts!r}, soft_reload={soft_reload})")
        gd_array_del(&scripts)

    # godot_extension: method(virtual=True)
    cdef inline void _reload_tool_script(self, gd_object_t script, gd_bool_t soft_reload):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_reload_tool_script(script=<object 0x{<size_t>script:x}>, soft_reload={soft_reload})")
        # `gd_object_t` doesn't need to be be deleted (is it just a raw pointer)

    # godot_extension: method(virtual=True)
    cdef inline void _remove_named_global_constant(self, gd_string_name_t name):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_remove_named_global_constant(name={gdapi.gd_string_name_to_pystr(&name)!r})")
        gd_string_name_del(&name)

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _supports_builtin_mode(self):
        spy_log(f"CALLED PythonScriptLanguage::_supports_builtin_mode()")
        return False

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_bool_t _supports_documentation(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_supports_documentation()")
        return False

    # godot_extension: method(virtual=True)
    cdef inline void _thread_enter(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_thread_enter()")

    # godot_extension: method(virtual=True)
    cdef inline void _thread_exit(self):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_thread_exit()")

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_dictionary_t _validate(self, gd_string_t script, gd_string_t path, gd_bool_t validate_functions, gd_bool_t validate_errors, gd_bool_t validate_warnings, gd_bool_t validate_safe_lines):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_validate(script={gdapi.gd_string_to_pystr(&script)!r}, path={gdapi.gd_string_to_pystr(&path)!r}, validate_functions={validate_functions}, validate_errors={validate_errors}, validate_warnings={validate_warnings}, validate_safe_lines={validate_safe_lines})")
        cdef gd_dictionary_t ret = gd_dictionary_new()
        gd_string_del(&script)
        gd_string_del(&path)
        return ret

    # godot_extension: method(virtual=True, const=True)
    cdef inline gd_string_t _validate_path(self, gd_string_t path):
        # TODO
        spy_log(f"CALLED PythonScriptLanguage::_validate_path(path={gdapi.gd_string_to_pystr(&path)!r})")
        cdef gd_string_t ret = gd_string_from_pybytes(b"")
        gd_string_del(&path)
        return ret

    # godot_extension: generate_class_code()

# godot_extension: generate_module_code()
