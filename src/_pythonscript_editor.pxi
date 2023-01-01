from godot.hazmat.gdapi cimport *


cdef public void _pythonscript_get_reserved_words(
    void *method_userdata,
    GDExtensionClassInstancePtr p_instance,
    GDExtensionTypePtr *p_args,
    GDExtensionTypePtr r_ret
):
    # TODO: r_ret is already an initialized array, reuse it instead of recreate (and leak) it ?
    cdef gd_packed_string_array_t arr = gd_packed_string_array_new()
    cdef gd_string_t string
    cdef (char*)[33] keywords = [
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    ]
    for keyword in keywords:
        string = gd_string_from_utf8(keyword, keyword.len())
        gd_packed_string_array_append(&arr, &string)
        gd_string_del(&string)


cdef public void _pythonscript_get_recognized_extensions(
    void *method_userdata,
    GDExtensionClassInstancePtr p_instance,
    GDExtensionTypePtr *p_args,
    GDExtensionTypePtr r_ret
):
    # TODO: r_ret is already an initialized array, reuse it instead of recreate (and leak) it ?
    cdef gd_packed_string_array_t arr = gd_packed_string_array_new()
    cdef gd_string_t string
    cdef (char*)[3] keywords = [
        "pyi",
        "pyd",
        "py",
    ]
    for keyword in keywords:
        string = gd_string_from_utf8(keyword, keyword.len())
        gd_packed_string_array_append(&arr, &string)
        gd_string_del(&string)


cdef public void _pythonscript_get_string_delimiters(
    void *method_userdata,
    GDExtensionClassInstancePtr p_instance,
    GDExtensionTypePtr *p_args,
    GDExtensionTypePtr r_ret
):
    # TODO: r_ret is already an initialized array, reuse it instead of recreate (and leak) it ?
    cdef gd_packed_string_array_t arr = gd_packed_string_array_new()
    cdef gd_string_t string
    cdef (char*)[3] keywords = [
	    "\" \"",
	    "' '",
	    "\"\"\" \"\"\"",
    ]
    for keyword in keywords:
        string = gd_string_from_utf8(keyword, keyword.len())
        gd_packed_string_array_append(&arr, &string)
        gd_string_del(&string)


cdef _register_editor_methods():
    # TODO: fixme !
    pass

    # cdef GDExtensionClassMethodInfo info
    # pythonscript_gdstringname_new(&info.name, "_get_reserved_words")
    # info.method_userdata = NULL
    # info.call_func = NULL
    # # info.ptrcall_func = &_pythonscript_get_reserved_words
    # info.method_flags = GDEXTENSION_METHOD_FLAG_NORMAL | GDEXTENSION_METHOD_FLAG_EDITOR | GDEXTENSION_METHOD_FLAG_CONST
    # info.argument_count = 0
    # info.has_return_value = True
    # info.get_argument_type_func = NULL
    # info.get_argument_info_func = NULL
    # info.get_argument_metadata_func = NULL
    # info.default_argument_count = 0
    # info.default_arguments = NULL
    # pythonscript_gdextension.classdb_register_extension_class_method(
    #     pythonscript_gdextension_library,
    #     "PythonScriptLanguageExtension",
    #     &info,
    # )
    # pythonscript_gdstringname_delete(&info.name)

    # pythonscript_gdstringname_new(&info.name, "_get_recognized_extensions")
    # info.method_userdata = NULL
    # info.call_func = NULL
    # # info.ptrcall_func = &_pythonscript_get_recognized_extensions
    # info.method_flags = GDEXTENSION_METHOD_FLAG_NORMAL | GDEXTENSION_METHOD_FLAG_EDITOR | GDEXTENSION_METHOD_FLAG_CONST
    # info.argument_count = 0
    # info.has_return_value = True
    # info.get_argument_type_func = NULL
    # info.get_argument_info_func = NULL
    # info.get_argument_metadata_func = NULL
    # info.default_argument_count = 0
    # info.default_arguments = NULL
    # pythonscript_gdextension.classdb_register_extension_class_method(
    #     pythonscript_gdextension_library,
    #     "PythonScriptLanguageExtension",
    #     &info,
    # )
    # pythonscript_gdstringname_delete(&info.name)

    # pythonscript_gdstringname_new(&info.name, "_get_string_delimiters")
    # info.method_userdata = NULL
    # info.call_func = NULL
    # # info.ptrcall_func = &_pythonscript_get_string_delimiters
    # info.method_flags = GDEXTENSION_METHOD_FLAG_NORMAL | GDEXTENSION_METHOD_FLAG_EDITOR | GDEXTENSION_METHOD_FLAG_CONST
    # info.argument_count = 0
    # info.has_return_value = True
    # info.get_argument_type_func = NULL
    # info.get_argument_info_func = NULL
    # info.get_argument_metadata_func = NULL
    # info.default_argument_count = 0
    # info.default_arguments = NULL
    # pythonscript_gdextension.classdb_register_extension_class_method(
    #     pythonscript_gdextension_library,
    #     "PythonScriptLanguageExtension",
    #     &info,
    # )
    # pythonscript_gdstringname_delete(&info.name)
