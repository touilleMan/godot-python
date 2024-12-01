extends Node

func _process(delta):
	# Godot print doesn't support flushing (since it may go through TCP when
	# doing remote debugging).
	# So we don't print anything here since the output cannot be reliably
	# ordered with the regular flushed prints done in `my.pyx`.

	# Exit godot
	self.get_tree().quit()
