from types import ModuleType
from pythonscriptcffi import ffi, lib
from functools import partial

from godot.hazmat.base import BaseObject
from godot.hazmat.allocator import (
    godot_pool_string_array_alloc,
    godot_variant_alloc,
    godot_array_alloc,
    godot_bool_alloc,
    godot_string_alloc,
    godot_int_alloc,
)
from godot.hazmat.tools import (
    variant_to_pyobj,
    pyobj_to_variant,
    new_uninitialized_gdobj,
    gdobj_to_pyobj,
    convert_arg,
    godot_string_from_pyobj,
)
from godot.vector2 import Vector2
from godot.rect2 import Rect2
from godot.vector3 import Vector3
from godot.transform2d import Transform2D
from godot.plane import Plane
from godot.quat import Quat
from godot.aabb import AABB
from godot.basis import Basis
from godot.transform import Transform
from godot.color import Color
from godot.node_path import NodePath
from godot.rid import RID
from godot.dictionary import Dictionary
from godot.array import Array
from godot.pool_arrays import (
    PoolByteArray,
    PoolIntArray,
    PoolRealArray,
    PoolStringArray,
    PoolVector2Array,
    PoolVector3Array,
    PoolColorArray,
)


class GlobalConstants:

    @classmethod
    def get_global_constants(cls):
        raw_consts = lib.godot_get_global_constants()
        return Dictionary.build_from_gdobj(raw_consts)


