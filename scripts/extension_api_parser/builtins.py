from typing import Dict, Optional, List
from dataclasses import dataclass

from .utils import correct_name, assert_api_consistency, camel_to_snake
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
        arg_type = TypeInUse.parse(item["type"])
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            type=arg_type,
            default_value=ValueInUse.parse(arg_type, item["default_value"])
            if item["default_value"]
            else None,
        )


@dataclass
class BuiltinConstructorSpec:
    index: int
    arguments: List[BuiltinMethodArgumentSpec]
    c_name: str

    @classmethod
    def parse(cls, item: dict, c_name_prefix: str) -> "BuiltinConstructorSpec":
        item.setdefault("arguments", [])
        args = [BuiltinMethodArgumentSpec.parse(x) for x in item["arguments"]]
        cooked_args = [arg.type.type_name.lower() for arg in args]
        if not cooked_args:
            item["c_name"] = f"{c_name_prefix}_new"
        else:
            item["c_name"] = f"{c_name_prefix}_new_from_" + "_".join(cooked_args)
        assert_api_consistency(cls, item)
        return cls(
            index=item["index"],
            c_name=item["c_name"],
            arguments=args,
        )


@dataclass
class BuiltinOperatorSpec:
    name: str
    c_name: str
    original_name: str
    variant_operator_name: str
    right_type: TypeInUse
    return_type: TypeInUse

    @classmethod
    def parse(cls, item: dict, c_name_prefix: str) -> "BuiltinOperatorSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("right_type", "Nil")
        item["name"], item["variant_operator_name"] = VARIANT_OPERATORS[item.pop("name")]
        item["c_name"] = f"{c_name_prefix}_op_{item['name']}"
        if item["right_type"] != "Nil":
            item["name"] = f"{item['name']}_{item['right_type'].lower()}"
        assert_api_consistency(cls, item)
        return cls(
            name=item["name"],
            c_name=item["c_name"],
            original_name=item["original_name"],
            variant_operator_name=item["variant_operator_name"],
            # `right_type` is kind of a special case: most of the time `Nil/None` is
            # used to represent the absence of a value (typically in a return type),
            # but here we want to compare a builtin value with the constant representing
            # emptiness.
            right_type=TypeInUse.parse(item["right_type"]),
            return_type=TypeInUse.parse(item["return_type"]),
        )


@dataclass
class BuiltinMemberSpec:
    name: str
    original_name: str
    offset: Optional[int]
    type: TypeInUse

    @property
    def is_in_struct(self) -> bool:
        return self.offset is not None

    @classmethod
    def parse(cls, item: dict) -> "BuiltinMemberSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("offset", None)
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            original_name=item["original_name"],
            offset=item["offset"],
            type=TypeInUse.parse(item["type"]),
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
            type=TypeInUse.parse(item["type"]),
            value=item["value"],
        )


