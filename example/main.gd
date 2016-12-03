extends Node

# class member variables go here, for example:
# var a = 2
# var b = "textvar"

func _ready():
	set_process(true)
	return
	# Called every time the node is added to the scene.
	# Initialization here
	var d = Directory.new()
	var a = d.file_exists('/home/emmanuel/.bashrc')
#	file_exists('/home/emmanuel/.bashrc')
	print(a)


class Leaker:
	var stuff = null
	var other = null
	func _init():
		# 32K data
		self.stuff = []
		for x in range(1000):
			self.stuff.append(x)

	func connect(other):
		self.other = other


func _process(delta):
	var a = Leaker.new()
	var first = a
	for i in range(100):
		var b = Leaker.new()
		a.connect(b)
		a = b
	a.connect(first)