class ClassDB:
    _instance = lib.godot_global_get_singleton(b"ClassDB")
    _meth_instance = lib.godot_method_bind_get_method(b"_ClassDB", b"instance")
    _meth_get_class_list = lib.godot_method_bind_get_method(
        b"_ClassDB", b"get_class_list"
    )
    _meth_get_method_list = lib.godot_method_bind_get_method(
        b"_ClassDB", b"class_get_method_list"
    )
    _meth_get_parent_class = lib.godot_method_bind_get_method(
        b"_ClassDB", b"get_parent_class"
    )
    _meth_get_property_list = lib.godot_method_bind_get_method(
        b"_ClassDB", b"class_get_property_list"
    )
    _meth_get_property = lib.godot_method_bind_get_method(
        b"_ClassDB", b"class_get_property"
    )
    _meth_set_property = lib.godot_method_bind_get_method(
        b"_ClassDB", b"class_set_property"
    )
    _meth_get_integer_constant_list = lib.godot_method_bind_get_method(
        b"_ClassDB", b"class_get_integer_constant_list"
    )
    _meth_get_integer_constant = lib.godot_method_bind_get_method(
        b"_ClassDB", b"class_get_integer_constant"
    )

    @classmethod
    def get_class_list(cls):
        ret = godot_pool_string_array_alloc()
        lib.godot_method_bind_ptrcall(
            cls._meth_get_class_list, cls._instance, ffi.NULL, ret
        )

        # Convert Godot return into Python civilized stuff
        unordered = []
        for i in range(lib.godot_pool_string_array_size(ret)):
            godot_str = lib.godot_pool_string_array_get(ret, i)
            raw_str = lib.godot_string_wide_str(ffi.addressof(godot_str))
            unordered.append(ffi.string(raw_str))

        # Order class to have a parent defined before their children
        classes = []
        while len(unordered) != len(classes):
            for classname in unordered:
                parentname = cls.get_parent_class(classname)
                if not parentname or parentname in classes:
                    if classname not in classes:
                        classes.append(classname)

        return classes

    @classmethod
    def get_class_constructor(cls, classname):

        def constructor(self):
            gd_classname = godot_string_from_pyobj(classname)
            # TODO: alloc this on the stack (using _malloca ?)
            args = ffi.new("void*[]", [gd_classname])
            ret = godot_variant_alloc()
            lib.godot_method_bind_ptrcall(cls._meth_instance, cls._instance, args, ret)
            objret = lib.godot_variant_as_object(ret)
            # Quick'n dirty fix to prevent Ressource objects from beeing automatically
            # freed when the variant is destroyed given it holds the only ref on it
            self._gd_var = ret
            return objret

        return constructor

    @classmethod
    def get_class_methods(cls, classname):
        methods = []
        ret = godot_array_alloc()
        lib.godot_array_new(ret)
        gd_classname = godot_string_from_pyobj(classname)
        gd_true = godot_bool_alloc(True)
        args = ffi.new("void*[2]", [gd_classname, gd_true])
        # 2nd arg should be false, which is what we get by not initializing it
        lib.godot_method_bind_ptrcall(
            cls._meth_get_method_list, cls._instance, args, ret
        )
        for i in range(lib.godot_array_size(ret)):
            var = lib.godot_array_get(ret, i)
            gddict = lib.godot_variant_as_dictionary(ffi.addressof(var))
            methdict = Dictionary.build_from_gdobj(gddict)
            methods.append(methdict)
        return methods

    @classmethod
    def build_property_getset(cls, prop):
        propname = prop["name"]
        gd_propname = godot_string_from_pyobj(propname)

        def getter(self):
            ret = godot_variant_alloc()
            lib.godot_variant_new_nil(ret)
            args = ffi.new("void*[]", [self._gd_ptr, gd_propname])
            lib.godot_method_bind_ptrcall(
                cls._meth_get_property, cls._instance, args, ret
            )
            return variant_to_pyobj(ret)

        def setter(self, value):
            gd_value = pyobj_to_variant(value)
            args = ffi.new("void*[]", [self._gd_ptr, gd_propname, gd_value])
            ret = godot_variant_alloc()
            lib.godot_variant_new_nil(ret)
            lib.godot_method_bind_ptrcall(
                cls._meth_set_property, cls._instance, args, ret
            )
            return variant_to_pyobj(ret)

        return getter, setter

    @classmethod
    def get_class_properties(cls, classname):
        properties = []
        ret = godot_array_alloc()
        lib.godot_array_new(ret)
        gd_classname = godot_string_from_pyobj(classname)
        gd_true = godot_bool_alloc(True)
        args = ffi.new("void*[2]", [gd_classname, gd_true])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(
            cls._meth_get_property_list, cls._instance, args, ret
        )
        for i in range(lib.godot_array_size(ret)):
            var = lib.godot_array_get(ret, i)
            gddict = lib.godot_variant_as_dictionary(ffi.addressof(var))
            propdict = Dictionary.build_from_gdobj(gddict)
            properties.append(propdict)
        return properties

    @classmethod
    def get_class_consts(cls, classname):
        consts = []
        ret = godot_pool_string_array_alloc()
        lib.godot_pool_string_array_new(ret)
        gd_classname = godot_string_from_pyobj(classname)
        gd_true = godot_bool_alloc(True)
        args = ffi.new("void*[2]", [gd_classname, gd_true])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(
            cls._meth_get_integer_constant_list, cls._instance, args, ret
        )
        for i in range(lib.godot_pool_string_array_size(ret)):
            godot_str = lib.godot_pool_string_array_get(ret, i)
            raw_str = lib.godot_string_wide_str(ffi.addressof(godot_str))
            consts.append(ffi.string(raw_str))
        return consts

    @classmethod
    def get_integer_constant(cls, classname, constname):
        ret = godot_int_alloc()
        gd_classname = godot_string_from_pyobj(classname)
        gd_constname = godot_string_from_pyobj(constname)
        args = ffi.new("void*[2]", [gd_classname, gd_constname])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(
            cls._meth_get_integer_constant, cls._instance, args, ret
        )
        return int(ret[0])

    @classmethod
    def get_parent_class(cls, classname):
        ret = godot_string_alloc()
        lib.godot_string_new(ret)
        gd_classname = godot_string_from_pyobj(classname)
        args = ffi.new("godot_string**", gd_classname)
        lib.godot_method_bind_ptrcall(
            cls._meth_get_parent_class, cls._instance, ffi.cast("void**", args), ret
        )
        raw_str = lib.godot_string_wide_str(ret)
        return ffi.string(raw_str)


def _gen_stub(msg):
    return lambda *args: print(msg)


