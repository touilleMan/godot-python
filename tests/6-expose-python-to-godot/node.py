from enum import IntEnum
from dataclasses import field
from typing import ClassVar

from godot import GDAny, GDArray, GDString, Vector2, signal, classes, gddataclass


@gddataclass(init=False)
class MyPythonNode(classes.Node):
    def __init__(self):
        super().__init__()
        self.foo = 1
        self._read_write_prop = Vector2()

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
