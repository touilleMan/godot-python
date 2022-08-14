import enum
from typing import Dict, Optional, List
from dataclasses import dataclass
from string import ascii_uppercase

from .utils import correct_name, assert_api_consistency
from .type import TypeInUse, ValueInUse


# Empirical list of return values:
# AABB
# Array
# Basis
# Callable
# Color
# Dictionary
# NodePath
# Object
# PackedByteArray
# PackedColorArray
# PackedFloat32Array
# PackedFloat64Array
# PackedInt32Array
# PackedInt64Array
# PackedStringArray
# PackedVector2Array
# PackedVector3Array
# Plane
# Quaternion
# RID
# Rect2
# Rect2i
# String
# StringName
# Transform2D
# Transform3D
# Variant
# Vector2
# Vector2i
# Vector3
# Vector3i
# bool
# float
# int
BUILTINS_NAMES = {
    "Variant": ("GDNativeVariantPtr", "void*"),
    "StringName": ("GDNativeStringNamePtr", "void*"),
    "String": ("GDNativeStringPtr", "void*"),
    "Object": ("GDNativeObjectPtr", "void*"),
    "Type": ("GDNativeTypePtr", "void*"),
    "Extension": ("GDNativeExtensionPtr", "void*"),
    "MethodBind": ("GDNativeMethodBindPtr", "void*"),
    "int": ("GDNativeInt", "int64_t"),
    "bool": ("GDNativeBool", "uint8_t"),
}


@dataclass
class BuiltinVariantOperatorValue:
    variant_type: str
    gdapi_type: str


VARIANT_OPERATORS = {
    # comparison
    "==": ("equal", "GDNATIVE_VARIANT_OP_EQUAL"),
    "!=": ("not_equal", "GDNATIVE_VARIANT_OP_NOT_EQUAL"),
    "<": ("less", "GDNATIVE_VARIANT_OP_LESS"),
    "<=": ("less_equal", "GDNATIVE_VARIANT_OP_LESS_EQUAL"),
    ">": ("greater", "GDNATIVE_VARIANT_OP_GREATER"),
    ">=": ("greater_equal", "GDNATIVE_VARIANT_OP_GREATER_EQUAL"),
    # mathematic
    "+": ("add", "GDNATIVE_VARIANT_OP_ADD"),
    "-": ("subtract", "GDNATIVE_VARIANT_OP_SUBTRACT"),
    "*": ("multiply", "GDNATIVE_VARIANT_OP_MULTIPLY"),
    "/": ("divide", "GDNATIVE_VARIANT_OP_DIVIDE"),
    "unary-": ("negate", "GDNATIVE_VARIANT_OP_NEGATE"),
    "unary+": ("positive", "GDNATIVE_VARIANT_OP_POSITIVE"),
    "%": ("module", "GDNATIVE_VARIANT_OP_MODULE"),
    "**": ("power", "GDNATIVE_VARIANT_OP_POWER"),
    # bitwise
    "<<": ("shift_left", "GDNATIVE_VARIANT_OP_SHIFT_LEFT"),
    ">>": ("shift_right", "GDNATIVE_VARIANT_OP_SHIFT_RIGHT"),
    "&": ("bit_and", "GDNATIVE_VARIANT_OP_BIT_AND"),
    "|": ("bit_or", "GDNATIVE_VARIANT_OP_BIT_OR"),
    "^": ("bit_xor", "GDNATIVE_VARIANT_OP_BIT_XOR"),
    "~": ("bit_negate", "GDNATIVE_VARIANT_OP_BIT_NEGATE"),
    # logic
    "and": ("and", "GDNATIVE_VARIANT_OP_AND"),
    "or": ("or", "GDNATIVE_VARIANT_OP_OR"),
    "xor": ("xor", "GDNATIVE_VARIANT_OP_XOR"),
    "not": ("not", "GDNATIVE_VARIANT_OP_NOT"),
    # containment
    "in": ("in", "GDNATIVE_VARIANT_OP_IN"),
}


@dataclass
class BuiltinMethodArgumentSpec:
    name: str
    original_name: str
    type: TypeInUse
    default_value: Optional[ValueInUse]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinMethodArgumentSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("default_value", None)
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=TypeInUse(item["type"]),
            default_value=ValueInUse(item["default_value"]) if item["default_value"] else None,
        )


@dataclass
class BuiltinConstructorSpec:
    index: int
    arguments: List[BuiltinMethodArgumentSpec]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinConstructorSpec":
        item.setdefault("arguments", [])
        assert_api_consistency(cls, item)
        return cls(
            index=item["index"],
            arguments=[BuiltinMethodArgumentSpec.parse(x) for x in item["arguments"]],
        )


