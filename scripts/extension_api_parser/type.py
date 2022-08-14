from typing import TYPE_CHECKING, Dict, Iterable
from dataclasses import dataclass, replace


if TYPE_CHECKING:
    from .api import GlobalEnumSpec
    from .classes import ClassSpec
    from .builtins import BuiltinSpec


# Type alias
TypeDBEntry = str


# We devide types into three categories:
# - scalars (native types already existing in C/Cython, e.g. float, int32 etc.)
# - builtins
# - classes


@dataclass
class TypeSpec:
    size: int
    # Type used within Godot `extension_api.json`
    gdapi_type: str
    # Type used for PEP 484 Python typing
    py_type: str
    # Type used when calling C api functions
    c_type: str
    # Type used in Cython, basically similar to c_type for scalars&enums
    # and to py_type for Godot objects&builtins
    cy_type: str
    # Type is a Godot object (i.e. defined in api.json)
    is_object: bool = False
    # Type is a Godot builtin (e.g. Vector2)
    is_builtin: bool = False
    # Nil type (aka None, or NULL) is very special ;-)
    is_nil: bool = False
    # Type is a scalar (e.g. int, float) or void
    is_scalar: bool = False
    # Type doesn't use the heap (hence no need for freeing it)
    is_stack_only: bool = False
    # Type is an enum (e.g. godot_error, Camera::KeepAspect)
    is_enum: bool = False
    # e.g. `GDNATIVE_VARIANT_TYPE_BOOL`
    # Default to an invalid value so that we detect incorrect use during Cython compilation
    variant_type_name: str = "<n/a>"

    def __post_init__(self):
        if self.is_scalar:
            assert not self.is_object
            assert not self.is_builtin
            assert self.is_stack_only
        if self.is_object:
            assert not self.is_builtin
            assert not self.is_scalar
            assert not self.is_stack_only
        if self.is_builtin:
            assert not self.is_object
            assert not self.is_scalar


# `Nil` is a special case, it is only needed for `BuiltinOperatorSpec.right_type`
# and in `ValueInUse`. But it meaning can differ:
# - `BuiltinOperatorSpec.right_type`: `Nil` represents the absence of value
# - `ValueInUse`: `Nil` represents a singleton value (like `None` in Python)
# So the template code is expected to use the `is_nil` attribute and do ad-hoc
# code according to it need instead of relying on py/c/cy_type


class NilTypeSpec(TypeSpec):
    def __init__(self):
        # Cannot use super().__init__() given py/cy/c_type are read-only !
        self.__dict__ = {
            # Default values from parent
            **{f.name: f.default for f in super().__dataclass_fields__.values()},
            # Our config values
            **{
                "size": 0,
                "gdapi_type": "Nil",
                "is_scalar": True,
                "is_stack_only": True,
                "is_nil": True,
                "variant_type_name": "GDNATIVE_VARIANT_TYPE_NIL",
            },
        }

    def __repr__(self):
        return f"<NilTypeSpec {id(self)}>"

    @property
    def py_type(self):
        raise RuntimeError(
            "Nil type ! Should handle this by hand with a if condition on `<my_type>.is_nil`"
        )

    @property
    def cy_type(self):
        raise RuntimeError(
            "Nil type ! Should handle this by hand with a if condition on `<my_type>.is_nil`"
        )

    @property
    def c_type(self):
        raise RuntimeError(
            "Nil type ! Should handle this by hand with a if condition on `<my_type>.is_nil`"
        )


# TODO: Object type should match GDNATIVE_VARIANT_TYPE_OBJECT


