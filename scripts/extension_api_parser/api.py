from typing import List, Dict, Tuple, Optional
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
import json
from enum import Enum

from .builtins import BuiltinSpec
from .classes import ClassSpec
from .type import (
    TYPES_DB,
    TypeInUse,
    ValueInUse,
    register_variant_in_types_db,
    register_builtins_in_types_db,
    register_classes_in_types_db,
    register_global_enums_in_types_db,
)
from .utils import correct_name, assert_api_consistency


class BuildConfig(Enum):
    FLOAT_32 = "float_32"
    DOUBLE_32 = "double_32"
    FLOAT_64 = "float_64"
    DOUBLE_64 = "double_64"


@dataclass
class GlobalConstantSpec:
    @classmethod
    def parse(cls, item: dict) -> "GlobalConstantSpec":
        # Don't known what it is supposed to contain given the list is so far empty in the JSON
        raise NotImplementedError


@dataclass
class GlobalEnumSpec:
    original_name: str
    name: str
    values: Dict[str, int]

    @classmethod
    def parse(cls, item: dict) -> "GlobalEnumSpec":
        item.setdefault("original_name", item["name"])
        # Fix `Variant.Operator` & `Variant.Type`
        item["name"] = item["name"].replace(".", "")
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            values={x["name"]: x["value"] for x in item["values"]},
        )


@dataclass
class UtilityFunctionArgumentSpec:
    name: str
    original_name: str
    type: TypeInUse
    default_value: Optional[ValueInUse]

    @classmethod
    def parse(cls, item: dict) -> "UtilityFunctionArgumentSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("default_value", None)
        assert_api_consistency(cls, item)
        arg_type = TypeInUse(item["type"])
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=arg_type,
            default_value=ValueInUse.parse(arg_type, item["default_value"])
            if item["default_value"]
            else None,
        )


@dataclass
class UtilityFunctionSpec:
    original_name: str
    name: str
    return_type: TypeInUse
    category: str
    is_vararg: bool
    hash: int
    arguments: List[Tuple[str, TypeInUse]]

    @classmethod
    def parse(cls, item: dict) -> "UtilityFunctionSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("arguments", [])
        item.setdefault("return_type", "Nil")
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            return_type=TypeInUse(item["return_type"]),
            category=item["category"],
            is_vararg=item["is_vararg"],
            hash=item["hash"],
            arguments=[UtilityFunctionArgumentSpec.parse(x) for x in item["arguments"]],
        )


@dataclass
class SingletonSpec:
    original_name: str
    name: str
    type: TypeInUse

    @classmethod
    def parse(cls, item: dict) -> "SingletonSpec":
        item.setdefault("original_name", item["name"])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=TypeInUse(item["type"]),
        )


@dataclass
class NativeStructureSpec:
    original_name: str
    name: str
    # Format is basically a dump of the C struct content, so don't try to be clever by parsing it
    format: str

    @classmethod
    def parse(cls, item: dict) -> "NativeStructureSpec":
        item.setdefault("original_name", item["name"])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            format=item["format"],
        )


@dataclass
class ExtensionApi:
    version_major: int  # e.g. 4
    version_minor: int  # e.g. 0
    version_patch: int  # e.g. 0
    version_status: str  # e.g. "alpha13"
    version_build: str  # e.g. "official"
    version_full_name: str  # e.g. "Godot Engine v4.0.alpha13.official"

    variant_size: int

    classes: List[ClassSpec]
    builtins: List[BuiltinSpec]
    global_constants: List[GlobalConstantSpec]
    global_enums: List[GlobalEnumSpec]
    utility_functions: List[UtilityFunctionSpec]
    singletons: List[SingletonSpec]
    native_structures: List[NativeStructureSpec]

    # Expose scalars

    @property
    def bool_spec(self):
        return TYPES_DB["bool"]
        # return next(builtin for builtin in self.builtins if builtin.name == "int")

    @property
    def int_spec(self):
        return TYPES_DB["int"]
        # return next(builtin for builtin in self.builtins if builtin.name == "int")

    @property
    def float_spec(self):
        return TYPES_DB["float"]
        # return next(builtin for builtin in self.builtins if builtin.name == "int")

    def get_class_meth_hash(self, classname: str, methname: str) -> int:
        klass = next(c for c in self.classes if c.original_name == classname)
        meth = next(m for m in klass.methods if m.original_name == methname)
        return meth.hash


