import sys
from types import ModuleType
from pythonscriptcffi import ffi, lib
from functools import partial


class GlobalConstants:

    @classmethod
    def get_global_constants(cls):
        raw_consts = lib.godot_get_global_constants()
        return Dictionary.build_from_gdobj(raw_consts)


class ClassDB:
    _instance = lib.godot_global_get_singleton(b"ClassDB")
    _meth_instance = lib.godot_method_bind_get_method(b"_ClassDB", b"instance")
    _meth_get_class_list = lib.godot_method_bind_get_method(b"_ClassDB", b"get_class_list")
    _meth_get_method_list = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_method_list")
    _meth_get_parent_class = lib.godot_method_bind_get_method(b"_ClassDB", b"get_parent_class")
    _meth_get_property_list = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_property_list")
    _meth_get_property = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_property")
    _meth_set_property = lib.godot_method_bind_get_method(b"_ClassDB", b"class_set_property")
    _meth_get_integer_constant_list = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_integer_constant_list")
    _meth_get_integer_constant = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_integer_constant")

    @classmethod
    def get_class_list(cls):
        ret = godot_pool_string_array_alloc()
        lib.godot_method_bind_ptrcall(cls._meth_get_class_list, cls._instance, ffi.NULL, ret)

        # Convert Godot return into Python civilized stuff
        unordered = []
        for i in range(lib.godot_pool_string_array_size(ret)):
            godot_str = lib.godot_pool_string_array_get(ret, i)
            raw_str = lib.godot_string_unicode_str(ffi.addressof(godot_str))
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
        lib.godot_method_bind_ptrcall(cls._meth_get_method_list, cls._instance, args, ret)
        for i in range(lib.godot_array_size(ret)):
            var = lib.godot_array_get(ret, i)
            gddict = lib.godot_variant_as_dictionary(ffi.addressof(var))
            methdict = Dictionary.build_from_gdobj(gddict)
            methods.append(methdict)
        return methods

    @classmethod
    def build_property_getset(cls, prop):
        propname = prop['name']
        gd_propname = godot_string_from_pyobj(propname)

        def getter(self):
            ret = godot_variant_alloc()
            lib.godot_variant_new_nil(ret)
            args = ffi.new("void*[]", [self._gd_ptr, gd_propname])
            lib.godot_method_bind_ptrcall(cls._meth_get_property, cls._instance, args, ret)
            return variant_to_pyobj(ret)

        def setter(self, value):
            gd_value = pyobj_to_variant(value)
            args = ffi.new("void*[]", [self._gd_ptr, gd_propname, gd_value])
            ret = godot_variant_alloc()
            lib.godot_variant_new_nil(ret)
            lib.godot_method_bind_ptrcall(cls._meth_set_property, cls._instance, args, ret)
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
        lib.godot_method_bind_ptrcall(cls._meth_get_property_list, cls._instance, args, ret)
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
        lib.godot_method_bind_ptrcall(cls._meth_get_integer_constant_list, cls._instance, args, ret)
        for i in range(lib.godot_pool_string_array_size(ret)):
            godot_str = lib.godot_pool_string_array_get(ret, i)
            raw_str = lib.godot_string_unicode_str(ffi.addressof(godot_str))
            consts.append(ffi.string(raw_str))
        return consts

    @classmethod
    def get_integer_constant(cls, classname, constname):
        ret = godot_int_alloc()
        gd_classname = godot_string_from_pyobj(classname)
        gd_constname = godot_string_from_pyobj(constname)
        args = ffi.new("void*[2]", [gd_classname, gd_constname])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(cls._meth_get_integer_constant, cls._instance, args, ret)
        return int(ret[0])

    @classmethod
    def get_parent_class(cls, classname):
        ret = godot_string_alloc()
        lib.godot_string_new(ret)
        gd_classname = godot_string_from_pyobj(classname)
        args = ffi.new("godot_string**", gd_classname)
        lib.godot_method_bind_ptrcall(cls._meth_get_parent_class, cls._instance, ffi.cast("void**", args), ret)
        raw_str = lib.godot_string_unicode_str(ret)
        return ffi.string(raw_str)


