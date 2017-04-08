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
#include "modules/dlscript/godot.h"
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
""")


with open(BASEDIR + '/mod_godot.inc.py', 'r') as fd:
    godot_module = fd.read()
with open(BASEDIR + '/tools.inc.py', 'r') as fd:
    tools = fd.read()
with open(BASEDIR + '/mod_godot_bindings.inc.py', 'r') as fd:
    godot_bindings_module = fd.read()


ffibuilder.embedding_init_code("""
print('============> INIT CFFI <===========')

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
    if handle:
        return handle
    else:
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


@ffi.def_extern()
def pybind_call_meth(handle, methname, args, argcount, ret, error):
    instance = ffi.from_handle(handle)
    meth = getattr(instance, ffi.string(methname))
    print('Calling %s on %s (%s) ==> %s' % (ffi.string(methname), handle, instance, meth))
    pyargs = [variant_to_pyobj(args[i]) for i in range(argcount)]
    try:
        pyret = meth(*pyargs)
        pyobj_to_variant(pyret, ret)
    except NotImplementedError:
        error[0] = 1
    except TypeError:
        error[0] = 2
    # TODO: handle errors here

# =====

@ffi.def_extern()
def do_stuff(x, y):
    return x + y

@ffi.def_extern()
def py_instance_set_godot_obj(instance_handle, godot_obj):
    self = ffi.from_handle(ffi.cast('void*', instance_handle))
    print('** %s switched from %s to %s' % (self, self._gd_obj, godot_obj))
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

""" + tools + godot_module + godot_bindings_module + """

""")


# TODO: this header extractor is not ready yet...
def load_dlscript_header_for_cdef(path, loaded_includes):
    src_lines = []
    macroif_stack = []
    with open(GODOT_HOME + '/modules/dlscript/' + path) as fd:
        for line in fd.readlines():
            # Skip the line if it is inside a #if 0 or #ifdef __cplusplus block
            if re.search(r'#[ \t]*ifdef[ \t]+__cplusplus', line) or re.search(r'#[ \t]+if[ \t]+0', line):
                print('========SKIP', line)
                macroif_stack.append('SKIP_BLOCK')
            elif re.search(r'#[ \t]*(ifdef|ifndef|if)', line):
                print('========KEEP', line)
                macroif_stack.append('KEEP_BLOCK')
            elif re.search(r'#[ \t]*endif', line):
                blk = macroif_stack.pop()
                print('======== ENDBLOCK', blk)
            elif 'SKIP_BLOCK' not in macroif_stack:
                match = re.search(r'#[ \t]*include[ \t]+["<]((godot/)?godot_[a-zA-Z0-9/_.]+)[>"]', line)
                if match:
                    header = match.group(1)
                    header = 'godot/' + header if not header.startswith('godot/') else header
                    if header in loaded_includes:
                        continue
                    loaded_includes.append(header)
                    src_lines.append('// ' + line)
                    src_lines.append(load_dlscript_header_for_cdef(header, loaded_includes))
                    print(src_lines[-1])
                elif re.search(r'^[ \t]*#', line):
                    # Ignore other macros
                    continue
                else:
                    src_lines.append(line.replace(' GDAPI ', ' '))
                    print(src_lines[-1])
    return '\n'.join(src_lines)


# C stuff exposed to Python
with open(BASEDIR + '/cdef.h') as fd:
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
"""
# + load_dlscript_header_for_cdef('godot.h', [])
+ cdef
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
//    void pybind_load_module(const wchar_t *modname, void *ret_mod, void *ret_cls);
    void *pybind_load_exposed_class_per_module(const wchar_t *modname);
""")


ffibuilder.emit_c_code(BASEDIR + "/pythonscriptcffi.cpp")
