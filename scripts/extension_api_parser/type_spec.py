from __future__ import annotations

from dataclasses import dataclass
import string


# We devide types into three categories:
# - scalars (native types already existing in C/Cython, e.g. float, int32 etc.)
# - builtins
# - classes


@dataclass(slots=True)
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
    # e.g. `GDEXTENSION_VARIANT_TYPE_BOOL`
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

    @property
    def is_native_structure(self) -> bool:
        return False


@dataclass(slots=True)
class ScalarTypeSpec(TypeSpec):
    """
    Type is a scalar (e.g. int, float) but not nil
    """

    @property
    def snake_name(self) -> str:
        return self.py_type

    def __init__(self, **kwargs):
        assert kwargs.setdefault("is_stack_only", True)
        TypeSpec.__init__(
            self,
            **kwargs,
        )


@dataclass(slots=True)
class RawCScalarTypeSpec(ScalarTypeSpec):
    """
    Special case for C types used in the native structures definition.

    Those types have a platform-dependent size and hence must be provided verbatim
    in Cyton/C code (otherwise the compiler might pick the wrong size for them...).
    """

    def __init__(self, c_type: str):
        TypeSpec.__init__(
            self,
            is_stack_only=True,
            variant_type_name="GDEXTENSION_VARIANT_TYPE_NIL",  # Never accessed dummy value
            size=0,  # Never accessed dummy value
            py_type="",  # Never accessed dummy value
            cy_type="",  # Never accessed dummy value
            original_name=c_type,
            c_type=c_type,
        )

    def __getattribute__(self, name: str):
        if name in ("variant_type_name", "size", "py_type", "cy_type"):
            raise RuntimeError(
                "Raw C scalar type ! Only `c_type` should be needed when defining the native structures"
            )
        return object.__getattribute__(self, name)


@dataclass(slots=True)
class EnumTypeSpec(ScalarTypeSpec):
    """
    Godot enum (e.g. godot_error, Camera::KeepAspect), note they are always
    composed of int values like a regular C enum
    """

    is_bitfield: bool
    original_values: dict[str, int]
    c_values: dict[str, int]
    py_values: dict[str, int]

    def __init__(self, **kwargs):
        self.is_bitfield = kwargs.pop("is_bitfield")
        self.original_values = kwargs.pop("values")
        self.c_values = self.original_values

        # Detect the common prefix
        first_key = next(iter(self.original_values.keys()))  # Any key will do it
        parts = iter(first_key.split("_"))
        prefix = ""
        while True:
            try:
                candidate_prefix = f"{next(parts)}_" if not prefix else f"{prefix}{next(parts)}_"
            except StopIteration:
                break
            if all(k.startswith(candidate_prefix) for k in self.original_values):
                prefix = candidate_prefix
                continue
            else:
                break

        def _strip_prefix(k: str) -> str:
            if k.startswith(prefix):
                new = k[len(prefix) :]
                if kwargs["original_name"] == "Key":
                    # Special case for `KEY_0`, `KEY_A`, etc.
                    if new in string.ascii_uppercase or new in string.digits:
                        new = f"K_{new}"
                if kwargs["original_name"] == "MethodFlags":
                    # Special case: all types are `FLAG_xxx` except for `FLAGS_DEFAULT`
                    needle = "FLAG_"
                    if new.startswith(needle):
                        new = new.removeprefix(needle)
                return new
            else:
                return k

        self.py_values = {_strip_prefix(k): v for k, v in self.original_values.items()}
        # Remove the `MAX` marker since it is not an actual valid value
        self.py_values.pop("MAX", None)

        ScalarTypeSpec.__init__(
            self,
            is_stack_only=True,
            size=4,
            c_type="int",
            variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
            **kwargs,
        )


@dataclass(slots=True)
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
        TypeSpec.__init__(
            self,
            size=0,
            original_name="Nil",
            is_stack_only=True,
            variant_type_name="GDEXTENSION_VARIANT_TYPE_NIL",
            py_type="",  # Never accessed dummy value
            c_type="",  # Never accessed dummy value
            cy_type="",  # Never accessed dummy value
        )

    def __getattribute__(self, name: str):
        if name in ("py_type", "c_type", "cy_type"):
            raise RuntimeError(
                "Nil type ! Should handle this by hand with a if condition on `<my_type>.is_nil`"
            )
        return object.__getattribute__(self, name)


