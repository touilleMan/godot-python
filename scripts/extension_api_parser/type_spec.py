from typing import Dict, Iterable, Optional
from dataclasses import dataclass


# We devide types into three categories:
# - scalars (native types already existing in C/Cython, e.g. float, int32 etc.)
# - builtins
# - classes


@dataclass(frozen=True, repr=False)
class TypeSpec:
    size: int
    # Type used within Godot `extension_api.json`
    original_name: str
    # Type used for PEP 484 Python typing
    py_type: str
    # Type used when calling C api functions
    c_type: str
    # Type used in Cython, basically similar to c_type for scalars&enums
    # and to py_type for Godot objects&builtins
    cy_type: str
    # Type doesn't use the heap (hence no need for freeing it)
    is_stack_only: bool
    # e.g. `GDNATIVE_VARIANT_TYPE_BOOL`
    variant_type_name: str

    def __repr__(self):
        return f"<{type(self).__name__} {self.original_name}>"

    @property
    def is_nil(self) -> bool:
        return isinstance(self, NilTypeSpec)

    @property
    def is_variant(self) -> bool:
        return isinstance(self, VariantTypeSpec)

    @property
    def is_enum(self) -> bool:
        return isinstance(self, EnumTypeSpec)

    @property
    def is_scalar(self) -> bool:
        return isinstance(self, ScalarTypeSpec)

    @property
    def is_object(self) -> bool:
        return False

    @property
    def is_builtin(self) -> bool:
        return False

    @property
    def is_transparent_builtin(self) -> bool:
        return False

    @property
    def is_opaque_builtin(self) -> bool:
        return False


class ScalarTypeSpec(TypeSpec):
    """
    Type is a scalar (e.g. int, float) but not nil
    """

    @property
    def c_name_prefix(self) -> str:
        return f"gd_{self.py_type}"

    def __init__(self, **kwargs):
        assert kwargs.setdefault("is_stack_only", True)
        super().__init__(
            **kwargs,
        )


class EnumTypeSpec(ScalarTypeSpec):
    """
    Godot enum (e.g. godot_error, Camera::KeepAspect), note they are always
    composed of int values like a regular C enum
    """

    is_bitfield: bool
    values: Dict[str, int]

    def __init__(self, **kwargs):
        self.is_bitfield = kwargs.pop("is_bitfield")
        self.values = kwargs.pop("values")
        super().__init__(
            is_stack_only=True,
            size=4,
            c_type="int",
            variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
            **kwargs,
        )


class NilTypeSpec(TypeSpec):
    """
    `Nil` is a special case, it is only needed for `BuiltinOperatorSpec.right_type`
    and in `ValueInUse`. But it meaning can differ:
    - `BuiltinOperatorSpec.right_type`: `Nil` represents the absence of value
    - `ValueInUse`: `Nil` represents a singleton value (like `None` in Python)
    So the template code is expected to use the `is_nil` attribute and do ad-hoc
    code according to it need instead of relying on py/c/cy_type
    """

    def __init__(self):
        super().__init__(
            size=0,
            original_name="Nil",
            is_stack_only=True,
            variant_type_name="GDNATIVE_VARIANT_TYPE_NIL",
            py_type="",  # Never accessed dummy value
            c_type="",  # Never accessed dummy value
            cy_type="",  # Never accessed dummy value
        )

    def __getattribute__(self, name: str):
        if name in ("py_type", "c_type", "cy_type"):
            raise RuntimeError(
                "Nil type ! Should handle this by hand with a if condition on `<my_type>.is_nil`"
            )
        return super().__getattribute__(name)


class VariantTypeSpec(TypeSpec):
    def __init__(self, size):
        super().__init__(
            size=size,
            is_stack_only=False,
            original_name="Variant",
            py_type="GDAny",
            c_type="gd_variant_t",
            cy_type="object",
            variant_type_name="",  # Never accessed dummy value
        )

    @property
    def c_name_prefix(self):
        return "gd_variant"

    def __getattribute__(self, name: str):
        if name == "variant_type_name":
            raise RuntimeError(
                "Variant type ! Should handle this by hand with a if condition on `<my_type>.is_variant`"
            )
        return super().__getattribute__(name)


# Type alias
TypeDBEntry = str


def TYPES_DB_REGISTER_TYPE(id: str, type_spec: "TypeSpec") -> None:
    if TYPES_DB.setdefault(id, type_spec) is not type_spec:
        raise RuntimeError(f"type {id} already registered !")


# Will be completed when calling `parse_extension_api_json`
TYPES_DB: Dict[TypeDBEntry, "TypeSpec"] = {
    "Nil": NilTypeSpec(),
    "bool": ScalarTypeSpec(
        size=1,
        original_name="bool",
        c_type="uint8_t",
        cy_type="uint8_t",
        py_type="bool",
        variant_type_name="GDNATIVE_VARIANT_TYPE_BOOL",
    ),
    # int is always 8bytes long
    "int": ScalarTypeSpec(
        size=8,
        original_name="int",
        c_type="uint64_t",
        cy_type="uint64_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    # Types marked as `meta` are used in the classes method args/return types
    "meta:int8": ScalarTypeSpec(
        size=1,
        original_name="int8",
        c_type="int8_t",
        cy_type="int8_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:int16": ScalarTypeSpec(
        size=2,
        original_name="int16",
        c_type="int16_t",
        cy_type="int16_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:int32": ScalarTypeSpec(
        size=4,
        original_name="int32",
        c_type="int32_t",
        cy_type="int32_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:int64": ScalarTypeSpec(
        size=8,
        original_name="int64",
        c_type="int64_t",
        cy_type="int64_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:uint8": ScalarTypeSpec(
        size=1,
        original_name="uint8",
        c_type="uint8_t",
        cy_type="uint8_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:uint16": ScalarTypeSpec(
        size=2,
        original_name="uint16",
        c_type="uint16_t",
        cy_type="uint16_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:uint32": ScalarTypeSpec(
        size=4,
        original_name="uint32",
        c_type="uint32_t",
        cy_type="uint32_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:uint64": ScalarTypeSpec(
        size=8,
        original_name="uint64",
        c_type="uint64_t",
        cy_type="uint64_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
    ),
    "meta:float": ScalarTypeSpec(
        size=4,
        original_name="float",
        c_type="float",
        cy_type="float",
        py_type="float",
        variant_type_name="GDNATIVE_VARIANT_TYPE_FLOAT",
    ),
    "meta:double": ScalarTypeSpec(
        size=8,
        original_name="double",
        c_type="double",
        cy_type="double",
        py_type="float",
        variant_type_name="GDNATIVE_VARIANT_TYPE_FLOAT",
    ),
    # The rest of the types will be added during parsing of builtins&classes
}


def ensure_types_db_consistency():
    # Now check the assumption we need on transparent builtins (see
    # `TransparentBuiltinTypeSpec` definition).
    # We had to wait until all the builtins has been parsed to do the check
    # given a transparent builtin can be made of other builtins.
    for t in TYPES_DB.values():
        if t.is_transparent_builtin:
            members = t.c_struct_members
            assert members

            # Ensure the members describe the entire content of the builtin
            assert sum(m.type.size for m in members) == t.size

            # Ensure the builtin is composed of scalar or transparent builtins
            for m in members:
                assert m.type.is_scalar or m.type.is_transparent_builtin
