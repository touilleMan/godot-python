from _godot import __global_constants


def __getattr__(name):
    try:
        return __global_constants[name]
    except KeyError:
        raise AttributeError


def __dir__():
    return list(__global_constants.keys())
