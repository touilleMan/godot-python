import cffi
import os
import re


BASEDIR = os.path.dirname(os.path.abspath(__file__))
GODOT_HOME = os.environ.get('GODOT_HOME', BASEDIR + '/../../godot')

ffibuilder = cffi.FFI()

# Python functions exposed to C
# ffibuilder.embedding_api(r"""
#     typedef struct { ...; } PyObject;
#     typedef struct { ...; } godot_variant;
#     typedef void godot_object;
#     int do_stuff(int, int);

#     PyObject *pybind_module_from_name(wchar_t *name);
#     PyObject *instanciate_binding_from_godot_obj(PyObject *py_cls, godot_object *godot_obj);
#     void py_instance_set_godot_obj(PyObject *py_instance, godot_object *godot_obj);
#     PyObject *variants_to_pyobjs(void **args, int argcount);
#     PyObject *variant_to_pyobj2(void *arg);
#     PyObject *pyobj_to_variant2(PyObject *arg);
#     godot_variant *call_with_variants(PyObject *func, const godot_variant **args, int argcount);

#     void *pybind_instanciate_from_classname(const wchar_t *classname);
#     void *pybind_wrap_gdobj_with_class(void *cls_handle, void *gdobj);
#     void pybind_release_instance(void *handle);
#     void pybind_call_meth(void *handle, const wchar_t *methname, void **args, int argcount, void *ret, int *error);
# //    void pybind_load_module(const wchar_t *modname, void *ret_mod, void *ret_cls);
#     void *pybind_load_exposed_class_per_module(const wchar_t *modname);
# """)


ffibuilder.set_source("pythonscriptcffi", """
#include "Include/Python.h"
#include "modules/gdnative/godot.h"
// TODO: MethodFlags not in ldscript headers
enum MethodFlags {
    METHOD_FLAG_NORMAL=1,
    METHOD_FLAG_EDITOR=2,
    METHOD_FLAG_NOSCRIPT=4,
    METHOD_FLAG_CONST=8,
    METHOD_FLAG_REVERSE=16, // used for events
    METHOD_FLAG_VIRTUAL=32,
    METHOD_FLAG_FROM_SCRIPT=64,
    METHOD_FLAG_VARARG=128,
    METHOD_FLAGS_DEFAULT=METHOD_FLAG_NORMAL,
};

CFFI_DLLEXPORT int pybind_init(void) {
    return cffi_start_python();
}

typedef struct {
    int type;
    godot_string name;
    int hint;
    godot_string hint_string;
    uint32_t usage;
} pybind_prop_info;

""")


embedding_init_code_extra = []
for to_include in (
        'mod_godot.inc.py',
        'builtin_vector2.inc.py',
        'builtin_vector3.inc.py',
        'builtin_basis.inc.py',
        'builtin_quat.inc.py',
        'tools.inc.py',
        'mod_godot_bindings.inc.py',):
    with open('%s/%s' % (BASEDIR, to_include), 'r') as fd:
        embedding_init_code_extra.append(fd.read())
embedding_init_code_extra = '\n'.join(embedding_init_code_extra)


