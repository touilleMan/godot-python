cdef bint __pythonscript_verbose
cdef object __exposed_classes_per_module


cdef inline bint get_pythonscript_verbose():
    return __pythonscript_verbose


cdef inline void set_pythonscript_verbose(bint status):
    global __pythonscript_verbose
    __pythonscript_verbose = status


cdef inline object get_exposed_class_per_module(str module_name):
    return __exposed_classes_per_module.get(module_name)


cdef inline void set_exposed_class_per_module(str module_name, object cls):
    __exposed_classes_per_module[module_name] = cls


cdef inline void destroy_exposed_classes():
    __exposed_classes_per_module.clear()
