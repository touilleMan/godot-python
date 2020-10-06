import os
import argparse
import json
import re
from warnings import warn
from functools import partial
from keyword import iskeyword
from dataclasses import dataclass, replace
from collections import defaultdict
from itertools import product
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from typing import List, Set

from type_specs import (
    TypeSpec,
    ALL_TYPES_EXCEPT_OBJECTS,
    TYPE_RID,
    TYPE_VECTOR3,
    TYPE_VECTOR2,
    TYPE_AABB,
    TYPE_BASIS,
    TYPE_COLOR,
    TYPE_STRING,
    TYPE_RECT2,
    TYPE_TRANSFORM2D,
    TYPE_PLANE,
    TYPE_QUAT,
    TYPE_TRANSFORM,
    TYPE_NODEPATH,
    TYPE_DICTIONARY,
    TYPE_ARRAY,
)


# TODO: after all, it may not be a great idea to share TypeSpec between builtin and binding scripts...


# Bonus types
TYPES_SIZED_INT = [
    TypeSpec(
        gdapi_type=f"{signed}int{size}_t",
        c_type=f"{signed}int{size}_t",
        cy_type=f"{signed}int{size}_t",
        py_type="int",
        is_base_type=True,
        is_stack_only=True,
    )
    for signed, size in product(["u", ""], [8, 32, 64])
]
ALL_TYPES = [
    *ALL_TYPES_EXCEPT_OBJECTS,
    *TYPES_SIZED_INT,
    TypeSpec(
        gdapi_type="godot_object",
        c_type="godot_object",
        cy_type="object",
        py_type="Object",
        is_object=True,
    ),
    TypeSpec(
        gdapi_type="int",
        c_type="int",
        cy_type="int",
        py_type="int",
        is_base_type=True,
        is_stack_only=True,
    ),
    TypeSpec(
        gdapi_type="size_t",
        c_type="size_t",
        cy_type="size_t",
        py_type="int",
        is_base_type=True,
        is_stack_only=True,
    ),
    # /!\ godot_real is a C float (note py_type is still `float` given that's how Python call all floating point numbers)
    TypeSpec(
        gdapi_type="double",
        c_type="double",
        cy_type="double",
        py_type="float",
        is_base_type=True,
        is_stack_only=True,
    ),
    TypeSpec(
        gdapi_type="wchar_t",
        c_type="wchar_t",
        cy_type="wchar_t",
        is_base_type=True,
        is_stack_only=True,
    ),
    TypeSpec(
        gdapi_type="char", c_type="char", cy_type="char", is_base_type=True, is_stack_only=True
    ),
    TypeSpec(
        gdapi_type="schar",
        c_type="schar",
        cy_type="signed char",
        is_base_type=True,
        is_stack_only=True,
    ),
    TypeSpec(
        gdapi_type="godot_char_string",
        c_type="godot_char_string",
        cy_type="godot_char_string",
        py_type="str",
        is_builtin=True,
    ),
    TypeSpec(
        gdapi_type="godot_string_name",
        c_type="godot_string_name",
        cy_type="godot_string_name",
        py_type="str",
        is_builtin=True,
    ),
    TypeSpec(
        gdapi_type="bool",
        c_type="bool",
        cy_type="bool",
        py_type="bool",
        is_base_type=True,
        is_stack_only=True,
    ),
]
C_NAME_TO_TYPE_SPEC = {s.c_type: s for s in ALL_TYPES}
BUILTINS_TYPES = [s for s in ALL_TYPES if s.is_builtin]


TARGET_TO_TYPE_SPEC = {
    "rid": TYPE_RID,
    "vector3": TYPE_VECTOR3,
    "vector2": TYPE_VECTOR2,
    "aabb": TYPE_AABB,
    "basis": TYPE_BASIS,
    "color": TYPE_COLOR,
    "gdstring": TYPE_STRING,
    "rect2": TYPE_RECT2,
    "transform2d": TYPE_TRANSFORM2D,
    "plane": TYPE_PLANE,
    "quat": TYPE_QUAT,
    "transform": TYPE_TRANSFORM,
    "node_path": TYPE_NODEPATH,
    "dictionary": TYPE_DICTIONARY,
    "array": TYPE_ARRAY,
}


