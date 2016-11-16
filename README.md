Python support for Godot
========================

/!\ nothing working so far, move along /!\


Overview
--------

The goal of this project is to provide Python language as scripting module for
[Godot](godotengine.org) game engine.
Instead of relying on CPython (default Python implementation), the choice has
been to use the [MicroPython](micropython.org) alternative implementation.
The reasons for this choices are:

Pros:
- [CPython's documentation](https://docs.python.org/3.6/extending/embedding.html) itself
  states it is a bad idea
- Much smaller dependency (MicroPython output is ~800ko vs CPython's ~4mo)
- No "battery included" policy unlike CPython, this allow to simply get rid
  of all the useless library from the final build (for example a standard
  CPython distribution is typically ~30mo)
- GIL can be disabled to allow real concurrent threading (which must be
  manually protected of course)
- It should be easy to tweak MicroPython in the future to allow multiple
  independent interpreters within the same application
- [Code emitter](http://docs.micropython.org/en/latest/wipy/reference/speed_python.html#the-native-code-emitter)
  allows compilation to native code of some parts of the script for speedup boost
- Unlike CPython reference counting, MicroPython make use of a garbage collector
  which allows can be manually triggered (i.g. to run it in parallel with
  rendering [given game logic is not run at this time](https://godotengine.org/article/why-does-godot-use-servers-and-rids))

Cons:
- Less support & documentation about MicroPython internals
- MicroPython doesn't implement all Python so far (e.g. no metaclasses) which
  typically means not all libraries are compatible with it
- Incompatible with SWIG and Boost::Python


Roadmap
-------

- [X] Integrate Micropython within Godot compilation toolchain
- [X] Create minimal compiling Godot module implementing `ScriptLanguage`, `Script` and `ScriptInstance`
- [X] Define Python API within Godot
- [ ] Load Python module as `Script`
- [ ] Instantiate Python class as `ScriptInstance`
- [ ] Connect Godot's `Variant` and basetypes with Python ones
- [ ] Expose Python `Script` through `ObjectTypeDB`
- [ ] Generate binding code to work with Godot's `MethodBind` & `ObjectTypeDB`
- [ ] Have a "HelloWorld" script working


API (work in progress)
----------------------

Godot API to implement a new language is based on three classes

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
Similarly in Python we instantiated the exposed class of the `Script` and
connect it to the node.
