from typing import Optional, Tuple
from dataclasses import dataclass
import re

from .type_spec import *


@dataclass(repr=False)
class TypeInUse:
    type_name: TypeDBEntry

    def __repr__(self) -> str:
        # Don't try to resolve it here, given it can lead to tenious recursion
        return f"{self.__class__.__name__}({self.type_name})"

    def resolve(self) -> TypeSpec:
        # From a runtime point of view, `typedarray::XXX` is just a regular Array with a
        # "trust me bro" promise on what the variants it contains are, so just ignore it
        if self.type_name.startswith("typedarray::"):
            type_name = "Array"
        else:
            type_name = self.type_name
        # Must be called after parsing is done, otherwise it's possible our
        # type is defined in a spec we haven't parsed yet
        try:
            return TYPES_DB[type_name]
        except KeyError:
            raise RuntimeError(f"Type {type_name} is not resolvable yet !")

    def __getattr__(self, name: str):
        try:
            return getattr(self.resolve(), name)
        except AttributeError as exc:
            raise RuntimeError(f"Error in TypeSpec accessing: {exc}") from exc

    @staticmethod
    def parse(type_name: str) -> "TypeInUse":
        if type_name.startswith("const "):
            type_name = type_name[len("const ") :]
        # TODO: Dummy workaround, should support uint8_t* and other stuff instead !
        if "*" in type_name:
            type_name = "int"
        type_name = type_name.strip()
        # Types are sometime a union of classes (e.g. `BaseMaterial3D,ShaderMaterial`)
        # in this case we consider the type as
        if "," in type_name:
            return TypeUnionInUse(type_name)
        else:
            return TypeInUse(type_name)


class TypeUnionInUse(TypeInUse):
    def __init__(self, types):
        # Actual types of classes is only used for type info, for C/Cython
        # code we just need to know we are handling a Godot Object
        super().__init__("Object")
        self.py_type = " | ".join(types.split(","))


# ValueInUse is only used to create function argument's default value,
# hence we should only take care that it is some valid Python code
@dataclass
class ValueInUse:
    type: TypeInUse
    original_value: str

    @property
    def py_value(self) -> str:
        return self.resolve()[0]

    # `None` indicates this should be passed as a NULL pointer in args array
    @property
    def cy_value(self) -> Optional[str]:
        return self.resolve()[1]

    @classmethod
    def parse(cls, value_type: TypeInUse, value: str) -> "ValueInUse":
        return cls(
            type=value_type,
            original_value=value,
        )

    def resolve(self) -> Tuple[str, Optional[str]]:
        # Default value field is very messy, so we have to clean it here
        # Non-exhaustive list of default params per type:
        # - String: "" "," " "
        # - Object: null
        # - Variant: null
        # - bool: true false
        # - int: 0 -1 1000
        # - float: -1.0 0.001 1e-05
        # - StringName: &"" ""
        # - Dictionary: {}
        # - Array: []
        # - Rect2i: Rect2i(0, 0, 0, 0)
        # - PackedByteArray: PackedByteArray()
        # - NodePath: NodePath("")

        def _is_number(val, expected_type):
            try:
                evaluated = eval(val)
                return isinstance(evaluated, expected_type)
            except SyntaxError:
                return False

        value = self.original_value
        value_py_type = self.type.py_type

        if value_py_type == "bool":
            assert value in ("true", "false")
            value = value.capitalize()
            py_value = cy_value = value.capitalize()

        elif value_py_type == "int":
            assert _is_number(value, int)
            py_value = cy_value = value

        elif value_py_type == "float":
            assert _is_number(value, (float, int))
            py_value = cy_value = value

        elif value_py_type == "GDString":
            assert value.startswith('"') and value.endswith('"')
            py_value = value
            cy_value = f"GDString({value})"

        elif value_py_type == "StringName":
            if value.startswith("&"):
                value = value[1:]
            assert value.startswith('"') and value.endswith('"')
            py_value = value
            cy_value = f"StringName({value})"

        elif value_py_type == "GDArray":
            assert re.match(r"\[\]|(Array\[\w+\]\(\[\]\))", value)  # Only support default value !
            py_value = value
            cy_value = "GDArray()"

        elif value_py_type == "GDDictionary":
            assert value == "{}"  # Only support default value !
            py_value = value
            cy_value = "GDDictionary()"

        elif value_py_type in ("RID", "GDCallable", "GDSignal"):
            assert value == f"{self.type.type_name}()"  # Only support default value !
            py_value = cy_value = value

        elif self.type.is_enum:
            assert _is_number(value, int)
            py_value = cy_value = value

        elif self.type.is_object:
            assert value == "null"
            py_value = "None"
            cy_value = None

        elif self.type.is_variant:
            if value == "null":
                py_value = "None"
                cy_value = None
            else:
                py_value = cy_value = value

        else:
            prefix = f"{value_py_type}("
            suffix = ")"
            assert value.startswith(prefix) and value.endswith(suffix)
            py_value = cy_value = value

        return py_value, cy_value

    # TODO: useful ? I'm not even sure GDScript handles this correctly...
    @property
    def reusable(self) -> bool:
        # TODO: see https://github.com/godotengine/godot/issues/64442
        return self.type.type_name not in ("RID", "Callable", "Signal")
