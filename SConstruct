#!/usr/bin/env python

import os, glob
from SCons.Errors import UserError


EnsureSConsVersion(2, 4)
env = Environment(**os.environ)


if 'GODOT' not in ARGUMENTS:
    raise UserError('GODOT var must point to main Godot source path')
env.Append(CXXFLAGS='-I' + env.Dir(ARGUMENTS['GODOT']).path)


python_backend = ARGUMENTS.get('PYTHONSCRIPT_BACKEND', 'cpython').lower()
if python_backend not in ('cpython', 'pypy'):
    raise UserError('PYTHONSCRIPT_BACKEND should be `cpython` (default) or `pypy`')


env.Append(CXXFLAGS='-I' + env.Dir('pythonscript').path)


if python_backend == 'cpython':
    try:
        python_lib = env.File(glob.glob('pythonscript/cpython/libpython*.so.*')[0])
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/cpython/libpython*.so.*`, has CPython been compiled ?" % os.getcwd())
    env.Append(CXXFLAGS='-I ' + env.Dir('pythonscript/cpython/').path)
    env.Append(CXXFLAGS='-I ' + env.Dir('pythonscript/cpython/Include').path)
    env.Append(CXXFLAGS='-DBACKEND_CPYTHON')
else:  # pypy
    try:
        python_lib = env.File(glob.glob('pythonscript/pypy/bin/libpypy3-c.so')[0])
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/pypy/bin/libpypy3-c.so`." % os.getcwd())
    env.Append(CXXFLAGS='-I ' + env.Dir('pythonscript/pypy/include').path)
    env.Append(CXXFLAGS='-DBACKEND_PYPY')

env.Append(CXXFLAGS='-std=c++11')
env.Append(CXXFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
    '-g -Wformat '
    '-Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 '
    '-Bsymbolic-functions -Wformat -Werror=format-security'.split())


# libpythonX.Ym.so.1.0 will be in the same directory as the godot binary,
# hence we need to inform the binary to look there.
env.Append(LINKFLAGS=["-Wl,-rpath,'$$ORIGIN'"])


sources = [
    "pythonscript/cffi_bindings/pythonscriptcffi.gen.cpp",
    # "register_types.cpp",
    # "py_language.cpp",
    # "py_editor.cpp",
    # "py_debug.cpp",
    # "py_script.cpp",
    # "py_instance.cpp",
    # "py_loader.cpp"
]
env.Append(LIBS=[python_lib, 'util'])
env.SharedLibrary('pythonscript', sources)
