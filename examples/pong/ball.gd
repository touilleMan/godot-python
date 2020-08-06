
extends Area2D

const DEFAULT_SPEED=220

var direction = Vector2(1,0)
var ball_speed = DEFAULT_SPEED
var stopped=false



onready var screen_size = get_viewport_rect().size

func _reset_ball(for_left):

	position = screen_size / 2
	if (for_left):
		direction = Vector2(-1,0)
	else:
		direction = Vector2( 1,0)

	ball_speed = DEFAULT_SPEED

func stop():
	stopped=true

func _process(delta):

	# ball will move normally for both players
	# even if it's sightly out of sync between them
	# so each player sees the motion as smooth and not jerky

	if (not stopped):
		translate( direction * ball_speed * delta )

	# check screen bounds to make ball bounce

	if ((position.y < 0 and direction.y < 0) or (position.y > screen_size.y and direction.y > 0)):
		direction.y = -direction.y

	if (position.x < 0 or position.x > screen_size.x):
		var for_left = position.x > 0
		get_parent().update_score(for_left)
		_reset_ball(for_left)

sync func bounce(left,random):

	#using sync because both players can make it bounce
	if (left):
		direction.x = abs(direction.x)
	else:
		direction.x = -abs(direction.x)

	ball_speed *= 1.1
	direction.y = random*2.0 - 1
	direction = direction.normalized()

func _ready():
	set_process(true)

