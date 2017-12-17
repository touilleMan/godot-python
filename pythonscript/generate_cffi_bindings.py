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


def generate_cffi_bindings(output, cdef_path, dev_dyn):

    ffibuilder = cffi.FFI()

    # Divide between functions declarations and struct definitions
    with open('%s/cffi_bindings_api.h' % BASEDIR, 'r') as fd:
        api_src = fd.read()
    with open('%s/cffi_bindings_api_struct.h' % BASEDIR, 'r') as fd:
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

    """ + api_src)

    # Python source code embedded and run at init time
    # (including python functions exposed to C through `@ffi.def_extern()`)
    EMBEDDING_INC_SOURCES = ('bootstrap.inc.py', )
    EMBEDDING_INC_DIR = '%s/embedded' % BASEDIR
    # Hack not to have to compile everytime we modify an `*.inc.py` file
    if dev_dyn:
        embedding_init_code = """
    code = []
    for to_include in {sources!r}:
        with open('%s/%s' % ({basedir!r}, to_include), 'r') as fd:
            code.append(fd.read())
    exec('\\n'.join(code))
    """.format(sources=EMBEDDING_INC_SOURCES, basedir=EMBEDDING_INC_DIR)
    else:
        embedding_init_code = []
        for to_include in EMBEDDING_INC_SOURCES:
            with open('%s/%s' % (EMBEDDING_INC_DIR, to_include), 'r') as fd:
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
    // TODO: use godot's custom malloc which tracks memory comsumption ?
    void *malloc(size_t size);
    void free(void *ptr);
    """ + cdef + strip_hashed_src(api_struct_src))

    # Python `@ffi.def_extern()` API exposed to C
    ffibuilder.embedding_api(strip_hashed_src(api_src).replace('DLL_EXPORT', ''))

    # Output .c code ready to be compiled ;-)
    ffibuilder.emit_c_code(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate CFFI binding .cpp file.')
    parser.add_argument('--output', '-o', default=BASEDIR + "/cffi_bindings.gen.c")
    parser.add_argument('--cdef', '-c', default=BASEDIR + '/cdef.gen.h')
    parser.add_argument('--dev-dyn', '-d', action='store_true',
                        help='Load at runtime *.inc.py files instead of embedding them in the .c')
    args = parser.parse_args()
    generate_cffi_bindings(args.output, args.cdef, args.dev_dyn)
