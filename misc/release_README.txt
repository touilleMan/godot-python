  ________           .___      __    __________          __  .__                   
 /  _____/  ____   __| _/_____/  |_  \______   \___.__._/  |_|  |__   ____   ____  
/   \  ___ /  _ \ / __ |/  _ \   __\  |     ___<   |  |\   __\  |  \ /  _ \ /    \ 
\    \_\  (  <_> ) /_/ (  <_> )  |    |    |    \___  | |  | |   Y  (  <_> )   |  \
 \______  /\____/\____ |\____/|__|    |____|    / ____| |__| |___|  /\____/|___|  /
        \/            \/                        \/                \/            \/ 
                                                                     {version} ({date})


Introduction
------------

This is a beta version of the Python module for Godot.

You are likely to encounter bugs and catastrophic crashes, if so please
report them to https://github.com/touilleMan/godot-python/issues.


Working features
----------------

Every Godot core features are expected to work fine:
- builtins (e.g. Vector2)
- Objects classes (e.g. Node)
- signals
- variable export
- rpc synchronisation

On top of that, mixing GDscript and Python code inside a project should work fine.

Python and pip are working, however depending on platform and backend they
- on Windows+CPython use `python.exe` and `python.exe -m pip`
- on Linux+CPython `bin/python` and `bin/pip` are provided out of the box.
  However you must provide path to `libpython3.6m.so` to make them run:
  ```
  $ LD_LIBRARY_PATH=`pwd`/lib ./bin/pip3  --version
  $ LD_LIBRARY_PATH=`pwd`/lib ./bin/python  --version
  ```
- on Linux+Pypy `bin/pypy` runs like a charm, you should use ensurepip to
  install pip:
  ```
  $ bin/pypy -m ensurepip
  $ bin/pypy -m pip --version
  ```


Not so well features
--------------------

Memory management is a big issue (given Godot and Python garbage collectors should be synchronized)
so leaks are possible (hence Godot complaining there is still MemoryPool allocs in use at exit...).

Exporting the project hasn't been tested at all (however exporting for linux should be pretty simple and
may work out of the box...).


Have fun ;-)

  - touilleMan
