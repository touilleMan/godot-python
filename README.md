
      ________           .___      __    __________          __  .__                   
     /  _____/  ____   __| _/_____/  |_  \______   \___.__._/  |_|  |__   ____   ____  
    /   \  ___ /  _ \ / __ |/  _ \   __\  |     ___<   |  |\   __\  |  \ /  _ \ /    \ 
    \    \_\  (  <_> ) /_/ (  <_> )  |    |    |    \___  | |  | |   Y  (  <_> )   |  \
     \______  /\____/\____ |\____/|__|    |____|    / ____| |__| |___|  /\____/|___|  /
            \/            \/                        \/                \/            \/ 

[![Build Status](https://travis-ci.org/touilleMan/godot-python.svg?branch=master)](https://travis-ci.org/touilleMan/godot-python)

Python support for Godot


Overview
--------

The goal of this project is to provide Python language as scripting module for
[Godot](http://godotengine.org) game engine.

Not everything is implemented so far, however there is enough to start
playing/reporting issues ;-)


Quickstart
----------

0 - Configure the repo
Beforehand, the repo has CPython as git submodule, don't forget to fetch it:
```
$ git clone --recursive https://github.com/touilleMan/godot-python.git
# Or if you have already cloned the repo
$ git submodule init && git submodule update
```

The current repo must have a `godot` directory (can be a symbolic link) pointing
on the godot's sources, itself having the `pythonscript` directory
in it `modules/pythonscript`.
```
$ make setup GODOT_TARGET_DIR='/path/to/godot_repo'
```

Basically we should endup with those links:
```
/godot # Godot source repo
/godot-python # *this* repo
/godot-python/godot -> /godot
/godot/modules/pythonscript -> /godot-python/pythonscript
```

1 - Generate `cdef.gen.h` (Godot's GDnative API header cooked for CFFI)
```
$ make generate_gdnative_cffidefs
```
Note this step is only useful if GDnative API has changed (should not
happen really often when Godot 3.0 will be released).

2 - Use CFFI to generate `pythonscriptcffi.cpp`
```
$ make generate_cffi_bindings
```
Or if you want to be able to modify *.inc.py files without having to recompile
everytime (useful for dev):
```
$ make generate_dev_dyn_cffi_bindings
```

4 - Compile CPython & Pythonscript module
```
$ make compile
```
By default the command uses clang as compiler, have a look at the `Makefile` if
you want to switch to gcc.

5 - Run tests & example
```
$ make tests
$ make example
```


API
---

example:

```python
# Explicit is better than implicit
from godot import exposed, export
from godot.bindings import Node2D, Vector2


@exposed
class Player(Node2D):
	"""
	This is the file's main class which will be made available to Godot. This
	class must inherit of `godot.Node` or any of it children (i.g.
	`godot.KinematicBody`).
	Obviously you can't have two `exposed` class in the same file given Godot
	retreives the class based on the file path alone.
	"""
	# Exposed class can define some attributes as export(<type>) to achieve
	# similar goal than GDSscript's `export` keyword
	name = export(str)

	# Can export property as well
	@export(int)
	@property
	def age(self):
		return self._age

	@age.setter
	def age(self, value):
		self._age = value

	# All methods are exposed to Godot
	def talk(self, msg):
		print("I'm saying %s" % msg)

	def _ready(self):
		# Don't confuse `__init__` with Godot's `_ready` !
		self._age = 42
		# Of course you can access property&methods defined in the parent
		name = self.get_name()
		print('%s position x=%s, y=%s' % (name, self.position.x, self.position.y))

	...


class Helper:
	"""
	Others class are considered as helper and cannot be called from outside
	Python. However they can be imported from another python module.
	"""
	...


```


Technical internals
-------------------

The project is built with the awesome [CFFI](https://cffi.readthedocs.io/en/latest/).
Before that, both [Micropython](https://github.com/micropython/micropython) and
[Pybind11](https://github.com/pybind/pybind11) has been tried, but each comes with
it own drawback (basically API complexity and compatibility for Micropython,
C++ craziness and output size for Pybind11) so they just couldn't compete with
CFFI ;-)

Godot is a C++ game engine, however CFFI only support C API, hence Pythonscript
module use two interfaces:
- Godot's default C++ API to expose Pythonscript as a script language
- [Godot's GDnative](https://godotengine.org/article/dlscript-here) for binding Godot's
  Classes (Node, Vector2 etc.)

The reason behind GDnative is C++ is a terrible language when it comes to redistribute
a shared library (unlike in C, output is compiler dependant).
The long term goal for this project is to only depend on GDnative, this way we
will be able to distribute Pythonscript as a shared library ready to be loaded
by the official Godot build !

Map of the code:
- `py_*.[cpp|h]`: Godot's C++ language classes implementations (i.g. Script, ScriptInstance).
- `cffi_bindings/api.h`&`cffi_bindings/api_struct.h`: Exposed C api use in the language classes implementations.
- `cffi_bindings/*.inc.py`: Python code that will be verbatim included in the pythonscript module.
- `cffi_bindings/builtin_*.inc.py`: Python binding for Godot builtins
- `cffi_bindings/embedding_init_code.inc.py`: Very first Python code that will be executed on module loading.
- `cffi_bindings/mod_godot.inc.py`: Python `godot` module code.
- `cffi_bindings/mod_godot_bindings.inc.py`: Python `godot.bindings` module code.
- `cffi_bindings/cdef.gen.h`: C Godot's GDnative API ready to be used by the CFFI generator.
  This file is generated by `tools/generate_gdnative_cffidefs.py`.
- `cffi_bindings/pythonscriptcffi.cpp`: Pythonscript module output by the CFFI generator.
  This file is generated by `cffi_bindings/generate.py`.
