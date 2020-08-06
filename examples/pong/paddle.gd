extends Area2D

export var left=false

const MOTION_SPEED=150

var motion = 0
var can_move = true
var action_prefix = ''

onready var screen_size = get_viewport_rect().size

func _process(delta):

	#is the master of the paddle
	motion = 0
	if (Input.is_action_pressed(action_prefix + "_move_up")):
		motion -= 1
	elif (Input.is_action_pressed(action_prefix + "_move_down")):
		motion += 1

	motion*=MOTION_SPEED
	if can_move:
		translate( Vector2(0,motion*delta) )

	# set screen limits
	if (position.y < 0 ):
		position.y = 0
	elif (position.y > screen_size.y):
		position.y = screen_size.y

func _ready():
	set_process(true)

func _on_paddle_area_enter( area ):
	area.bounce(left, randf()) #random for new direction generated on each peer
