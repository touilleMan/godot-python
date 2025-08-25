from .classes import _load_singleton


def __getattr__(name: str):
    try:
        return _load_singleton(name)
    except RuntimeError:
        raise AttributeError
