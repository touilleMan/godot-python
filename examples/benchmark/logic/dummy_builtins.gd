extends Node
## GDScript node stressing Godot builtin type creation and operations.
##
## Mirrors dummy_builtins_python.py exactly so the two can be compared fairly.


func _process(_delta: float) -> void:
	# --- Vector2: create, arithmetic, method returning builtin ---
	var v := Vector2(1.0, 2.0)
	var v2 := v + Vector2(0.5, 0.5)
	var _n := v2.normalized()
	var _l := v2.length()

	var v3 := Vector2(3.0, 4.0)
	var _d := v3.distance_to(v2)
	var _dot := v3.dot(v2)

	# --- StringName: construction and comparison ---
	var s1 := StringName("benchmark")
	var s2 := StringName("godot_python")
	var _eq := (s1 == s2)

	# --- String: construction and method returning new String ---
	var gs := "Benchmark_Test_String"
	var _lower := gs.to_lower()
