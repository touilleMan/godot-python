# TODO: remove this stuff, this is no longer in use

# /!\ Those containers are strictly private /!\
# They contain class objects that are referenced from Godot without refcounting,
# so droping an item from there will likely cause a segfault !
__modules_with_exposed_class: dict[str, type] = {}
# __all_exposed_classes: list[type] = []
import threading

__exposed_classes_lock: threading.Lock = threading.Lock()
del threading


def _get_exposed_class(module_name: str) -> type | None:
    with __exposed_classes_lock:
        try:
            return __modules_with_exposed_class[module_name]
        except KeyError:
            return None


def _set_exposed_class(cls: type) -> None:
    modname = cls.__module__

    # Use a threadlock to avoid data races in case godot loads/unloads scripts in multiple threads
    with __exposed_classes_lock:
        # We must keep track of reference counts for the module when reloading a script,
        # godot calls pythonscript_script_init BEFORE pythonscript_script_finish
        # this happens because Godot can make multiple PluginScript instances for the same resource.

        # Godot calls
        try:
            mod = __modules_with_exposed_class[modname]
        except KeyError:
            __modules_with_exposed_class[modname] = cls
        # else:
        #     # When reloading a script, Godot calls `pythonscript_script_init` BEFORE
        #     # `pythonscript_script_finish`. Hence we drop replace the old class
        #     # here but have to increase the refcount so
        #     mod.kls = cls
        #     mod.refcount += 1

        # # Sometimes Godot fails to reload a script, and when this happens we end
        # # up with a stale PyObject* for the class, which is then garbage collected by Python
        # # so next time a script is instantiated from Godot we end up with a sefault :(
        # # To avoid this we keep reference forever to all the classes.
        # # TODO: This may be troublesome when running the Godot editor given the classes are
        # # reloaded each time they are modified, hence leading to a small memory leak...
        # __all_exposed_classes.append(cls)


def _destroy_exposed_class(cls: type) -> None:
    modname = cls.__module__

    # Use a threadlock to avoid data races in case godot loads/unloads scripts in multiple threads
    with __exposed_classes_lock:
        try:
            __modules_with_exposed_class.pop(modname)
        except KeyError:
            print(f"Error: class module is already destroyed: {modname}", flush=True)

        # try:
        #     mod = __modules_with_exposed_class[modname]
        # except KeyError:
        #     print(f'Error: class module is already destroyed: {modname}')
        # else:
        #     if mod.refcount == 1:
        #         del __modules_with_exposed_class[modname]
        #         # Not safe to ever get rid of all references...
        #         # see: https://github.com/touilleMan/godot-python/issues/170
        #         # and: https://github.com/godotengine/godot/issues/10946
        #         # sometimes script reloading craps out leaving dangling references
        #         # __all_exposed_classes.remove(modname, cls)
        #     else:
        #         mod.refcount -= 1



def exposed(cls=None, /, *, tool=False):
    """
    Decorator used to mark a class as beeing exposed to Godot (hence making
    it available from other Godot languages and the Godot IDE).
    Due to how Godot identifiest classes by their file pathes, only a single
    class can be marked with this decorator per file.

    usage::

        @exposed
        class CustomObject(godot.bindings.Object):
            pass
    """
    from godot.classes import Object, BaseGDObject

    def _exposed(cls: type):
        parents = [x for x in cls.__bases__ if issubclass(x, Object)]
        if len(parents) == 1:
            cls_parent = parents[0]
        elif len(parents) == 0:
            raise ValueError(
                f"{cls!r} must inherit from a Godot (e.g. `godot.bindings.Node`) "
                "class to be marked as @exposed"
            )
        else:
            raise ValueError(
                f"{cls!r} cannot inherit from multiple Godot classes (got {parents!r})"
            )

        existing_cls_for_module = _get_exposed_class(cls.__module__)
        if existing_cls_for_module:
            raise ValueError(
                "Only a single class can be marked as @exposed per module"
                f" (already got {existing_cls_for_module!r})"
            )

        # If `cls_parent` is itself a script it has `__owner_cls` defined,
        # otherwise it must be the Godot class we are looking for.
        cls.__owner_cls = getattr(cls_parent, "__owner_cls", cls_parent)
        cls.__tool = tool
        cls.__exposed_python_class = True
        cls.__exported = {}

        # Retrieve parent exported stuff
        for b in cls.__bases__:
            cls.__exported.update(getattr(b, "__exported", {}))

        init_func_code = "def __init__(self):\n    pass\n"

        # Collect exported stuff: attributes (marked with @exported), properties, signals, and methods
        for k, v in cls.__dict__.items():
            if callable(v):
                cls.__exported[k] = v
            # if isinstance(v, ExportedField):
            #     cls.__exported[k] = v
            #     v.name = k  # hard to bind this earlier...
            #     if v.property:
            #         # If export has been used to decorate a property, expose it
            #         # in the generated class
            #         setattr(cls, k, v.property)
            #     else:
            #         # Otherwise, the value must be initialized as part of __init__
            #         if v.default is None or isinstance(v.default, (int, float, bool)):
            #             init_func_code += f"    self.{k} = {repr(v.default)}\n"
            #         else:
            #             init_func_code += f"    self.{k} = self.__exported['{k}'].default\n"
            # elif isinstance(v, SignalField):
            #     v.name = v.name or k
            #     cls.__exported[v.name] = v
            #     setattr(cls, k, v)
            # elif callable(v):
            #     cls.__exported[k] = v

        # Overwrite parent __init__ to avoid creating a Godot object given
        # exported script are always initialized with an existing Godot object
        # On top of that, we must initialize the attributes defined in the class
        # and it parents
        g = {}
        exec(init_func_code, g)
        assert "__init__" not in cls.__dict__  # TODO: accept ?
        cls.__init__ = g["__init__"]
        if cls.__repr__ is BaseGDObject.__repr__:

            def _repr(self):
                return f"<{type(self).__name__} script owned by {cls.__owner_cls.__name__} on 0x{self._get_gd_ptr():x}>"

            cls.__repr__ = _repr

        # Also overwrite parent new otherwise we would return an instance
        # of a Godot class without our script attached to it...
        @classmethod
        def new(cls):
            raise NotImplementedError(
                "Instantiating Python script from Python is not implemented yet :'("
            )
            # try:
            #     ptr = cls._new()
            # except AttributeError:
            #     # It's also possible we try to instantiate a singleton, but a better
            #     # message will be provided anyway if the user try the provided hint
            #     raise RuntimeError(f"Refcounted Godot object must be created with `{ cls.__name__ }()`")
            # instance = cls._from_ptr(ptr)
            # # TODO: We should generate a Resource instance containing the script
            # # and attach it to the main class here.
            # # instance.set_script(???)

        cls.new = new

        _set_exposed_class(cls)
        return cls

    if cls is None:
        # We're called as `@exposed()` with parens.
        return _exposed

    else:
        # We're called as `@exposed` without parens.
        return _exposed(cls)
