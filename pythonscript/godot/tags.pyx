import builtins
import enum

from godot._hazmat.gdnative_api_struct cimport (
    godot_method_rpc_mode,
    godot_property_usage_flags,
    godot_method_rpc_mode,
    godot_property_hint,
    godot_variant,
)
from godot._hazmat.gdapi cimport pythonscript_gdapi10 as gdapi10
from godot._hazmat.conversion cimport (
    is_pytype_compatible_with_godot_variant,
    pyobj_to_godot_variant,
    godot_variant_to_pyobj,
)
from godot._hazmat.internal cimport get_exposed_class, set_exposed_class
from godot.builtins cimport Array, Dictionary, GDString
from godot.bindings cimport Object, Resource


# Make Godot enums accesible from Python at runtime


class MethodRPCMode(enum.IntEnum):
    DISABLED = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_DISABLED
    REMOTE = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_REMOTE
    MASTER = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_MASTER
    PUPPET = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_PUPPET
    SLAVE = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_SLAVE
    REMOTESYNC = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_REMOTESYNC
    SYNC = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_SYNC
    MASTERSYNC = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_MASTERSYNC
    PUPPETSYNC = godot_method_rpc_mode.GODOT_METHOD_RPC_MODE_PUPPETSYNC


class PropertyHint(enum.IntEnum):
    NONE = godot_property_hint.GODOT_PROPERTY_HINT_NONE
    RANGE = godot_property_hint.GODOT_PROPERTY_HINT_RANGE
    EXP_RANGE = godot_property_hint.GODOT_PROPERTY_HINT_EXP_RANGE
    ENUM = godot_property_hint.GODOT_PROPERTY_HINT_ENUM
    EXP_EASING = godot_property_hint.GODOT_PROPERTY_HINT_EXP_EASING
    LENGTH = godot_property_hint.GODOT_PROPERTY_HINT_LENGTH
    SPRITE_FRAME = godot_property_hint.GODOT_PROPERTY_HINT_SPRITE_FRAME
    KEY_ACCEL = godot_property_hint.GODOT_PROPERTY_HINT_KEY_ACCEL
    FLAGS = godot_property_hint.GODOT_PROPERTY_HINT_FLAGS
    LAYERS_2D_RENDER = godot_property_hint.GODOT_PROPERTY_HINT_LAYERS_2D_RENDER
    LAYERS_2D_PHYSICS = godot_property_hint.GODOT_PROPERTY_HINT_LAYERS_2D_PHYSICS
    LAYERS_3D_RENDER = godot_property_hint.GODOT_PROPERTY_HINT_LAYERS_3D_RENDER
    LAYERS_3D_PHYSICS = godot_property_hint.GODOT_PROPERTY_HINT_LAYERS_3D_PHYSICS
    FILE = godot_property_hint.GODOT_PROPERTY_HINT_FILE
    DIR = godot_property_hint.GODOT_PROPERTY_HINT_DIR
    GLOBAL_FILE = godot_property_hint.GODOT_PROPERTY_HINT_GLOBAL_FILE
    GLOBAL_DIR = godot_property_hint.GODOT_PROPERTY_HINT_GLOBAL_DIR
    RESOURCE_TYPE = godot_property_hint.GODOT_PROPERTY_HINT_RESOURCE_TYPE
    MULTILINE_TEXT = godot_property_hint.GODOT_PROPERTY_HINT_MULTILINE_TEXT
    PLACEHOLDER_TEXT = godot_property_hint.GODOT_PROPERTY_HINT_PLACEHOLDER_TEXT
    COLOR_NO_ALPHA = godot_property_hint.GODOT_PROPERTY_HINT_COLOR_NO_ALPHA
    IMAGE_COMPRESS_LOSSY = godot_property_hint.GODOT_PROPERTY_HINT_IMAGE_COMPRESS_LOSSY
    IMAGE_COMPRESS_LOSSLESS = godot_property_hint.GODOT_PROPERTY_HINT_IMAGE_COMPRESS_LOSSLESS
    OBJECT_ID = godot_property_hint.GODOT_PROPERTY_HINT_OBJECT_ID
    TYPE_STRING = godot_property_hint.GODOT_PROPERTY_HINT_TYPE_STRING
    NODE_PATH_TO_EDITED_NODE = godot_property_hint.GODOT_PROPERTY_HINT_NODE_PATH_TO_EDITED_NODE
    METHOD_OF_VARIANT_TYPE = godot_property_hint.GODOT_PROPERTY_HINT_METHOD_OF_VARIANT_TYPE
    METHOD_OF_BASE_TYPE = godot_property_hint.GODOT_PROPERTY_HINT_METHOD_OF_BASE_TYPE
    METHOD_OF_INSTANCE = godot_property_hint.GODOT_PROPERTY_HINT_METHOD_OF_INSTANCE
    METHOD_OF_SCRIPT = godot_property_hint.GODOT_PROPERTY_HINT_METHOD_OF_SCRIPT
    PROPERTY_OF_VARIANT_TYPE = godot_property_hint.GODOT_PROPERTY_HINT_PROPERTY_OF_VARIANT_TYPE
    PROPERTY_OF_BASE_TYPE = godot_property_hint.GODOT_PROPERTY_HINT_PROPERTY_OF_BASE_TYPE
    PROPERTY_OF_INSTANCE = godot_property_hint.GODOT_PROPERTY_HINT_PROPERTY_OF_INSTANCE
    PROPERTY_OF_SCRIPT = godot_property_hint.GODOT_PROPERTY_HINT_PROPERTY_OF_SCRIPT
    MAX = godot_property_hint.GODOT_PROPERTY_HINT_MAX


