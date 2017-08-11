extends "res://gdnode.gd"


var sub_ready_called = false
export var child_prop = "sub:default"
# Cannot overload a property in GDScript

func _ready():
    sub_ready_called = true


func is_sub_ready_called():
    return sub_ready_called


func overloaded_by_child_meth(attr):
    return "sub:" + attr
