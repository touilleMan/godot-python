#!/usr/bin/env python
from __future__ import print_function
import os, glob
from SCons.Errors import UserError

from tools.generate_gdnative_cffidefs import generate_cdef


EnsureSConsVersion(2, 4)

vars = Variables('custom.py', ARGUMENTS)
vars.Add(EnumVariable('bits', "Target platform bits", '64',
    allowed_values=('64', '32')
))
vars.Add(BoolVariable('dev_dyn', "Load at runtime *.inc.py files instead of embedding them", False))
vars.Add('PYTHON', "Python executable to use for scripts", '')
env = Environment(variables=vars)
Help(vars.GenerateHelpText(env))


### Save my eyes plz ###

# for item in sorted(env.Dictionary().items()):
#     print("construction variable = '%s', value = '%s'" % item)

if 'clang' in env.get('CC'):
    env.Append(CCFLAGS="-fcolor-diagnostics")
if 'gcc' in env.get('CC'):
    env.Append(CCFLAGS="-fdiagnostics-color=always")


### GDnative include/wrapper ###


if 'GDNATIVE_INCLUDE_DIR' not in ARGUMENTS:
    print('GDNATIVE_INCLUDE_DIR argument not provided, assuming `./godot/modules/gdnative/include`')
    ARGUMENTS['GDNATIVE_INCLUDE_DIR'] = './godot/modules/gdnative/include'
gdnative_include_dir = env.Dir(ARGUMENTS['GDNATIVE_INCLUDE_DIR'])
if not gdnative_include_dir.exists():
    raise UserError("Invalid GDNATIVE_INCLUDE_DIR var (%s),  must point to Godot's GDnative include directory" %
                    gdnative_include_dir)


if 'GDNATIVE_WRAPPER_LIB' not in ARGUMENTS:
    print('GDNATIVE_WRAPPER_LIB argument not provided, assuming `./godot/bin/libgdnative_wrapper_code.*.a`')
    match = glob.glob('./godot/bin/libgdnative_wrapper_code.*.a')
    ARGUMENTS['GDNATIVE_WRAPPER_LIB'] = match[0] if match else './godot/bin/libgdnative_wrapper_code.*.a'
gdnative_wrapper_lib = env.File(ARGUMENTS['GDNATIVE_WRAPPER_LIB'])
if not gdnative_wrapper_lib.exists():
    raise UserError("Invalid GDNATIVE_WRAPPER_LIB var (%s),  must point to Godot's GDnative wrapper static lib" %
                    gdnative_wrapper_lib)


env.Append(CPPPATH=gdnative_include_dir.path)
env.Append(LIBS=gdnative_wrapper_lib)


### Python backend ###


python_backend = ARGUMENTS.get('PYTHON_BACKEND', 'cpython').lower()
if python_backend not in ('cpython', 'pypy'):
    raise UserError('PYTHON_BACKEND should be `cpython` (default) or `pypy`')


if python_backend == 'cpython':
    try:
        python_lib = env.File(glob.glob('pythonscript/cpython/libpython*.so.*')[0])
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/cpython/libpython*.so.*`, has CPython been compiled ?" % os.getcwd())
    Command('libpython.so', python_lib, Copy("$TARGET", "$SOURCE"))
    python_lib = env.File('libpython.so')
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/cpython/').path)
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/cpython/Include').path)
    env.Append(CFLAGS='-DBACKEND_CPYTHON')
else:  # pypy
    try:
        python_lib = env.File('pythonscript/pypy/bin/libpypy3-c.so')
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/pypy/bin/libpypy3-c.so`." % os.getcwd())
    env.Command('libpypy-c.so', python_lib, Copy("$TARGET", "$SOURCE"))
    python_lib = env.File('libpypy-c.so')
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/pypy/include').path)
    env.Append(CFLAGS='-DBACKEND_PYPY')


### Generate ###


cdef_gen = env.Command('pythonscript/cffi_bindings/cdef.gen.h', gdnative_include_dir,
    "${PYTHON} ./tools/generate_gdnative_cffidefs.py ${SOURCE} --output=${TARGET} --bits=${bits}")
env.Append(HEADER=cdef_gen)


if env['dev_dyn']:
    print("\033[0;32mPython .inc.py files are dynamically loaded (dev_dyn=True), don't share the binary !\033[0m\n")
python_inc_srcs = Glob('pythonscript/cffi_bindings/*.inc.py')
(pythonscriptcffi_gen, ) = env.Command(
    'pythonscript/cffi_bindings/pythonscriptcffi.gen.c',
    cdef_gen + python_inc_srcs,
    "${PYTHON} ./pythonscript/cffi_bindings/generate.py --cdef=${SOURCE} --output=${TARGET}" +
        (" --dev-dyn" if env['dev_dyn'] else "")
)


### Main compilation stuff ###


env.Append(CFLAGS='-I' + env.Dir('pythonscript').path)
env.Append(CFLAGS='-std=c11')
env.Append(CFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
    '-g -Wformat '
    '-Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 '
    '-Bsymbolic-functions -Wformat -Werror=format-security'.split())


# libpythonX.Ym.so.1.0 will be in the same directory as the godot binary,
# hence we need to inform the binary to look there.
env.Append(LINKFLAGS=["-Wl,-rpath,'$$ORIGIN'"])


sources = [
    "pythonscript/pythonscript.c",
    pythonscriptcffi_gen,
]
env.Append(LIBS=[python_lib, 'util'])
env.Append(LIBPATH='godot/bin/')
env.SharedLibrary('pythonscript', sources)
