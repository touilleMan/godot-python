from godot import gddataclass, Vector2, StringName, classes


BALL_NAME = StringName("Ball")


@gddataclass(init=False)
class CeilingFloor(classes.Area2D):
    _bounce_direction: float = 1

    def __init__(self):
        self._bounce_direction = 1

    def _on_area_entered(self, area: classes.Area2D) -> None:
        if area.name == BALL_NAME:
            area.direction = (area.direction + Vector2(0, self._bounce_direction)).normalized()
