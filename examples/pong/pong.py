from godot import exposed, signal, export, Node2D


SCORE_TO_WIN = 2


@exposed
class Pong(Node2D):
    game_finished = signal()

    def _ready(self):
        self.score_left = 0
        self.score_right = 0
        # let each paddle know which one is left, too
        p1 = self.get_node("player1")
        p2 = self.get_node("player2")
        p1.left = True
        p2.left = False
        p1.action_prefix = "p1"
        p2.action_prefix = "p2"

    def update_score(self, add_to_left):
        if add_to_left:
            self.score_left += 1
            self.get_node("score_left").set_text(str(self.score_left))
        else:
            self.score_right += 1
            self.get_node("score_right").set_text(str(self.score_right))

        game_ended = False
        if self.score_left == SCORE_TO_WIN:
            self.get_node("winner_left").show()
            game_ended = True
        elif self.score_right == SCORE_TO_WIN:
            self.get_node("winner_right").show()
            game_ended = True

        if game_ended:
            self.get_node("ball").stop()
            self.get_node("player1").can_move = False
            self.get_node("player2").can_move = False
