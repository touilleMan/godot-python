cdef bint __pythonscript_verbose = False


# /!\ This dict is strictly private /!\
# It contains class objects that are referenced
# from Godot without refcounting, so droping an
# item from there will likely cause a segfault
cdef dict __exposed_classes_per_module = {}


cdef object get_exposed_class(str module_name):
    return __exposed_classes_per_module.get(module_name)


cdef void set_exposed_class(object cls):
    __exposed_classes_per_module[cls.__module__] = cls


cdef void destroy_exposed_class(object cls):
    del __exposed_classes_per_module[cls.__module__]
