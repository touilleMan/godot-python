import sys
from types import ModuleType
from pythonscriptcffi import ffi, lib
from functools import partial


class GlobalConstants:
    _instance = lib.godot_global_get_singleton(b"GlobalConstants")
    _meth_get_global_constant_count = lib.godot_method_bind_get_method(b"_GlobalConstants", b"get_global_constant_count")
    _meth_get_global_constant_name = lib.godot_method_bind_get_method(b"_GlobalConstants", b"get_global_constant_name")
    _meth_get_global_constant_value = lib.godot_method_bind_get_method(b"_GlobalConstants", b"get_global_constant_value")


    @classmethod
    def get_global_constansts(cls):
        constants = {}
        for i in range(lib.godot_get_global_constant_count()):
            key = ffi.string(lib.godot_get_global_constant_name(i)).decode()
            value = lib.godot_get_global_constant_value(i)
            constants[key] = value
        return constants

    # ClassDB doesn't provide access for GlobalContansts yet
    # @classmethod
    # def get_global_constansts(cls):
    #     constants = {}
    #     ret = ffi.new("godot_int*")
    #     import pdb; pdb.set_trace()
    #     lib.godot_method_bind_ptrcall(cls._meth_get_global_constant_count, cls._instance, ffi.NULL, ret)
    #     for i in range(int(ret)):
    #         arg = ffi.new("godot_int*", i)
    #         args = ffi.new("void*[1]", [arg])
    #         # Retrieve key
    #         ret = ffi.new("godot_string*")
    #         lib.godot_method_bind_ptrcall(cls._meth_get_global_constant_name, cls._instance, args, ret)
    #         key = ffi.string(ret)
    #         # Retrieve value
    #         ret = ffi.new("godot_int*")
    #         lib.godot_method_bind_ptrcall(cls._meth_get_global_constant_value, cls._instance, args, ret)
    #         value = int(ret)
    #         constants[key] = value
    #     return constants


class ClassDB:
    _instance = lib.godot_global_get_singleton(b"ClassDB")
    _meth_instance = lib.godot_method_bind_get_method(b"_ClassDB", b"instance")
    _meth_get_class_list = lib.godot_method_bind_get_method(b"_ClassDB", b"get_class_list")
    _meth_get_method_list = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_method_list")
    _meth_get_parent_class = lib.godot_method_bind_get_method(b"_ClassDB", b"get_parent_class")
    _meth_get_property_list = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_property_list")
    _meth_get_integer_constant_list = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_integer_constant_list")
    _meth_get_integer_constant = lib.godot_method_bind_get_method(b"_ClassDB", b"class_get_integer_constant")

    @classmethod
    def get_class_list(cls):
        ret = ffi.new("godot_pool_string_array*")
        lib.godot_pool_string_array_new(ret)
        lib.godot_method_bind_ptrcall(cls._meth_get_class_list, cls._instance, ffi.NULL, ret)

        # Convert Godot return into Python civilized stuff
        unordered = []
        for i in range(lib.godot_pool_string_array_size(ret)):
            godot_str = lib.godot_pool_string_array_get(ret, i)
            c_str = lib.godot_string_c_str(ffi.new('godot_string*', godot_str))
            unordered.append(ffi.string(c_str))

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

        def constructor():
            gd_classname = ffi.new("godot_string*")
            lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
            args = ffi.new("void*[]", [gd_classname])
            ret = ffi.new("godot_object*")
            lib.godot_method_bind_ptrcall(cls._meth_instance, cls._instance, args, ret)
            return ret

        return constructor

    @classmethod
    def get_class_methods(cls, classname):
        methods = []
        ret = ffi.new("godot_array*")
        gd_classname = ffi.new("godot_string*")
        lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
        gd_true = ffi.new("godot_bool*", 1)
        args = ffi.new("void*[2]", [gd_classname, gd_true])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(cls._meth_get_method_list, cls._instance, args, ret)
        for i in range(lib.godot_array_size(ret)):
            var = lib.godot_array_get(ret, i)
            gddict = lib.godot_variant_as_dictionary(var)
            methdict = godot_dictionary_to_pyobj(ffi.addressof(gddict))
            methods.append(methdict)
        return methods

    @classmethod
    def get_class_properties(cls, classname):
        properties = []
        ret = ffi.new("godot_array*")
        gd_classname = ffi.new("godot_string*")
        lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
        gd_true = ffi.new("godot_bool*", 1)
        args = ffi.new("void*[2]", [gd_classname, gd_true])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(cls._meth_get_property_list, cls._instance, args, ret)
        for i in range(lib.godot_array_size(ret)):
            var = lib.godot_array_get(ret, i)
            gddict = lib.godot_variant_as_dictionary(var)
            propdict = godot_dictionary_to_pyobj(ffi.addressof(gddict))
            properties.append(propdict)
        return properties

    @classmethod
    def get_class_consts(cls, classname):
        consts = []
        ret = ffi.new("godot_pool_string_array*")
        lib.godot_pool_string_array_new(ret)
        gd_classname = ffi.new("godot_string*")
        gd_true = ffi.new("godot_bool*", 1)
        lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
        args = ffi.new("void*[2]", [gd_classname, gd_true])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(cls._meth_get_integer_constant_list, cls._instance, args, ret)
        for i in range(lib.godot_pool_string_array_size(ret)):
            godot_str = lib.godot_pool_string_array_get(ret, i)
            c_str = lib.godot_string_c_str(ffi.new('godot_string*', godot_str))
            consts.append(ffi.string(c_str))
        return consts

    @classmethod
    def get_integer_constant(cls, classname, constname):
        ret = ffi.new("godot_int*")
        gd_classname = ffi.new("godot_string*")
        lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
        gd_constname = ffi.new("godot_string*")
        lib.godot_string_new_data(gd_constname, constname.encode(), len(constname.encode()))
        args = ffi.new("void*[2]", [gd_classname, gd_constname])
        # 2nd arg should be false, which what we get by not initializing it
        lib.godot_method_bind_ptrcall(cls._meth_get_integer_constant, cls._instance, args, ret)
        return int(ret[0])

    @classmethod
    def get_parent_class(cls, classname):
        ret = ffi.new("godot_string*")
        gd_classname = ffi.new("godot_string*")
        lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
        args = ffi.new("godot_string**", gd_classname)
        lib.godot_method_bind_ptrcall(cls._meth_get_parent_class, cls._instance, ffi.cast("void**", args), ret)
        c_str = lib.godot_string_c_str(ret)
        return ffi.string(c_str)


