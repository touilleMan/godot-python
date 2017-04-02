import imp
import sys


__exposed_classes = {}
__exposed_classes_per_module = {}


class ExportedField:
    def __init__(self, type, default):
        self.type = type
        self.default = default


def exposed(cls=None, tool=False):

    def wrapper(cls):
        global __exposed_classes, __exposed_classes_per_module
        print("Exposing %s.%s Python class to Godot." % (cls.__module__, cls))
        assert cls.__name__ not in __exposed_classes
        assert cls.__module__ not in __exposed_classes_per_module
        cls._tool = tool
        __exposed_classes[cls.__name__] = cls
        __exposed_classes_per_module[cls.__module__] = cls
        return cls

    if cls:
        return wrapper(cls)
    else:
        return wrapper


def export(type, default=None):
    return ExportedField(type, default)


def get_exposed_class_per_module(module):
    if not isinstance(module, str):
        module = module.__name__
    print('RESOLVED', module, __exposed_classes_per_module[module])
    return __exposed_classes_per_module[module]


def get_exposed_class_per_name(classname):
    return __exposed_classes[classname]


module = imp.new_module("godot")
module.export = export
module.exposed = exposed
module.get_exposed_class_per_module = get_exposed_class_per_module
module.get_exposed_class_per_name = get_exposed_class_per_name

sys.modules["godot"] = module