def merge_builtins_size_info(api_json: dict, build_config: BuildConfig) -> None:
    # Builtins size depend of the build config, hence it is stored separatly from
    # the rest of the built class definition.
    # Here we retreive the correct config and merge it back in the builtins classes
    # definition to simplify the rest of the parsing.

    builtin_class_sizes = next(
        x["sizes"]
        for x in api_json["builtin_class_sizes"]
        if x["build_configuration"] == build_config.value
    )
    builtin_class_sizes = {x["name"]: x["size"] for x in builtin_class_sizes}
    builtin_class_member_offsets = next(
        x["classes"]
        for x in api_json["builtin_class_member_offsets"]
        if x["build_configuration"] == build_config.value
    )
    builtin_class_member_offsets = {x["name"]: x["members"] for x in builtin_class_member_offsets}

    # TODO: remove me once https://github.com/godotengine/godot/pull/64690 is merged
    if "Projection" not in builtin_class_member_offsets:
        builtin_class_member_offsets["Projection"] = [
            {"member": "x", "offset": 0},
            {"member": "y", "offset": builtin_class_sizes["Vector4"]},
            {"member": "z", "offset": 2 * builtin_class_sizes["Vector4"]},
            {"member": "w", "offset": 3 * builtin_class_sizes["Vector4"]},
        ]

    for item in api_json["builtin_classes"]:
        name = item["name"]
        item["size"] = builtin_class_sizes[name]
        for member in builtin_class_member_offsets.get(name, ()):
            for item_member in item["members"]:
                if item_member["name"] == member["member"]:
                    item_member["offset"] = member["offset"]
                    # Float builtin in extension_api.json is always 64bits long,
                    # however builtins made of floating point number can be made of
                    # 32bits (C float) or 64bits (C double)
                    if item_member["type"] == "float":
                        if build_config in (BuildConfig.FLOAT_32, BuildConfig.FLOAT_64):
                            item_member["type"] = "meta:float"
                        else:
                            assert build_config in (BuildConfig.DOUBLE_32, BuildConfig.DOUBLE_64)
                            item_member["type"] = "meta:double"
                    elif item_member["type"] == "int":
                        # Builtins containing int is always made of int32
                        item_member["type"] = "meta:int32"
                    break
            else:
                raise RuntimeError(f"Member `{member}` doesn't seem to be part of `{name}` !")

    # Variant is not present among the `builtin_classes`, only it size is provided.
    # So we have to create our own custom entry for this value.
    api_json["variant_size"] = builtin_class_sizes["Variant"]


def order_classes(classes: List[ClassSpec]) -> List[ClassSpec]:
    # Order classes by inheritance dependency needs
    ordered_classes = OrderedDict()  # Makes it explicit we need ordering here !
    ordered_count = 0

    while len(classes) != len(ordered_classes):
        for klass in classes:
            if klass.inherits is None or klass.inherits in ordered_classes:
                ordered_classes[klass.name] = klass

        # Sanity check to avoid infinite loop in case of error in `extension_api.json`
        if ordered_count == len(ordered_classes):
            bad_class = next(
                klass
                for klass in classes
                if klass.inherits is not None and klass.inherits not in ordered_classes
            )
            raise RuntimeError(
                f"Class `{bad_class.name}` inherits of unknown class `{bad_class.inherits}`"
            )
        ordered_count = len(ordered_classes)

    return list(ordered_classes.values())


def parse_extension_api_json(path: Path, build_config: BuildConfig) -> ExtensionApi:
    api_json = json.loads(path.read_text(encoding="utf8"))
    assert isinstance(api_json, dict)

    merge_builtins_size_info(api_json, build_config)

    api = ExtensionApi(
        version_major=api_json["header"]["version_major"],
        version_minor=api_json["header"]["version_minor"],
        version_patch=api_json["header"]["version_patch"],
        version_status=api_json["header"]["version_status"],
        version_build=api_json["header"]["version_build"],
        version_full_name=api_json["header"]["version_full_name"],
        variant_size=api_json["variant_size"],
        classes=order_classes([ClassSpec.parse(x) for x in api_json["classes"]]),
        builtins=[BuiltinSpec.parse(x) for x in api_json["builtin_classes"]],
        global_constants=[GlobalConstantSpec.parse(x) for x in api_json["global_constants"]],
        global_enums=[GlobalEnumSpec.parse(x) for x in api_json["global_enums"]],
        utility_functions=[UtilityFunctionSpec.parse(x) for x in api_json["utility_functions"]],
        singletons=[SingletonSpec.parse(x) for x in api_json["singletons"]],
        native_structures=[NativeStructureSpec.parse(x) for x in api_json["native_structures"]],
    )

    # This is the kind-of ugly part where we register in a global dict the types
    # we've just parsed (so that they could be lazily retreived from all the
    # `TypeInUse` that reference them)
    register_variant_in_types_db(api.variant_size)
    register_builtins_in_types_db(api.builtins)
    register_classes_in_types_db(api.classes)
    register_global_enums_in_types_db(api.global_enums)

    return api
