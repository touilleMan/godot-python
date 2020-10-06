extends Node

var accessors = []
var type = "GDScript"

func set_accessed(name):
    accessors.append(name)
