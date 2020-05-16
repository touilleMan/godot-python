cdef bint __pythonscript_verbose = False
import threading

# /!\ This dict is strictly private /!\
# It contains class objects that are referenced
# from Godot without refcounting, so droping an
# item from there will likely cause a segfault
cdef dict __exposed_classes_per_module = {}
__all_loaded_classes = {}
__exposed_classes_lock = threading.Lock()

import sys
cdef object get_exposed_class(str module_name):
    sys.stdout.flush()
    return __exposed_classes_per_module.get(module_name, (None, None))[0]


cdef void set_exposed_class(object cls):
    sys.stdout.flush()

    modname = cls.__module__
    # use a threadlock to avoid data races in case godot loads/unloads scripts in multiple threads
    with __exposed_classes_lock:

        # we must keep track of reference counts for the module when reloading a script,
        # godot calls pythonscript_script_init BEFORE pythonscript_script_finish
        # this happens because Godot can make multiple PluginScript instances for the same resource.
        if modname in __exposed_classes_per_module:
            cls, mod_refcount = __exposed_classes_per_module[modname]
            __exposed_classes_per_module[cls.__module__] = (cls, mod_refcount + 1)
        else:
            __exposed_classes_per_module[cls.__module__] = (cls, 1)
        
        # Sometimes godot fails to reload a script, and when this happens
        # we end up with a stale PyObject* for the class, which then python collects
        # and next time script is instantiated, SIGSEGV. so we keep a reference and avoid
        # stale classes being collected
        classlist = __all_loaded_classes.get(modname, [])
        classlist.append(cls)
        __all_loaded_classes[modname] = classlist


cdef void destroy_exposed_class(object cls):
    sys.stdout.flush()

    modname = cls.__module__
    # use a threadlock to avoid data races in case godot loads/unloads scripts in multiple threads
    with __exposed_classes_lock:
        if modname in __exposed_classes_per_module:
            cls, mod_refcount = __exposed_classes_per_module[modname]

            if mod_refcount == 1:
                del __exposed_classes_per_module[modname]
                # Not safe to ever get rid of all references...
                # see: https://github.com/touilleMan/godot-python/issues/170
                # and: https://github.com/godotengine/godot/issues/10946
                # sometimes script reloading craps out leaving dangling references
                # del __all_loaded_classes[modname]
            else:
                __exposed_classes_per_module[modname] = (cls, mod_refcount - 1)
        else:
            print('Error: class module is already destroyed: {modname}')