import cffi
import os


BASEDIR = os.path.dirname(os.path.abspath(__file__))
GODOT_HOME = os.environ.get('GODOT_HOME', BASEDIR + '/../../godot')


def strip_hashed_src(src):
    return '\n'.join([l for l in src.split('\n') if not l.startswith('#')])


ffibuilder = cffi.FFI()

# Divide between functions declarations and struct definitions
with open('%s/api.h' % BASEDIR, 'r') as fd:
    api_src = fd.read()
with open('%s/api_struct.h' % BASEDIR, 'r') as fd:
    api_struct_src = fd.read()


# Def needed to compile output .cpp file
ffibuilder.set_source("pythonscriptcffi", """
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

""" + api_src)


# Python source code embedded and run at init time
# (including python functions exposed to C through `@ffi.def_extern()`)
embedding_init_code = []
for to_include in (
        'embedding_init_code.inc.py',
        'mod_godot.inc.py',
        'builtin_vector2.inc.py',
        'builtin_vector3.inc.py',
        'builtin_basis.inc.py',
        'builtin_quat.inc.py',
        'tools.inc.py',
        'mod_godot_bindings.inc.py',):
    with open('%s/%s' % (BASEDIR, to_include), 'r') as fd:
        embedding_init_code.append(fd.read())
ffibuilder.embedding_init_code('\n'.join(embedding_init_code))


# C API exposed to Python
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

""" + cdef + strip_hashed_src(api_struct_src))


# Python `@ffi.def_extern()` API exposed to C
ffibuilder.embedding_api(strip_hashed_src(api_src))


# Output .cpp code ready to be compiled ;-)
ffibuilder.emit_c_code(BASEDIR + "/pythonscriptcffi.cpp")
