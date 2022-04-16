from contextlib import contextmanager
from contextvars import ContextVar
from typing import Dict, List, Sequence, Set, Callable, Union, Optional, Any, Union, TypeVar, Type

from ._exceptions import IsengardError


_parent: ContextVar["Isengard"] = ContextVar("context")


def get_parent() -> "Isengard":
    try:
        return _parent.get()
    except LookupError as exc:
        raise IsengardError("Not in a subdir !") from exc


@contextmanager
def _set_parent(parent: "Isengard"):
    try:
        token = _parent.set(parent)
        yield
    finally:
        _parent.reset(token)
