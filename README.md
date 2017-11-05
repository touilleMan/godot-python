
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


Quickstart
----------

0 - Build Godot
This project needs Godot 3 and it GDnative wrapper static library system.
Right now this wrapper library is not provided with Godot 3 alpha builds so we
must compile Godot ourself with the `gdnative_wrapper=yes` option:

```
$ scons platform=x11 gdnative_wrapper=yes target=debug tools=no
```

1 - Choose a Python interpreter
The project is compatible with both [CPython](https://github.com/python/cpython)
(default Python implementation) and [Pypy](https://pypy.org/) (alternative
high performance implementation with a JIT).

For CPython you need to build it yourself:
```
$ git clone git@github.com:python/cpython.git cpython-3.6.3
$ git checkout v3.6.3  # optional, but better use a release version that master tip
```
To simplify compilation of cpython you can use the Makefile rule provided:
```
$ make build_python PYTHON_SRC_DIR=./cpython-3.6.3
```

For Pypy, things are simpler because you can get precompiled binary. We
recomand the [portable binaries](https://github.com/squeaky-pl/portable-pypy#portable-pypy-distribution-for-linux)
```
$ wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.5-5.9-beta-linux_x86_64-portable.tar.bz2
$ tar xf pypy3.5-5.9-beta-linux_x86_64-portable.tar.bz2
```

2 - Compilation
We use SCons with Python 3 for this task.

For CPython:
```
$ make build BACKEND_DIR=cpython-3.6.3/build
```

or for pypy:
```
$ make build BACKEND_DIR=pypy3.5-5.9-beta-linux_x86_64-portable/ BACKEND=pypy
```

Note if you want to be able to modify *.inc.py files without having to recompile
everytime (useful for dev) you can pass the `dev_dyn=true` option to scons.
```
$ make build BACKEND_DIR=cpython-3.6.3/build EXTRA_OPTS='dev_dyn=true'
```

3 - Run tests & example
```
$ make build BACKEND_DIR=cpython-3.6.3/build tests
$ make build BACKEND_DIR=cpython-3.6.3/build example
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

CFFI connects with Godot C APIs:
- [GDnative](https://godotengine.org/article/dlscript-here) for calling Godot functions
- Pluginscript for registering callback function for Godot
CFFI connects to Godot C

Map of the code:
- `pythonscript.[c|h]`: Godot Pluginscript entry point.
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
