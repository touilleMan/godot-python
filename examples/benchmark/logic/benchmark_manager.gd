extends Node
## Orchestrates benchmark runs comparing Python vs GDScript node performance.
##
## Three benchmark categories:
##
##   Builtins   — Vector2/StringName/GDString construction, arithmetic, and
##                Godot builtin methods (normalized, length, distance_to, to_lower…).
##                Measures Python↔Godot type-wrapping overhead.
##
##   Classes    — Calls on Godot singleton classes (Time, OS, Engine) and Node tree
##                traversal.  Measures Python→Godot class method-dispatch overhead.
##
##   Exposed    — A Python class (DummyExposedTarget) is instantiated and its tick()
##                method is called each frame, once from GDScript and once from Python.
##                Measures GDScript→Python and Python→Python dispatch overhead.
##
## For every pair the ratio (GDScript fps / Python fps) is shown so you can see how
## much slower the Python path is relative to the native GDScript baseline.
##
## Headless / one-shot mode:
##   godot --headless --path . -- --nodes 1000 --test all
##   (--test can be: builtins | classes | exposed | all)

enum State { IDLE, WARMING, MEASURING }

const WARMUP_DURATION := 0.5
const MEASURE_DURATION := 3.0

var node_count: int = 1000
var state: State = State.IDLE
var state_timer: float = 0.0
var fps_samples: Array = []
var current_test_name: String = ""
var all_results: Array = []
var pending_tests: Array = []
var headless_mode: bool = false

@onready var fps_label: Label = $UI/Panel/Margin/VBox/FPSLabel
@onready var status_label: Label = $UI/Panel/Margin/VBox/StatusLabel
@onready var count_label: Label = $UI/Panel/Margin/VBox/NodeCountRow/CountLabel
@onready var results_label: RichTextLabel = $UI/Panel/Margin/VBox/Results
@onready var node_container: Node = $NodeContainer
@onready var builtins_btn: Button = $UI/Panel/Margin/VBox/Buttons/BuiltinsBtn
@onready var classes_btn: Button = $UI/Panel/Margin/VBox/Buttons/ClassesBtn
@onready var exposed_btn: Button = $UI/Panel/Margin/VBox/Buttons/ExposedBtn
@onready var all_btn: Button = $UI/Panel/Margin/VBox/Buttons/AllBtn


func _ready() -> void:
	headless_mode = DisplayServer.get_name() == "headless"

	if headless_mode:
		_run_headless()
	else:
		$UI/Panel/Margin/VBox/NodeCountRow/LessBtn.pressed.connect(_on_less_pressed)
		$UI/Panel/Margin/VBox/NodeCountRow/MoreBtn.pressed.connect(_on_more_pressed)
		builtins_btn.pressed.connect(_on_builtins_pressed)
		classes_btn.pressed.connect(_on_classes_pressed)
		exposed_btn.pressed.connect(_on_exposed_pressed)
		all_btn.pressed.connect(_on_all_pressed)
		update_count_label()
		update_results_display()


func _run_headless() -> void:
	var user_args := OS.get_cmdline_user_args()

	var idx := user_args.find("--nodes")
	if idx >= 0 and idx + 1 < user_args.size():
		node_count = int(user_args[idx + 1])

	var test_name := "all"
	idx = user_args.find("--test")
	if idx >= 0 and idx + 1 < user_args.size():
		test_name = user_args[idx + 1]

	print("Godot-Python Benchmark  [headless, %d nodes, warmup %.1fs, measure %.1fs]" % [
		node_count, WARMUP_DURATION, MEASURE_DURATION
	])
	print("")

	match test_name:
		"builtins":
			_on_builtins_pressed()
		"classes":
			_on_classes_pressed()
		"exposed":
			_on_exposed_pressed()
		_:
			_on_all_pressed()


