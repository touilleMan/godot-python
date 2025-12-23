extends Node

var quit_on_next_tick = false
var simple_signal_received = false
var data_signal_received = false
var data_signal_count = 0
var data_signal_message = ""

func _process(delta: float):
	# Guard to avoid ending never exiting if the test code is broken

	if quit_on_next_tick:
		self.get_tree().quit()
		return
	quit_on_next_tick = true

	# Actual test stuff

	var node = $"../MyPythonNode"

	# Methods
	assert(node.hello(42) == "World")
	assert(node.hello_static_method("World") == 42)
	assert(node.hello_class_method([42, "World"], node) == "World")

	# Attributes
	assert(node.foo == 1)
	node.foo = 42
	assert(node.foo == 42)

	# Python @property
	assert(node.read_only_prop == "RO")
	# assert(node.read_write_prop == Vector2(0, 0))
	# node.read_write_prop = Vector2(1, 2)
	# assert(node.read_write_prop == Vector2(1, 2))

	# Integer constant

	assert(node.CONST == 11)

	# Integer enum constant

	assert(node.ENUM_A == 1)
	assert(node.ENUM_B == 2)

	# Signals

	node.simple_signal.connect(func():
		print("GDScript: simple_signal received")
		simple_signal_received = true
	)

	node.data_signal.connect(func(count: int, message: String):
		print("GDScript: data_signal received with count=%d, message=%s" % [count, message])
		data_signal_received = true
		data_signal_count = count
		data_signal_message = message
	)

	node.simple_signal.emit()
	node.data_signal.emit(99, "test message")

	assert(simple_signal_received)
	assert(data_signal_received)
	assert(data_signal_count == 99)
	assert(data_signal_message == "test message")
