from typing import List, Dict, Optional
from dataclasses import dataclass

from .utils import *
from .type_spec import *
from .builtins import *
from .in_use import *


def parse_class_enum(spec: dict, class_name: str) -> EnumTypeSpec:
    spec.setdefault("is_bitfield", False)
    assert spec.keys() == {"name", "is_bitfield", "values"}, spec.keys()
    return EnumTypeSpec(
        original_name=spec["name"],
        py_type=f"{class_name}.{spec['name']}",
        cy_type=f"{class_name}.{spec['name']}",
        is_bitfield=spec["is_bitfield"],
        values={x["name"]: x["value"] for x in spec["values"]},
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
    is_property_accessor: bool
    hash: Optional[int]
    hash_compatibility: Optional[int]
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
        item.setdefault("hash_compatibility", None)
        item.setdefault("is_property_accessor", False)
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            is_const=item["is_const"],
            is_vararg=item["is_vararg"],
            is_static=item["is_static"],
            is_virtual=item["is_virtual"],
            is_property_accessor=item["is_property_accessor"],
            hash=item["hash"],
            hash_compatibility=item["hash_compatibility"],
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


class ClassTypeSpec(TypeSpec):
    """
    Godot object defined in extension_api.json's `classes` entry (e.g. Node2D, Reference)

    Godot object is always manipulated as a pointer, hence the `size` field here is
    always the size of a pointer.
    """

    c_name_prefix: str
    is_refcounted: bool
    is_instantiable: bool
    inherits: Optional[TypeInUse]
    api_type: str
    enums: List[EnumTypeSpec]
    methods: List[ClassMethodSpec]
    signals: List[ClassSignalSpec]
    properties: List[ClassPropertySpec]
    constants: Dict[str, int]

    @property
    def is_object(self) -> bool:
        return True

    def __init__(self, **kwargs):
        self.c_name_prefix = kwargs.pop("c_name_prefix")
        self.is_refcounted = kwargs.pop("is_refcounted")
        self.is_instantiable = kwargs.pop("is_instantiable")
        self.inherits = kwargs.pop("inherits")
        self.api_type = kwargs.pop("api_type")
        self.enums = kwargs.pop("enums")
        self.methods = kwargs.pop("methods")
        self.signals = kwargs.pop("signals")
        self.properties = kwargs.pop("properties")
        self.constants = kwargs.pop("constants")
        super().__init__(
            c_type="gd_object_t",
            cy_type=kwargs["py_type"],
            variant_type_name="GDEXTENSION_VARIANT_TYPE_OBJECT",
            # Of course the object instance live on the heap, but we are talking
            # here about the pointer
            is_stack_only=True,
            **kwargs,
        )


def parse_class(spec: dict, object_size: int) -> ClassTypeSpec:
    spec.setdefault("enums", [])
    spec.setdefault("signals", [])
    spec.setdefault("methods", [])
    spec.setdefault("properties", [])
    spec.setdefault("constants", [])
    spec["inherits"] = spec.get("inherits") or None
    assert spec.keys() == {
        "name",
        "is_refcounted",
        "is_instantiable",
        "inherits",
        "api_type",
        "enums",
        "methods",
        "signals",
        "properties",
        "constants",
    }, spec.keys()

    original_name = spec["name"]
    snake_name = camel_to_snake(original_name)
    # Special case for the Object type, this is because `Object` is too
    # broad of a name (it's easy to mix with Python's regular `object`)
    if spec["name"] == "Object":
        spec["name"] = "GDObject"

    return ClassTypeSpec(
        size=object_size,
        original_name=original_name,
        c_name_prefix=f"gd_{snake_name}",
        py_type=spec["name"],
        is_refcounted=spec["is_refcounted"],
        is_instantiable=spec["is_instantiable"],
        inherits=TypeInUse(spec["inherits"]) if spec["inherits"] else None,
        api_type=spec["api_type"],
        enums=[parse_class_enum(x, class_name=spec["name"]) for x in spec["enums"]],
        methods=[ClassMethodSpec.parse(x) for x in spec["methods"]],
        signals=[ClassSignalSpec.parse(x) for x in spec["signals"]],
        properties=[ClassPropertySpec.parse(x) for x in spec["properties"]],
        constants={x["name"]: x["value"] for x in spec["constants"]},
    )
