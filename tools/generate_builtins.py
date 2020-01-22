import os
import argparse
import json
import re
from keyword import iskeyword
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


BASEDIR = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(f"{BASEDIR}/builtins_templates"),
    trim_blocks=True,
    lstrip_blocks=False,
    extensions=["jinja2.ext.loopcontrols"],
)
env.filters["merge"] = lambda x, **kwargs: {**x, **kwargs}


BUILTINS_TYPES = [
    # Render target / Python type / Godot type
    ("aabb", "AABB", "godot_aabb",),
    ("array", "Array", "godot_array",),
    ("basis", "Basis", "godot_basis",),
    ("color", "Color", "godot_color",),
    ("dictionary", "Dictionary", "godot_dictionary",),
    ("node_path", "NodePath", "godot_node_path",),
    ("plane", "Plane", "godot_plane",),
    ("quat", "Quat", "godot_quat",),
    ("rect2", "Rect2", "godot_rect2",),
    ("rid", "RID", "godot_rid",),
    # transform2d before transform to avoid bad detection in cook_c_signature
    ("transform2d", "Transform2D", "godot_transform2d",),
    ("transform", "Transform", "godot_transform",),
    ("vector2", "Vector2", "godot_vector2",),
    ("vector3", "Vector3", "godot_vector3",),
    ("pool_byte_array", "PoolByteArray", "godot_pool_byte_array",),
    ("pool_int_array", "PoolIntArray", "godot_pool_int_array",),
    ("pool_real_array", "PoolRealArray", "godot_pool_real_array",),
    ("pool_string_array", "PoolStringArray", "godot_pool_string_array",),
    ("pool_vector2_array", "PoolVector2Array", "godot_pool_vector2_array",),
    ("pool_vector3_array", "PoolVector3Array", "godot_pool_vector3_array",),
    ("pool_color_array", "PoolColorArray", "godot_pool_color_array",),
    ("gdstring", "GDString", "godot_string",),
    ("variant", "object", "godot_variant",),
]
BASE_TYPES = [
    ("godot_int", "godot_int"),
    ("godot_real", "godot_real"),
    ("bint", "godot_bool"),
    ("uint32_t", "uint32_t"),
    ("uint64_t", "uint64_t"),
]

GD_TO_PY = {
    **{x[2]: x[1] for x in BUILTINS_TYPES},
    **{x[1]: x[0] for x in BASE_TYPES},
}

PY_TO_GD = {
    **{x[1]: x[2] for x in BUILTINS_TYPES},
    **{x[0]: x[1] for x in BASE_TYPES},
}


def render_target_to_py_type(render_target):
    return next(x[1] for x in BUILTINS_TYPES if x[0] == render_target)


def render_target_to_template(render_target):
    return f"{render_target}.tmpl.pxi"


def py_to_gd_type(type):
    try:
        return PY_TO_GD[type]
    except KeyError:
        # Assume it's a Godot Object type
        return type


def gd_to_py_type(type):
    try:
        return GD_TO_PY[type]
    except KeyError:
        # Assume it's a Godot Object type
        return type


def gd_to_py_signature_type(type):
    if type is None:
        return "None"
    py_type = gd_to_py_type(type)
    if py_type == "bint":
        return "bool"
    elif py_type == "godot_int":
        return "int"
    elif py_type == "godot_real":
        return "float"
    return py_type


def is_base_type(type):
    return any(True for x in BASE_TYPES if x[1] == type)


def is_builtin(type):
    return any(True for x in BUILTINS_TYPES if x[2] == type)


def is_object(type):
    return not is_base_type(type) and not is_builtin(type)


def cook_c_signatures(signatures):
    cooked_signatures = {}
    gdapi = ""
    for line in signatures.splitlines():
        line = line.strip()
        match = re.match(r"^//\WGDAPI:\W([0-9])\.([0-9])", line)
        if match:
            gdapi_major, gdapi_minor = match.groups()
            gdapi = f"{gdapi_major}{gdapi_minor}"
            continue
        if not line or line.startswith("//"):
            continue
        cooked = cook_c_signature(line, gdapi=gdapi)
        cooked_signatures[cooked["pyname"]] = cooked
    return cooked_signatures


