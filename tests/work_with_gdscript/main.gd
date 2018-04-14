extends Node

var _test_done = false

func _process(delta):
	if _test_done:
		return
	for path in ["pymain", "gdmain"]:
#	for path in ["pymain"]:
		self.get_node(path).run_tests()
	_test_done = true
	self.get_tree().quit()
