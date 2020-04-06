from random import random

from godot import exposed, export, Vector2, GDString, Area2D, Input


MOTION_SPEED = 150


@exposed
class Paddle(Area2D):

    left = export(bool, default=False)
    action_prefix = export(str, default="")
    can_move = export(bool, default=False)

    def _ready(self):
        self.motion = 0
        self.can_move = True
        self.screen_size = self.get_viewport_rect().size
        self.set_process(True)

    def _process(self, delta):
        motion = 0
        if Input.is_action_pressed(self.action_prefix + GDString("_move_up")):
            motion -= 1
        elif Input.is_action_pressed(self.action_prefix + GDString("_move_down")):
            motion += 1

        motion *= MOTION_SPEED
        if self.can_move:
            self.translate(Vector2(0, motion * delta))

        # set screen limits
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > self.screen_size.y:
            self.position.y = self.screen_size.y

    def _on_paddle_area_enter(self, area):
        # random for new direction generated on each peer
        area.bounce(self.left, random())
