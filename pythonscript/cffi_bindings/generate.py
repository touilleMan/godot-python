#! /usr/bin/env python3

try:
    import cffi
except ImportError:
    raise SystemExit('Module cffi is missing, install it with `pip install cffi`')
import os
import argparse


BASEDIR = os.path.dirname(os.path.abspath(__file__))


def strip_hashed_src(src):
    return '\n'.join([l for l in src.split('\n') if not l.startswith('#')])


def generate_pythonscriptcffi(output, cdef_path, dev_dyn):

    ffibuilder = cffi.FFI()

    # Divide between functions declarations and struct definitions
    with open('%s/api.h' % BASEDIR, 'r') as fd:
        api_src = fd.read()
    with open('%s/api_struct.h' % BASEDIR, 'r') as fd:
        api_struct_src = fd.read()

    # Def needed to compile output .c file
    ffibuilder.set_source("pythonscriptcffi", """
    #include <gdnative_api_struct.gen.h>
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

    """ + api_src#)
    + """
    static godot_real (*ptrfunc_godot_vector2_distance_to)(const godot_vector2 *p_self, const godot_vector2 *p_to) = godot_vector2_distance_to;

    typedef struct {
        godot_real (*_godot_vector2_distance_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
    } structfunc_t;
    static structfunc_t structfunc = {
        ._godot_vector2_distance_to=godot_vector2_distance_to
    };
    godot_real structfunc_godot_vector2_distance_to(const godot_vector2 *p_self, const godot_vector2 *p_to) {
        return structfunc._godot_vector2_distance_to(p_self, p_to);
    }
    godot_real staticfunc_godot_vector2_distance_to(const godot_vector2 *p_self, const godot_vector2 *p_to) {
        return ptrfunc_godot_vector2_distance_to(p_self, p_to);
    }
    """)

    # Python source code embedded and run at init time
    # (including python functions exposed to C through `@ffi.def_extern()`)
    EMBEDDING_INC_SOURCES = (
        'embedding_init_code.inc.py',
        'profiler.inc.py',
        'allocator.inc.py',
        'mod_godot.inc.py',
        'builtin_rid.inc.py',
        'builtin_color.inc.py',
        'builtin_node_path.inc.py',
        'builtin_vector2.inc.py',
        'builtin_vector3.inc.py',
        'builtin_plane.inc.py',
        'builtin_rect2.inc.py',
        'builtin_aabb.inc.py',
        'builtin_basis.inc.py',
        'builtin_quat.inc.py',
        'builtin_transform2d.inc.py',
        'builtin_transform.inc.py',
        'builtin_pool_arrays.inc.py',
        'builtin_array.inc.py',
        'builtin_dictionary.inc.py',
        'tools.inc.py',
        'mod_godot_bindings.inc.py'
    )
    # Hack not to have to compile everytime we modify an `*.inc.py` file
    if dev_dyn:
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
    with open(cdef_path) as fd:
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

    // We use malloc to bypass Python garbage collector for Godot Object
    void *malloc(size_t size);
    void free(void *ptr);
    """ + cdef + strip_hashed_src(api_struct_src) + """
    extern godot_real (*ptrfunc_godot_vector2_distance_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
    extern godot_real structfunc_godot_vector2_distance_to(const godot_vector2 *p_self, const godot_vector2 *p_to);
    extern godot_real staticfunc_godot_vector2_distance_to(const godot_vector2 *p_self, const godot_vector2 *p_to);

    typedef struct {
        godot_real (*_godot_vector2_distance_to)(const godot_vector2 *p_self, const godot_vector2 *p_to);
    } structfunc_t;
    extern structfunc_t structfunc;
    """)

    # Python `@ffi.def_extern()` API exposed to C
    ffibuilder.embedding_api(strip_hashed_src(api_src))

    # Output .c code ready to be compiled ;-)
    ffibuilder.emit_c_code(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate CFFI binding .cpp file.')
    parser.add_argument('--output', '-o', default=BASEDIR + "/pythonscriptcffi.gen.c")
    parser.add_argument('--cdef', '-c', default=BASEDIR + '/cdef.gen.h')
    parser.add_argument('--dev-dyn', '-d', action='store_true',
                        help='Load at runtime *.inc.py files instead of embedding them in the .c')
    args = parser.parse_args()
    generate_pythonscriptcffi(args.output, args.cdef, args.dev_dyn)
