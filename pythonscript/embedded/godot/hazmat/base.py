import imp
import sys
import builtins

from pythonscriptcffi import lib, ffi


__exposed_classes = {}
__exposed_classes_per_module = {}


# Expose RPC modes can be used both as a decorator and a value to pass
# to ExportedField ;-)


class RPCMode:

    def __init__(self, mod, modname):
        self.mod = mod
        self.modname = modname

    def __call__(self, decorated):
        if isinstance(decorated, ExportedField):
            decorated.rpc = self.mod
        else:
            decorated.__rpc = self.mod

    def __repr__(self):
        return "<%s(%s)>" % (type(self).__name__, self.modname)


rpcmaster = RPCMode(lib.GODOT_METHOD_RPC_MODE_MASTER, "master")
rpcslave = RPCMode(lib.GODOT_METHOD_RPC_MODE_SLAVE, "slave")
rpcremote = RPCMode(lib.GODOT_METHOD_RPC_MODE_REMOTE, "remote")
rpcsync = RPCMode(lib.GODOT_METHOD_RPC_MODE_SYNC, "sync")


class SignalField:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%s(%r)>" % (type(self).__name__, self.name)


# TODO: this can be greatly improved to make it more pythonic


class ExportedField:

    def __init__(
        self,
        type,
        default=None,
        name="",
        hint=0,
        usage=lib.GODOT_PROPERTY_USAGE_DEFAULT,
        hint_string="",
        rpc=lib.GODOT_METHOD_RPC_MODE_DISABLED,
    ):
        self.property = None

        self.type = type
        self.default = default
        self.name = name
        self.hint = hint
        self.usage = usage
        self.hint_string = hint_string
        if isinstance(rpc, RPCMode):
            self.rpc = rpc.mod
        else:
            self.rpc = rpc

    def __repr__(self):
        return "<{x.__class__.__name__}(type={x.type}, default={x.default})>".format(
            x=self
        )

    def __call__(self, decorated):
        # This object is used as a decorator
        if not callable(decorated) and not isinstance(decorated, builtins.property):
            raise RuntimeError("@export should decorate function or property.")

        # It's possible decorated has already been passed through a rpc decorator
        rpc = getattr(decorated, "__rpc", None)
        if rpc:
            self.rpc = rpc
        self.property = decorated
        return self

    def setter(self, setfunc):
        if not self.property:
            raise RuntimeError(
                "Cannot use setter attribute before defining the getter !"
            )

        self.property = self.property.setter(setfunc)
        return self


def signal(name=None):
    return SignalField(name)


def exposed(cls=None, tool=False):

    def wrapper(cls):
        global __exposed_classes, __exposed_classes_per_module
        assert issubclass(cls, BaseObject), (
            "%s must inherit from a Godot (e.g. `godot.bindings.Node`) "
            "class to be marked as @exposed" % cls
        )
        assert cls.__name__ not in __exposed_classes
        assert cls.__module__ not in __exposed_classes_per_module
        cls.__tool = tool
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


def destroy_exposed_classes():
    global __exposed_classes
    global __exposed_classes_per_module
    __exposed_classes.clear()
    __exposed_classes_per_module.clear()


class BuiltinInitPlaceholder:
    __slots__ = ("_gd_ptr",)


class BaseBuiltin:
    __slots__ = ("_gd_ptr",)

    GD_TYPE = lib.GODOT_VARIANT_TYPE_NIL  # Overwritten by children

    def __copy__(self):
        return self.build_from_gdobj(self._gd_obj)

    @classmethod
    def build_from_gdobj(cls, gdobj, steal=False):
        # Avoid calling cls.__init__ by first instanciating a placeholder, then
        # overloading it __class__ to turn it into an instance of the right class
        ret = BuiltinInitPlaceholder()
        if steal:
            assert ffi.typeof(gdobj).kind == "pointer"
            ret._gd_ptr = gdobj
        else:
            if ffi.typeof(gdobj).kind == "pointer":
                ret._gd_ptr = cls._copy_gdobj(gdobj)
            else:
                ret._gd_ptr = cls._copy_gdobj(ffi.addressof(gdobj))
        ret.__class__ = cls
        return ret

    @staticmethod
    def _check_param_type(argname, arg, type):
        if not isinstance(arg, type):
            raise TypeError("Param `%s` should be of type `%s`" % (argname, type))

    @staticmethod
    def _check_param_float(argname, arg):
        if not isinstance(arg, (int, float)):
            raise TypeError("Param `%s` should be of type `float`" % argname)