func _process(delta: float) -> void:
	if not headless_mode:
		fps_label.text = "FPS: %.1f" % Engine.get_frames_per_second()

	match state:
		State.WARMING:
			state_timer -= delta
			if state_timer <= 0.0:
				state = State.MEASURING
				state_timer = MEASURE_DURATION
				fps_samples.clear()
				if not headless_mode:
					status_label.text = "Measuring: %s (%d nodes)..." % [
						current_test_name, node_container.get_child_count()
					]

		State.MEASURING:
			fps_samples.append(Engine.get_frames_per_second())
			state_timer -= delta
			if state_timer <= 0.0:
				_finish_measurement()


func _finish_measurement() -> void:
	var avg_fps := 0.0
	var min_fps := INF
	var max_fps := 0.0
	for f: float in fps_samples:
		avg_fps += f
		if f < min_fps:
			min_fps = f
		if f > max_fps:
			max_fps = f
	avg_fps /= float(fps_samples.size())

	all_results.append({
		"name": current_test_name,
		"count": node_container.get_child_count(),
		"avg_fps": avg_fps,
		"min_fps": min_fps,
		"max_fps": max_fps,
	})

	if headless_mode:
		print("  done  avg=%.1f  min=%.1f  max=%.1f fps" % [avg_fps, min_fps, max_fps])

	_clear_nodes()

	if pending_tests.is_empty():
		state = State.IDLE
		if headless_mode:
			_print_headless_results()
			get_tree().quit()
		else:
			_set_buttons_disabled(false)
			status_label.text = "Done! See results below."
			update_results_display()
	else:
		_start_next_test()


func _start_next_test() -> void:
	var test: Dictionary = pending_tests.pop_front()
	current_test_name = test["name"]
	var spawn_func: Callable = test["spawn"]
	spawn_func.call()
	state = State.WARMING
	state_timer = WARMUP_DURATION
	if headless_mode:
		print("Running: %s  (%d nodes)" % [current_test_name, node_count])
	else:
		status_label.text = "Warming up: %s (%d nodes)..." % [
			current_test_name, node_container.get_child_count()
		]


func run_tests(tests: Array) -> void:
	if state != State.IDLE:
		return
	all_results.clear()
	pending_tests = tests.duplicate()
	if not headless_mode:
		_set_buttons_disabled(true)
		update_results_display()
	_start_next_test()


func _spawn_python_nodes(class_name_str: String) -> void:
	for i in range(node_count):
		var node: Object = ClassDB.instantiate(class_name_str)
		node_container.add_child(node)


func _spawn_gdscript_nodes(script_path: String) -> void:
	var script: Script = load(script_path)
	for i in range(node_count):
		var node := Node.new()
		node.set_script(script)
		node_container.add_child(node)


func _clear_nodes() -> void:
	for child in node_container.get_children():
		child.queue_free()


func _set_buttons_disabled(disabled: bool) -> void:
	builtins_btn.disabled = disabled
	classes_btn.disabled = disabled
	exposed_btn.disabled = disabled
	all_btn.disabled = disabled


func _on_less_pressed() -> void:
	if state != State.IDLE:
		return
	if node_count <= 10:
		node_count = max(1, node_count - 1)
	else:
		node_count = node_count / 10
	update_count_label()


func _on_more_pressed() -> void:
	if state != State.IDLE:
		return
	if node_count < 10:
		node_count += 1
	else:
		node_count = min(100000, node_count * 10)
	update_count_label()


func update_count_label() -> void:
	count_label.text = "%d" % node_count


func _on_builtins_pressed() -> void:
	run_tests([
		{
			"name": "Python builtins",
			"spawn": func(): _spawn_python_nodes("DummyBuiltinsPython"),
		},
		{
			"name": "GDScript builtins",
			"spawn": func(): _spawn_gdscript_nodes("res://logic/dummy_builtins.gd"),
		},
	])