@dataclass
class BuiltinOperatorSpec:
    name: str
    original_name: str
    variant_operator_name: str
    right_type: TypeInUse
    return_type: TypeInUse

    @classmethod
    def parse(cls, item: dict) -> "BuiltinOperatorSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("right_type", "Nil")
        item["name"], item["variant_operator_name"] = VARIANT_OPERATORS[item.pop("name")]
        if item["right_type"] != "Nil":
            item["name"] = f"{item['name']}_{item['right_type'].lower()}"
        assert_api_consistency(cls, item)
        return cls(
            name=item["name"],
            original_name=item["original_name"],
            variant_operator_name=item["variant_operator_name"],
            # `right_type` is kind of a special case: most of the time `Nil/None` is
            # used to represent the absence of a value (typically in a return type),
            # but here we want to compare a builtin value with the constant representing
            # emptiness.
            right_type=TypeInUse(item["right_type"]),
            return_type=TypeInUse(item["return_type"]),
        )


@dataclass
class BuiltinMemberSpec:
    name: str
    original_name: str
    offset: Optional[int]
    type: TypeInUse

    @classmethod
    def parse(cls, item: dict) -> "BuiltinMemberSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("offset", None)
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            offset=item["offset"],
            type=TypeInUse(item["type"]),
        )


@dataclass
class BuiltinConstantSpec:
    name: str
    original_name: str
    type: TypeInUse
    value: str

    @classmethod
    def parse(cls, item: dict) -> "BuiltinConstantSpec":
        item.setdefault("original_name", item["name"])
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=TypeInUse(item["type"]),
            value=item["value"],
        )


@dataclass
class BuiltinMethodSpec:
    name: str
    original_name: str
    return_type: Optional[TypeInUse]
    is_vararg: bool
    is_const: bool
    is_static: bool
    hash: int
    arguments: List[BuiltinMethodArgumentSpec]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinMethodSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("arguments", [])
        item.setdefault("return_type", "Nil")
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            return_type=TypeInUse(item["return_type"]),
            is_vararg=item["is_vararg"],
            is_const=item["is_const"],
            is_static=item["is_static"],
            hash=item["hash"],
            arguments=[BuiltinMethodArgumentSpec.parse(x) for x in item["arguments"]],
        )


@dataclass
class BuiltinEnumSpec:
    name: str
    original_name: str
    is_bitfield: bool
    values: List[Dict[str, int]]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinEnumSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("is_bitfield", False)
        assert_api_consistency(cls, item)
        return cls(
            name=item["name"],
            original_name=item["original_name"],
            is_bitfield=item["is_bitfield"],
            values=[{x["name"]: x["value"]} for x in item["values"]],
        )


@dataclass
class BuiltinSpec:
    # Name as it is in `extension_api.json`
    original_name: str
    # Name used for the binding (e.g. `from godot import Vector2`)
    name: str
    # Name used for the C structure binding (e.g. `from godot.hazmat.gdapi cimport Vector2`)
    c_struct_name: str
    is_scalar: bool
    size: int
    indexing_return_type: Optional[str]
    is_keyed: bool
    constructors: List[BuiltinConstructorSpec]
    has_destructor: bool
    operators: List[BuiltinOperatorSpec]
    methods: List[BuiltinMethodSpec]
    members: List[BuiltinMemberSpec]
    constants: List[BuiltinConstantSpec]
    variant_type_name: str
    enums: List[BuiltinEnumSpec]

    @property
    def c_struct_members(self) -> List[BuiltinMemberSpec]:
        struct_members = [m for m in self.members if m.offset is not None]
        if struct_members:
            # Sanity check
            assert sum(m.type.size for m in struct_members) == self.size
            return struct_members
        else:
            # Opaque structure
            return []

    @classmethod
    def parse(cls, item: dict) -> "BuiltinSpec":
        item["is_scalar"] = item["name"] in ("Nil", "bool", "int", "float")
        # Camel to upper snake case
        snake = ""
        # Gotcha with Transform2D&Transform3D
        for c in item["name"].replace("2D", "2d").replace("3D", "3d"):
            if c in ascii_uppercase and snake and snake[-1] not in ascii_uppercase:
                snake += "_"
            snake += c
        item["variant_type_name"] = f"GDNATIVE_VARIANT_TYPE_{snake.upper()}"
        item.setdefault("original_name", item["name"])
        # Special case for the String type, this is because `String` is too
        # broad of a name (it's easy to mix with Python's regular `str`)
        # On top of that `str` and Godot `String` are two totally separated
        # string types that require conversions to work together, so it's better
        # to make extra clear they are not the same types !
        if item["name"] == "String":
            item["name"] = "GDString"
        item.setdefault("c_struct_name", item["name"])
        item.setdefault("indexing_return_type", None)
        item.setdefault("methods", [])
        item.setdefault("members", [])
        item.setdefault("constants", [])
        item.setdefault("enums", [])
        assert_api_consistency(cls, item)
        assert len(item["constructors"]) >= 1

        return cls(
            original_name=item["original_name"],
            # name=correct_type_name(item["name"]),
            name=item["name"],
            c_struct_name=item["c_struct_name"],
            is_scalar=item["is_scalar"],
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
            enums=[BuiltinEnumSpec.parse(x) for x in item["enums"]],
        )
