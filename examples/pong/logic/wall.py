from godot import gddataclass, classes, StringName


BALL_NAME = StringName("Ball")


@gddataclass(init=False)
class Wall(classes.Area2D):
    def _on_wall_area_entered(self, area: classes.Area2D) -> None:
        if area.name == BALL_NAME:
            # Ball went out of bounds, reset.
            area.reset()
