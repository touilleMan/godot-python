#!/usr/bin/env python

import os, glob
from SCons.Errors import UserError


EnsureSConsVersion(2, 4)
env = Environment(**os.environ)


if 'GODOT' not in ARGUMENTS:
    raise UserError('GODOT var must point to main Godot source path')
env.Append(CFLAGS='-I' + env.Dir(ARGUMENTS['GODOT']).path)


python_backend = ARGUMENTS.get('PYTHONSCRIPT_BACKEND', 'cpython').lower()
if python_backend not in ('cpython', 'pypy'):
    raise UserError('PYTHONSCRIPT_BACKEND should be `cpython` (default) or `pypy`')

if 'clang' in env.get('CC'):
    env.Append(CCFLAGS="-fcolor-diagnostics -fcolor-diagnostics")
env.Append(CFLAGS='-I' + env.Dir('pythonscript').path)


if python_backend == 'cpython':
    try:
        python_lib = env.File(glob.glob('pythonscript/cpython/libpython*.so.*')[0])
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/cpython/libpython*.so.*`, has CPython been compiled ?" % os.getcwd())
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/cpython/').path)
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/cpython/Include').path)
    env.Append(CFLAGS='-DBACKEND_CPYTHON')
else:  # pypy
    try:
        python_lib = env.File(glob.glob('pythonscript/pypy/bin/libpypy3-c.so')[0])
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/pypy/bin/libpypy3-c.so`." % os.getcwd())
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/pypy/include').path)
    env.Append(CFLAGS='-DBACKEND_PYPY')

env.Append(CFLAGS='-std=c11')
env.Append(CFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
    '-g -Wformat '
    '-Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 '
    '-Bsymbolic-functions -Wformat -Werror=format-security'.split())


# libpythonX.Ym.so.1.0 will be in the same directory as the godot binary,
# hence we need to inform the binary to look there.
env.Append(LINKFLAGS=["-Wl,-rpath,'$$ORIGIN'"])


sources = [
    "pythonscript/cffi_bindings/pythonscriptcffi.gen.c",
    "pythonscript/pythonscript.c"
]
env.Append(LIBS=[python_lib, 'util'])
env.SharedLibrary('pythonscript', sources)
