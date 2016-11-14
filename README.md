Python support for Godot
========================

/!\ nothing working so far, move along /!\


Roadmap
-------

- [X] Integrate Micropython within Godot compilation toolchain
- [X] Create minimal compiling Godot module implementing `ScriptLanguage`, `Script` and `ScriptInstance`
- [X] Define Python API within Godot
- [ ] Load Python module as `Script`
- [ ] Instanciate Python class as `ScriptInstance`
- [ ] Connect Godot's `Variant` and basetypes with Python ones
- [ ] Expose Python `Script` through `ObjectTypeDB`
- [ ] Generate binding code to work with Godot's `MethodBind` & `ObjectTypeDB`
- [ ] Have a "HelloWorld" script working


API (work in progress)
----------------------

Godot API to implement a new language is based on three clases

### ScriptLanguage
- Initialize&teardown micropython interpreter
- Keep track of the scripts
- Provide editor&debug stuff (reload scripts, display language extension and keywords etc.)


### Script
A single file, in GDscript a file represent a class however this is not the case
in python.

example:

```python
from godot import Node, exposed, export


@exposed
class Player(Node):
	"""
	This is the file's main class which will be made available to Godot. This
	class must inherit of `godot.Node` or any of it children (i.g.
	`godot.KinematicBody`).
	Obviously you can't have two `exposed` class in the same file.
	"""
	# Exposed class can define some attributes as export(<type>) to achieve
	# similar goal than GDSscript's `export` keyword
	name = export(str)
	...


class Helper:
	"""
	Others class are considered as helper and cannot be called from outside
	Python. However they can be imported from another python module.
	"""
	...


```


### ScriptInstance
In GDscript this is an instance of a `Script` binded to a node.
Similarly in Python we instancied the exposed class of the `Script` and
connect it to the node.
