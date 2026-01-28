from typing import ClassVar
from dataclasses import field

from godot import gddataclass, Vector2, classes


@gddataclass(init=False)
class Ball(classes.Area2D):
    DEFAULT_SPEED: ClassVar[float] = 100.0

    _speed: float = DEFAULT_SPEED
    direction: Vector2 = Vector2.LEFT
    _initial_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))

    def __init__(self):
        super().__init__()
        self._speed = self.DEFAULT_SPEED
        self.direction = Vector2.LEFT()
        self._initial_pos = Vector2()

    def _ready(self):
        self._initial_pos = self.position

    def _process(self, delta: float) -> None:
        self._speed += delta * 2
        self.position += self.direction * (self._speed * delta)

    def reset(self) -> None:
        self.direction = Vector2.LEFT
        self.position = self._initial_pos
        self._speed = self.DEFAULT_SPEED
