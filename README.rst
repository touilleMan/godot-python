.. image:: https://travis-ci.org/touilleMan/godot-python.svg?branch=master
   :target: https://travis-ci.org/touilleMan/godot-python
   :alt: Automated test status (Linux and MacOS)

.. image:: https://ci.appveyor.com/api/projects/status/af4eyed8o8tc3t0r/branch/master?svg=true
   :target: https://ci.appveyor.com/project/touilleMan/godot-python/branch/master
   :alt: Automated test status (Windows)

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black


================================================
Godot Python, because you want Python on Godot !
================================================


.. image:: https://cdn.rawgit.com/touilleMan/godot-python/104c90e3/misc/godot_python.svg
   :width: 200px
   :align: right

The goal of this project is to provide Python language support as a scripting
module for the `Godot <http://godotengine.org>`_ game engine.


Quickstart
==========

By order of simplicity:

- Directly download the project from within Godot with the asset library tab.
- You can also download manually `here <https://godotengine.org/asset-library/asset/179>`_ (CPython backend) and `there <https://godotengine.org/asset-library/asset/192>`_ (for Pypy backend).
- Finally you can also head to the project `release page <https://github.com/touilleMan/godot-python/releases>`_ if you want to only download one specific platform build

Building
========

To build the project from source, first checkout the repo or download the
latest tarball.

Linux
-----

On a fresh Ubuntu install, you will need to install these:

.. code-block:: bash

	$ apt install build-essential scons python3 python3-pip curl git
	$ pip3 install virtualenv --user

If you are using CPython as your backend, you will need additional
libraries to build from source. The simplest way is to uncomment the
main deb-src in `/etc/apt/sources.list`:

.. code-block:: bash

	deb-src http://archive.ubuntu.com/ubuntu/ artful main

and instruct apt to install the needed packages:

.. code-block:: bash

	$ apt update
	$ apt build-dep python3.6

See the `Python Developer's Guide <https://devguide.python.org/setup/#build-dependencies>`_
for instructions on additional platforms.

MacOS
-----

With MacOS, you will need XCode installed and install the command line tools.

.. code-block:: bash

	$ xcode-select --install

If you are using CPython as your backend, you will need openssl. To install with Homebrew:

.. code-block:: bash

	$ brew install openssl

You will also need virtualenv for your python.

Running the build
-----------------

From your `godot-python` directory:


For Linux:

.. code-block:: bash

	godot-python$ scons platform=x11-64 backend=cpython release

For Windows:

.. code-block:: bash

	godot-python$ scons platform=windows-64 backend=cpython release

For MacOS, you will need to customize our cpp to use clang. Your final command will look like:

.. code-block:: bash

	godot-python$ scons platform=osx-64 backend=cpython gdnative_parse_cpp="clang -E" release

Valid platforms are `x11-64`, `x11-32`, `windows-64`, `windows-32` and `osx-64`. Check Travis
or Appveyor links above to see the current status of your platform.

Valid backends are `cpython`, `pypy`.

This command will download the pinned version of the Godot GDNative wrapper
library (defined in SConstruct and platform specific SCSub files). It will then
download a pinned pypy release binary or checkout cpython, move to a pinned
commit and build cpython from source. It will generate the CFFI bindings and
compile the shared library for your platform. The output of this command
is a zip file which are shared on the release page.

Testing your build
------------------

.. code-block:: bash

	godot-python$ scons platform=<platform> backend=<backend> test

This will run pytests defined in `tests/bindings` inside the Godot environment.
If not present, will download a precompiled Godot binary
(defined in SConstruct and platform specific SCSub files) to and set the
correct library path for the GDNative wrapper.

Running the example project
---------------------------

.. code-block:: bash

	godot-python$ scons platform=<platform> backend=cpython example

This will run the converted pong example in `examples/pong` inside the Godot
environment. If not present, will download a precompiled Godot binary
(defined in SConstruct) to and set the correct library path for the GDNative wrapper.


Using a local Godot version
---------------------------

If you have a pre-existing version of godot, you can instruct the build script to
use that the static library and binary for building and tests.

