from .builtins import _load_singleton, BaseGDObject


def __getattr__(name: str) -> BaseGDObject:
    # Skip dunder attributes (e.g. `my_module.__path__`) since no singletons are
    # named this way, and trying to load a non-existing singleton leads Godot to
    # output an error log.
    if name.startswith("__"):
        raise AttributeError
    try:
        return _load_singleton(name)
    except RuntimeError:
        raise AttributeError
