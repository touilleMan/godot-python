extends Node
## GDScript node stressing calls into Godot class methods.
##
## Mirrors dummy_classes_python.py exactly so the two can be compared fairly.


func _process(_delta: float) -> void:
	# --- Godot singleton methods ---
	var _t_ms := Time.get_ticks_msec()
	var _t_us := Time.get_ticks_usec()
	var _os_name := OS.get_name()
	var _fps := Engine.get_frames_per_second()
	var _frames := Engine.get_process_frames()

	# --- Node tree traversal ---
	var root := get_tree().get_root()
	var _root_name := root.name
	var _root_children := root.get_child_count()
	var _parent := get_parent()
	var _parent_name := _parent.name