def build_method(classname, meth):
    methname = meth["name"]
    # Flag METHOD_FLAG_VIRTUAL only available when compiling godot with DEBUG_METHODS_ENABLED
    methbind = lib.godot_method_bind_get_method(classname.encode(), methname.encode())
    if meth["flags"] & lib.METHOD_FLAG_VIRTUAL or methbind == ffi.NULL:
        return None

    # def bind(self, *args):
    #     raise NotImplementedError("Method %s.%s is virtual" % (classname, methname))
    elif meth["flags"] & lib.METHOD_FLAG_VARARG:
        # Vararg methods are not supported by ptrcall, must use slower dynamic mode instead
        rettype = meth["return"]["type"]
        fixargs_count = len(meth["args"])

        def bind(self, *args):
            # print('[PY->GD] Varargs call %s.%s (%s) on %s with %s' % (classname, methname, meth, self, args))
            vaargs = [
                convert_arg(meth_arg["type"], meth_arg["name"], arg, to_variant=True)
                for arg, meth_arg in zip(args, meth["args"])
            ]
            vaargs += [pyobj_to_variant(arg) for arg in args[fixargs_count:]]
            vavaargs = ffi.new("godot_variant*[]", vaargs) if vaargs else ffi.NULL
            # TODO: use `godot_variant_call_error` to raise exceptions
            varret = lib.godot_method_bind_call(
                methbind, self._gd_ptr, vavaargs, len(args), ffi.NULL
            )
            ret = variant_to_pyobj(ffi.addressof(varret))
            lib.godot_variant_destroy(ffi.addressof(varret))
            # print('[PY->GD] returned:', ret)
            return ret

    else:
        # Use ptrcall for calling method
        rettype = meth["return"]["type"]

        def bind(self, *args):
            # TODO: allow **kwargs
            # check number of args
            n_args, nm_args, nmd_args = len(args), len(meth["args"]), len(
                meth["default_args"]
            )
            nr_args = nm_args - nmd_args  # number of required arguments
            if n_args < nr_args:  # not enough args, raise error
                if nr_args - n_args == 1:
                    raise TypeError(
                        "%s() missing 1 required positional argument: '%s'"
                        % (methname, meth["args"][nr_args - 1]["name"])
                    )

                else:
                    raise TypeError(
                        "%s() missing %i required positional arguments: "
                        % (methname, nr_args - n_args)
                        + ", ".join(
                            "'%s'" % (arg["name"])
                            for arg in meth["args"][n_args:nr_args - 1]
                        )
                        + " and '%s'"
                        % (meth["args"][nr_args - 1]["name"])
                    )

            if n_args > nm_args:  # too many args, raise error
                if nmd_args == 0:
                    raise TypeError(
                        "%s() takes %i positional argument%s but %i were given"
                        % (methname, nm_args, "s" if nm_args > 1 else "", n_args)
                    )

                else:
                    raise TypeError(
                        "%s() takes from %i to %i positional arguments but %i were given"
                        % (methname, nr_args, nm_args, n_args)
                    )

            # complete missing optional args with default values
            diff = len(args) - len(meth["args"])
            args = args + tuple(meth["default_args"][diff:])

            # TODO: check args type here (ptrcall means segfault on bad args...)
            # print('[PY->GD] Ptrcall %s.%s (%s) on %s with %s' % (classname, methname, meth, self, args))
            raw_args = [
                convert_arg(meth_arg["type"], meth_arg["name"], arg)
                for arg, meth_arg in zip(args, meth["args"])
            ]
            gdargs = ffi.new("void*[]", raw_args) if raw_args else ffi.NULL
            ret = new_uninitialized_gdobj(rettype)
            lib.godot_method_bind_ptrcall(methbind, self._gd_ptr, gdargs, ret)
            ret = gdobj_to_pyobj(rettype, ret)
            # print('[PY->GD] returned:', ret)
            return ret

    return bind


def build_property(classname, prop):
    gdprop = prop.copy()
    gdprop.pop("type")
    getter, setter = ClassDB.build_property_getset(prop)
    return property(getter).setter(setter)


# TODO: Node exported doesn't seems to be shown by the script,
# uncomment this if it's the case
# prop_field = ExportedField(type=gd_to_py_type(prop['type']), **gdprop)
# getter, setter = ClassDB.build_property_getset(prop)
# prop_field.property = property(getter).setter(setter)
# return prop_field


def build_class(godot_bindings_module, classname, binding_classname=None):
    binding_classname = binding_classname or classname
    nmspc = {
        "__is_godot_native_class": True,
        "__slots__": (),
        "_gd_name": classname,
        "_gd_constructor": ClassDB.get_class_constructor(classname),
    }
    # Methods
    for meth in ClassDB.get_class_methods(classname):
        # Godot cannot tell which Python function is virtual, so we
        # don't provide them
        methbind = build_method(classname, meth)
        if methbind:
            nmspc[meth["name"]] = methbind
    # nmspc[meth['name']] = build_method(classname, meth)
    # Properties
    for prop in ClassDB.get_class_properties(classname):
        propname = prop["name"]
        nmspc[propname] = build_property(classname, prop)
    # Constants
    for constname in ClassDB.get_class_consts(classname):
        nmspc[constname] = ClassDB.get_integer_constant(classname, constname)
    parentname = ClassDB.get_parent_class(classname)
    if parentname:
        if parentname in GODOT_SINGLETONS:
            parentname = "_%s" % parentname
        bases = (getattr(godot_bindings_module, parentname),)
    else:
        bases = (BaseObject,)
    return type(binding_classname, bases, nmspc)