@dataclass(slots=True)
class VariantTypeSpec(TypeSpec):
    def __init__(self, size):
        TypeSpec.__init__(
            self,
            size=size,
            is_stack_only=False,
            original_name="Variant",
            py_type="GDAny",
            c_type="gd_variant_t",
            cy_type="object",
            variant_type_name="",  # Never accessed dummy value
        )

    @property
    def snake_name(self) -> str:
        return "variant"

    def __getattribute__(self, name: str):
        if name == "variant_type_name":
            raise RuntimeError(
                "Variant type ! Should handle this by hand with a if condition on `<my_type>.is_variant`"
            )
        return object.__getattribute__(self, name)


# Type alias
TypeDBEntry = str


def TYPES_DB_REGISTER_TYPE(id: str, type_spec: TypeSpec) -> None:
    if TYPES_DB.setdefault(id, type_spec) is not type_spec:
        raise RuntimeError(f"type {id} already registered !")


# Will be completed when calling `parse_extension_api_json`
TYPES_DB: dict[TypeDBEntry, TypeSpec] = {
    "Nil": NilTypeSpec(),
    "bool": ScalarTypeSpec(
        size=1,
        original_name="bool",
        c_type="uint8_t",
        cy_type="uint8_t",
        py_type="bool",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_BOOL",
    ),
    # Note `float` will be added at runtime since its size depends of the build config
    # `int` is always 8bytes long
    "int": ScalarTypeSpec(
        size=8,
        original_name="int",
        c_type="int64_t",
        cy_type="int64_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    # Types marked as `c` are used in the native structures definition and have
    # a size that depends on the compilation platform.
    "c:int": RawCScalarTypeSpec(c_type="int"),
    "c:float": RawCScalarTypeSpec(c_type="float"),
    "c:double": RawCScalarTypeSpec(c_type="double"),
    # Types marked as `meta` are used in the classes method args/return types
    # Note `meta:real` will be added at runtime since its size depends of the build config
    "meta:int8": ScalarTypeSpec(
        size=1,
        original_name="int8",
        c_type="int8_t",
        cy_type="int8_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:int16": ScalarTypeSpec(
        size=2,
        original_name="int16",
        c_type="int16_t",
        cy_type="int16_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:int32": ScalarTypeSpec(
        size=4,
        original_name="int32",
        c_type="int32_t",
        cy_type="int32_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:int64": ScalarTypeSpec(
        size=8,
        original_name="int64",
        c_type="int64_t",
        cy_type="int64_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:uint8": ScalarTypeSpec(
        size=1,
        original_name="uint8",
        c_type="uint8_t",
        cy_type="uint8_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:uint16": ScalarTypeSpec(
        size=2,
        original_name="uint16",
        c_type="uint16_t",
        cy_type="uint16_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:uint32": ScalarTypeSpec(
        size=4,
        original_name="uint32",
        c_type="uint32_t",
        cy_type="uint32_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:uint64": ScalarTypeSpec(
        size=8,
        original_name="uint64",
        c_type="uint64_t",
        cy_type="uint64_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    "meta:float": ScalarTypeSpec(
        size=4,
        original_name="float",
        c_type="float",
        cy_type="float",
        py_type="float",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_FLOAT",
    ),
    "meta:double": ScalarTypeSpec(
        size=8,
        original_name="double",
        c_type="double",
        cy_type="double",
        py_type="float",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_FLOAT",
    ),
    "meta:char32": ScalarTypeSpec(
        size=4,
        original_name="char32",
        c_type="char32_t",
        cy_type="char32_t",
        py_type="int",
        variant_type_name="GDEXTENSION_VARIANT_TYPE_INT",
    ),
    # The rest of the types will be added during parsing of builtins&classes
}


def ensure_types_db_consistency():
    from .builtins import BuiltinTypeSpec

    # Now check the assumption we need on transparent builtins (see
    # `TransparentBuiltinTypeSpec` definition).
    # We had to wait until all the builtins has been parsed to do the check
    # given a transparent builtin can be made of other builtins.
    for t in TYPES_DB.values():
        if t.is_transparent_builtin:
            assert isinstance(t, BuiltinTypeSpec)
            members = t.c_struct_members
            assert members

            # Ensure the members describe the entire content of the builtin
            assert sum(m.type.size for m in members) == t.size

            # Ensure the builtin is composed of scalar or transparent builtins
            for m in members:
                assert m.type.is_scalar or m.type.is_transparent_builtin
