# from godot import exposed, GDString, Export, GDAny, Signal
from enum import IntEnum
from godot import GDAny, GDArray, GDString, Vector2
from godot.classes import Node, signal

from dataclasses import dataclass, field
from typing import ClassVar, dataclass_transform


@dataclass_transform()
def gddataclass(
    cls=None,
    /,
    virtual: bool = False,
    abstract: bool = False,
    exposed: bool = True,
    runtime: bool = True,
    icon_path: str | None = None,
    **kwargs,
):
    assert kwargs.get("init", True), "Cannot disable `init=True` param"

    def _gddataclass(cls):
        cls.__gdpy_is_virtual = virtual
        cls.__gdpy_is_abstract = abstract
        cls.__gdpy_is_exposed = exposed  # Show the class in the editor's class picker?
        cls.__gdpy_is_runtime = runtime  # Inverse of the `@tool` marker
        cls.__gdpy_icon_path = icon_path
        return dataclass(**kwargs)(cls)

    if cls is not None:
        # Called without parenthesis
        return _gddataclass(cls)
    else:
        return _gddataclass


@gddataclass
class MyPythonNode(Node):
    CONST: ClassVar[int] = 11

    class ENUM(IntEnum):
        A = 1
        B = 2

    foo: int = 1
    _read_write_prop: Vector2 = field(default_factory=lambda: Vector2(0, 0))

    @property
    def read_only_prop(self) -> GDString:
        return GDString("RO")

    @property
    def read_write_prop(self) -> Vector2:
        return self._read_write_prop

    @read_write_prop.setter
    def read_write_prop(self, val: Vector2) -> None:
        self._read_write_prop = val

    simple_signal = signal()
    data_signal = signal(("count", int), ("message", GDString))

    def _ready(self):
        print("MyPythonNode: _ready", flush=True)

    def hello(self, a: int) -> GDString:
        print(f"MyPythonNode: hello({a})", flush=True)
        return GDString("World")

    @staticmethod
    def hello_static_method(a: GDString) -> int:
        print(f"MyPythonNode: hello_static_method({a})", flush=True)
        return 42

    @classmethod
    def hello_class_method(cls, a: GDArray, b: GDAny) -> GDString:
        print(f"MyPythonNode: hello_class_method({a}, {b})", flush=True)
        return GDString("World")


def initialize(level: int):
    if level != 2:  # GDEXTENSION_INITIALIZATION_SCENE
        return

    from godot.classes import register_python_extension_class

    # MyPythonNode.__gdpy_is_virtual = False
    # MyPythonNode.__gdpy_is_abstract = False
    # MyPythonNode.__gdpy_is_exposed = True  # Don't show the class in the editor's class picker
    # MyPythonNode.__gdpy_is_runtime = True  # Inverse of the `@tool` marker
    # MyPythonNode.__gdpy_icon_path = None
    # MyPythonNode._ready.__gdpy_register = True
    register_python_extension_class(MyPythonNode)
