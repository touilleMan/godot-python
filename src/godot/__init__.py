# TODO: now that the gdptrs are located in `libgdpy.so`, doing a `import godot`
# from a python interpreter cause a `ImportError: libgdpy.so: cannot open shared object file: No such file or directory`
# when doing `from godot.builtins import *`. We should change the sanity check accordingly...

# Start with a sanity check to ensure the loading is done from Godot-Python
# (and not from a regular Python interpreter which would lead to a segfault).
# The idea is we should have the following loading order:
# godot binary -> libgdpy.so -> godot/__init__.py
import sys
from dataclasses import dataclass
from typing import dataclass_transform

if sys.argv[0] != "":  # `sys.argv` is configured later on by `godot._lang._gdpy_initialize()`
    raise ImportError(
        "Cannot initialize godot module given Godot GDExtension API not available.\n"
        "This is most likely because you are running code from a regular Python interpreter"
        " (i.e. using a REPL or doing something like `python my_script.py`) while godot module"
        " is only available to Python code loaded from Godot through Godot-Python plugin."
    )
del sys

from ._version import __version__  # noqa: E402, F401

# from .tags import (
#     MethodRPCMode,
#     PropertyHint,
#     PropertyUsageFlag,
#     rpcdisabled,
#     rpcremote,
#     rpcmaster,
#     rpcpuppet,
#     rpcslave,
#     rpcremotesync,
#     rpcsync,
#     rpcmastersync,
#     rpcpuppetsync,
#     signal,
#     export,
#     exposed,
# )
from .builtins import *  # noqa: E402, F403
from . import utils  # noqa: E402, F401

# import typing
# type Export[x] = typing.Annotated[x, _export_tag]

# from .classes import _load_singleton, _load_class


# def __getattr__(name):
#     # Look for singleton first given they have the same name than their class
#     item = _load_singleton(name) or _load_class(name)

#     if not item:
#         raise AttributeError

#     # Cache entry
#     setattr(globals(), name, item)

#     return item


@dataclass_transform()
def gddataclass(
    cls=None,
    /,
    virtual: bool = False,
    abstract: bool = False,
    exposed: bool = True,
    runtime: bool = True,
    icon_path: str | None = None,
    **kwargs,
):
    assert kwargs.get("init", True), "Cannot disable `init=True` param"

    def _gddataclass(cls):
        cls.__gdpy_is_virtual = virtual
        cls.__gdpy_is_abstract = abstract
        cls.__gdpy_is_exposed = exposed  # Show the class in the editor's class picker?
        cls.__gdpy_is_runtime = runtime  # Inverse of the `@tool` marker
        cls.__gdpy_icon_path = icon_path
        return dataclass(**kwargs)(cls)

    if cls is not None:
        # Called without parenthesis
        return _gddataclass(cls)
    else:
        return _gddataclass