def cook_c_signature(signature, gdapi="10"):
    # Hacky signature parsing
    a, b = signature.split("(", 1)
    assert b.endswith(")"), signature
    assert "(" not in b, signature
    b = b[:-1]
    args = []
    for arg in b.split(","):
        assert arg.count("*") < 2, signature
        if "*" in arg:
            arg_type, arg_name = [x.strip() for x in arg.split("*") if x.strip()]
            arg_type = f"{arg_type}*"
        else:
            arg_type, arg_name = [x for x in arg.split(" ") if x]
        if arg_name.startswith("p_"):
            arg_name = arg_name[2:]
        args.append((arg_type, arg_name))
    args.pop(0)  # Remove self argument

    assert "*" not in a, signature
    return_type, gdname = [x for x in a.rsplit(" ", 1) if x]
    if return_type == "void":
        return_type = None

    for type_gdname in GD_TO_PY.keys():
        if gdname.startswith(type_gdname):
            pyname = gdname[len(type_gdname) + 1 :]
            break

    return {
        "pyname": pyname,
        "gdname": pyname,
        "return_type": return_type,
        "args": args,
        "gdapi": gdapi,
    }


def cook_return_type(return_type):
    if return_type is None:
        return {
            "gd_type": "",
            "py_type": "",
            "signature_type": "None",
            "is_builtin": False,
            "is_object": False,
            "is_base_type": False,
            "is_void": True,
        }
    else:
        return {
            "gd_type": return_type,
            "py_type": gd_to_py_type(return_type),
            "signature_type": gd_to_py_signature_type(return_type),
            "is_builtin": is_builtin(return_type),
            "is_object": is_object(return_type),
            "is_base_type": is_base_type(return_type),
            "is_void": False,
        }


def cook_args(args):
    return [cook_arg(arg) for arg in args]


def cook_name(name):
    return f"{name}_" if iskeyword(name) else name


def cook_arg(args):
    try:
        type, name, default = args
    except ValueError:
        type, name = args
        default = None
    if type.endswith("*"):
        gd_type = type[:-1]
        is_ptr = True
    else:
        gd_type = type
        is_ptr = False
    return {
        "name": cook_name(name),
        "gd_type": gd_type,
        "py_type": gd_to_py_type(gd_type),
        "signature_type": gd_to_py_signature_type(gd_type),
        "is_ptr": is_ptr,
        "is_builtin": is_builtin(gd_type),
        "is_object": is_object(gd_type),
        "is_base_type": is_base_type(gd_type),
        "has_default": default is not None,
        # TODO: handle default here !
    }


def generate_pool_array(output_path):
    context = {
        "render_target_to_py_type": render_target_to_py_type,
        "render_target_to_template": render_target_to_template,
        "py_to_gd_type": py_to_gd_type,
        "gd_to_py_type": gd_to_py_type,
        "gd_to_py_signature_type": gd_to_py_signature_type,
        "is_base_type": is_base_type,
        "is_builtin": is_builtin,
        "cook_return_type": cook_return_type,
        "cook_args": cook_args,
        "cook_arg": cook_arg,
        "cook_c_signature": cook_c_signature,
        "cook_c_signatures": cook_c_signatures,
    }

    template = env.get_template("builtins.tmpl.pyx")
    out = template.render(**context)
    with open(output_path, "w") as fd:
        fd.write(out)

    pxd_output_path = output_path.rsplit(".", 1)[0] + ".pxd"
    template = env.get_template("builtins.tmpl.pxd")
    out = template.render(**context)
    with open(pxd_output_path, "w") as fd:
        fd.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate godot builtins bindings files (except pool arrays)"
    )
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()
    generate_pool_array(args.output or f"builtins.pyx")