TYPES_DB: Dict[TypeDBEntry, TypeSpec] = {
    "Nil": NilTypeSpec(),
    # Types marked as `meta` are used in the classes method args/return types
    "meta:int8": TypeSpec(
        size=1,
        gdapi_type="int8",
        c_type="int8_t",
        cy_type="int8_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:int16": TypeSpec(
        size=2,
        gdapi_type="int16",
        c_type="int16_t",
        cy_type="int16_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:int32": TypeSpec(
        size=4,
        gdapi_type="int32",
        c_type="int32_t",
        cy_type="int32_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:int64": TypeSpec(
        size=8,
        gdapi_type="int64",
        c_type="int64_t",
        cy_type="int64_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:uint8": TypeSpec(
        size=1,
        gdapi_type="uint8",
        c_type="uint8_t",
        cy_type="uint8_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:uint16": TypeSpec(
        size=2,
        gdapi_type="uint16",
        c_type="uint16_t",
        cy_type="uint16_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:uint32": TypeSpec(
        size=4,
        gdapi_type="uint32",
        c_type="uint32_t",
        cy_type="uint32_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:uint64": TypeSpec(
        size=8,
        gdapi_type="uint64",
        c_type="uint64_t",
        cy_type="uint64_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    # int is always 8bytes long
    "int": TypeSpec(
        size=8,
        gdapi_type="int",
        c_type="uint64_t",
        cy_type="uint64_t",
        py_type="int",
        variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:float": TypeSpec(
        size=4,
        gdapi_type="float",
        c_type="float",
        cy_type="float",
        py_type="float",
        variant_type_name="GDNATIVE_VARIANT_TYPE_FLOAT",
        is_scalar=True,
        is_stack_only=True,
    ),
    "meta:double": TypeSpec(
        size=8,
        gdapi_type="double",
        c_type="double",
        cy_type="double",
        py_type="float",
        variant_type_name="GDNATIVE_VARIANT_TYPE_FLOAT",
        is_scalar=True,
        is_stack_only=True,
    ),
    # The rest of the types will be added during parsing of builtins&classes
}


def register_variant_in_types_db(variant_size: int) -> None:
    TYPES_DB["Variant"] = TypeSpec(
        size=variant_size,
        gdapi_type="Variant",
        c_type="Variant",
        cy_type="object",
        py_type="GDAny",
        is_builtin=True,
    )


def register_builtins_in_types_db(builtins: Iterable["BuiltinSpec"]) -> None:
    for spec in builtins:
        if spec.name == "Nil":
            # `Nil` is already part of `TYPES_DB`
            nil_spec = TYPES_DB["Nil"]
            assert nil_spec.gdapi_type == spec.original_name  # Sanity check
            assert nil_spec.variant_type_name == spec.variant_type_name  # Sanity check
            continue
        assert spec.size is not None
        if spec.name == "bool":
            ts = TypeSpec(
                size=spec.size,
                gdapi_type=spec.original_name,
                py_type="bool",
                # Cython provide a `bint` type for boolean, however it is defined in C as
                # a `int` (so 32bits), so I guess it won't work for Godot's 8bits bool
                c_type=f"uint{spec.size*8}_t",
                cy_type=f"uint{spec.size*8}_t",
                is_stack_only=True,
                is_scalar=True,
                variant_type_name=spec.variant_type_name,
            )

        elif spec.name == "int":
            # Configure `int` type according to the size configuration
            ts = replace(TYPES_DB[f"meta:int{spec.size*8}"], gdapi_type=spec.original_name)

        elif spec.name == "float":
            # Configure `float` type according to the size configuration
            if spec.size == 4:
                ts = replace(TYPES_DB[f"meta:float"], gdapi_type=spec.original_name)
            else:
                assert spec.size == 8
                ts = replace(TYPES_DB[f"meta:double"], gdapi_type=spec.original_name)
        else:
            ts = TypeSpec(
                size=spec.size,
                gdapi_type=spec.original_name,
                py_type=spec.name,
                c_type=spec.c_struct_name,
                cy_type=spec.name,
                is_stack_only=not spec.has_destructor,
                is_builtin=True,
                variant_type_name=spec.variant_type_name,
            )
        TYPES_DB[ts.gdapi_type] = ts


def register_classes_in_types_db(classes: Iterable["ClassSpec"]) -> None:
    for spec in classes:
        ts = TypeSpec(
            # Class instance is always manipulated as a pointer,
            # hence `size` field is never supposed to be used here
            size=0,  # Dummy value
            gdapi_type=spec.original_name,
            py_type=spec.name,
            c_type="GDNativeObjectPtr",
            cy_type="GDNativeObjectPtr",
            variant_type_name="GDNATIVE_VARIANT_TYPE_OBJECT",
        )
        TYPES_DB[ts.gdapi_type] = ts
        for e in spec.enums:
            ts = TypeSpec(
                size=4,
                gdapi_type=f"enum::{spec.original_name}.{e.original_name}",
                py_type=f"{spec.name}.{e.name}",
                c_type="int",
                cy_type=f"{spec.name}.{e.name}",
                is_scalar=True,
                is_stack_only=True,
                is_enum=True,
                variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
            )
            TYPES_DB[ts.gdapi_type] = ts


def register_global_enums_in_types_db(enums: Iterable["GlobalEnumSpec"]) -> None:
    for spec in enums:
        ts = TypeSpec(
            size=4,
            gdapi_type=f"enum::{spec.original_name}",
            py_type=spec.name,
            c_type="int",
            cy_type=spec.name,
            is_scalar=True,
            is_stack_only=True,
            is_enum=True,
            variant_type_name="GDNATIVE_VARIANT_TYPE_INT",
        )
        TYPES_DB[ts.gdapi_type] = ts


@dataclass(repr=False)
class TypeInUse:
    type_name: TypeDBEntry

    def __repr__(self) -> str:
        try:
            resolved = TYPES_DB[self.type_name]
        except KeyError:
            resolved = "<not resolved yet>"
        return f"{self.__class__.__name__}({self.type_name}, {resolved})"

    def resolve(self) -> TypeSpec:
        # Must be called after parsing is done, otherwise it's possible our
        # type is defined in a spec we haven't parsed yet
        try:
            return TYPES_DB[self.type_name]
        except KeyError:
            raise RuntimeError(f"Type {self.type_name} is not resolvable yet !")

    def __getattr__(self, name: str):
        try:
            return getattr(self.resolve(), name)
        except AttributeError as exc:
            raise RuntimeError(f"Error in TypeSpec accessing: {exc}") from exc


# ValueInUse is only used to create function argument's default value,
# hence we should only take care that it is some valid Python code
@dataclass
class ValueInUse:
    value: str

    def __post_init__(self):
        if self.value == "true":
            self.value = "True"
        elif self.value == "false":
            self.value = "False"
        elif self.value == "null":
            self.value = "None"
