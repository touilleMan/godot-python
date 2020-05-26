from godot.bindings cimport Object


cdef bint __pythonscript_verbose


cdef inline bint get_pythonscript_verbose():
    return __pythonscript_verbose


cdef inline void set_pythonscript_verbose(bint status):
    global __pythonscript_verbose
    __pythonscript_verbose = status


cdef object get_exposed_class(str module_name)
cdef void set_exposed_class(object cls)
cdef void destroy_exposed_class(object cls)
