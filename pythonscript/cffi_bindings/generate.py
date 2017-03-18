import cffi
import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))

ffibuilder = cffi.FFI()

ffibuilder.embedding_api(r"""
    typedef struct { ...; } PyObject;
    typedef void godot_object;
    int do_stuff(int, int);
    void py_instance_set_godot_obj(PyObject *py_instance, godot_object *godot_obj);
""")

ffibuilder.set_source("pythonscriptcffi", """
#include "Include/Python.h"
#include "modules/dlscript/godot.h"
""")

with open(BASEDIR + '/mod_godot.py', 'r') as fd:
    godot_module = fd.read()
with open(BASEDIR + '/mod_godot_bindings.py', 'r') as fd:
    godot_bindings_module = fd.read()

ffibuilder.embedding_init_code("""
print('============> INIT CFFI <===========')
import os
import sys
import imp

from pythonscriptcffi import ffi, lib

""" + godot_module + godot_bindings_module + """

@ffi.def_extern()
def do_stuff(x, y):
    return x + y

@ffi.def_extern()
def py_instance_set_godot_obj(instance_handle, godot_obj):
    self = ffi.from_handle(ffi.cast('void*', instance_handle))
    print('** %s switched from %s to %s' % (self, self._gd_obj, godot_obj))
    self._gd_obj = godot_obj
""")

# with open(BASEDIR + "../../modules/dlscript/godot.h", 'r') as fd:
#     ffibuilder.cdef()
ffibuilder.cdef("""
typedef void godot_object;

typedef struct godot_method_bind {
    uint8_t _dont_touch_that[1]; // TODO
} godot_method_bind;

godot_method_bind *godot_method_bind_get_method(const char *p_classname, const char *p_methodname);
void godot_method_bind_ptrcall(godot_method_bind *p_method_bind, godot_object *p_instance, const void **p_args, void *p_ret);


char **godot_get_class_list();
typedef godot_object *(*godot_class_constructor)();
godot_class_constructor godot_get_class_constructor(const char *p_classname);
const char **godot_get_class_methods(const char *p_classname);
const char **godot_get_class_constants(const char *p_classname);
const char **godot_get_class_properties(const char *p_classname);
const char *godot_get_class_parent(const char *p_classname);


typedef float godot_real;
typedef double godot_real64;

typedef struct godot_vector2 {
    uint8_t _dont_touch_that[8];
} godot_vector2;

void godot_vector2_new(godot_vector2 *p_v, const godot_real p_x, const godot_real p_y);

void godot_vector2_set_x(godot_vector2 *p_v, const godot_real p_x);
void godot_vector2_set_y(godot_vector2 *p_v, const godot_real p_y);
godot_real godot_vector2_get_x(const godot_vector2 *p_v);
godot_real godot_vector2_get_y(const godot_vector2 *p_v);

void godot_vector2_normalize(godot_vector2 *p_v);
void godot_vector2_normalized(godot_vector2 *p_dest, const godot_vector2 *p_src);

godot_real godot_vector2_length(const godot_vector2 *p_v);
godot_real godot_vector2_length_squared(const godot_vector2 *p_v);

godot_real godot_vector2_distance_to(const godot_vector2 *p_a, const godot_vector2 *p_b);
godot_real godot_vector2_distance_squared_to(const godot_vector2 *p_a, const godot_vector2 *p_b);
""")

# ffibuilder.compile(target="pythonscriptcffi.*", verbose=True)
ffibuilder.emit_c_code(BASEDIR + "/pythonscriptcffi.cpp")