ffibuilder.embedding_init_code("""
from pythonscriptcffi import ffi, lib

# Protect python objects passed to C from beeing garbage collected
class ProtectFromGC:
    def __init__(self):
        self._data = {}

    def register(self, value):
        self._data[id(value)] = value

    def unregister(self, value):
        del self._data[id(value)]

    def unregister_by_id(self, id):
        del self._data[id]
protect_from_gc = ProtectFromGC()


def connect_handle(obj):
    handle = obj.__dict__.get('_cffi_handle')
    if not handle:
        handle = ffi.new_handle(obj)
        obj._cffi_handle = handle
    return handle


@ffi.def_extern()
def pybind_load_exposed_class_per_module(modname):
    modname = ffi.string(modname)
    __import__(modname)  # Force lazy loading of the module
    cls = get_exposed_class_per_module(modname)
    return connect_handle(cls)


@ffi.def_extern()
def pybind_wrap_gdobj_with_class(cls_handle, gdobj):
    instance = ffi.from_handle(cls_handle)(gdobj)
    protect_from_gc.register(instance)
    return connect_handle(instance)


@ffi.def_extern()
def pybind_instanciate_from_classname(classname):
    cls = get_exposed_class_per_name(ffi.string(classname))
    instance = cls()
    protect_from_gc.register(instance)
    return connect_handle(instance)


@ffi.def_extern()
def pybind_release_instance(handle):
    instance = ffi.from_handle(handle)
    protect_from_gc.unregister(instance)


CALL_METH_OK = 0
CALL_METH_ERROR_INVALID_METHOD = 1
CALL_METH_ERROR_INVALID_ARGUMENT = 2
CALL_METH_ERROR_TOO_MANY_ARGUMENTS = 3
CALL_METH_ERROR_TOO_FEW_ARGUMENTS = 4
CALL_METH_ERROR_INSTANCE_IS_NULL = 5

CALL_METH_TYPE_NIL = 0 << 4
CALL_METH_TYPE_BOOL = 1 << 4
CALL_METH_TYPE_INT = 2 << 4
CALL_METH_TYPE_REAL = 3 << 4
CALL_METH_TYPE_STRING = 4 << 4
CALL_METH_TYPE_VECTOR2 = 5 << 4
CALL_METH_TYPE_RECT2 = 6 << 4
CALL_METH_TYPE_VECTOR3 = 7 << 4
CALL_METH_TYPE_TRANSFORM2D = 8 << 4
CALL_METH_TYPE_PLANE = 9 << 4
CALL_METH_TYPE_QUAT = 10 << 4
CALL_METH_TYPE_RECT3 = 11 << 4
CALL_METH_TYPE_BASIS = 12 << 4
CALL_METH_TYPE_TRANSFORM = 13 << 4
CALL_METH_TYPE_COLOR = 14 << 4
CALL_METH_TYPE_IMAGE = 15 << 4
CALL_METH_TYPE_NODE_PATH = 16 << 4
CALL_METH_TYPE__RID = 17 << 4
CALL_METH_TYPE_OBJECT = 18 << 4
CALL_METH_TYPE_INPUT_EVENT = 19 << 4
CALL_METH_TYPE_DICTIONARY = 20 << 4
CALL_METH_TYPE_ARRAY = 21 << 4
CALL_METH_TYPE_POOL_BYTE_ARRAY = 22 << 4
CALL_METH_TYPE_POOL_INT_ARRAY = 23 << 4
CALL_METH_TYPE_POOL_REAL_ARRAY = 24 << 4
CALL_METH_TYPE_POOL_STRING_ARRAY = 25 << 4
CALL_METH_TYPE_POOL_VECTOR2_ARRAY = 26 << 4
CALL_METH_TYPE_POOL_VECTOR3_ARRAY = 27 << 4
CALL_METH_TYPE_POOL_COLOR_ARRAY = 28 << 4


@ffi.def_extern()
def pybind_call_meth(handle, methname, args, argcount, ret, error):
    instance = ffi.from_handle(handle)
    meth = getattr(instance, ffi.string(methname))
    print('[GD->PY] Calling %s on %s (%s) ==> %s' % (ffi.string(methname), handle, instance, meth))
    pyargs = [variant_to_pyobj(args[i]) for i in range(argcount)]
    # error is an hacky int compressing Variant::CallError values
    try:
        pyret = meth(*pyargs)
        pyobj_to_variant(pyret, ret)
        error[0] = CALL_METH_OK
    except NotImplementedError:
        error[0] = CALL_METH_ERROR_INVALID_METHOD
    except TypeError as exc:
        print(exc)
        error[0] = 1 | CALL_METH_ERROR_INVALID_ARGUMENT | CALL_METH_TYPE_NIL
    # TODO: handle errors here


@ffi.def_extern()
def pybind_set_prop(handle, propname, val):
    instance = ffi.from_handle(handle)
    try:
        pyval = variant_to_pyobj(val)
        setattr(instance, ffi.string(propname), pyval)
        return True
    except Exception as exc:
        print(exc)
        return False


@ffi.def_extern()
def pybind_get_prop(handle, propname, ret):
    instance = ffi.from_handle(handle)
    try:
        pyret = getattr(instance, ffi.string(propname))
        pyobj_to_variant(pyret, ret)
        return True
    except Exception as exc:
        print(exc)
        return False


@ffi.def_extern()
def pybind_get_prop_type(handle, propname, prop_type):
    instance = ffi.from_handle(handle)
    prop = instance._exported.get(ffi.string(propname), None)
    if not prop:
        return False
    else:
        prop_type[0] = prop.gd_type
        return True


@ffi.def_extern()
def pybind_get_prop_default_value(handle, propname, r_val):
    cls_or_instance = ffi.from_handle(handle)
    prop = cls_or_instance._exported.get(ffi.string(propname), None)
    if not prop:
        return False
    print('default_value for ', ffi.string(propname), prop)
    pyobj_to_variant(prop.default, r_val)
    return True


@ffi.def_extern()
def pybind_get_prop_info(handle, propname, r_prop_info):
    cls_or_instance = ffi.from_handle(handle)
    prop = cls_or_instance._exported.get(ffi.string(propname), None)
    if not prop:
        return False
    r_prop_info.type = prop.gd_type
    r_prop_info.hint = prop.gd_hint
    r_prop_info.name = prop.gd_name[0]
    r_prop_info.hint_string = prop.gd_hint_string[0]
    r_prop_info.usage = prop.gd_usage
    return True


@ffi.def_extern()
def pybind_get_prop_list(handle):
    cls_or_instance = ffi.from_handle(handle)
    return cls_or_instance._exported_raw_list


# =====


@ffi.def_extern()
def do_stuff(x, y):
    return x + y


@ffi.def_extern()
def py_instance_set_godot_obj(instance_handle, godot_obj):
    self = ffi.from_handle(ffi.cast('void*', instance_handle))
    print('[GD->PY] %s switched from %s to %s' % (self, self._gd_obj, godot_obj))
    self._gd_obj = godot_obj


# TODO: find a cleaner way to prevent the newly initialized binding from beeing
# garbage collected as soon as we leave the function
newly_intanciated_anchor = []
@ffi.def_extern()
def instanciate_binding_from_godot_obj(py_cls_handle, godot_obj):
    global newly_intanciated_anchor
    py_cls = ffi.from_handle(ffi.cast('void*', py_cls_handle))
    instance = py_cls(godot_obj)
    instance_handle = ffi.new_handle(instance)
    newly_intanciated_anchor.append((instance, instance_handle))
    return instance_handle


@ffi.def_extern()
def variant_to_pyobj2(v):
    global newly_intanciated_anchor
    instance = variant_to_pyobj(v)
    instance_handle = ffi.new_handle(instance)
    newly_intanciated_anchor.append((instance, instance_handle))
    return instance_handle


@ffi.def_extern()
def pyobj_to_variant2(v):
    global newly_intanciated_anchor
    instance = pyobj_to_variant(v)
    instance_handle = ffi.new_handle(instance)
    newly_intanciated_anchor.append((instance, instance_handle))
    return instance_handle


@ffi.def_extern()
def variants_to_pyobjs(args, argcount):
    return [variant_to_pyobj(args[i]) for i in range(argcount)]


@ffi.def_extern()
def call_with_variants(func, args, argcount):
    pyfunc = ffi.from_handle(ffi.cast('void*', func))
    pyargs = [variant_to_pyobj(args[i]) for i in range(argcount)]
    pyret = pyfunc(*pyargs)
    return pyobj_to_variant(pyret)

""" + embedding_init_code_extra + """

""")