@dataclass
class BuiltinMethodSpec:
    name: str
    c_name: str
    original_name: str
    return_type: Optional[TypeInUse]
    is_vararg: bool
    is_const: bool
    is_static: bool
    hash: int
    arguments: List[BuiltinMethodArgumentSpec]

    @property
    def contains_unsuported_types(self) -> bool:
        # TODO: support Varaint & Object !
        def _unsuported_type(t):
            return t.is_variant or t.is_object

        return any(_unsuported_type(a.type) for a in self.arguments) or _unsuported_type(
            self.return_type
        )

    @classmethod
    def parse(cls, item: dict, c_name_prefix: str) -> "BuiltinMethodSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("arguments", [])
        item.setdefault("return_type", "Nil")
        item.setdefault("c_name", f"{c_name_prefix}_{item['original_name']}")
        assert_api_consistency(cls, item)
        return cls(
            name=correct_name(item["name"]),
            c_name=item["c_name"],
            original_name=item["original_name"],
            return_type=TypeInUse.parse(item["return_type"]),
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
    values: Dict[str, int]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinEnumSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("is_bitfield", False)
        assert_api_consistency(cls, item)
        return cls(
            name=item["name"],
            original_name=item["original_name"],
            is_bitfield=item["is_bitfield"],
            values={x["name"]: x["value"] for x in item["values"]},
        )


@dataclass(repr=False)
class BuiltinSpec:
    # Name as it is in `extension_api.json`
    original_name: str
    # Name used for the binding (e.g. `from godot import Vector2`)
    name: str
    # Name used for the C structure binding (e.g. `from godot.hazmat.gdapi cimport gd_vector2_t`)
    snake_name: str
    is_scalar: bool
    is_nil: bool
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

    def __repr__(self):
        return f"{type(self).__name__}({self.name})"

    @property
    def c_name_prefix(self) -> str:
        return f"gd_{self.snake_name}"

    @property
    def c_destructor_name(self) -> str:
        assert self.has_destructor
        return f"gd_{self.snake_name}_del"

    @property
    def c_struct_name(self) -> str:
        return f"gd_{self.snake_name}_t"

    @property
    def is_packed_array(self) -> bool:
        return self.original_name.startswith("Packed") and self.original_name.endswith("Array")

    def get_constructor_index_from(self, *args_types: str) -> int:
        # `args_types` is expected to contains py types ! (i.e. `GDString`, `float`)
        for constructor in self.constructors:
            if len(args_types) != len(constructor.arguments):
                continue
            if all(a == b.type.py_type for a, b in zip(args_types, constructor.arguments)):
                return constructor.index
        else:
            raise RuntimeError("No compatible constructor in extension_api.json !")

    @property
    def clone_constructor_index(self) -> int:
        return next(
            c.index
            for c in self.constructors
            if len(c.arguments) == 1 and c.arguments[0].type.type_name == self.original_name
        )

    @property
    def empty_constructor_index(self) -> int:
        return next(c.index for c in self.constructors if len(c.arguments) == 0)

    # Returns true if the builtin structure is entirely composed of it members
    # (this means we can initialize this structure without calling Godot)
    @property
    def is_transparent_c_struct(self) -> bool:
        # TODO: this detection is fine for now given Godot type are either fully
        # transparent or fully opaque. However it would break for a semi-opaque
        # type (e.g. a structure containing a string and a float, so only the float
        # would have an offset)
        return bool(self.c_struct_members)

    @property
    def c_struct_members(self) -> List[BuiltinMemberSpec]:
        # Don't try any sanity check, this is because this property is going to
        # be used by `register_builtins_in_types_db`, and at this point all types
        # are not resolvable yet.
        # So we leave the sanity check to `register_builtins_in_types_db`.
        return [m for m in self.members if m.offset is not None]

    @classmethod
    def parse(cls, item: dict) -> "BuiltinSpec":
        item["is_scalar"] = item["name"] in ("Nil", "bool", "int", "float")
        item["is_nil"] = item["name"] == "Nil"
        # Gotcha with Transform2D&Transform3D
        snake_name = camel_to_snake(item["name"].replace("2D", "2d").replace("3D", "3d"))
        item["snake_name"] = snake_name
        item["variant_type_name"] = f"GDNATIVE_VARIANT_TYPE_{snake_name.upper()}"
        item.setdefault("original_name", item["name"])
        # Special case for the very commpon types to make them more explicit (e.g. to
        # avoid mixing Python's regular `str` with Godot `String`)
        # On top of that `str` and Godot `String` are two totally separated
        # string types that require conversions to work together, so it's better
        # to make extra clear they are not the same types !
        if item["name"] == "String":
            item["name"] = "GDString"
        elif item["name"] == "Array":
            item["name"] = "GDArray"
        elif item["name"] == "Dictionary":
            item["name"] = "GDDictionary"
        elif item["name"] == "Callable":
            item["name"] = "GDCallable"
        item.setdefault("indexing_return_type", None)
        item.setdefault("methods", [])
        item.setdefault("members", [])
        item.setdefault("constants", [])
        item.setdefault("enums", [])
        assert_api_consistency(cls, item)
        assert len(item["constructors"]) >= 1
        # TODO: remove me once https://github.com/godotengine/godot/pull/64692 is merged
        if item["name"] in ("Transform2D", "AABB", "Basis", "Transform3D"):
            item["has_destructor"] = False
        c_name_prefix = f"gd_{snake_name}"
        return cls(
            original_name=item["original_name"],
            name=item["name"],
            snake_name=snake_name,
            is_scalar=item["is_scalar"],
            is_nil=item["is_nil"],
            size=item["size"],
            indexing_return_type=item["indexing_return_type"],
            is_keyed=item["is_keyed"],
            constructors=[
                BuiltinConstructorSpec.parse(x, c_name_prefix) for x in item["constructors"]
            ],
            has_destructor=item["has_destructor"],
            operators=[BuiltinOperatorSpec.parse(x, c_name_prefix) for x in item["operators"]],
            methods=[BuiltinMethodSpec.parse(x, c_name_prefix) for x in item["methods"]],
            members=[BuiltinMemberSpec.parse(x) for x in item["members"]],
            constants=[BuiltinConstantSpec.parse(x) for x in item["constants"]],
            variant_type_name=item["variant_type_name"],
            enums=[BuiltinEnumSpec.parse(x) for x in item["enums"]],
        )
