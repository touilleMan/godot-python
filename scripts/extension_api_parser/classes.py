from typing import List, Dict, Optional
from dataclasses import dataclass

from .utils import correct_name, assert_api_consistency
from .type import TypeInUse, ValueInUse


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
    default_value: Optional[ValueInUse]

    @classmethod
    def parse(cls, item: dict) -> "ClassMethodArgumentSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("default_value", None)
        # Meta attribute is used to further specify the type (e.g. type=int meta=uint32)
        meta = item.pop("meta", None)
        if meta:
            item["type"] = f"meta:{meta}"
        assert_api_consistency(cls, item)
        arg_type = TypeInUse.parse(item["type"])
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=arg_type,
            default_value=(
                None
                if item["default_value"] is None
                else ValueInUse.parse(arg_type, item["default_value"])
            ),
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
    return_type: TypeInUse
    arguments: List[ClassMethodArgumentSpec]

    @classmethod
    def parse(cls, item: dict) -> "ClassMethodSpec":
        item.setdefault("original_name", item["name"])
        return_value = item.pop("return_value", {"type": "Nil"})
        return_type_meta = return_value.get("meta")
        if return_type_meta:
            item["return_type"] = TypeInUse(f"meta:{return_type_meta}")
        else:
            item["return_type"] = TypeInUse.parse(return_value["type"])
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
            return_type=item["return_type"],
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
    getter: str
    setter: Optional[str]
    index: Optional[int]

    @classmethod
    def parse(cls, item: dict) -> "ClassPropertySpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("getter", None)
        assert item["getter"] is not None
        item.setdefault("setter", None)
        item.setdefault("index", None)
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=TypeInUse.parse(item["type"]),
            getter=item["getter"],
            setter=item["setter"],
            index=item["index"],
        )


@dataclass
class ClassSpec:
    original_name: str
    name: str
    is_refcounted: bool
    is_instantiable: bool
    inherits: Optional[str]
    api_type: str
    enums: List[ClassEnumSpec]
    methods: List[ClassMethodSpec]
    signals: List[ClassSignalSpec]
    properties: List[ClassPropertySpec]
    constants: Dict[str, int]

    @classmethod
    def parse(cls, item: dict) -> "ClassSpec":
        item.setdefault("original_name", item["name"])
        # Special case for the Object type, this is because `Object` is too
        # broad of a name (it's easy to mix with Python's regular `object`)
        if item["name"] == "Object":
            item["name"] = "GDObject"
        item["inherits"] = item.get("inherits") or None
        if item["inherits"] == "Object":
            item["inherits"] = "GDObject"
        item.setdefault("enums", [])
        item.setdefault("signals", [])
        item.setdefault("methods", [])
        item.setdefault("properties", [])
        item.setdefault("constants", [])
        assert_api_consistency(cls, item)
        # TODO: remove me once https://github.com/godotengine/godot/pull/64427 is merged
        for prop in item["properties"]:
            if prop.get("getter") == "":
                prop.pop("getter")
            if prop.get("setter") == "":
                prop.pop("setter")
            if prop.get("index") == -1:
                prop.pop("index")
        # TODO: remove me once https://github.com/godotengine/godot/pull/64428 is merged
        def _filter_bad_property(prop: dict) -> bool:
            if "/" in prop["name"]:
                return False
            # e.g. `Modifications,modifications/`
            if "/" in prop["type"]:
                return False
            if "getter" not in prop:
                return False

        item["properties"] = [prop for prop in item["properties"] if _filter_bad_property(prop)]
        return cls(
            name=item["name"],
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