class MetaBaseObject(type):
    GD_TYPE = lib.GODOT_VARIANT_TYPE_OBJECT

    def __new__(cls, name, bases, nmspc):
        if ('__init__' in nmspc or '__new__' in nmspc) and name != 'BaseObject':
            raise RuntimeError('Exported to Godot class must not redefine '
                               '`__new__` or `__init__`, use `_ready` instead')
        exported = {}
        signals = {}
        cooked_nmspc = {'__exported': exported, '__signals': signals}
        # Retrieve parent exported fields
        for b in bases:
            exported.update(getattr(b, '__exported', {}))
            signals.update(getattr(b, '__signals', {}))
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
    __slots__ = ('_gd_ptr', '_gd_var')

    def __init__(self, gd_obj_ptr=None):
        """
        Note that gd_obj_ptr should not have ownership of the Godot's Object
        memory given it livespan is not related to its Python wrapper.
        """
        gd_ptr = gd_obj_ptr if gd_obj_ptr else self._gd_constructor()
        object.__setattr__(self, '_gd_ptr', gd_ptr)

    def __getattr__(self, name):
        # If a script is attached to the object, we expose here it methods
        script = self.get_script()
        if not script:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
        if self.has_method(name):
            return lambda *args: self.call(name, *args)
        elif any(x for x in self.get_property_list() if x['name'] == name):
            # TODO: Godot currently lacks a `has_property` method
            return self.get(name)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))

    def __setattr__(self, name, value):
        try:
            object.__setattr__(self, name, value)
        except AttributeError:
            # Could retrieve the item inside the Godot class, try to look into
            # the attached script if it has one
            script = self.get_script()
            if not script:
                raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
            ret = self.set(name, value)

    def __eq__(self, other):
        return hasattr(other, '_gd_ptr') and self._gd_ptr == other._gd_ptr


def _gen_stub(msg):
    return lambda *args: print(msg)


def build_method(classname, meth):
    methname = meth['name']
    # Flag METHOD_FLAG_VIRTUAL only available when compiling godot with DEBUG_METHODS_ENABLED
    methbind = lib.godot_method_bind_get_method(classname.encode(), methname.encode())
    if meth['flags'] & lib.METHOD_FLAG_VIRTUAL or methbind == ffi.NULL:
        return None
        # def bind(self, *args):
        #     raise NotImplementedError("Method %s.%s is virtual" % (classname, methname))
    elif meth['flags'] & lib.METHOD_FLAG_VARARG:
        # Vararg methods are not support by ptrcall, must use slower dynamic mode instead
        rettype = meth['return']['type']
        fixargs_count = len(meth['args'])

        def bind(self, *args):
            # print('[PY->GD] Varargs call %s.%s (%s) on %s with %s' % (classname, methname, meth, self, args))
            vaargs = [convert_arg(meth_arg['type'], meth_arg['name'], arg, to_variant=True)
                        for arg, meth_arg in zip(args, meth['args'])]
            vaargs += [pyobj_to_variant(arg) for arg in args[fixargs_count:]]
            vavaargs = ffi.new("godot_variant*[]", vaargs) if vaargs else ffi.NULL
            # TODO: use `godot_variant_call_error` to raise exceptions
            varret = lib.godot_method_bind_call(methbind, self._gd_ptr, vavaargs, len(args), ffi.NULL)
            ret = variant_to_pyobj(ffi.addressof(varret))
            # print('[PY->GD] returned:', ret)
            return ret
    else:
        # Use ptrcall for calling method
        rettype = meth['return']['type']

        def bind(self, *args):
            if len(args) != len(meth['args']):
                raise TypeError('%s() takes %s positional argument but %s were given' %
                                (methname, len(meth['args']), len(args)))
            # TODO: check args number and type here (ptrcall means segfault on bad args...)
            # print('[PY->GD] Ptrcall %s.%s (%s) on %s with %s' % (classname, methname, meth, self, args))
            raw_args = [convert_arg(meth_arg['type'], meth_arg['name'], arg)
                        for arg, meth_arg in zip(args, meth['args'])]
            gdargs = ffi.new("void*[]", raw_args) if raw_args else ffi.NULL
            ret = new_uninitialized_gdobj(rettype)
            lib.godot_method_bind_ptrcall(methbind, self._gd_ptr, gdargs, ret)
            ret = gdobj_to_pyobj(rettype, ret)
            # print('[PY->GD] returned:', ret)
            return ret

    return bind


