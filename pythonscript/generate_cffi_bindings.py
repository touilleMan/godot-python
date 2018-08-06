#! /usr/bin/env python3

try:
    import cffi
except ImportError:
    raise SystemExit("Module cffi is missing, install it with `pip install cffi`")

import os
import argparse


BASEDIR = os.path.dirname(os.path.abspath(__file__))


def strip_hashed_src(src):
    return "\n".join([l for l in src.split("\n") if not l.startswith("#")])


def generate_cffi_bindings(output, cdef_path):

    ffibuilder = cffi.FFI()

    # Divide between functions declarations and struct definitions
    with open("%s/cffi_bindings_api.h" % BASEDIR, "r") as fd:
        api_src = fd.read()
    with open("%s/cffi_bindings_api_struct.h" % BASEDIR, "r") as fd:
        api_struct_src = fd.read()

    # Def needed to compile output .c file
    ffibuilder.set_source(
        "pythonscriptcffi",
        """
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

    """
        + api_src,
    )

    # Python source code embedded and run at init time
    # (including python functions exposed to C through `@ffi.def_extern()`)
    # Given this code is included inside a cffi-generated C source file, pdb
    # cannot display it at all. This is why it should not contain anything
    # but imports.
    ffibuilder.embedding_init_code("""from godot.hazmat.ffi import *""")

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
    """
        + cdef
        + strip_hashed_src(api_struct_src)
    )

    # Python `@ffi.def_extern()` API exposed to C
    ffibuilder.embedding_api(strip_hashed_src(api_src).replace("DLL_EXPORT", ""))

    # Output .c code ready to be compiled ;-)
    ffibuilder.emit_c_code(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CFFI binding .cpp file.")
    parser.add_argument("--output", "-o", default=BASEDIR + "/cffi_bindings.gen.c")
    parser.add_argument("--cdef", "-c", default=BASEDIR + "/cdef.gen.h")
    args = parser.parse_args()
    generate_cffi_bindings(args.output, args.cdef)