.. code-block:: bash

	godot-python$ scons platform=x11-64 backend=cpython godot_binary=../godot/bin/godot.x11.opt.64 gdnative_wrapper_lib=../godot/modules/include/libgdnative_wrapper_code.x11.opt.64.a

Additional build options
------------------------

You check out all the build options `in this file <https://github.com/touilleMan/godot-python/blob/master/SConstruct#L23>`_.


API
---

example:

.. code-block:: python

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


Technical internals
===================

The project is built with the awesome `CFFI <https://cffi.readthedocs.io/en/latest/>`_.
Before that, both `Micropython <https://github.com/micropython/micropython>`_ and
`Pybind11 <https://github.com/pybind/pybind11>`_ have been tried, but each comes with
its own drawback (basically API complexity and compatibility for Micropython,
C++ craziness and output size for Pybind11) so they just couldn't compete with
CFFI ;-)

CFFI connects with Godot C APIs:
- `GDnative <https://godotengine.org/article/dlscript-here>`_ for calling Godot functions
- Pluginscript for registering callback function for Godot
CFFI connects to Godot C

Map of the code:

- ``pythonscript.[c|h]``: Godot Pluginscript entry point.
- ``cffi_bindings/api.h`` & ``cffi_bindings/api_struct.h``: Exposed C api use in the language classes implementations.
- ``cffi_bindings/*.inc.py``: Python code that will be verbatim included in the pythonscript module.
- ``cffi_bindings/builtin_*.inc.py``: Python binding for Godot builtins
- ``cffi_bindings/embedding_init_code.inc.py``: Very first Python code that will be executed on module loading.
- ``cffi_bindings/mod_godot.inc.py``: Python ``godot`` module code.
- ``cffi_bindings/mod_godot_bindings.inc.py``: Python ``godot.bindings`` module code.
- ``cffi_bindings/cdef.gen.h``: C Godot's GDnative API ready to be used by the CFFI generator.
  This file is generated by ``tools/generate_gdnative_cffidefs.py``.
- ``cffi_bindings/pythonscriptcffi.cpp``: Pythonscript module output by the CFFI generator.
  This file is generated by ``cffi_bindings/generate.py``.


FAQ
===

**How can I debug my project with PyCharm?**

This can be done using "Attach to Local Process", but first you have to change the Godot binary filename to include :code:`python`, for example :code:`Godot_v3.0.2-stable_win64.exe` to :code:`python_Godot_v3.0.2-stable_win64.exe`.
For more detailed guide and explanation see this `external blog post <https://medium.com/@prokopst/debugging-godot-python-with-pycharm-b5f9dd2cf769>`_.

**How can I autoload a python script without attaching it to a Node?**

In your :code:`project.godot` file, add the following section::

  [autoload]
  autoloadpy="*res://autoload.py"

In addition to the usual::

  [gdnative]
  singletons=[ "res://pythonscript.gdnlib" ]

You can use any name for the python file and the class name
:code:`autoloadpy`.

Then :code:`autoload.py` can expose a Node::

  from godot import exposed, export
  from godot.bindings import *

  @exposed
  class autoload(Node):

      def hi(self, to):
          return 'Hello %s from Python !' % to

which can then be called from your gdscript code as an attribute of
the :code:`autoloadpy` class (use the name defined in your :code:`project.godot`)::

  print(autoloadpy.hi('root'))

**How can I efficiently access PoolArrays?**

:code:`PoolIntArray`, :code:`PoolFloatArray`, :code:`PoolVector3Array`
and the other pool arrays can't be accessed directly because they must
be locked in memory first. Use the :code:`arr.raw_access()` context
manager to lock it::

  arr = PoolIntArray() # create the array
  arr.resize(10000)

  with arr.raw_access() as ptr:
      for i in range(10000):
          ptr[i] = i # this is fast

  # read access:
  with arr.raw_access() as ptr:
      for i in range(10000):
          assert ptr[i] == i # so is this

See the `godot-python issue <https://github.com/touilleMan/godot-python/issues/84>`_.
