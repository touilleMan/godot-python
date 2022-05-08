#! /usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Optional, List
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from dataclasses import dataclass
from string import ascii_uppercase

BASEDIR = Path(__file__).parent
env = Environment(
    loader=FileSystemLoader(BASEDIR / "builtins_templates"),
    trim_blocks=True,
    lstrip_blocks=False,
    extensions=["jinja2.ext.loopcontrols"],
    undefined=StrictUndefined,
)
env.filters["merge"] = lambda x, **kwargs: {**x, **kwargs}


# `extension_api.json` is pretty big, hence it's much easier to have it
# format reproduced here as typed classes, especially given we want to cook
# it a bit before using it in the templates


BuiltinType = str


@dataclass
class FnArgument:
    name: str
    type: BuiltinType
    default_value: Optional[str]

    @classmethod
    def parse(cls, item: dict) -> "FnArgument":
        item.setdefault("default_value", None)
        assert item.keys() == cls.__dataclass_fields__.keys()
        return cls(
            name=item["name"],
            type=item["type"],
            default_value=item["default_value"],
        )


@dataclass
class BuiltinConstructorSpec:
    index: int
    arguments: List[FnArgument]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinConstructorSpec":
        item.setdefault("arguments", [])
        assert item.keys() == cls.__dataclass_fields__.keys()
        return cls(
            index=item["index"],
            arguments=[FnArgument.parse(x) for x in item["arguments"]],
        )


@dataclass
class BuiltinOperatorSpec:
    name: str
    right_type: Optional[BuiltinType]
    return_type: BuiltinType

    @classmethod
    def parse(cls, item: dict) -> "BuiltinOperatorSpec":
        item.setdefault("right_type", None)
        assert item.keys() == cls.__dataclass_fields__.keys()
        return cls(
            name=item["name"],
            right_type=item["right_type"],
            return_type=item["return_type"],
        )


@dataclass
class BuiltinMemberSpec:
    name: str
    offset: int
    type: BuiltinType

    @classmethod
    def parse(cls, item: dict) -> "BuiltinMemberSpec":
        item.setdefault("offset", 0)  # Dummy value, will be set later on
        assert item.keys() == cls.__dataclass_fields__.keys()
        return cls(
            name=item["name"],
            offset=item["offset"],
            type=item["type"],
        )


@dataclass
class BuiltinConstantSpec:
    name: str
    type: BuiltinType
    value: str

    @classmethod
    def parse(cls, item: dict) -> "BuiltinConstantSpec":
        assert item.keys() == cls.__dataclass_fields__.keys()
        return cls(
            name=item["name"],
            type=item["type"],
            value=item["value"],
        )


@dataclass
class BuiltinMethodSpec:
    name: str
    return_type: BuiltinType
    is_vararg: bool
    is_const: bool
    is_static: bool
    hash: int
    arguments: List[FnArgument]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinMethodSpec":
        item.setdefault("arguments", [])
        item.setdefault("return_type", "Nil")
        assert item.keys() == cls.__dataclass_fields__.keys()
        return cls(
            name=item["name"],
            return_type=item["return_type"],
            is_vararg=item["is_vararg"],
            is_const=item["is_const"],
            is_static=item["is_static"],
            hash=item["hash"],
            arguments=item["arguments"],
        )


@dataclass
class BuiltinSpec:
    name: str
    original_name: str
    size: Optional[int]
    indexing_return_type: Optional[str]
    is_keyed: bool
    constructors: List[BuiltinConstructorSpec]
    has_destructor: bool
    operators: List[BuiltinOperatorSpec]
    methods: List[BuiltinMethodSpec]
    members: List[BuiltinMemberSpec]
    constants: List[BuiltinConstantSpec]
    variant_type_name: str

    @classmethod
    def parse(cls, item: dict) -> "BuiltinSpec":
        item.setdefault("size", None)  # Dummy value, will be set later on
        item.setdefault("variant_type_name", "")  # See above
        item.setdefault("original_name", "")  # See above
        item.setdefault("indexing_return_type", None)
        item.setdefault("methods", [])
        item.setdefault("members", [])
        item.setdefault("constants", [])

        # Ensure the fields are as expected, in theory we should also check typing
        # but it's cumbersome and it's very likely bad typing will lead anyway to a
        # runtime error in this script or a compilation error on the generated code
        assert item.keys() == cls.__dataclass_fields__.keys()
        assert len(item["constructors"]) >= 1

        # Camel to upper snake case
        snake = ""
        # Gotcha with Transform2D&Transform3D
        for c in item["name"].replace("2D", "2d").replace("3D", "3d"):
            if c in ascii_uppercase and snake and snake[-1] not in ascii_uppercase:
                snake += "_"
            snake += c
        item["variant_type_name"] = f"GDNATIVE_VARIANT_TYPE_{snake.upper()}"

        # Avoid overwritting default Python types
        if item["name"] in ("bool", "int", "float", "String"):
            patched_name = "GD" + item["name"][0].upper() + item["name"][1:]
        else:
            patched_name = item["name"]

        return cls(
            original_name=item["name"],
            name=patched_name,
            size=item["size"],
            indexing_return_type=item["indexing_return_type"],
            is_keyed=item["is_keyed"],
            constructors=[BuiltinConstructorSpec.parse(x) for x in item["constructors"]],
            has_destructor=item["has_destructor"],
            operators=[BuiltinOperatorSpec.parse(x) for x in item["operators"]],
            methods=[BuiltinMethodSpec.parse(x) for x in item["methods"]],
            members=[BuiltinMemberSpec.parse(x) for x in item["members"]],
            constants=[BuiltinConstantSpec.parse(x) for x in item["constants"]],
            variant_type_name=item["variant_type_name"],
        )


