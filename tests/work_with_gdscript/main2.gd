extends Node

export (int) var exported = 42

var python_scene = preload("res://python_scene.tscn")


func _ready():
	var python_scene_instance = python_scene.instance()
	python_scene_instance.set_name("python_scene")
	self.add_child(python_scene_instance)


func exit_test(error):
	if error:
		print("Error: " + error)
		OS.set_exit_code(1)
	else:
		print('Test success !')
	self.test_closing = true
	self.get_tree().quit()


var test_started = false
var test_ended = false
var test_closing = false


func _process(delta):
	if self.test_closing:
		# Wait for application to stop
		return
	if self.test_started:
		if self.test_ended:
			self.exit_test("")
		else:
			self.exit_test("Test started but didn't ended !")
	self.test_started = true
	var python_scene_instance = self.get_node("python_scene")
	# Test property
	python_scene_instance.python_prop = 42
	var prop_val = python_scene_instance.python_prop
	if prop_val != 42:
		self.exit_test('python_scene_instance.python_prop != 42 (value = %s)' % prop_val)
	# Test method
	var meth_ret = python_scene_instance.python_method("foo")
	if meth_ret != "foo":
		self.exit_test('python_scene_instance.python_method("foo") != "foo" (value = %s)' % meth_ret)
	# End of test, we will exit at next _process call
	self.test_ended = true
