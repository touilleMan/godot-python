from godot import gddataclass, classes


@gddataclass
class Wall(classes.Area2D):
    def _on_wall_area_entered(self, area: classes.Area2D) -> None:
        if area.name == "Ball":
            # Ball went out of bounds, reset.
            area.reset()
