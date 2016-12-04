__exposed_classes = {}
__exposed_classes_per_module = {}


# TODO provide `tool` parameter
def exposed(cls):
    print(cls, cls.__module__)
    assert cls.__name__ not in __exposed_classes
    assert cls.__module__ not in __exposed_classes_per_module
    __exposed_classes[cls.__name__] = cls
    __exposed_classes_per_module[cls.__module__] = cls
    return cls


def export(type):
    return None


def get_exposed_class_per_module(module_name):
    return __exposed_classes_per_module[module_name]


class Node:
    pass


class Node2D(Node):
    pass
