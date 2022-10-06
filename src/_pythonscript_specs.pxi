# editor
#
# Dictionary _validate ( String script, String path, bool validate_functions, bool validate_errors, bool validate_warnings, bool validate_safe_lines ) virtual const
# String _validate_path ( String path ) virtual const
# String _auto_indent_code ( String code, int from_line, int to_line ) virtual const
# Dictionary _complete_code ( String code, String path, Object owner ) virtual const
# int _find_function ( String class_name, String function_name ) virtual const
# Error _open_in_external_editor ( Script script, int line, int column ) virtual
# String _make_function ( String class_name, String function_name, PackedStringArray function_args ) virtual const
# Script _make_template ( String template, String class_name, String base_class_name ) virtual const
# Dictionary _lookup_code ( String code, String symbol, String path, Object owner ) virtual const
# bool _overrides_external_editor ( ) virtual
#
# debug
#
# Dictionary _debug_get_current_stack_info ( ) virtual
# String _debug_get_error ( ) virtual const
# Dictionary _debug_get_globals ( int max_subitems, int max_depth ) virtual
# int _debug_get_stack_level_count ( ) virtual const
# String _debug_get_stack_level_function ( int level ) virtual const
# void* _debug_get_stack_level_instance ( int level ) virtual
# int _debug_get_stack_level_line ( int level ) virtual const
# Dictionary _debug_get_stack_level_locals ( int level, int max_subitems, int max_depth ) virtual
# Dictionary _debug_get_stack_level_members ( int level, int max_subitems, int max_depth ) virtual
# String _debug_parse_stack_level_expression ( int level, String expression, int max_subitems, int max_depth ) virtual
#
# profiling
#
# int _profiling_get_accumulated_data ( ScriptLanguageExtensionProfilingInfo* info_array, int info_max ) virtual
# int _profiling_get_frame_data ( ScriptLanguageExtensionProfilingInfo* info_array, int info_max ) virtual
# void _profiling_start ( ) virtual
# void _profiling_stop ( ) virtual
#
# spec
#
# bool _can_inherit_from_file ( ) virtual const
# PackedStringArray _get_comment_delimiters ( ) virtual const
# String _get_extension ( ) virtual const
# String _get_name ( ) virtual const
# PackedStringArray _get_recognized_extensions ( ) virtual const
# PackedStringArray _get_reserved_words ( ) virtual const
# PackedStringArray _get_string_delimiters ( ) virtual const
# String _get_type ( ) virtual const
# bool _has_named_classes ( ) virtual const
# bool _is_control_flow_keyword ( String keyword ) virtual const
# bool _is_using_templates ( ) virtual
# bool _supports_builtin_mode ( ) virtual const
# bool _supports_documentation ( ) virtual const
#
# Dictionary _get_built_in_templates ( StringName object ) virtual const
# Dictionary _get_global_class_name ( String path ) virtual const
# Dictionary _get_public_annotations ( ) virtual const
# Dictionary _get_public_constants ( ) virtual const
# Dictionary _get_public_functions ( ) virtual const
#
# runtime
#
# void _add_global_constant ( StringName name, Variant value ) virtual
# void _add_named_global_constant ( StringName name, Variant value ) virtual
# void _remove_named_global_constant ( StringName name ) virtual
#
# void _init ( ) virtual
# void _finish ( ) virtual
# void _frame ( ) virtual
#
# void* _alloc_instance_binding_data ( Object object ) virtual
# void _free_instance_binding_data ( void* data ) virtual
#
# bool _refcount_decremented_instance_binding ( Object object ) virtual
# void _refcount_incremented_instance_binding ( Object object ) virtual
# void _thread_enter ( ) virtual
# void _thread_exit ( ) virtual
#
# Object _create_script ( ) virtual const
# bool _handles_global_class_type ( String type ) virtual const
# Error _execute_file ( String path ) virtual
# void _reload_all_scripts ( ) virtual
# void _reload_tool_script ( Script script, bool soft_reload ) virtual


cdef bool _can_inherit_from_file():

cdef bool _has_named_classes():
    return True

cdef PackedStringArray _get_comment_delimiters():
    pass

cdef String _get_extension():
    return gd_string_to_pystr("py")

cdef PackedStringArray _get_recognized_extensions():
    pass

cdef String _get_name():
    return gd_string_to_pystr("Python")

cdef PackedStringArray _get_reserved_words():
    pass

cdef PackedStringArray _get_string_delimiters():
    pass

cdef String _get_type():
    pass

cdef bool _is_control_flow_keyword(String keyword):
    pass

cdef bool _is_using_templates():
    pass

cdef bool _supports_builtin_mode():
    pass

cdef bool _supports_documentation():
    pass