class BaseObject:
    def __init__(self, gd_obj=None):
        self._gd_obj = gd_obj if gd_obj else self._gd_constructor()

    def _gd_set_godot_obj(self, obj):
        self._gd_obj = obj

    def __eq__(self, other):
        if hasattr(other, '_gd_obj'):
            return self._gd_obj == other._gd_obj
        else:
            return False


# TODO: use pybind11 for this ?
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self._gd_obj = ffi.new('godot_vector2*')
        lib.godot_vector2_new(self._gd_obj, x, y)

    @property
    def x(self):
        return lib.godot_vector2_get_x(self._gd_obj)

    @property
    def y(self):
        return lib.godot_vector2_get_y(self._gd_obj)

    @x.setter
    def x(self, val):
        lib.godot_vector2_set_x(self._gd_obj, val)

    @y.setter
    def y(self, val):
        lib.godot_vector2_set_y(self._gd_obj, val)

    @property
    def width(self):
        return self.x

    @property
    def height(self):
        return self.y

    @width.setter
    def width(self, val):
        self.x = val

    @height.setter
    def height(self, val):
        self.y = val

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector2) and other.x == self.x and other.y == self.y

    def __neg__(self):
        return type(self)(-self.x, -self.y)

    def __pos__(self):
        return self


def _gen_stub(msg):
    return lambda *args: print(msg)


def build_method(classname, meth):
    methname = meth['name']
    # Flag METHOD_FLAG_VIRTUAL only available when compiling godot with DEBUG_METHODS_ENABLED
    methbind = lib.godot_method_bind_get_method(classname.encode(), methname.encode())
    if meth['flags'] & lib.METHOD_FLAG_VIRTUAL or methbind == ffi.NULL:
        def bind(self, *args):
            raise NotImplementedError()
    else:
        def bind(self, *args):
            # TODO: check args number and type here (ptrcall means segfault on bad args...)
            print('++++ Calling %s.%s (%s) on %s with %s' % (classname, methname, meth, self, args))
            # TODO: check len(args)
            raw_args = [pyobj_to_raw(meth_arg['type'], arg)
                        for arg, meth_arg in zip(args, meth['args'])]
            # args_as_variants = [pyobj_to_variant(arg) for arg in args]
            gdargs = ffi.new("void*[]", raw_args) if raw_args else ffi.NULL
            ret = new_raw(meth['return']['type'])
            print('==============================>>>', methbind, self._gd_obj, gdargs, ret)
            lib.godot_method_bind_ptrcall(methbind, self._gd_obj, gdargs, ret)
            return raw_to_pyobj(meth['return']['type'], ret, meth['return']['hint_string'])

    return bind


def build_property(classname, prop):
    propname = prop['name']
    getbind = lib.godot_method_bind_get_method(classname.encode(), propname.encode())
    ######################### BUG getbind is NULL !!!

    def getter(self):
        print('++++ Property GET %s.%s (%s) on %s' % (classname, propname, prop, self))
        ret = new_raw(prop['type'])
        print('==============================>>>', getbind, self._gd_obj, ffi.NULL, ret)
        lib.godot_method_bind_ptrcall(getbind, self._gd_obj, ffi.NULL, ret)
        return raw_to_pyobj(prop['type'], ret, prop['hint_string'])

    def setter(self, value):
        print('++++ Property SET %s.%s (%s) on %s with %s' % (classname, propname, prop, self, value))
        gdvalue = pyobj_to_raw(prop['type'], value, prop['hint_string'])
        gdargs = ffi.new("void*[]", [gdvalue])
        ret = new_raw(prop['type'])
        print('==============================>>>', getbind, self._gd_obj, ffi.NULL, ret)
        lib.godot_method_bind_ptrcall(getbind, self._gd_obj, gdargs, ret)
        return raw_to_pyobj(prop['type'], ret, prop['hint_string'])

    propobj = property(getter)
    return propobj.setter(setter)