class PropertyUsageFlag(enum.IntFlag):
    STORAGE = godot_property_usage_flags.GODOT_PROPERTY_USAGE_STORAGE
    EDITOR = godot_property_usage_flags.GODOT_PROPERTY_USAGE_EDITOR
    NETWORK = godot_property_usage_flags.GODOT_PROPERTY_USAGE_NETWORK
    EDITOR_HELPER = godot_property_usage_flags.GODOT_PROPERTY_USAGE_EDITOR_HELPER
    CHECKABLE = godot_property_usage_flags.GODOT_PROPERTY_USAGE_CHECKABLE
    CHECKED = godot_property_usage_flags.GODOT_PROPERTY_USAGE_CHECKED
    INTERNATIONALIZED = godot_property_usage_flags.GODOT_PROPERTY_USAGE_INTERNATIONALIZED
    GROUP = godot_property_usage_flags.GODOT_PROPERTY_USAGE_GROUP
    CATEGORY = godot_property_usage_flags.GODOT_PROPERTY_USAGE_CATEGORY
    STORE_IF_NONZERO = godot_property_usage_flags.GODOT_PROPERTY_USAGE_STORE_IF_NONZERO
    STORE_IF_NONONE = godot_property_usage_flags.GODOT_PROPERTY_USAGE_STORE_IF_NONONE
    NO_INSTANCE_STATE = godot_property_usage_flags.GODOT_PROPERTY_USAGE_NO_INSTANCE_STATE
    RESTART_IF_CHANGED = godot_property_usage_flags.GODOT_PROPERTY_USAGE_RESTART_IF_CHANGED
    SCRIPT_VARIABLE = godot_property_usage_flags.GODOT_PROPERTY_USAGE_SCRIPT_VARIABLE
    STORE_IF_NULL = godot_property_usage_flags.GODOT_PROPERTY_USAGE_STORE_IF_NULL
    ANIMATE_AS_TRIGGER = godot_property_usage_flags.GODOT_PROPERTY_USAGE_ANIMATE_AS_TRIGGER
    UPDATE_ALL_IF_MODIFIED = godot_property_usage_flags.GODOT_PROPERTY_USAGE_UPDATE_ALL_IF_MODIFIED
    DEFAULT = godot_property_usage_flags.GODOT_PROPERTY_USAGE_DEFAULT
    DEFAULT_INTL = godot_property_usage_flags.GODOT_PROPERTY_USAGE_DEFAULT_INTL
    NOEDITOR = godot_property_usage_flags.GODOT_PROPERTY_USAGE_NOEDITOR


# Expose RPC modes can be used both as a decorator and as a value to pass
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
        return f"<{type(self).__name__}({self.modname!r})>"


rpcdisabled = RPCMode(MethodRPCMode.DISABLED, "disabled")
rpcremote = RPCMode(MethodRPCMode.REMOTE, "remote")
rpcmaster = RPCMode(MethodRPCMode.MASTER, "master")
rpcpuppet = RPCMode(MethodRPCMode.PUPPET, "puppet")
rpcslave = RPCMode(MethodRPCMode.SLAVE, "slave")
rpcremotesync = RPCMode(MethodRPCMode.REMOTESYNC, "remotesync")
rpcsync = RPCMode(MethodRPCMode.SYNC, "sync")
rpcmastersync = RPCMode(MethodRPCMode.MASTERSYNC, "mastersync")
rpcpuppetsync = RPCMode(MethodRPCMode.PUPPETSYNC, "puppetsync")


class SignalField:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{type(self).__name__}({self.name!r})>"


def signal(name: str=None):
    # If signal name is None, we will determine the name
    # later by using the class's attribute containing it
    if name is not None and not isinstance(name, str):
        raise ValueError("`name` must be a str")
    return SignalField(name)


# TODO: this can be greatly improved to make it more pythonic


