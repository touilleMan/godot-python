from godot import exposed, rpcsync, Area2D, Vector2


DEFAULT_SPEED = 80


@exposed
class Ball(Area2D):
    @rpcsync
    def _reset_ball(self, for_left):
        print("RESET BALL", for_left)
        self.position = self.screen_size / 2
        if for_left:
            self.direction = Vector2(-1, 0)
        else:
            self.direction = Vector2(1, 0)
        self.ball_speed = DEFAULT_SPEED

    @rpcsync
    def stop(self):
        self.stopped = True

    def _process(self, delta):
        # ball will move normally for both players
        # even if it's sightly out of sync between them
        # so each player sees the motion as smooth and not jerky
        if not self.stopped:
            self.translate(self.direction * self.ball_speed * delta)
        # check screen bounds to make ball bounce
        if (self.position.y < 0 and self.direction.y < 0) or (
            self.position.y > self.screen_size.y and self.direction.y > 0
        ):
            self.direction.y = -self.direction.y
        if self.is_network_master():
            # only master will decide when the ball is out in the left side (it's own side)
            # this makes the game playable even if latency is high and ball is going fast
            # otherwise ball might be out in the other player's screen but not this one
            if self.position.x < 0:
                self.get_parent().rpc("update_score", False)
                self.rpc("_reset_ball", False)
        else:
            # only the slave will decide when the ball is out in the right side (it's own side)
            # this makes the game playable even if latency is high and ball is going fast
            # otherwise ball might be out in the other player's screen but not this one
            if self.position.x > self.screen_size.x:
                self.get_parent().rpc("update_score", True)
                self.rpc("_reset_ball", True)

    @rpcsync
    def bounce(self, left, random):
        # using sync because both players can make it bounce
        if self.left:
            self.direction.x = abs(self.direction.x)
        else:
            self.direction.x = -abs(self.direction.x)
        self.ball_speed *= 1.1
        self.direction.y = random * 2.0 - 1
        self.direction = self.direction.normalized()

    def _ready(self):
        self.direction = Vector2(1, 0)
        self.ball_speed = DEFAULT_SPEED
        self.stopped = False
        self.screen_size = self.get_viewport_rect().size
        self.set_process(True)  # REMOVE ME
