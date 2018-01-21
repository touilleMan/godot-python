
      ________           .___      __    __________          __  .__                   
     /  _____/  ____   __| _/_____/  |_  \______   \___.__._/  |_|  |__   ____   ____  
    /   \  ___ /  _ \ / __ |/  _ \   __\  |     ___<   |  |\   __\  |  \ /  _ \ /    \ 
    \    \_\  (  <_> ) /_/ (  <_> )  |    |    |    \___  | |  | |   Y  (  <_> )   |  \
     \______  /\____/\____ |\____/|__|    |____|    / ____| |__| |___|  /\____/|___|  /
            \/            \/                        \/                \/            \/ 

[![Build Status](https://travis-ci.org/touilleMan/godot-python.svg?branch=master)](https://travis-ci.org/touilleMan/godot-python)
[![Build status](https://ci.appveyor.com/api/projects/status/1y8gifqjoru07e2n/branch/master?svg=true)](https://ci.appveyor.com/project/touilleMan/godot-python/branch/master)

Python support for Godot


Overview
--------

The goal of this project is to provide Python language support as a scripting module for
[Godot](http://godotengine.org) game engine.


Quickstart
----------

Head to the [Releases](https://github.com/touilleMan/godot-python/releases) page and download the 
latest version for your platform.

Building
--------

To build the project from source, first checkout the repo or download the 
latest tarball.


### Build Requirements

On a fresh Ubuntu install, you will need to install these:

```
$ apt install build-essential scons python3 python3-pip curl git
$ pip3 install virtualenv --user
```

If you are using CPython as your backend, you will need additional 
libraries to build from source. The simplest way is to uncomment the 
main deb-src in `/etc/apt/sources.list`:
 
```
deb-src http://archive.ubuntu.com/ubuntu/ artful main
```
 
and instruct apt to install the needed packages:

```
$ apt update
$ apt build-dep python3.6
```

See the [Python Developer's Guide](https://devguide.python.org/setup/#build-dependencies) 
for instructions on additional platforms.

### Running the build

From your `godot-python` directory:


```bash
godot-python$ scons platform=x11-64 backend=cpython release
```

Valid platforms are `x11-64`, `x11-32`, `windows-64`, `windows-32`. Check Travis 
or Appveyor links above to see the current status of your platform.

Valid backends are `cpython`, `pypy`.

This command will download the pinned version of the Godot GDNative wrapper 
library (defined in SConstruct and platform specific SCSub files). It will then 
download a pinned pypy release binary or checkout cpython, move to a pinned 
commit and build cpython from source. It will generate the CFFI bindings and 
compile the shared library for your platform. The output of this command 
is a zip file which are shared on the release page.

### Testing your build

```bash
godot-python$ scons platform=x11-64 backend=cpython test
```

This will run pytests defined in `tests/bindings` inside the Godot environment. 
If not present, will download a precompiled Godot binary 
(defined in SConstruct and platform specific SCSub files) to and set the 
correct library path for the GDNative wrapper.

### Running the example project

```bash
godot-python$ scons platform=x11-64 backend=cpython example
```

This will run the converted pong example in `examples/pong` inside the Godot 
environment. If not present, will download a precompiled Godot binary 
(defined in SConstruct) to and set the correct library path for the GDNative wrapper.


### Using a local Godot version

If you have a pre-existing version of godot, you can instruct the build script to 
use that the static library and binary for building and tests.

```
godot-python$ scons platform=x11-64 backend=cpython godot_binary=../godot/bin/godot.x11.opt.64 gdnative_wrapper_lib=../godot/modules/include/libgdnative_wrapper_code.x11.opt.64.a
```

### Additional build options

You check out all the build options [in this file](https://github.com/touilleMan/godot-python/blob/master/SConstruct#L23).


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
	class must inherit from `godot.Node` or any of its children (i.g.
	`godot.KinematicBody`).
	
	Because Godot scripts only accept file paths, you can't have two `exposed` classes in the same file.
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
		# Don't confuse `__init__` with Godot's `_ready`!
		self._age = 42
		# Of course you can access property & methods defined in the parent
		name = self.get_name()
		print('%s position x=%s, y=%s' % (name, self.position.x, self.position.y))

	...


class Helper:
	"""
	Othes classes are considered helpers and cannot be called from outside
	Python. However they can be imported from another python module.
	"""
	...


```


Technical internals
-------------------

The project is built with the awesome [CFFI](https://cffi.readthedocs.io/en/latest/).
Before that, both [Micropython](https://github.com/micropython/micropython) and
[Pybind11](https://github.com/pybind/pybind11) have been tried, but each comes with
its own drawback (basically API complexity and compatibility for Micropython,
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