with open(BASEDIR + '/cdef.gen.h') as fd:
    cdef = fd.read()
ffibuilder.cdef(
    """
// TODO: not in ldscript headers ?
enum MethodFlags {
    METHOD_FLAG_NORMAL=1,
    METHOD_FLAG_EDITOR=2,
    METHOD_FLAG_NOSCRIPT=4,
    METHOD_FLAG_CONST=8,
    METHOD_FLAG_REVERSE=16, // used for events
    METHOD_FLAG_VIRTUAL=32,
    METHOD_FLAG_FROM_SCRIPT=64,
    METHOD_FLAG_VARARG=128,
    METHOD_FLAGS_DEFAULT=METHOD_FLAG_NORMAL,
};

""" + cdef + """

typedef struct {
    int type;
    godot_string name;
    int hint;
    godot_string hint_string;
    uint32_t usage;
} pybind_prop_info;

"""
)

ffibuilder.embedding_api(r"""
    typedef struct { ...; } PyObject;
//    typedef struct { ...; } godot_variant;
    typedef void godot_object;
    int do_stuff(int, int);

    PyObject *pybind_module_from_name(wchar_t *name);
    PyObject *instanciate_binding_from_godot_obj(PyObject *py_cls, godot_object *godot_obj);
    void py_instance_set_godot_obj(PyObject *py_instance, godot_object *godot_obj);
    PyObject *variants_to_pyobjs(void **args, int argcount);
    PyObject *variant_to_pyobj2(void *arg);
    PyObject *pyobj_to_variant2(PyObject *arg);
    godot_variant *call_with_variants(PyObject *func, const godot_variant **args, int argcount);

    void *pybind_instanciate_from_classname(const wchar_t *classname);
    void *pybind_wrap_gdobj_with_class(void *cls_handle, void *gdobj);
    void pybind_release_instance(void *handle);
    void pybind_call_meth(void *handle, const wchar_t *methname, void **args, int argcount, void *ret, int *error);
    godot_bool pybind_set_prop(void *handle, const wchar_t *propname, const godot_variant *value);
    godot_bool pybind_get_prop(void *handle, const wchar_t *propname, godot_variant *ret);
    godot_bool pybind_get_prop_type(void *handle, const wchar_t *propname, int *prop_type);
    godot_bool pybind_get_prop_default_value(void *handle, const wchar_t *propname, godot_variant *r_val);
    const godot_string *pybind_get_prop_list(void *handle);
    godot_bool pybind_get_prop_info(void *handle, const wchar_t *propname, pybind_prop_info *r_prop_info);

//    void pybind_load_module(const wchar_t *modname, void *ret_mod, void *ret_cls);
    void *pybind_load_exposed_class_per_module(const wchar_t *modname);
""")


ffibuilder.emit_c_code(BASEDIR + "/pythonscriptcffi.cpp")
