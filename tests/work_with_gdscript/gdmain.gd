extends Node


var _py_node_scene = preload("res://pynode.tscn")
var _py_subnode_scene = preload("res://pysubnode.tscn")
var _gd_node_scene = preload("res://gdnode.tscn")
var _gd_subnode_scene = preload("res://gdsubnode.tscn")


var _test_error = 0
var _test_total = 0
var _current_test = ""


func set_test(name):
	self._test_total += 1
	self._current_test = name


func assert_true(val, msg):
	if not val:
		self._test_error += 1
		print("- [ERROR] ", self._current_test, ": '", msg, "' expected to be true")
		return false
	else:
		return true


func assert_eq(a, b, msg):
	if not a == b:
		self._test_error += 1
		print("- [ERROR] ", self._current_test, ": '", a, "' != '", b, "' in '", msg, "'")
		return false
	else:
		return true


func test_native_method(node):
	var original_name = node.get_name()
	node.set_name("foo")
	var name = node.get_name()
	assert_eq(name, "foo", "node.get_name()")
	# Reset to original name to allow this test to work again with same node name
	node.set_name(original_name)


func test_prop(node, sub_node):
	var value

	# No default value means the property is set to null
	value = node.prop
	assert_eq(value, null, "node.prop")
	value = sub_node.prop
	assert_eq(value, null, "sub_node.prop")

	node.prop = 42
	value = node.prop
	assert_eq(value, 42, "node.prop")
	sub_node.prop = 42
	value = sub_node.prop
	assert_eq(value, 42, "sub_node.prop")

	value = node.overloaded_by_child_prop
	assert_eq(value, "default", "node.overloaded_by_child_prop")
	value = sub_node.overloaded_by_child_prop
	assert_eq(value, "sub:default", "sub_node.overloaded_by_child_prop")

	# node.overloaded_by_child_prop = "foo"
	# value = node.overloaded_by_child_prop
	# assert_eq(value, "foo", "node.overloaded_by_child_prop")
	# sub_node.overloaded_by_child_prop = "foo"
	# value = sub_node.overloaded_by_child_prop
	# assert_eq(value, "sub:foo", "sub_node.overloaded_by_child_prop")


func test_method(node, sub_node):
	var ret

	ret = node.meth("foo")
	assert_eq(ret, "foo", "node.meth(\"foo\")")
	ret = sub_node.meth("foo")
	assert_eq(ret, "foo", "sub_node.meth(\"foo\")")
	ret = node.overloaded_by_child_meth("foo")
	assert_eq(ret, "foo", "node.overloaded_by_child_meth(\"foo\")")
	ret = sub_node.overloaded_by_child_meth("foo")
	assert_eq(ret, "sub:foo", "sub_node.overloaded_by_child_meth(\"foo\")")


func test_ready_called(node, sub_node):
	assert_true(node.is_ready_called(), "node.is_ready_called()")
	assert_true(sub_node.is_ready_called(), "sub_node.is_ready_called()")
	assert_true(sub_node.is_sub_ready_called(), "sub_node.is_sub_ready_called()")


func run_tests():
	print('======= gdmain tests ==========')
	for args in [
			["pynodes", _py_node_scene, _py_subnode_scene],
			["gdnodes", _gd_node_scene, _gd_subnode_scene],
	]:
		var nodes_type = args[0]
		var node_scene = args[1]
		var sub_node_scene = args[2]

		var node = node_scene.instance()
		var sub_node = sub_node_scene.instance()
		self.add_child(node)
		self.add_child(sub_node)
		print('---', nodes_type, ' ', self.get_node(node.get_name()))

		# self.set_test(nodes_type + ":test_ready_called")
		# test_ready_called(node, sub_node)
		self.set_test(nodes_type + ":test_native_method(node)")
		test_native_method(node)
		self.set_test(nodes_type + ":test_native_method(sub_node)")
		test_native_method(sub_node)
		self.set_test(nodes_type + ":test_prop")
		test_prop(node, sub_node)
		self.set_test(nodes_type + ":test_method")
		test_method(node, sub_node)

		self.remove_child(node)
		self.remove_child(sub_node)

	if self._test_error:
		print('ERROR %s errors in %s tests' % [self._test_error, self._test_total])
		return 1
	else:
		print('SUCCESS %s tests' % self._test_total)
		return 0
