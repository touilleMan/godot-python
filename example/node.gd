extends Node2D

func _on_button_pressed():
	print("-----------------------------------")

func _ready():
	self.rotate(1.5)
	get_parent().get_node("Button").connect("pressed",self,"_on_button_pressed")