class BaseBuiltinWithGDObjOwnership(BaseBuiltin):
    __slots__ = ()

    # def __init__(self, __copy_gdobj=None, __steal_gdobj=None):
    #     raise NotImplementedError()

    # @classmethod
    # def build_from_gdobj(cls, gdobj, steal=True):
    #     # TODO: find a way to avoid copy
    #     if not steal:
    #         gdobj = self._copy_gdobj(gdobj)
    #     return super().build_from_gdobj(gdobj)

    # @staticmethod
    # def _copy_gdobj(gdobj):
    #     raise NotImplementedError()

    def __copy__(self):
        return self.build_from_gdobj(self._hazmat_gdobj_alloc(self._gd_ptr))


# def __del__(self):
#     raise NotImplementedError()


class MetaBaseObject(type):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_OBJECT

    def __new__(cls, name, bases, nmspc):
        if ("__init__" in nmspc or "__new__" in nmspc) and name != "BaseObject":
            raise RuntimeError(
                "Exported to Godot class must not redefine "
                "`__new__` or `__init__`, use `_ready` instead"
            )

        exported = {}
        signals = {}
        cooked_nmspc = {"__exported": exported, "__signals": signals}
        godot_parent_classes = [b for b in bases if issubclass(b, BaseObject)]
        if len(godot_parent_classes) > 1:
            raise RuntimeError(
                "Exported to Godot class cannot inherit more than one Godot class"
            )

        # Retrieve parent exported fields
        for b in bases:
            exported.update(getattr(b, "__exported", {}))
            signals.update(getattr(b, "__signals", {}))
        # Collect exported fields
        for k, v in nmspc.items():
            if isinstance(v, ExportedField):
                exported[k] = v
                v.name = k  # hard to bind this earlier...
                if v.property:
                    # If export has been used to decorate a property, expose it
                    # in the generated class
                    cooked_nmspc[k] = v.property
                else:
                    cooked_nmspc[k] = v.default
            elif isinstance(v, SignalField):
                v.name = v.name if v.name else k
                signals[v.name] = v
                cooked_nmspc[k] = v
            else:
                cooked_nmspc[k] = v
        return type.__new__(cls, name, bases, cooked_nmspc)


# TODO: create a BaseReferenceObject which store the variant to avoid
# garbage collection


class BaseObject(metaclass=MetaBaseObject):
    __slots__ = ("_gd_ptr", "_gd_var")

    def __init__(self, gd_obj_ptr=None):
        """
        Note that gd_obj_ptr should not have ownership of the Godot's Object
        memory given it livespan is not related to its Python wrapper.
        """
        gd_ptr = gd_obj_ptr if gd_obj_ptr else self._gd_constructor()
        object.__setattr__(self, "_gd_ptr", gd_ptr)

    def __getattr__(self, name):
        # If a script is attached to the object, we expose here it methods
        script = self.get_script()
        if not script:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self).__name__, name)
            )

        if self.has_method(name):
            return lambda *args: self.call(name, *args)

        elif any(x for x in self.get_property_list() if x["name"] == name):
            # TODO: Godot currently lacks a `has_property` method
            return self.get(name)

        else:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self).__name__, name)
            )

    def __setattr__(self, name, value):
        try:
            object.__setattr__(self, name, value)
        except AttributeError:
            # Could retrieve the item inside the Godot class, try to look into
            # the attached script if it has one
            script = self.get_script()
            if not script:
                raise AttributeError(
                    "'%s' object has no attribute '%s'" % (type(self).__name__, name)
                )

            self.set(name, value)

    def __eq__(self, other):
        return hasattr(other, "_gd_ptr") and self._gd_ptr == other._gd_ptr
