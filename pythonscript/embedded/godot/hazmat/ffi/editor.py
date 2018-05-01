from pythonscriptcffi import ffi, lib

from godot.hazmat.tools import (
    godot_string_to_pyobj,
    godot_string_from_pyobj_for_ffi_return,
    variant_to_pyobj,
)
from godot.bindings import PoolStringArray
import godot.globals


@ffi.def_extern()
def pybind_get_template_source_code(handle, class_name, base_class_name):
    class_name = godot_string_to_pyobj(class_name) or "MyExportedCls"
    base_class_name = godot_string_to_pyobj(base_class_name)
    src = """from godot import exposed, export
from godot.bindings import *
from godot.globals import *


@exposed
class %s(%s):

    # member variables here, example:
    a = export(int)
    b = export(str, default='foo')

    def _ready(self):
        \"\"\"
        Called every time the node is added to the scene.
        Initialization here.
        \"\"\"
        pass
""" % (
        class_name, base_class_name
    )
    return godot_string_from_pyobj_for_ffi_return(src)[0]


@ffi.def_extern()
def pybind_validate(
    handle, script, r_line_error, r_col_error, test_error, path, r_functions
):
    return 1


@ffi.def_extern()
def pybind_find_function(handle, function, code):
    pass


@ffi.def_extern()
def pybind_make_function(handle, class_, name, args):
    args = PoolStringArray.build_from_gdobj(args, steal=True)
    name = godot_string_to_pyobj(name)
    src = ["def %s(" % name]
    src.append(", ".join([arg.split(":", 1)[0] for arg in args]))
    src.append("):\n    pass")
    return "".join(src)


@ffi.def_extern()
def pybind_complete_code(
    handle, p_code, p_base_path, p_owner, r_options, r_force, r_call_hint
):
    return lib.GODOT_OK


@ffi.def_extern()
def pybind_auto_indent_code(handle, code, from_line, to_line):
    try:
        import autopep8
    except ImportError:
        print(
            "[Pythonscript] Auto indent requires module `autopep8`, "
            "install it with `pip install autopep8`"
        )
    pycode = godot_string_to_pyobj(code).splitlines()
    before = "\n".join(pycode[:from_line])
    to_fix = "\n".join(pycode[from_line:to_line])
    after = "\n".join(pycode[to_line:])
    fixed = autopep8.fix_code(to_fix)
    final_code = "\n".join((before, fixed, after))
    # TODO: modify code instead of replace it when binding on godot_string
    # operation is available
    lib.godot_string_destroy(code)
    lib.godot_string_new_unicode_data(code, final_code, len(final_code))


@ffi.def_extern()
def pybind_add_global_constant(handle, name, value):
    name = godot_string_to_pyobj(name)
    value = variant_to_pyobj(value)
    # Update `godot.globals` module here
    godot.globals.__dict__[name] = value


@ffi.def_extern()
def pybind_debug_get_error(handle):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_line(handle, level):
    return 1


@ffi.def_extern()
def pybind_debug_get_stack_level_function(handle, level):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_source(handle, level):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]


@ffi.def_extern()
def pybind_debug_get_stack_level_locals(
    handle, level, locals, values, max_subitems, max_depth
):
    pass


@ffi.def_extern()
def pybind_debug_get_stack_level_members(
    handle, level, members, values, max_subitems, max_depth
):
    pass


@ffi.def_extern()
def pybind_debug_get_globals(handle, locals, values, max_subitems, max_depth):
    pass


@ffi.def_extern()
def pybind_debug_parse_stack_level_expression(
    handle, level, expression, max_subitems, max_depth
):
    return godot_string_from_pyobj_for_ffi_return("Nothing")[0]
