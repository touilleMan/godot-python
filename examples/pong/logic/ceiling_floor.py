from godot import gddataclass, Vector2, classes


@gddataclass(init=False)
class CeilingFloor(classes.Area2D):
    _bounce_direction: float = 1

    def __init__(self):
        self._bounce_direction = 1

    def _on_area_entered(self, area: classes.Area2D) -> None:
        if area.name == "Ball":
            area.direction = (area.direction + Vector2(0, self._bounce_direction)).normalized()
