import sys
from types import ModuleType
from pythonscriptcffi import ffi, lib


class ClassDB:
    _instance = lib.godot_global_get_singleton(b"ClassDB")
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
            methdict = convert_godot_dictionary(lib.godot_variant_as_dictionary(var))
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
            propdict = convert_godot_dictionary(lib.godot_variant_as_dictionary(var))
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


# TODO: use pybind11 for this ?
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.__gdobj = ffi.new('godot_vector2*')
        lib.godot_vector2_new(self.__gdobj, x, y)

    @property
    def x(self):
        return lib.godot_vector2_get_x(self.__gdobj)

    @property
    def y(self):
        return lib.godot_vector2_get_y(self.__gdobj)

    @x.setter
    def x(self, val):
        return lib.godot_vector2_set_x(self.__gdobj, val)

    @y.setter
    def y(self, val):
        return lib.godot_vector2_set_y(self.__gdobj, val)

    def __repr__(self):
        return "<%s(x=%s, y=%s)>" % (type(self).__name__, self.x, self.y)


# Werkzeug style lazy module
class LazyBindingsModule(ModuleType):

    """Automatically import objects from the modules."""

    def __init__(self, name, doc=None):
        super().__init__(name, doc=doc)
        self._loaded = {'Vector2': Vector2}
        self._available = ClassDB.get_class_list()
        setattr(self, '__package__', name)
        setattr(self, '__all__', self._available)

    def __getattr__(self, name):
        if name not in self._loaded:
            if name not in self._available:
                return ModuleType.__getattribute__(self, name)
            self._loaded[name] = build_class(name)
        return self._loaded[name]

    def __dir__(self):
        """Just show what we want to show."""
        result = list(self.__all__)
        result.extend(('__all__', '__doc__', '__loader__', '__name__',
                       '__package__', '__spec__', '_available', '_loaded'))
        return result


module = LazyBindingsModule("godot.bindings")


class BaseObject:
    def __init__(self):
        self._gd_obj = self._gd_constructor()

    def _gd_set_godot_obj(self, obj):
        self._gd_obj = obj


def _gen_stub(msg):
    return lambda *args: print(msg)


def build_method(classname, methname):
        # methbind = lib.godot_method_bind_get_method(classname, methname)
        # def bind(self, *args):
        #     lib.godot_method_bind_get_method(methbind)
        #     ret = ffi.new()
        #     lib.godot_method_bind_ptrcall(methbind, self, )
        return lambda *args: print('**** Should have called %s.%s' % (classname, methname))


def build_property(classname, propname):
    prop = property(lambda *args: print('***** Should have called %s.%s getter' % (classname, propname)))
    return prop.setter(lambda *args: print('***** Should have called %s.%s setter' % (classname, propname)))


def build_class(classname):
    cclassname = classname.encode()
    nmspc = {
        '_gd_name': classname,
        '_gd_constructor': lib.godot_get_class_constructor(cclassname)
    }
    print('======> BINDING', classname)
    # Methods
    for meth in ClassDB.get_class_methods(classname):
        methname = meth['name']
        print('=> M', methname)
        nmspc[methname] = build_method(classname, methname)
    # Properties
    for prop in ClassDB.get_class_properties(classname):
        propname = prop['name']
        print('=> P', propname)
        nmspc[propname] = build_property(classname, propname)
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
    return type(classname, bases, nmspc)


def convert_godot_dictionary(gddict):
    pdict = {}
    p_gddict = ffi.new("godot_dictionary*", gddict)
    gdkeys = lib.godot_dictionary_keys(p_gddict)
    p_gdkeys = ffi.new("godot_array*", gdkeys)
    for i in range(lib.godot_array_size(p_gdkeys)):
        p_key = lib.godot_array_get(p_gdkeys, i)
        keystr = lib.godot_variant_as_string(p_key)
        p_keystr = ffi.new("godot_string*", keystr)
        c_str = lib.godot_string_c_str(p_keystr)
        value = lib.godot_dictionary_operator_index(p_gddict, p_key)
        # Finger crossed everything is a string...
        valuestr = lib.godot_variant_as_string(value)
        p_valuestr = ffi.new("godot_string*", valuestr)
        c_valuestr = lib.godot_string_c_str(p_valuestr)
        pdict[ffi.string(c_str)] = ffi.string(c_valuestr)
    return pdict


def variant_to_pyobj(gdvar):
    pass


sys.modules["godot.bindings"] = module
