import cffi
import os
import argparse


parser = argparse.ArgumentParser(description='Generate CFFI binding .cpp file.')
parser.add_argument('--dev-dyn', '-d', action='store_true',
                    help='Load at runtime *.inc.py files instead of embedding them in the .cpp')
args = parser.parse_args()


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
EMBEDDING_INC_SOURCES = (
    'embedding_init_code.inc.py',
    'mod_godot.inc.py',
    'builtin_node_path.inc.py',
    'builtin_rect2.inc.py',
    'builtin_vector2.inc.py',
    'builtin_vector3.inc.py',
    'builtin_basis.inc.py',
    'builtin_quat.inc.py',
    'tools.inc.py',
    'mod_godot_bindings.inc.py'
)
# Hack not to have to compile everytime we modify an `*.inc.py` file
if args.dev_dyn:
    embedding_init_code = """
code = []
for to_include in {sources!r}:
    with open('%s/%s' % ({basedir!r}, to_include), 'r') as fd:
        code.append(fd.read())
exec('\\n'.join(code))
""".format(sources=EMBEDDING_INC_SOURCES, basedir=BASEDIR)
else:
    embedding_init_code = []
    for to_include in EMBEDDING_INC_SOURCES:
        with open('%s/%s' % (BASEDIR, to_include), 'r') as fd:
            embedding_init_code.append(fd.read())
    embedding_init_code = '\n'.join(embedding_init_code)

ffibuilder.embedding_init_code(embedding_init_code)



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
