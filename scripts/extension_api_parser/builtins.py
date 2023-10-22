from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass

from .utils import *
from .in_use import *
from .type_spec import *


@dataclass
class BuiltinVariantOperatorValue:
    variant_type: str
    gdapi_type: str


VARIANT_OPERATORS = {
    # comparison
    "==": ("equal", "GDEXTENSION_VARIANT_OP_EQUAL"),
    "!=": ("not_equal", "GDEXTENSION_VARIANT_OP_NOT_EQUAL"),
    "<": ("less", "GDEXTENSION_VARIANT_OP_LESS"),
    "<=": ("less_equal", "GDEXTENSION_VARIANT_OP_LESS_EQUAL"),
    ">": ("greater", "GDEXTENSION_VARIANT_OP_GREATER"),
    ">=": ("greater_equal", "GDEXTENSION_VARIANT_OP_GREATER_EQUAL"),
    # mathematic
    "+": ("add", "GDEXTENSION_VARIANT_OP_ADD"),
    "-": ("subtract", "GDEXTENSION_VARIANT_OP_SUBTRACT"),
    "*": ("multiply", "GDEXTENSION_VARIANT_OP_MULTIPLY"),
    "/": ("divide", "GDEXTENSION_VARIANT_OP_DIVIDE"),
    "unary-": ("negate", "GDEXTENSION_VARIANT_OP_NEGATE"),
    "unary+": ("positive", "GDEXTENSION_VARIANT_OP_POSITIVE"),
    "%": ("module", "GDEXTENSION_VARIANT_OP_MODULE"),
    "**": ("power", "GDEXTENSION_VARIANT_OP_POWER"),
    # bitwise
    "<<": ("shift_left", "GDEXTENSION_VARIANT_OP_SHIFT_LEFT"),
    ">>": ("shift_right", "GDEXTENSION_VARIANT_OP_SHIFT_RIGHT"),
    "&": ("bit_and", "GDEXTENSION_VARIANT_OP_BIT_AND"),
    "|": ("bit_or", "GDEXTENSION_VARIANT_OP_BIT_OR"),
    "^": ("bit_xor", "GDEXTENSION_VARIANT_OP_BIT_XOR"),
    "~": ("bit_negate", "GDEXTENSION_VARIANT_OP_BIT_NEGATE"),
    # logic
    "and": ("and", "GDEXTENSION_VARIANT_OP_AND"),
    "or": ("or", "GDEXTENSION_VARIANT_OP_OR"),
    "xor": ("xor", "GDEXTENSION_VARIANT_OP_XOR"),
    "not": ("not", "GDEXTENSION_VARIANT_OP_NOT"),
    # containment
    "in": ("in", "GDEXTENSION_VARIANT_OP_IN"),
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
    base_name: str

    @property
    def c_name(self) -> str:
        cooked_args = [arg.type.c_name_prefix[3:] for arg in self.arguments]
        if not cooked_args:
            return self.base_name
        else:
            return self.base_name + "_from_" + "_".join(cooked_args)

    @classmethod
    def parse(cls, item: dict, c_name_prefix: str) -> "BuiltinConstructorSpec":
        item.setdefault("arguments", [])
        args = [BuiltinMethodArgumentSpec.parse(x) for x in item["arguments"]]
        item["base_name"] = f"{c_name_prefix}_new"
        assert_api_consistency(cls, item)
        return cls(
            index=item["index"],
            arguments=args,
            base_name=item["base_name"],
        )


@dataclass
class BuiltinOperatorSpec:
    name: str
    c_name: str
    original_name: str
    variant_operator_name: str
    right_type: Optional[TypeInUse]
    return_type: TypeInUse

    @classmethod
    def parse(cls, item: dict, c_name_prefix: str) -> "BuiltinOperatorSpec":
        item.setdefault("original_name", item["name"])
        item.setdefault("right_type", None)
        item["name"], item["variant_operator_name"] = VARIANT_OPERATORS[item.pop("name")]
        item["c_name"] = f"{c_name_prefix}_op_{item['name']}"
        if item["right_type"] is not None:
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
            right_type=None if item["right_type"] is None else TypeInUse.parse(item["right_type"]),
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
        # TODO: support Variant & Object !
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


def parse_builtin_enum(spec: dict, builtin_cy_type: str, builtin_py_type: str) -> EnumTypeSpec:
    spec.setdefault("is_bitfield", False)
    assert spec.keys() == {"name", "is_bitfield", "values"}, spec.keys()
    return EnumTypeSpec(
        original_name=spec["name"],
        py_type=f"{builtin_py_type}.{spec['name']}",
        cy_type=f"{builtin_cy_type}.{spec['name']}",
        is_bitfield=spec["is_bitfield"],
        values={x["name"]: x["value"] for x in spec["values"]},
    )


@dataclass(frozen=True, repr=False)
class BuiltinTypeSpec(TypeSpec):
    """
    Non-scalar, non-nil, non-object, non-variant types
    """

    c_name_prefix: str
    indexing_return_type: Optional[TypeInUse]
    is_keyed: bool
    constructors: List["BuiltinConstructorSpec"]
    operators: List["BuiltinOperatorSpec"]
    methods: List["BuiltinMethodSpec"]
    members: List["BuiltinMemberSpec"]
    constants: List["BuiltinConstantSpec"]
    enums: List[EnumTypeSpec]

    @property
    def is_builtin(self) -> bool:
        return True

    @property
    def is_packed_array(self) -> bool:
        return self.original_name.startswith("Packed") and self.original_name.endswith("Array")

    @property
    def packed_array_item_type(self) -> TypeSpec:
        assert self.is_packed_array
        if self.original_name == "PackedByteArray":
            return TYPES_DB["meta:uint8"]
        elif self.original_name == "PackedInt32Array":
            return TYPES_DB["meta:int32"]
        elif self.original_name == "PackedInt64Array":
            return TYPES_DB["meta:int64"]
        elif self.original_name == "PackedFloat32Array":
            return TYPES_DB["meta:float"]
        elif self.original_name == "PackedFloat64Array":
            return TYPES_DB["meta:double"]
        elif self.original_name == "PackedStringArray":
            return TYPES_DB["String"]
        elif self.original_name == "PackedVector2Array":
            return TYPES_DB["Vector2"]
        elif self.original_name == "PackedVector3Array":
            return TYPES_DB["Vector3"]
        elif self.original_name == "PackedColorArray":
            return TYPES_DB["Color"]
        else:
            raise RuntimeError("Unknown packed array type :(")

    def get_constructor_from(self, *args_types: str) -> BuiltinConstructorSpec:
        # `args_types` is expected to contains original names ! (i.e. `String`, `float`)
        for constructor in self.constructors:
            if len(args_types) != len(constructor.arguments):
                continue
            if all(a == b.type.original_name for a, b in zip(args_types, constructor.arguments)):
                return constructor
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

    @property
    def c_struct_members(self) -> List["BuiltinMemberSpec"]:
        return [m for m in self.members if m.offset is not None]


@dataclass(frozen=True, repr=False)
class OpaqueBuiltinTypeSpec(BuiltinTypeSpec):
    """
    Builtin that can only be manipulated by the Godot's API methods (e.g. String, RID)
    """

    @property
    def c_destructor_name(self) -> str:
        if self.is_stack_only:
            raise RuntimeError("Stack only builtin doesn't need to call a destructor !")
        return f"{self.c_name_prefix}_del"

    @property
    def is_opaque_builtin(self) -> bool:
        return True


@dataclass(frozen=True, repr=False)
class TransparentBuiltinTypeSpec(BuiltinTypeSpec):
    """
    Builtin whose c struct layout is fully known to us (e.g. Vector2, Transform2D)
    On top of that we requires:
    - The builtin must not have a destructor (i.e. is_stack_only == True)
    - The builtin's members must be scalar or transparent builtins
    The builtins currently exposed by Godot all respect those requirements, but we
    want to be extra careful in case of future evolution in the API given we take
    them for granted in the code generation
    """

    @property
    def c_destructor_name(self) -> str:
        raise RuntimeError("Transparent builtin doesn't need to call a destructor !")

    @property
    def is_transparent_builtin(self) -> bool:
        return True

    def __post_init__(self):
        assert self.is_stack_only


def _parse_builtin(spec: dict) -> BuiltinTypeSpec:
    # Sanity check on api format
    spec.setdefault("indexing_return_type", None)
    spec.setdefault("operators", [])
    spec.setdefault("constructors", [])
    spec.setdefault("methods", [])
    spec.setdefault("members", [])
    spec.setdefault("constants", [])
    spec.setdefault("enums", [])
    assert spec.keys() == {
        "name",
        "indexing_return_type",
        "is_keyed",
        "operators",
        "methods",
        "constructors",
        "has_destructor",
        "size",
        "members",
        "constants",
        "enums",
    }

    original_name = spec["name"]
    # Gotcha with Transform2D&Transform3D
    snake_name = camel_to_snake(original_name.replace("2D", "2d").replace("3D", "3d"))
    is_stack_only = not spec["has_destructor"]
    c_name_prefix = f"gd_{snake_name}"
    c_type = f"{c_name_prefix}_t"

    # Special case for the very commpon types to make them more explicit (e.g. to
    # avoid mixing Python's regular `str` with Godot `String`)
    # On top of that `str` and Godot `String` are two totally separated
    # string types that require conversions to work together, so it's better
    # to make extra clear they are not the same types !
    if original_name == "String":
        cy_type = "GDString"
    elif original_name == "Array":
        cy_type = "GDArray"
    elif original_name == "Dictionary":
        cy_type = "GDDictionary"
    elif original_name == "Callable":
        cy_type = "GDCallable"
    else:
        cy_type = original_name

    py_type = cy_type

    variant_type_name = f"GDEXTENSION_VARIANT_TYPE_{snake_name.upper()}"
    constructors = [BuiltinConstructorSpec.parse(x, c_name_prefix) for x in spec["constructors"]]
    operators = [BuiltinOperatorSpec.parse(x, c_name_prefix) for x in spec["operators"]]
    methods = [BuiltinMethodSpec.parse(x, c_name_prefix) for x in spec["methods"]]
    members = [BuiltinMemberSpec.parse(x) for x in spec["members"]]
    constants = [BuiltinConstantSpec.parse(x) for x in spec["constants"]]
    enums = [
        parse_builtin_enum(x, builtin_cy_type=cy_type, builtin_py_type=py_type)
        for x in spec["enums"]
    ]

    # TODO: this detection is fine for now given Godot type are either fully
    # transparent or fully opaque. However it would break for a semi-opaque
    # type (e.g. a structure containing a string and a float, so only the float
    # would have an offset)
    c_struct_members = [m for m in members if m.offset is not None]
    is_transparent = bool(c_struct_members)

    if is_transparent:
        return TransparentBuiltinTypeSpec(
            size=spec["size"],
            original_name=original_name,
            c_name_prefix=c_name_prefix,
            py_type=py_type,
            c_type=c_type,
            cy_type=cy_type,
            is_stack_only=is_stack_only,
            variant_type_name=variant_type_name,
            indexing_return_type=TypeInUse(spec["indexing_return_type"])
            if spec["indexing_return_type"]
            else None,
            is_keyed=spec["is_keyed"],
            constructors=constructors,
            operators=operators,
            methods=methods,
            members=members,
            constants=constants,
            enums=enums,
        )
    else:
        return OpaqueBuiltinTypeSpec(
            size=spec["size"],
            original_name=original_name,
            c_name_prefix=c_name_prefix,
            py_type=py_type,
            c_type=c_type,
            cy_type=cy_type,
            is_stack_only=is_stack_only,
            variant_type_name=variant_type_name,
            indexing_return_type=TypeInUse(spec["indexing_return_type"])
            if spec["indexing_return_type"]
            else None,
            is_keyed=spec["is_keyed"],
            constructors=constructors,
            operators=operators,
            methods=methods,
            members=members,
            constants=constants,
            enums=enums,
        )


def parse_builtins_ignore_scalars_and_nil(builtin_classes: List[dict]) -> List[BuiltinTypeSpec]:
    builtins: List[BuiltinTypeSpec] = []
    for spec in builtin_classes:
        if spec["name"] in ("Nil", "bool", "int", "float"):
            continue

        builtins.append(_parse_builtin(spec))

    return builtins
