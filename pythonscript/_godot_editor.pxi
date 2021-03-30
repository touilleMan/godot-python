# cython: c_string_type=unicode, c_string_encoding=utf8

from libc.stddef cimport wchar_t

from godot._hazmat.gdnative_api_struct cimport (
    godot_pluginscript_language_data,
    godot_string,
    godot_bool,
    godot_array,
    godot_pool_string_array,
    godot_object,
    godot_variant,
    godot_error,
    godot_dictionary
)
from godot._hazmat.gdapi cimport pythonscript_gdapi10 as gdapi10
from godot._hazmat.conversion cimport (
    godot_string_to_pyobj,
    pyobj_to_godot_string,
    godot_variant_to_pyobj,
)


cdef api godot_string pythonscript_get_template_source_code(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_class_name,
    const godot_string *p_base_class_name
) with gil:
    cdef str class_name
    if p_class_name == NULL:
        class_name = "MyExportedCls"
    else:
        class_name = godot_string_to_pyobj(p_class_name)
    cdef str base_class_name = godot_string_to_pyobj(p_base_class_name)
    cdef str src = f"""from godot import exposed, export
from godot import *


@exposed
class {class_name}({base_class_name}):

    # member variables here, example:
    a = export(int)
    b = export(str, default='foo')

    def _ready(self):
        \"\"\"
        Called every time the node is added to the scene.
        Initialization here.
        \"\"\"
        pass
"""
    cdef godot_string ret
    pyobj_to_godot_string(src, &ret)
    return ret


cdef api godot_bool pythonscript_validate(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_script,
    int *r_line_error,
    int *r_col_error,
    godot_string *r_test_error,
    const godot_string *p_path,
    godot_pool_string_array *r_functions
) with gil:
    return True


cdef api int pythonscript_find_function(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_function,
    const godot_string *p_code
) with gil:
    return 0


cdef api godot_string pythonscript_make_function(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_class,
    const godot_string *p_name,
    const godot_pool_string_array *p_args
) with gil:
    cdef str name = godot_string_to_pyobj(p_name)

    # TODO: replace this with PoolStringArray binding once implemented
    cdef int i
    cdef godot_string gdarg
    cdef list args_names = []
    for i in range(gdapi10.godot_pool_string_array_size(p_args)):
        gdarg = gdapi10.godot_pool_string_array_get(p_args, i)
        arg = godot_string_to_pyobj(&gdarg)
        gdapi10.godot_string_destroy(&gdarg)
        args_names.append(arg.split(":", 1)[0])

    cdef str src = """\
    def {name}(self, { ','.join(args_names) }):
        pass
"""
    cdef godot_string ret
    pyobj_to_godot_string(src, &ret)
    return ret


cdef api godot_error pythonscript_complete_code(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_code,
    const godot_string *p_base_path,
    godot_object *p_owner,
    godot_array *r_options,
    godot_bool *r_force,
    godot_string *r_call_hint
) with gil:
    return godot_error.GODOT_OK


cdef api void pythonscript_auto_indent_code(
    godot_pluginscript_language_data *p_data,
    godot_string *p_code,
    int p_from_line,
    int p_to_line
) with gil:
    # TODO: use black for this job
#     try:
#         import autopep8
#     except ImportError:
#         print(
#             "[Pythonscript] Auto indent requires module `autopep8`, "
#             "install it with `pip install autopep8`"
#         )
#     pycode = godot_string_to_pyobj(code).splitlines()
#     before = "\n".join(pycode[:from_line])
#     to_fix = "\n".join(pycode[from_line:to_line])
#     after = "\n".join(pycode[to_line:])
#     fixed = autopep8.fix_code(to_fix)
#     final_code = "\n".join((before, fixed, after))
#     # TODO: modify code instead of replace it when binding on godot_string
#     # operation is available
#     lib.godot_string_destroy(code)
#     lib.godot_string_new_unicode_data(code, final_code, len(final_code))
    pass


__global_constants = {}


cdef api void pythonscript_add_global_constant(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_variable,
    const godot_variant *p_value
) with gil:
    # However, Godot add global constants very early (first as an empty variant
    # placeholder before any script is loaded, then as a proper loaded script).
    # So it's possible this function get called before `pythonscript_script_init`
    # (which is supposed to do the lazy `_initialize_bindings`).
    _initialize_bindings()
    name = godot_string_to_pyobj(p_variable)
    value = godot_variant_to_pyobj(p_value)
    __global_constants[name] = value


cdef api godot_string pythonscript_debug_get_error(
    godot_pluginscript_language_data *p_data
) with gil:
    cdef godot_string ret
    pyobj_to_godot_string("Nothing", &ret)
    return ret


cdef api int pythonscript_debug_get_stack_level_count(
    godot_pluginscript_language_data *p_data
) with gil:
    return 1


cdef api int pythonscript_debug_get_stack_level_line(
    godot_pluginscript_language_data *p_data,
    int p_level
) with gil:
    return 1


cdef api godot_string pythonscript_debug_get_stack_level_function(
    godot_pluginscript_language_data *p_data,
    int p_level
) with gil:
    cdef godot_string ret
    pyobj_to_godot_string("Nothing", &ret)
    return ret


cdef api godot_string pythonscript_debug_get_stack_level_source(
    godot_pluginscript_language_data *p_data,
    int p_level
) with gil:
    cdef godot_string ret
    pyobj_to_godot_string("Nothing", &ret)
    return ret


cdef api void pythonscript_debug_get_stack_level_locals(
    godot_pluginscript_language_data *p_data,
    int p_level,
    godot_pool_string_array *p_locals,
    godot_array *p_values,
    int p_max_subitems,
    int p_max_depth
) with gil:
    pass


cdef api void pythonscript_debug_get_stack_level_members(
    godot_pluginscript_language_data *p_data,
    int p_level,
    godot_pool_string_array *p_members,
    godot_array *p_values,
    int p_max_subitems,
    int p_max_depth
) with gil:
    pass


cdef api void pythonscript_debug_get_globals(
    godot_pluginscript_language_data *p_data,
    godot_pool_string_array *p_locals,
    godot_array *p_values,
    int p_max_subitems,
    int p_max_depth
) with gil:
    pass


cdef api godot_string pythonscript_debug_parse_stack_level_expression(
    godot_pluginscript_language_data *p_data,
    int p_level,
    const godot_string *p_expression,
    int p_max_subitems,
    int p_max_depth
) with gil:
    cdef godot_string ret
    pyobj_to_godot_string("Nothing", &ret)
    return ret


cdef api void pythonscript_get_public_functions(
    godot_pluginscript_language_data *p_data,
    godot_array *r_functions
) with gil:
    pass


cdef api void pythonscript_get_public_constants(
    godot_pluginscript_language_data *p_data,
    godot_dictionary *r_constants
) with gil:
    pass
