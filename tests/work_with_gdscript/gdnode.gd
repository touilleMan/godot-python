extends Node


var ready_called = false
export(int) var prop
export var overloaded_by_child_prop = "default"


func _ready():
    ready_called = true


func is_ready_called():
    return ready_called


func meth(attr):
    return attr


func overloaded_by_child_meth(attr):
    return attr


static func static_meth(attr):
	return 'static:' + attr
