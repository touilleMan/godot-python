import imp
import sys
import builtins

__version__ = '0.9.0'
__author__ = 'Emmanuel Leblond'
__email__ = 'emmanuel.leblond@gmail.com'

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
        return '<%s(%s)>' % (type(self).__name__, self.modname)


class SignalField:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s(%r)>' % (type(self).__name__, self.name)


class ExportedField:

    def __init__(self, type, default=None, name='', hint=0,
                 usage=lib.GODOT_PROPERTY_USAGE_DEFAULT, hint_string='',
                 rpc=lib.GODOT_METHOD_RPC_MODE_DISABLED):
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

        self.gd_hint = self.hint
        self.gd_usage = self.usage
        self.gd_hint_string = pyobj_to_gdobj(self.hint_string)
        self.gd_type = py_to_gd_type(self.type)
        if self.default is not None:
            self.gd_default = pyobj_to_gdobj(self.default)
        else:
            self.gd_default = ffi.NULL

    @property
    def gd_name(self):
        # Name is defined lazily when ExportedField is connected to it class
        return pyobj_to_gdobj(self.name)

    def __repr__(self):
        return '<{x.__class__.__name__}(type={x.type}, default={x.default})>'.format(x=self)

    def __call__(self, decorated):
        # This object is used as a decorator
        if not callable(decorated) and not isinstance(decorated, builtins.property):
            raise RuntimeError("@export should decorate function or property.")
        # It's possible decorated has already been passed through a rpc decorator
        rpc = getattr(decorated, '__rpc', None)
        if rpc:
            self.rpc = rpc
        self.property = decorated
        return self

    def setter(self, setfunc):
        if not self.property:
            raise RuntimeError("Cannot use setter attribute before defining the getter !")
        self.property = self.property.setter(setfunc)
        return self


def signal(name=None):
    return SignalField(name)


def exposed(cls=None, tool=False):

    def wrapper(cls):
        global __exposed_classes, __exposed_classes_per_module
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


class BuiltinInitPlaceholder:
    __slots__ = ('_gd_ptr', )


class BaseBuiltin:
    __slots__ = ('_gd_ptr', )

    GD_TYPE = lib.GODOT_VARIANT_TYPE_NIL  # Overwritten by children

    def __copy__(self):
        return self.build_from_gdobj(self._gd_obj)

    @classmethod
    def build_from_gdobj(cls, gdobj, steal=False):
        # Avoid calling cls.__init__ by first instanciating a placeholder, then
        # overloading it __class__ to turn it into an instance of the right class
        ret = BuiltinInitPlaceholder()
        if steal:
            assert ffi.typeof(gdobj).kind == 'pointer'
            ret._gd_ptr = gdobj
        else:
            if ffi.typeof(gdobj).kind == 'pointer':
                ret._gd_ptr = cls._copy_gdobj(gdobj)
            else:
                ret._gd_ptr = cls._copy_gdobj(ffi.addressof(gdobj))
        ret.__class__ = cls
        return ret

    @staticmethod
    def _check_param_type(argname, arg, type):
        if not isinstance(arg, type):
            raise TypeError('Param `%s` should be of type `%s`' % (argname, type))

    @staticmethod
    def _check_param_float(argname, arg):
        if not isinstance(arg, (int, float)):
            raise TypeError('Param `%s` should be of type `float`' % argname)


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


module = imp.new_module("godot")
module.__version__ = __version__
module.__author__ = __author__
module.__email__ = __email__
module.signal = signal
module.export = export
module.exposed = exposed
module.get_exposed_class_per_module = get_exposed_class_per_module
module.get_exposed_class_per_name = get_exposed_class_per_name
module.rpcmaster = RPCMode(lib.GODOT_METHOD_RPC_MODE_MASTER, 'master')
module.rpcslave = RPCMode(lib.GODOT_METHOD_RPC_MODE_SLAVE, 'slave')
module.rpcremote = RPCMode(lib.GODOT_METHOD_RPC_MODE_REMOTE, 'remote')
module.rpcsync = RPCMode(lib.GODOT_METHOD_RPC_MODE_SYNC, 'sync')

sys.modules["godot"] = module
