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
)


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
    ("transform", "Transform", "godot_transform",),
    ("transform2d", "Transform2D", "godot_transform2d",),
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
        return 'None'
    py_type = gd_to_py_type(type)
    if py_type == 'bint':
        return 'bool'
    return py_type


def is_base_type(type):
    return any(True for x in BASE_TYPES if x[1] == type)


def is_builtin(type):
    return any(True for x in BUILTINS_TYPES if x[2] == type)


def is_object(type):
    return not is_base_type(type) and not is_builtin(type)


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
    return {
        "name": cook_name(name),
        "gd_type": type,
        "py_type": gd_to_py_type(type),
        "signature_type": gd_to_py_signature_type(type),
        "is_builtin": is_builtin(type),
        "is_object": is_object(type),
        "is_base_type": is_base_type(type),
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
