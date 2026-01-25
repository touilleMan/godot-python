from typing import ClassVar

from godot import gddataclass, Vector2, classes, GDString, StringName, utils
from godot.singletons import Input


@gddataclass
class Paddle(classes.Area2D):
    MOVE_SPEED: ClassVar[float] = 100.0

    _ball_dir: int
    _up: GDString
    _down: GDString
    _screen_size_y: float

    def _ready(self) -> None:
        self._screen_size_y = self.get_viewport_rect().size.y
        n = self.name.to_lower()
        self._up = StringName(f"{n}_move_up")
        self._down = StringName(f"{n}_move_down")
        if n == "left":
            self._ball_dir = 1
        else:
            self._ball_dir = -1

    def _process(self, delta: float) -> None:
        # Move up and down based on input.
        self.input = Input.get_action_strength(self._down) - Input.get_action_strength(self._up)
        self.position.y = utils.clamp(
            self.position.y + input * self.MOVE_SPEED * delta, 16, self._screen_size_y - 16
        )

    def _on_area_entered(self, area: classes.Area2D) -> None:
        if area.name == "Ball":
            # Assign new direction.
            area.direction = Vector2(self._ball_dir, utils.randf() * 2 - 1).normalized()
