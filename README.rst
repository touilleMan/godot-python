.. image:: https://github.com/touilleMan/godot-python/actions/workflows/build.yml/badge.svg
    :target: https://github.com/touilleMan/godot-python/actions
    :alt: Github action tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black


================================================
Godot Python, because you want Python on Godot !
================================================


.. image:: https://github.com/touilleMan/godot-python/raw/master/misc/godot_python.svg
   :width: 200px
   :align: right

The goal of this project is to provide Python language support as a scripting
module for the `Godot <http://godotengine.org>`_ game engine.


Quickstart
==========

By order of simplicity:

- Directly download the project from within Godot with the asset library tab.
- Download from the `asset library website <https://godotengine.org/asset-library/asset/179>`_.
- Finally you can also head to the project `release page <https://github.com/touilleMan/godot-python/releases>`_ if you want to only download one specific platform build


.. image:: https://github.com/touilleMan/godot-python/raw/master/misc/showcase.png
   :align: center


API
===

example:

.. code-block:: python

	# Explicit is better than implicit
	from godot import exposed, export, Vector2, Node2D, ResourceLoader

	WEAPON_RES = ResourceLoader.load("res://weapon.tscn")
	SPEED = Vector2(10, 10)

	@exposed
	class Player(Node2D):
		"""
		This is the file's main class which will be made available to Godot. This
		class must inherit from `godot.Node` or any of its children (e.g.
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
			print(f"I'm saying {msg}")

		def _ready(self):
			# Don't confuse `__init__` with Godot's `_ready`!
			self.weapon = WEAPON_RES.instance()
			self._age = 42
			# Of course you can access property & methods defined in the parent
			name = self.get_name()
			print(f"{name} position x={self.position.x}, y={self.position.y}")

		def _process(self, delta):
			self.position += SPEED * delta

		...


	class Helper:
		"""
		Other classes are considered helpers and cannot be called from outside
		Python. However they can be imported from another python module.
		"""
		...


Building
========

To build the project from source, first checkout the repo or download the
latest tarball.

Godot-Python requires Python >= 3.7 and a C compiler.


Godot GDNative header
---------------------


The Godot GDNative headers are provided as git submodule:

.. code-block:: bash

	$ git submodule init
	$ git submodule update

Alternatively, you can get them `from github <https://github.com/GodotNativeTools/godot_headers>`_.


Linux
-----


On a fresh Ubuntu install, you will need to install these:

.. code-block:: bash

	$ apt install python3 python3-pip python3-venv build-essential

On top of that build the CPython interpreter requires development headers
of it `extension modules <https://devguide.python.org/setup/#install-dependencies>`_
(for instance if you lack sqlite dev headers, your Godot-Python build won't
contain the sqlite3 python module)

The simplest way is to uncomment the main deb-src in `/etc/apt/sources.list`:

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

If you are using CPython as your backend, you will need these. To install with Homebrew:

.. code-block:: bash

	$ brew install python3 openssl zlib

You will also need virtualenv for your python.


Windows
-------


Install VisualStudio and Python3, then submit a PR to improve this paragraph ;-)


Create the virtual env
----------------------

Godot-Python build system is heavily based on Python (mainly Scons, Cython and Jinja2).
Hence we have to create a Python virtual env to install all those dependencies
without clashing with your global Python configuration.


.. code-block:: bash

	$ cd <godot-python-dir>
	godot-python$ python3 -m venv venv


Now you need to activate the virtual env, this is something you should do
every time you want to use the virtual env.

For Linux/MacOS:

.. code-block:: bash

	godot-python$ . ./venv/bin/activate

For Windows:

.. code-block:: bash

	godot-python$ ./venv/bin/activate.bat


Finally we can install dependencies:

.. code-block:: bash

	godot-python(venv)$ pip install -r requirements.txt


Running the build
-----------------


For Linux:

.. code-block:: bash

	godot-python(venv)$ scons platform=x11-64 release

For Windows:

.. code-block:: bash

	godot-python(venv)$ scons platform=windows-64 release

For MacOS:

.. code-block:: bash

	godot-python(venv)$ scons platform=osx-64 CC=clang release

Valid platforms are `x11-64`, `x11-32`, `windows-64`, `windows-32` and `osx-64`.
Check Travis or Appveyor links above to see the current status of your platform.

This command will checkout CPython repo, move to a pinned commit and build
CPython from source.

It will then generate ``pythonscript/godot/bindings.pyx`` (Godot api bindings)
from GDNative's ``api.json`` and compile it.
This part is long and really memory demanding so be patient ;-)
When hacking godot-python you can heavily speedup this step by passing
``sample=true`` to scons in order to build only a small subset of the bindings.

Eventually the rest of the source will be compiled and a zip build archive
will be available in the build directory.


Testing your build
------------------

.. code-block:: bash

	godot-python(venv)$ scons platform=<platform> test

This will run pytests defined in `tests/bindings` inside the Godot environment.
If not present, will download a precompiled Godot binary (defined in SConstruct
and platform specific SCSub files) to and set the correct library path for
the GDNative wrapper.


Running the example project
---------------------------

.. code-block:: bash

	godot-python(venv)$ scons platform=<platform> example

This will run the converted pong example in `examples/pong` inside the Godot
environment. If not present, will download a precompiled Godot binary
(defined in SConstruct) to and set the correct library path for the GDNative
wrapper.


Using a local Godot version
---------------------------

If you have a pre-existing version of godot, you can instruct the build script to
use that the static library and binary for building and tests.

.. code-block:: bash

	godot-python(venv)$ scons platform=x11-64 godot_binary=../godot/bin/godot.x11.opt.64


Additional build options
------------------------

You check out all the build options `in this file <https://github.com/touilleMan/godot-python/blob/master/SConstruct#L23>`_.


FAQ
===

**How can I export my project?**

Currently, godot-python does not support automatic export, which means that the python environment is not copied to the release when using Godot's export menu. A release can be created manually:

First, export the project in .zip format.

Second, extract the .zip in a directory. For sake of example let's say the directory is called :code:`godotpythonproject`.

Third, copy the correct Python environment into this folder (if it hasn't been automatically included in the export). Inside your project folder, you will need to find :code:`/addons/pythonscript/x11-64`, replacing "x11-64" with the correct target system you are deploying to. Copy the entire folder for your system, placing it at the same relative position, e.g. :code:`godotpythonproject/addons/pythonscript/x11-64` if your unzipped directory was "godotpythonproject". Legally speaking you should also copy LICENSE.txt from the pythonscript folder. (The lazy option at this point is to simply copy the entire addons folder from your project to your unzipped directory.)

Fourth, place a godot release into the directory. The Godot export menu has probably downloaded an appropriate release already, or you can go to Editor -> Manage Export Templates inside Godot to download fresh ones. These are stored in a location which depends on your operating system. For example, on Windows they may be found at :code:`%APPDATA%\Godot\templates\ `; in Linux or OSX it is :code:`~/.godot/templates/`. Copy the file matching your export. (It may matter whether you selected "Export With Debug" when creating the .zip file; choose the debug or release version accordingly.)

Running the Godot release should now properly execute your release. However, if you were developing on a different Python environment (say, the one held in the osx-64 folder) than you include with the release (for example the windows-64 folder), and you make any alterations to that environment, such as installing Python packages, these will not carry over; take care to produce a suitable Python environment for the target platform.

See also `this issue <https://github.com/touilleMan/godot-python/issues/146>`_.

**How can I use Python packages in my project?**

In essence, godot-python installs a python interpreter inside your project which can then be distributed as part of the final game. Python packages you want to use need to be installed for that interpreter and of course included in the final release. This can be accomplished by using pip to install packages; however, pip is not provided, so it must be installed too.

First, locate the correct python interpreter. This will be inside your project at :code:`addons\pythonscript\windows-64\python.exe` for 64-bit Windows, :code:`addons/pythonscript/ox-64/bin/python3` for OSX, etc. Then install pip by running:

.. code-block::

	addons\pythonscript\windows-64\python.exe -m ensurepip

(substituting the correct python for your system). Any other method of installing pip at this location is fine too, and this only needs to be done once. Afterward, any desired packages can be installed by running

.. code-block::

	addons\pythonscript\windows-64\python.exe -m pip install numpy

again, substituting the correct python executable, and replacing numpy with whatever packages you desire. The package can now be imported in your Python code as normal.

Note that this will only install packages onto the target platform (here, windows-64), so when exporting the project to a different platform, care must be taken to provide all the necessary libraries.

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

Keep in mind great performances comes with great responsabilities: there is no
boundary check so you may end up with memory corruption if you don't take care ;-)

See the `godot-python issue <https://github.com/touilleMan/godot-python/issues/84>`_.
