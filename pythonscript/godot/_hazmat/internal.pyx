import threading

from godot.bindings cimport Object


cdef bint __pythonscript_verbose = False


cdef class ModExposedClass:
    cdef object kls
    cdef int refcount

    def __init__(self, object kls):
        self.kls = kls
        self.refcount = 1


# /!\ Those containers are strictly private /!\
# They contain class objects that are referenced from Godot without refcounting,
# so droping an item from there will likely cause a segfault !
cdef dict __modules_with_exposed_class = {}
cdef list __all_exposed_classes = []
cdef object __exposed_classes_lock = threading.Lock()


cdef object get_exposed_class(str module_name):
    with __exposed_classes_lock:
        try:
            return (<ModExposedClass>__modules_with_exposed_class[module_name]).kls
        except KeyError:
            return None


cdef void set_exposed_class(object cls):
    cdef ModExposedClass mod
    cdef str modname = cls.__module__

    # Use a threadlock to avoid data races in case godot loads/unloads scripts in multiple threads
    with __exposed_classes_lock:

        # We must keep track of reference counts for the module when reloading a script,
        # godot calls pythonscript_script_init BEFORE pythonscript_script_finish
        # this happens because Godot can make multiple PluginScript instances for the same resource.

        # Godot calls
        try:
            mod = __modules_with_exposed_class[modname]
        except KeyError:
            __modules_with_exposed_class[modname] = ModExposedClass(cls)
        else:
            # When reloading a script, Godot calls `pythonscript_script_init` BEFORE
            # `pythonscript_script_finish`. Hence we drop replace the old class
            # here but have to increase the refcount so
            mod.kls = cls
            mod.refcount += 1

        # Sometimes Godot fails to reload a script, and when this happens we end
        # up with a stale PyObject* for the class, which is then garbage collected by Python
        # so next time a script is instantiated from Godot we end up with a sefault :(
        # To avoid this we keep reference forever to all the classes.
        # TODO: This may be troublesome when running the Godot editor given the classes are
        # reloaded each time they are modified, hence leading to a small memory leak...
        __all_exposed_classes.append(cls)


cdef void destroy_exposed_class(object cls):
    cdef ModExposedClass mod
    cdef str modname = cls.__module__

    # Use a threadlock to avoid data races in case godot loads/unloads scripts in multiple threads
    with __exposed_classes_lock:

        try:
            mod = __modules_with_exposed_class[modname]
        except KeyError:
            print(f'Error: class module is already destroyed: {modname}')
        else:
            if mod.refcount == 1:
                del __modules_with_exposed_class[modname]
                # Not safe to ever get rid of all references...
                # see: https://github.com/touilleMan/godot-python/issues/170
                # and: https://github.com/godotengine/godot/issues/10946
                # sometimes script reloading craps out leaving dangling references
                # __all_exposed_classes.remove(modname, cls)
            else:
                mod.refcount -= 1
