extends Node
## GDScript node that calls tick() on a DummyExposedTarget from GDScript.
##
## Measures the cost of GDScript → GDExtension-registered-Python-class method dispatch.
## Each instance creates its own DummyExposedTarget child in _ready() and calls
## tick() on it every frame via Object.call() (dynamic dispatch).

var _target: Object


func _ready() -> void:
	_target = ClassDB.instantiate("DummyExposedTarget")
	add_child(_target)


func _process(_delta: float) -> void:
	_target.call("tick")