def build_global(godot_bindings_module, name, clsname):
    return getattr(godot_bindings_module, clsname)(
        lib.godot_global_get_singleton(name.encode())
    )


def get_builtins():
    return {
        "Vector2": Vector2,
        "Rect2": Rect2,
        "Vector3": Vector3,
        "Transform2D": Transform2D,
        "Plane": Plane,
        "Quat": Quat,
        "AABB": AABB,
        "Basis": Basis,
        "Transform": Transform,
        "Color": Color,
        "NodePath": NodePath,
        "RID": RID,
        "Dictionary": Dictionary,
        "Array": Array,
        "PoolByteArray": PoolByteArray,
        "PoolIntArray": PoolIntArray,
        "PoolRealArray": PoolRealArray,
        "PoolStringArray": PoolStringArray,
        "PoolVector2Array": PoolVector2Array,
        "PoolVector3Array": PoolVector3Array,
        "PoolColorArray": PoolColorArray,
    }


GODOT_SPECIAL_CLASSES_SINGLETONS = (
    "ResourceLoader", "ResourceSaver", "OS", "Geometry", "ClassDB", "Engine"
)
GODOT_REGULAR_CLASSES_SINGLETONS = (
    "AudioServer",
    "ProjectSettings",
    "Input",
    "InputMap",
    "Marshalls",
    "Performance",
    "Physics2DServer",
    "PhysicsServer",
    "TranslationServer",
    "VisualServer",
)
GODOT_SINGLETONS = GODOT_SPECIAL_CLASSES_SINGLETONS + GODOT_REGULAR_CLASSES_SINGLETONS


# Werkzeug style lazy module


class LazyBindingsModule(ModuleType):

    """Automatically import objects from the modules."""

    def _bootstrap_global_singletons(self):
        # TODO: ProjectSettings doesn't provide a `list_singletons` to load
        # this dynamically :'-(
        # Special classes generated in `godot/core/core_bind.h`, classname
        # has a "_" prefix
        for name in GODOT_SPECIAL_CLASSES_SINGLETONS:
            clsname = "_%s" % name
            self._available[name] = partial(build_global, self, name, clsname)
        # Regular classses, we have to rename the classname with a "_" prefix
        # to give the name to the singleton
        for name in GODOT_REGULAR_CLASSES_SINGLETONS:
            new_clsname = "_%s" % name
            if new_clsname not in self._available:
                self._available[new_clsname] = self._available[name]
            self._available[name] = partial(build_global, self, name, new_clsname)

    def _ensure_godot_instrospection_availability(self):
        # Just pick one method and check if it contains introspection info or not
        if ClassDB.get_class_methods("_OS")[0]["flags"] is None:
            raise RuntimeError(
                "Godot introspection is required for Python, use release-debug or "
                "tools version of Godot (i.e. `godot.x11.tools.64`)"
            )

    def __init__(self, name, doc=None):
        super().__init__(name, doc=doc)
        # First and firemost: make sure Godot introspection is available
        self._ensure_godot_instrospection_availability()
        # Load global constants
        self.__dict__.update(get_builtins())
        self.__dict__.update(GlobalConstants.get_global_constants())
        # Register classe types
        self._available = {
            name: partial(build_class, self, name) for name in ClassDB.get_class_list()
        }
        self._bootstrap_global_singletons()
        setattr(self, "__package__", name)

    @property
    def __all__(self):
        # Cannot compute this statically given builtins will be added
        # by pybind11 after this module's creation
        elems = [k for k in self.__dict__.keys() if not k.startswith("_")]
        elems.extend(self._available.keys())
        return list(set(elems))

    def __getattr__(self, name):
        loader = self._available.get(name)
        if not loader:
            return ModuleType.__getattribute__(self, name)

        self.__dict__[name] = loader()
        return self.__dict__[name]

    def __dir__(self):
        """Just show what we want to show."""
        result = list(self.__all__)
        result.extend(
            (
                "__all__",
                "__doc__",
                "__loader__",
                "__name__",
                "__package__",
                "__spec__",
                "_available",
            )
        )
        return result
