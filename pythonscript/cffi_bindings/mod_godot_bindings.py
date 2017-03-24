module = imp.new_module("godot.bindings")


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


module.Vector2 = Vector2


class BaseObject:
    def __init__(self):
        self._gd_obj = self._gd_constructor()

    def _gd_set_godot_obj(self, obj):
        self._gd_obj = obj


def iter_on_c(cstruct):
    i = 0
    while cstruct[i] != ffi.NULL:
        yield cstruct[i]
        i += 1


def build_class(classname):
    cclassname = classname.encode()
    nmspc = {
        '_gd_name': classname,
        '_gd_constructor': lib.godot_get_class_constructor(cclassname)
    }
    # Methods
    for crawmeth in iter_on_c(lib.godot_get_class_methods(cclassname)):
        cmethname = ffi.string(crawmeth)
        methname = cmethname.decode()
        # methbind = lib.godot_method_bind_get_method(classname, methname)
        # def bind(self, *args):
        #     lib.godot_method_bind_get_method(methbind)
        #     ret = ffi.new()
        #     lib.godot_method_bind_ptrcall(methbind, self, )
        nmspc[methname] = lambda *args: print('**** Should have called ', classname, methname)
    # Properties
    for crawprop in iter_on_c(lib.godot_get_class_properties(cclassname)):
        cpropname = ffi.string(crawprop)
        propname = cpropname.decode()
        nmspc[propname] = property(lambda self: print('***** Should have called %s.%s getter' % (classname, propname)))
        nmspc[propname].setter(lambda self, value: print('***** Should have called %s.%s setter' % (classname, propname)))
    # Constants
    for crawconst in iter_on_c(lib.godot_get_class_constants(cclassname)):
        cconstname = ffi.string(crawconst)
        constname = cconstname.decode()
        nmspc[constname] = 42
    parent_name = ffi.string(lib.godot_get_class_parent(cclassname)).decode()
    if parent_name:
        bases = (getattr(module, parent_name), )
    else:
        bases = (BaseObject, )
    return type(classname, bases, nmspc)


def get_class_list():
    instance = lib.godot_global_get_singleton(b"ClassDB")
    meth = lib.godot_method_bind_get_method(b"_ClassDB", b"get_class_list")
    ret = ffi.new("godot_pool_string_array*")
    lib.godot_pool_string_array_new(ret)
    lib.godot_method_bind_ptrcall(meth, instance, ffi.NULL, ret)

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
            parentname = get_class_parent(classname)
            if not parentname or parentname in classes:
                if classname not in classes:
                    classes.append(classname)

    return classes


def get_class_parent(classname):
    instance = lib.godot_global_get_singleton(b"ClassDB")
    meth = lib.godot_method_bind_get_method(b"_ClassDB", b"get_parent_class")
    ret = ffi.new("godot_string*")
    gd_classname = ffi.new("godot_string*")
    lib.godot_string_new_data(gd_classname, classname.encode(), len(classname.encode()))
    args = ffi.new("godot_string**", gd_classname)
    lib.godot_method_bind_ptrcall(meth, instance, ffi.cast("void**", args), ret)
    c_str = lib.godot_string_c_str(ret)
    return ffi.string(c_str)


for classname in get_class_list():
    setattr(module, classname, build_class(classname))

# clist = lib.godot_get_class_list()
# i = 0
# while clist[i] != ffi.NULL:
#     cclassname = ffi.string(clist[i])
#     classname = cclassname.decode()
#     constructor = lib.godot_get_class_constructor(cclassname)
#     cmethods = lib.godot_get_class_methods()
#     j = 0

#     setattr(module, classname, type(classname, (BaseObject, ), {'_gd_constructor': constructor, '_gd_name': classname}))
#     i += 1


sys.modules["godot.bindings"] = module
