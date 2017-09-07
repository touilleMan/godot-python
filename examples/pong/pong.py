from godot import exposed, signal
from godot.bindings import Node2D


SCORE_TO_WIN = 10


@exposed
class Pong(Node2D):

    game_finished = signal()

    def _ready(self):
        self.score_left = 0
        self.score_right = 0
        # let each paddle know which one is left, too
        self.get_node("player1").left
        self.get_node("player1").left = True
        self.get_node("player2").left = False
        self.get_node("player1").action_prefix = 'p1'
        self.get_node("player2").action_prefix = 'p2'

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