@dataclass
class ArgumentSpec:
    name: str
    type: TypeSpec
    is_ptr: bool
    is_const: bool

    def __getattr__(self, key):
        return getattr(self.type, key)


@dataclass
class BuiltinMethodSpec:
    # Builtin type this method apply on (e.g. Vector2)
    klass: TypeSpec
    # Name of the function in the GDNative C API
    c_name: str
    # Basically gd_name without the `godot_<type>_` prefix
    py_name: str
    return_type: TypeSpec
    args: List[ArgumentSpec]
    gdapi: str


def cook_name(name):
    return f"{name}_" if iskeyword(name) else name


BASEDIR = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(f"{BASEDIR}/builtins_templates"),
    trim_blocks=True,
    lstrip_blocks=False,
    extensions=["jinja2.ext.loopcontrols"],
    undefined=StrictUndefined,
)
env.filters["merge"] = lambda x, **kwargs: {**x, **kwargs}


def load_builtin_method_spec(func: dict, gdapi: str) -> BuiltinMethodSpec:
    c_name = func["name"]
    assert c_name.startswith("godot_"), func
    for builtin_type in BUILTINS_TYPES:
        prefix = f"{builtin_type.c_type}_"
        if c_name.startswith(prefix):
            py_name = c_name[len(prefix) :]
            break
    else:
        # This function is not part of a builtin class (e.g. godot_print), we can ignore it
        return

    def _cook_type(raw_type):
        # Hack type detection, might need to be improved with api evolutions
        match = re.match(r"^(const\W+|)([a-zA-Z_0-9]+)(\W*\*|)$", raw_type.strip())
        if not match:
            raise RuntimeError(f"Unsuported type `{raw_type}` in function `{c_name}`")
        is_const = bool(match.group(1))
        c_type = match.group(2)
        is_ptr = bool(match.group(3))

        for type_spec in ALL_TYPES:
            if c_type == type_spec.c_type:
                break
        else:
            raise RuntimeError(f"Unsuported type `{raw_type}` in function `{c_name}`")

        return is_const, is_ptr, type_spec

    args = []
    for arg_type, arg_name in func["arguments"]:
        if arg_name.startswith("p_"):
            arg_name = arg_name[2:]
        arg_name = cook_name(arg_name)
        arg_is_const, arg_is_ptr, arg_type_spec = _cook_type(arg_type)
        args.append(
            ArgumentSpec(
                name=arg_name, type=arg_type_spec, is_ptr=arg_is_ptr, is_const=arg_is_const
            )
        )

    ret_is_const, ret_is_ptr, ret_type_spec = _cook_type(func["return_type"])
    return_type = ArgumentSpec(
        name="", type=ret_type_spec, is_ptr=ret_is_ptr, is_const=ret_is_const
    )

    return BuiltinMethodSpec(
        klass=builtin_type,
        c_name=c_name,
        py_name=py_name,
        return_type=return_type,
        args=args,
        gdapi=gdapi,
    )


def pre_cook_patch_stuff(gdnative_api):
    revision = gdnative_api["core"]
    while revision:
        for func in revision["api"]:
            # `signed char` is used in some string methods to return comparison
            # information (see `godot_string_casecmp_to`).
            # The type in two word messes with our (poor) type parsing.
            if func["return_type"] == "signed char":
                func["return_type"] = "int8_t"
        revision = revision["next"]


def load_builtins_specs_from_gdnative_api_json(gdnative_api: dict) -> List[BuiltinMethodSpec]:
    pre_cook_patch_stuff(gdnative_api)
    revision = gdnative_api["core"]
    specs = []
    while revision:
        revision_gdapi = f"gdapi{revision['version']['major']}{revision['version']['minor']}"
        for func in revision["api"]:
            assert func["name"] not in specs
            # Ignore godot pool (generate by another script)
            if func["name"].startswith("godot_pool_") or func["name"].startswith("godot_variant_"):
                continue
            spec = load_builtin_method_spec(func, gdapi=revision_gdapi)
            if spec:
                specs.append(spec)
        revision = revision["next"]

    return specs


