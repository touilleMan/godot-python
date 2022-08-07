from dataclasses import dataclass
from typing import List, Dict, Optional

from .utils import correct_name, assert_api_consistency
from .type import TypeInUse, ValueInUse, TypeSpec, TYPES_DB


@dataclass
class ClassEnumSpec:
    original_name: str
    name: str
    is_bitfield: bool
    values: Dict[str, int]

    @classmethod
    def parse(cls, item: dict) -> "ClassEnumSpec":
        item.setdefault("original_name", item["name"])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            is_bitfield=item["is_bitfield"],
            values={x["name"]: x["value"] for x in item["values"]},
        )


@dataclass
class ClassMethodArgumentSpec:
    name: str
    original_name: str
    type: TypeInUse
    default_value: ValueInUse

    @classmethod
    def parse(cls, item: dict) -> "ClassMethodArgumentSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("default_value", None)
        # Meta attribute is used to further specify the type (e.g. type=int meta=uint32)
        meta = item.pop("meta", None)
        if meta:
            item["type"] = f"meta:{meta}"
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=TypeInUse(item["type"]),
            default_value=ValueInUse(item["default_value"])
            if item["default_value"] is not None
            else None,
        )


@dataclass
class ClassMethodSpec:
    original_name: str
    name: str
    is_const: bool
    is_vararg: bool
    is_static: bool
    is_virtual: bool
    hash: Optional[int]
    return_value: TypeInUse
    arguments: List[ClassMethodArgumentSpec]

    @classmethod
    def parse(cls, item: dict) -> "ClassMethodSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("return_value", {"type": "Nil"})
        item.setdefault("arguments", [])
        item.setdefault("hash", None)
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            is_const=item["is_const"],
            is_vararg=item["is_vararg"],
            is_static=item["is_static"],
            is_virtual=item["is_virtual"],
            hash=item["hash"],
            return_value=TypeInUse(item["return_value"]),
            arguments=[ClassMethodArgumentSpec.parse(x) for x in item["arguments"]],
        )


@dataclass
class ClassSignalSpec:
    original_name: str
    name: str
    arguments: List[ClassMethodArgumentSpec]

    @classmethod
    def parse(cls, item: dict) -> "ClassSignalSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("arguments", [])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            arguments=[ClassMethodArgumentSpec.parse(x) for x in item["arguments"]],
        )


@dataclass
class ClassPropertySpec:
    original_name: str
    name: str
    type: TypeInUse
    setter: str
    getter: str
    index: int

    @classmethod
    def parse(cls, item: dict) -> "ClassPropertySpec":
        item.setdefault("original_name", item["name"])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=TypeInUse(item["type"]),
            setter=item["setter"],
            getter=item["getter"],
            index=item["index"],
        )


@dataclass
class ClassSpec:
    original_name: str
    name: str
    is_refcounted: bool
    is_instantiable: bool
    inherits: List[str]
    api_type: str
    enums: List[ClassEnumSpec]
    methods: List[ClassMethodSpec]
    signals: List[ClassSignalSpec]
    properties: List[ClassPropertySpec]
    constants: Dict[str, int]

    @classmethod
    def parse(cls, item: dict) -> "ClassSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("inherits", [])
        item.setdefault("enums", [])
        item.setdefault("signals", [])
        item.setdefault("methods", [])
        item.setdefault("properties", [])
        item.setdefault("constants", [])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            is_refcounted=item["is_refcounted"],
            is_instantiable=item["is_instantiable"],
            inherits=item["inherits"],
            api_type=item["api_type"],
            enums=[ClassEnumSpec.parse(x) for x in item["enums"]],
            methods=[ClassMethodSpec.parse(x) for x in item["methods"]],
            signals=[ClassSignalSpec.parse(x) for x in item["signals"]],
            properties=[ClassPropertySpec.parse(x) for x in item["properties"]],
            constants={x["name"]: x["value"] for x in item["constants"]},
        )
