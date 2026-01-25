from .builtins import _load_class, StringName


def __getattr__(name: str) -> type:
    try:
        return _load_class(StringName(name))
    except RuntimeError:
        raise AttributeError