def parse_extension_api_json(path: Path) -> List[BuiltinSpec]:
    api_json = json.loads(path.read_text(encoding="utf8"))
    assert isinstance(api_json, dict)

    builtin_class_sizes = next(
        x["sizes"]
        for x in api_json["builtin_class_sizes"]
        if x["build_configuration"] == args.build_config
    )
    builtin_class_sizes = {x["name"]: x["size"] for x in builtin_class_sizes}
    builtin_class_member_offsets = next(
        x["classes"]
        for x in api_json["builtin_class_member_offsets"]
        if x["build_configuration"] == args.build_config
    )
    builtin_class_member_offsets = {x["name"]: x["members"] for x in builtin_class_member_offsets}

    # Temporary fix, see https://github.com/godotengine/godot/pull/60884
    for member in builtin_class_member_offsets["Color"]:
        member["member"] = {
            "x": "r",
            "y": "g",
            "z": "b",
            "w": "a",
        }[member["member"]]

    specs = []
    for item in api_json["builtin_classes"]:
        spec = BuiltinSpec.parse(item)
        # Special case for size
        spec.size = builtin_class_sizes.get(spec.original_name, None)
        # Special case for member offsets
        for member in builtin_class_member_offsets.get(spec.original_name, []):
            member_spec = next(
                candidate for candidate in spec.members if candidate.name == member["member"]
            )
            member_spec.offset = member["offset"]
        specs.append(spec)

    return specs


def generate_builtins(output_dir: Path, output_basename: str, specs: List[BuiltinSpec]) -> None:
    context = {
        "specs": specs,
    }

    template = env.get_template("builtins.tmpl.pyx")
    pyx_output_path = output_dir / f"{output_basename}.pyx"
    print(f"Generating {pyx_output_path}")
    pyx_output_path.write_text(template.render(**context))

    # template = env.get_template("builtins.tmpl.pxd")
    pxd_output_path = output_dir / f"{output_basename}.pxd"
    print(f"Generating {pxd_output_path}")
    # pxd_output_path.write_text(template.render(**context))
    pxd_output_path.write_text("")

    # template = env.get_template("builtins.tmpl.pyi")
    pyi_output_path = output_dir / f"{output_basename}.pyi"
    print(f"Generating {pyi_output_path}")
    # pyi_output_path.write_text(template.render(**context))
    pyi_output_path.write_text("")


if __name__ == "__main__":

    def _parse_output(val):
        suffix = ".pyx"
        if not val.endswith(suffix):
            raise argparse.ArgumentTypeError(f"Must have a `{suffix}` suffix")
        path = Path(val[: -len(suffix)]).resolve()
        return (path.parent, path.name)

    parser = argparse.ArgumentParser(description="Generate Godot builtins bindings files")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="EXTENSION_API_PATH",
        type=Path,
        help="Path to Godot extension_api.json file",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        metavar="BUILTINS_PYX",
        type=_parse_output,
        help="Path to store the generated builtins.pyx (also used to determine .pxd/.pyi output path)",
    )
    parser.add_argument(
        "--build-config",
        required=True,
        choices=["float_32", "float_64", "double_32", "double_64"],
    )

    args = parser.parse_args()
    output_dir, output_basename = args.output

    specs = parse_extension_api_json(args.input)
    generate_builtins(output_dir, output_basename, specs)
