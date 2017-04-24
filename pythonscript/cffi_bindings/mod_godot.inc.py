import imp
import sys
import builtins


__exposed_classes = {}
__exposed_classes_per_module = {}


class ExportedField:

    def __init__(self, type, default=None, name='', hint=0, usage=lib.GODOT_PROPERTY_USAGE_DEFAULT, hint_string=''):
        self.property = None

        self.type = type
        self.default = default
        self.name = name
        self.hint = hint
        self.usage = usage
        self.hint_string = hint_string

        self.gd_hint = self.hint
        self.gd_usage = self.usage
        self.gd_hint_string = pyobj_to_raw(lib.GODOT_VARIANT_TYPE_STRING, self.hint_string)
        self.gd_type = py_to_gd_type(self.type)
        if self.default is not None:
            self.gd_default = pyobj_to_raw(self.gd_type, self.default)
        else:
            self.gd_default = ffi.NULL

    @property
    def gd_name(self):
        # Name is defined lazily when ExportedField is connected to it class
        return pyobj_to_raw(lib.GODOT_VARIANT_TYPE_STRING, self.name)

    def __repr__(self):
        return '<{x.__class__.__name__}(type={x.type}, default={x.default})>'.format(x=self)

    def __call__(self, decorated):
        # This object is used as a decorator
        if not callable(decorated) and not isinstance(decorated, builtins.property):
            raise RuntimeError("@export should decorate function or property.")
        # Next time this object is called, call the decorated instead
        self.property = decorated
        return self

    def setter(self, setfunc):
        self.property = self.property.setter(setfunc)
        return self


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


def export(type, default=None, **kwargs):
    return ExportedField(type, default, **kwargs)


def get_exposed_class_per_module(module):
    if not isinstance(module, str):
        module = module.__name__
    return __exposed_classes_per_module[module]


def get_exposed_class_per_name(classname):
    return __exposed_classes[classname]


module = imp.new_module("godot")
module.export = export
module.exposed = exposed
module.get_exposed_class_per_module = get_exposed_class_per_module
module.get_exposed_class_per_name = get_exposed_class_per_name

sys.modules["godot"] = module
