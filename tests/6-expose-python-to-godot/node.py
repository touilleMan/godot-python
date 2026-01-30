from enum import IntEnum
from typing import ClassVar

from godot import (
    GDAny,
    GDArray,
    GDString,
    Vector2i,
    Rect2i,
    signal,
    classes,
    gddataclass,
    GDCallable,
)


@gddataclass(init=False)
class MyPythonNode(classes.Node):
    def __init__(self):
        super().__init__()
        self.attribute_scalar = 1
        self.attribute_composed = Rect2i()
        self._read_write_prop = Vector2i()

    CONST: ClassVar[int] = 11

    class ENUM(IntEnum):
        A = 1
        B = 2

    attribute_scalar: int
    attribute_composed: Rect2i
    _read_write_prop: Vector2i

    @property
    def read_only_prop(self) -> GDString:
        return GDString("RO")

    @property
    def read_write_prop(self) -> Vector2i:
        return self._read_write_prop

    @read_write_prop.setter
    def read_write_prop(self, val: Vector2i) -> None:
        self._read_write_prop = val

    simple_signal = signal()
    data_signal = signal(("count", int), ("message", GDString))

    def _ready(self):
        print("MyPythonNode: _ready", flush=True)
        self.tree_exiting.connect(GDCallable.create(self, "_on_tree_exiting"))

    def _on_tree_entered(self):
        print("MyPythonNode: _on_tree_entered", flush=True)

    def _on_tree_exiting(self):
        print("MyPythonNode: _on_tree_exiting", flush=True)

    def hello(self, a: int) -> GDString:
        print(f"MyPythonNode: hello({a!r})", flush=True)
        return GDString("World")

    @staticmethod
    def hello_static_method(a: GDString) -> int:
        print(f"MyPythonNode: hello_static_method({a!r})", flush=True)
        return 42

    @classmethod
    def hello_class_method(cls, a: GDArray, b: GDAny) -> GDString:
        print(f"MyPythonNode: hello_class_method({a!r}, {b!r})", flush=True)
        return GDString("World")