func _on_classes_pressed() -> void:
	run_tests([
		{
			"name": "Python Godot classes",
			"spawn": func(): _spawn_python_nodes("DummyClassesPython"),
		},
		{
			"name": "GDScript Godot classes",
			"spawn": func(): _spawn_gdscript_nodes("res://logic/dummy_classes.gd"),
		},
	])


func _on_exposed_pressed() -> void:
	run_tests([
		{
			"name": "Python calls Python class",
			"spawn": func(): _spawn_python_nodes("DummyExposedPythonCaller"),
		},
		{
			"name": "GDScript calls Python class",
			"spawn": func(): _spawn_gdscript_nodes("res://logic/dummy_exposed_gdscript_caller.gd"),
		},
	])


func _on_all_pressed() -> void:
	run_tests([
		{
			"name": "Python builtins",
			"spawn": func(): _spawn_python_nodes("DummyBuiltinsPython"),
		},
		{
			"name": "GDScript builtins",
			"spawn": func(): _spawn_gdscript_nodes("res://logic/dummy_builtins.gd"),
		},
		{
			"name": "Python Godot classes",
			"spawn": func(): _spawn_python_nodes("DummyClassesPython"),
		},
		{
			"name": "GDScript Godot classes",
			"spawn": func(): _spawn_gdscript_nodes("res://logic/dummy_classes.gd"),
		},
		{
			"name": "Python calls Python class",
			"spawn": func(): _spawn_python_nodes("DummyExposedPythonCaller"),
		},
		{
			"name": "GDScript calls Python class",
			"spawn": func(): _spawn_gdscript_nodes("res://logic/dummy_exposed_gdscript_caller.gd"),
		},
	])


func _print_headless_results() -> void:
	var sep := "-".repeat(68)
	print("")
	print("Results:")
	print("%-32s %6s %8s %8s %8s" % ["Test", "Nodes", "Avg FPS", "Min FPS", "Max FPS"])
	print(sep)

	var i := 0
	while i < all_results.size():
		var r: Dictionary = all_results[i]
		var line := "%-32s %6d %8.1f %8.1f %8.1f" % [
			r["name"], r["count"], r["avg_fps"], r["min_fps"], r["max_fps"]
		]

		if i + 1 < all_results.size():
			print(line)
			var nxt: Dictionary = all_results[i + 1]
			var ratio: float = float(nxt["avg_fps"]) / float(r["avg_fps"]) if float(r["avg_fps"]) > 0.0 else 0.0
			print("%-32s %6d %8.1f %8.1f %8.1f  x%.2f faster" % [
				nxt["name"], nxt["count"], nxt["avg_fps"], nxt["min_fps"], nxt["max_fps"], ratio
			])
			print(sep)
			i += 2
		else:
			print(line)
			i += 1


func update_results_display() -> void:
	if all_results.is_empty():
		results_label.text = "[i]No results yet. Run a benchmark above.[/i]"
		return

	var lines: PackedStringArray = PackedStringArray()
	lines.append("[b]%-30s %6s %8s %8s[/b]" % ["Test", "Nodes", "Avg FPS", "Min FPS"])
	lines.append("─".repeat(58))

	# Print results in pairs, appending a GDScript/Python ratio on the second row.
	var i := 0
	while i < all_results.size():
		var r: Dictionary = all_results[i]
		var line := "%-30s %6d %8.1f %8.1f" % [r["name"], r["count"], r["avg_fps"], r["min_fps"]]

		if i + 1 < all_results.size():
			var nxt: Dictionary = all_results[i + 1]
			lines.append(line)
			var ratio: float = float(nxt["avg_fps"]) / float(r["avg_fps"]) if float(r["avg_fps"]) > 0.0 else 0.0
			lines.append("%-30s %6d %8.1f %8.1f  ×%.2f faster" % [
				nxt["name"], nxt["count"], nxt["avg_fps"], nxt["min_fps"], ratio
			])
			lines.append("")
			i += 2
		else:
			lines.append(line)
			i += 1

	results_label.text = "\n".join(lines)
