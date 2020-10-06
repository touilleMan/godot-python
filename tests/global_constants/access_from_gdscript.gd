extends Node


var outcome = null

func _ready():
    for data in [["global_py", "Python"], ["global_gd", "GDScript"]]:
        var name = data[0]
        var type = data[1]
        var path = "/root/%s" % name
        var node = get_node(path)
        if not node:
            outcome = "Cannot retrieve node `%s`" % path
            return
        if node.type != type:
            outcome = "Invalid Node type for `%s` (expected `%s`, got `%s`)" % [path, type, node.type]
            return
        node.set_accessed("GDScript")
    outcome = "ok"
