#!/usr/bin/env python

import os, glob
from SCons.Errors import UserError


EnsureSConsVersion(2, 4)
env = Environment(**os.environ)


# if 'GODOT' not in ARGUMENTS:
#     print('GODOT argument not provided, assuming `./godot`')
#     ARGUMENTS['GODOT'] = './godot'
# godot_path = ARGUMENTS['GODOT']
# if not os.path.exists(godot_path):
#     raise UserError('Invalid GODOT var (%s),  must point to main Godot source path' %
#         godot_path)


if 'GDNATIVE_INCLUDE' not in ARGUMENTS:
    print('GDNATIVE_INCLUDE argument not provided, assuming `./godot/modules/gdnative/include`')
    ARGUMENTS['GDNATIVE_INCLUDE'] = './godot/modules/gdnative/include'
gdnative_include = ARGUMENTS['GDNATIVE_INCLUDE']
if not os.path.exists(gdnative_include):
    raise UserError("Invalid GDNATIVE_INCLUDE var (%s),  must point to Godot's GDnative include directory" %
                    gdnative_include)


env.Append(CPPPATH=[gdnative_include])


if 'BUILD' not in ARGUMENTS:
    print('BUILD argument not provided, assuming `./build`')
    ARGUMENTS['BUILD'] = './build'
build_path = ARGUMENTS['BUILD']


env.Append(CPPPATH=env.Dir(gdnative_include).path)
# env.Append(CFLAGS='-I' + env.Dir(godot_path).path)
# The fuck dude ?
# env.Append(CFLAGS='-I%s/modules/gdnative' % env.Dir(godot_path).path)


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
    Command('libpypy-c.so', python_lib, Copy("$TARGET", "$SOURCE"))
    python_lib = env.File('libpypy-c.so')
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
    # "pythonscript/gdnative_wrappers.gen.c",
    "pythonscript/cffi_bindings/pythonscriptcffi.gen.c",
    "pythonscript/pythonscript.c"
]
env.Append(LIBS=[python_lib, 'util', 'libgdnative_wrapper_code.x11.tools.64.a'])
env.Append(LIBPATH='godot/bin/')
env.SharedLibrary('pythonscript', sources)