def generate_builtins(
    no_suffix_output_path: str, methods_specs: List[BuiltinMethodSpec]
) -> Set[str]:
    methods_c_name_to_spec = {s.c_name: s for s in methods_specs}

    # Track the methods used in the templates to enforce they are in sync with the gdnative_api.json
    rendered_methods = set()

    def _mark_rendered(method_c_name):
        rendered_methods.add(method_c_name)
        return ""  # Return empty string to not output anything when used in a template

    def _render_target_to_template(render_target):
        assert isinstance(render_target, str)
        return f"{render_target}.tmpl.pxi"

    def _get_builtin_method_spec(method_c_name):
        assert isinstance(method_c_name, str)
        try:
            _mark_rendered(method_c_name)
            return methods_c_name_to_spec[method_c_name]
        except KeyError:
            raise RuntimeError(f"Unknown method `{method_c_name}`")

    def _get_type_spec(py_type):
        assert isinstance(py_type, str)
        try:
            return next(t for t in ALL_TYPES if t.py_type == py_type)
        except StopIteration:
            raise RuntimeError(f"Unknown type `{py_type}`")

    def _get_target_method_spec_factory(render_target):
        assert isinstance(render_target, str)
        try:
            type_spec = TARGET_TO_TYPE_SPEC[render_target]
        except KeyError:
            raise RuntimeError(f"Unknown target `{render_target}`")

        def _get_target_method_spec(method_py_name):
            return _get_builtin_method_spec(f"{type_spec.c_type}_{method_py_name}")

        return _get_target_method_spec

    context = {
        "render_target_to_template": _render_target_to_template,
        "get_builtin_method_spec": _get_builtin_method_spec,
        "get_type_spec": _get_type_spec,
        "get_target_method_spec_factory": _get_target_method_spec_factory,
        "force_mark_rendered": _mark_rendered,
    }

    template = env.get_template("builtins.tmpl.pyx")
    pyx_output_path = f"{no_suffix_output_path}.pyx"
    print(f"Generating {pyx_output_path}")
    out = template.render(**context)
    with open(pyx_output_path, "w") as fd:
        fd.write(out)

    pyi_output_path = f"{no_suffix_output_path}.pyi"
    print(f"Generating {pyi_output_path}")
    template = env.get_template("builtins.tmpl.pyi")
    out = template.render(**context)
    with open(pyi_output_path, "w") as fd:
        fd.write(out)

    pxd_output_path = f"{no_suffix_output_path}.pxd"
    print(f"Generating {pxd_output_path}")
    template = env.get_template("builtins.tmpl.pxd")
    out = template.render(**context)
    with open(pxd_output_path, "w") as fd:
        fd.write(out)

    return rendered_methods


def ensure_all_methods_has_been_rendered(
    methods_specs: List[BuiltinMethodSpec], rendered_methods: Set[str]
):
    all_methods = {s.c_name for s in methods_specs}

    unknown_rendered_methods = rendered_methods - all_methods
    for method in sorted(unknown_rendered_methods):
        print(f"ERROR: `{method}` is used in the templates but not present in gnative_api.json")

    not_rendered_methods = all_methods - rendered_methods

    for method in sorted(not_rendered_methods):
        print(f"ERROR: `{method}` is listed in gnative_api.json but not used in the templates")

    return not unknown_rendered_methods and not not_rendered_methods


if __name__ == "__main__":

    def _parse_output(val):
        suffix = ".pyx"
        if not val.endswith(suffix):
            raise argparse.ArgumentTypeError(f"Must have a `{suffix}` suffix")
        return val[: -len(suffix)]

    parser = argparse.ArgumentParser(
        description="Generate godot builtins bindings files (except pool arrays)"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="GDNATIVE_API_PATH",
        type=argparse.FileType("r", encoding="utf8"),
        help="Path to Godot gdnative_api.json file",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        metavar="BUILTINS_PYX",
        type=_parse_output,
        help="Path to store the generated builtins.pyx (also used to determine .pxd/.pyi output path)",
    )
    args = parser.parse_args()
    gdnative_api_json = json.load(args.input)
    methods_specs = load_builtins_specs_from_gdnative_api_json(gdnative_api_json)
    rendered_methods = generate_builtins(args.output, methods_specs)
    if not ensure_all_methods_has_been_rendered(methods_specs, rendered_methods):
        raise SystemExit(
            "Generated builtins are not in line with the provided gdnative_api.json :'("
        )