def build_property(classname, prop):
    gdprop = prop.copy()
    gdprop.pop('type')
    getter, setter = ClassDB.build_property_getset(prop)
    return property(getter).setter(setter)
    # TODO: Node exported doesn't seems to be shown by the script,
    # uncomment this if it's the case
    # prop_field = ExportedField(type=gd_to_py_type(prop['type']), **gdprop)
    # getter, setter = ClassDB.build_property_getset(prop)
    # prop_field.property = property(getter).setter(setter)
    # return prop_field


def build_class(classname, binding_classname=None):
    binding_classname = binding_classname or classname
    nmspc = {
        '__slots__': (),
        '_gd_name': classname,
        '_gd_constructor': ClassDB.get_class_constructor(classname)
    }
    # Methods
    for meth in ClassDB.get_class_methods(classname):
        # Godot cannot tell which Python function is virtual, so we
        # don't provide them
        methbind = build_method(classname, meth)
        if methbind:
            nmspc[meth['name']] = methbind
        # nmspc[meth['name']] = build_method(classname, meth)
    # Properties
    for prop in ClassDB.get_class_properties(classname):
        propname = prop['name']
        nmspc[propname] = build_property(classname, prop)
    # Constants
    for constname in ClassDB.get_class_consts(classname):
        nmspc[constname] = ClassDB.get_integer_constant(classname, constname)
    parentname = ClassDB.get_parent_class(classname)
    if parentname:
        if parentname in GODOT_SINGLETONS:
            parentname = '_%s' % parentname
        bases = (getattr(godot_bindings_module, parentname), )
    else:
        bases = (BaseObject, )
    return type(binding_classname, bases, nmspc)


def build_global(name, clsname):
    return getattr(godot_bindings_module, clsname)(lib.godot_global_get_singleton(name.encode()))


def get_builtins():
    return {
        'Vector2': Vector2,
        'Rect2': Rect2,
        'Vector3': Vector3,
        'Transform2D': Transform2D,
        'Plane': Plane,
        'Quat': Quat,
        'Rect3': Rect3,
        'Basis': Basis,
        'Transform': Transform,
        'Color': Color,
        'NodePath': NodePath,
        'RID': RID,
        'Dictionary': Dictionary,
        'Array': Array,
        'PoolByteArray': PoolByteArray,
        'PoolIntArray': PoolIntArray,
        'PoolRealArray': PoolRealArray,
        'PoolStringArray': PoolStringArray,
        'PoolVector2Array': PoolVector2Array,
        'PoolVector3Array': PoolVector3Array,
        'PoolColorArray': PoolColorArray,
    }


GODOT_SPECIAL_CLASSES_SINGLETONS = (
    'ResourceLoader', 'ResourceSaver', 'OS', 'Geometry', 'ClassDB', 'Engine'
)
GODOT_REGULAR_CLASSES_SINGLETONS = (
    'AudioServer', 'ProjectSettings', 'Input', 'InputMap', 'Marshalls', 'Performance',
    'Physics2DServer', 'PhysicsServer', 'TranslationServer', 'VisualServer'
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
            clsname = '_%s' % name
            self._available[name] = partial(build_global, name, clsname)
        # Regular classses, we have to rename the classname with a "_" prefix
        # to give the name to the singleton
        for name in GODOT_REGULAR_CLASSES_SINGLETONS:
            new_clsname = '_%s' % name
            if new_clsname not in self._available:
                self._available[new_clsname] = self._available[name]
            self._available[name] = partial(build_global, name, new_clsname)

    def __init__(self, name, doc=None):
        super().__init__(name, doc=doc)
        # Load global constants
        self.__dict__.update(get_builtins())
        self.__dict__.update(GlobalConstants.get_global_constants())
        # Register classe types
        self._available = {name: partial(build_class, name) for name in ClassDB.get_class_list()}
        self._bootstrap_global_singletons()
        setattr(self, '__package__', name)

    @property
    def __all__(self):
        # Cannot compute this statically given builtins will be added
        # by pybind11 after this module's creation
        elems = [k for k in self.__dict__.keys() if not k.startswith('_')]
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
        result.extend(('__all__', '__doc__', '__loader__', '__name__',
                       '__package__', '__spec__', '_available'))
        return result


godot_bindings_module = LazyBindingsModule("godot.bindings")
sys.modules["godot.bindings"] = godot_bindings_module