def build_class(classname, binding_classname=None):
    binding_classname = binding_classname or classname
    nmspc = {
        '_gd_name': classname,
        '_gd_constructor': ClassDB.get_class_constructor(classname)
    }
    print('======> BINDING', classname)
    # Methods
    for meth in ClassDB.get_class_methods(classname):
        print('=> M', meth['name'])
        nmspc[meth['name']] = build_method(classname, meth)
    # Properties
    for prop in ClassDB.get_class_properties(classname):
        propname = prop['name']
        print('=> P', propname)
        nmspc[propname] = build_property(classname, prop)
    # Constants
    for constname in ClassDB.get_class_consts(classname):
        nmspc[constname] = ClassDB.get_integer_constant(classname, constname)
        print('=> C', constname)
    parentname = ClassDB.get_parent_class(classname)
    print('=> P', parentname)
    if parentname:
        bases = (getattr(module, parentname), )
    else:
        bases = (BaseObject, )
    return type(binding_classname, bases, nmspc)


def build_global(name, clsname):
    return getattr(module, clsname)(lib.godot_global_get_singleton(name.encode()))


# Werkzeug style lazy module
class LazyBindingsModule(ModuleType):

    """Automatically import objects from the modules."""

    def _bootstrap_global_singletons(self):
        # Special classes generated in `godot/core/core_bind.h`, classname
        # has a "_" prefix
        for clsname, name in (
                ('_ResourceLoader', 'ResourceLoader'),
                ('_ResourceSaver', 'ResourceSaver'),
                ('_OS', 'OS'),
                ('_Geometry', 'Geometry'),
                ('_ClassDB', 'ClassDB'),
                ('_Engine', 'Engine'),):
            self._available[name] = partial(build_global, name, clsname)
        # Regular classses, we have to rename the classname with a "_" prefix
        # to give the name to the singleton
        # TODO: GlobalConfig doesn't provide a `list_singletons` to load
        # this dynamically :'-(
        for new_clsname, name in (
                ('_AudioServer', 'AudioServer'),
                ('_AudioServer', 'AS'),
                ('_GlobalConfig', 'GlobalConfig'),
                ('_IP', 'IP'),
                ('_Input', 'Input'),
                ('_InputMap', 'InputMap'),
                ('_Marshalls', 'Marshalls'),
                # TODO: seems to have been removed...
                # ('_PathRemap', 'PathRemap'),
                ('_Performance', 'Performance'),
                ('_Physics2DServer', 'Physics2DServer'),
                ('_Physics2DServer', 'PS2D'),
                ('_PhysicsServer', 'PhysicsServer'),
                ('_PhysicsServer', 'PS'),
                # TODO: seems to have been removed...
                # ('_SpatialSound2DServer', 'SpatialSound2DServer'),
                # ('_SpatialSound2DServer', 'SS2D'),
                # ('_SpatialSoundServer', 'SpatialSoundServer'),
                # ('_SpatialSoundServer', 'SS'),
                ('_TranslationServer', 'TranslationServer'),
                ('_TranslationServer', 'TS'),
                ('_VisualServer', 'VisualServer'),
                ('_VisualServer', 'VS')):
            if new_clsname not in self._available:
                self._available[new_clsname] = self._available[name]
            self._available[name] = partial(build_global, name, new_clsname)

    def __init__(self, name, doc=None):
        super().__init__(name, doc=doc)
        self._loaded = {'Vector2': Vector2}
        # Load global constants
        self._loaded.update(GlobalConstants.get_global_constansts())
        # Register classe types
        self._available = {name: partial(build_class, name) for name in ClassDB.get_class_list()}
        self._bootstrap_global_singletons()
        # self._bootstrap_builtins()
        setattr(self, '__package__', name)
        setattr(self, '__all__', list(self._loaded.keys()) + list(self._available.keys()))

    def __getattr__(self, name):
        if name not in self._loaded:
            loader = self._available.get(name)
            if not loader:
                return ModuleType.__getattribute__(self, name)
            self._loaded[name] = loader()
        return self._loaded[name]

    def __dir__(self):
        """Just show what we want to show."""
        result = list(self.__all__)
        result.extend(('__all__', '__doc__', '__loader__', '__name__',
                       '__package__', '__spec__', '_available', '_loaded'))
        return result


module = LazyBindingsModule("godot.bindings")
sys.modules["godot.bindings"] = module