class ExportedField:
    def __init__(
        self,
        type,
        default,
        name,
        hint,
        usage,
        hint_string,
        rpc,
    ):
        self.property = None

        type = GDString if type == str else type
        type = Array if type == list else type
        type = Dictionary if type == dict else type

        if not is_pytype_compatible_with_godot_variant(type):
            raise ValueError(f"{type!r} type value not compatible with Godot")

        cdef godot_variant gd_default
        if default is not None:
            # Convert `default` to a Godot-compatible value (e.g. str -> GDString)
            if not pyobj_to_godot_variant(default, &gd_default):
                gdapi10.godot_variant_destroy(&gd_default)
                raise ValueError(f"{default!r} default value not compatible with Godot")
            default = godot_variant_to_pyobj(&gd_default)
            gdapi10.godot_variant_destroy(&gd_default)

            if not isinstance(default, type):
                raise ValueError(f"{default!r} default value not compatible with {type!r} type")

        if issubclass(type, Resource):
            if hint not in (PropertyHint.NONE, PropertyHint.RESOURCE_TYPE) or hint_string not in ("", type.__name__):
                raise ValueError(f"Resource type doesn't support hint/hint_string fields")
            hint = PropertyHint.RESOURCE_TYPE
            hint_string = type.__name__
            type = Object

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
        return f"<{type(self).__name__}(type={self.type!r}, default={self.default!r})>"

    def _copy(self):
        return ExportedField(
            type=self.type,
            default=self.default,
            name=self.name,
            hint=self.hint,
            usage=self.usage,
            hint_string=self.hint_string,
            rpc=self.rpc,
        )

    def __call__(self, decorated):
        if self.default is not None:
            raise ValueError("export should not define a default attribute when used as a decorator")

        # This object is used as a decorator
        if not callable(decorated) and not isinstance(decorated, builtins.property):
            raise ValueError("@export should decorate function or property.")

        updated = self._copy()

        # It's possible decorated has already been passed through a rpc decorator
        rpc = getattr(decorated, "__rpc", None)
        if rpc:
            updated.rpc = rpc
        updated.property = decorated
        return updated

    def setter(self, setfunc):
        if not self.property:
            raise ValueError(
                "Cannot use setter attribute before defining the getter !"
            )

        updated = self._copy()
        updated.property = self.property.setter(setfunc)
        return updated


def export(
        type,
        default=None,
        hint: PropertyHint=PropertyHint.NONE,
        usage: PropertyUsageFlag=PropertyUsageFlag.DEFAULT,
        hint_string: str="",
        rpc: MethodRPCMode=MethodRPCMode.DISABLED
    ):
    """
    Decorator used to mark a class attribute as beeing exported to Godot
    (hence making it readable/writable from Godot)

    usage::
        @exposed
        class CustomObject(godot.bindings.Object):
            a = export(str)  # Expose attribute
            b = export(int, default=42)

            @export(int)  # Expose property
            @property
            def c(self):
                return 42

            @export(str)  # Expose method
            def d(self):
                return "foo"
    """
    return ExportedField(
        type=type,
        default=default,
        name=None,
        hint=hint,
        usage=usage,
        hint_string=hint_string,
        rpc=rpc,
    )


def exposed(cls=None, tool=False):
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
    def wrapper(cls):
        if not issubclass(cls, Object):
            raise ValueError(
                f"{cls!r} must inherit from a Godot (e.g. `godot.bindings.Node`) "
                "class to be marked as @exposed"
            )

        existing_cls_for_module = get_exposed_class(cls.__module__)
        if existing_cls_for_module:
            raise ValueError(
                "Only a single class can be marked as @exposed per module"
                f" (already got {existing_cls_for_module!r})"
            )

        cls.__tool = tool
        cls.__exposed_python_class = True
        cls.__exported = {}

        # Retrieve parent exported stuff
        for b in cls.__bases__:
            cls.__exported.update(getattr(b, "__exported", {}))

        init_func_code = "def __init__(self):\n    pass\n"

        # Collect exported stuff: attributes (marked with @exported), properties, signals, and methods
        for k, v in cls.__dict__.items():
            if isinstance(v, ExportedField):
                cls.__exported[k] = v
                v.name = k  # hard to bind this earlier...
                if v.property:
                    # If export has been used to decorate a property, expose it
                    # in the generated class
                    setattr(cls, k, v.property)
                else:
                    # Otherwise, the value must be initialized as part of __init__
                    if v.default is None or isinstance(v.default, (int, float, bool)):
                        init_func_code += f"    self.{k} = {repr(v.default)}\n"
                    else:
                        init_func_code += f"    self.{k} = self.__exported['{k}'].default\n"
            elif isinstance(v, SignalField):
                v.name = v.name or k
                cls.__exported[v.name] = v
                setattr(cls, k, v)
            elif callable(v):
                cls.__exported[k] = v

        # Overwrite parent __init__ to avoid creating a Godot object given
        # exported script are always initialized with an existing Godot object
        # On top of that, we must initialize the attributes defined in the class
        # and it parents
        g = {}
        exec(init_func_code, g)
        cls.__init__ = g["__init__"]
        # Also overwrite parent new otherwise we would return an instance
        # of a Godot class without our script attached to it...
        @classmethod
        def new(cls):
            raise NotImplementedError("Instantiating Python script from Python is not implemented yet :'(")
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

        set_exposed_class(cls)
        return cls

    if cls is not None:
        return wrapper(cls)

    else:
        return wrapper
