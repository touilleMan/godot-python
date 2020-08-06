
extends Node2D

const SCORE_TO_WIN = 2

var score_left = 0
var score_right = 0

signal game_finished()

func update_score(add_to_left):
	if (add_to_left):

		score_left+=1
		get_node("score_left").set_text( str(score_left) )
	else:

		score_right+=1
		get_node("score_right").set_text( str(score_right) )

	var game_ended = false

	if (score_left==SCORE_TO_WIN):
		get_node("winner_left").show()
		game_ended=true
	elif (score_right==SCORE_TO_WIN):
		get_node("winner_right").show()
		game_ended=true

	if (game_ended):
		get_node("ball").stop()
		get_node("player1").can_move=false
		get_node("player2").can_move=false

func _ready():

	#let each paddle know which one is left, too
	get_node("player1").left=true
	get_node("player2").left=false
	get_node("player1").action_prefix = 'p1'
	get_node("player2").action_prefix = 'p2'

