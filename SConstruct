#!/usr/bin/env python
from __future__ import print_function
import os, glob
from SCons.Errors import UserError

from tools.generate_gdnative_cffidefs import generate_cdef


EnsureSConsVersion(2, 4)

vars = Variables('custom.py', ARGUMENTS)
vars.Add(EnumVariable('bits', "Target platform bits", '64', allowed_values=('64', '32')))
vars.Add(BoolVariable('dev_dyn', "Load at runtime *.inc.py files instead of "
                                 "embedding them (useful for dev)", False))
vars.Add('gdnative_include_dir', "Path to GDnative include directory",
         './godot/modules/gdnative/include')
vars.Add('gdnative_wrapper_lib', "Path to GDnative wrapper library",
         './godot/bin/libgdnative_wrapper_code.*.a')
vars.Add(EnumVariable('backend', "Python interpreter", 'cpython', allowed_values=('cpython', 'pypy')))
vars.Add('PYTHON', "Python executable to use for scripts (a virtualenv will be"
                   " created with it in `tools/venv`)", 'python3')
vars.Add("CC", "C compiler")
vars.Add("CFLAGS", "Custom flags for the C compiler")
vars.Add("LINKFLAGS", "Custom flags for the linker")

env = Environment(variables=vars)
Help(vars.GenerateHelpText(env))


### Build dir ###


build_dir_name = 'build-%s' % env['backend']
if env['dev_dyn']:
    build_dir_name += '-dev_dyn'
build_dir_name += '-%s' % env['bits']
build_dir = Dir(build_dir_name)


### Save my eyes plz ###


if 'clang' in env.get('CC'):
    env.Append(CCFLAGS="-fcolor-diagnostics")
if 'gcc' in env.get('CC'):
    env.Append(CCFLAGS="-fdiagnostics-color=always")


### GDnative include/wrapper ###


try:
    gdnative_include_dir = env.Dir(glob.glob(env['gdnative_include_dir'])[0])
except IndexError:
    raise UserError("Invalid gdnative_include_dir var `%s`,  must point to "
                    "Godot's GDnative include directory" % env['gdnative_include_dir'])
try:
    gdnative_wrapper_lib = env.File(glob.glob(env['gdnative_wrapper_lib'])[0])
except IndexError:
    raise UserError("Invalid gdnative_wrapper_lib var `%s`,  must point to"
                    " Godot's GDnative wrapper static lib" % env['gdnative_wrapper_lib'])

env.Append(CPPPATH=gdnative_include_dir)
env.Append(LIBS=gdnative_wrapper_lib)


### Python backend ###


if env['backend'] == 'cpython':
    try:
        python_lib = env.File(glob.glob('pythonscript/cpython/libpython*.so.*')[0])
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/cpython/libpython*.so.*`, has CPython been compiled ?" % os.getcwd())
    python_lib = env.Command('%s/libpython.so' % build_dir, python_lib, Copy("$TARGET", "$SOURCE"))
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/cpython/').path)
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/cpython/Include').path)
    env.Append(CFLAGS='-DBACKEND_CPYTHON')
else:  # pypy
    try:
        python_lib = env.File('pythonscript/pypy/bin/libpypy3-c.so')
    except IndexError:
        raise UserError("Cannot find `%s/pythonscript/pypy/bin/libpypy3-c.so`." % os.getcwd())
    ptyhon_lib = env.Command('%s/libpypy-c.so' % build_dir, python_lib, Copy("$TARGET", "$SOURCE"))
    env.Append(CFLAGS='-I ' + env.Dir('pythonscript/pypy/include').path)
    env.Append(CFLAGS='-DBACKEND_PYPY')


### Build venv with CFFI for python scripts ###


venv_dir = Dir('tools/venv')
env.Command(venv_dir, None, "${PYTHON} -m virtualenv ${TARGET} && . ${TARGET}/bin/activate && python -m pip install cffi")


### Generate cdef and cffi C source ###


cdef_gen = env.Command('pythonscript/cffi_bindings/cdef.gen.h', (venv_dir, gdnative_include_dir),
    ". ${SOURCES[0]}/bin/activate &&" +
    " python ./tools/generate_gdnative_cffidefs.py ${SOURCES[1]} --output=${TARGET} --bits=${bits}")
env.Append(HEADER=cdef_gen)


if env['dev_dyn']:
    print("\033[0;32mPython .inc.py files are dynamically loaded (dev_dyn=True), don't share the binary !\033[0m\n")
python_inc_srcs = Glob('pythonscript/cffi_bindings/*.inc.py')
(pythonscriptcffi_gen, ) = env.Command(
    'pythonscript/cffi_bindings/pythonscriptcffi.gen.c',
    [venv_dir] + cdef_gen + python_inc_srcs,
    ". ${SOURCES[0]}/bin/activate &&" +
    "python ./pythonscript/cffi_bindings/generate.py --cdef=${SOURCES[1]} --output=${TARGET}" +
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
env.SharedLibrary('%s/pythonscript' % build_dir, sources)


### Generate build dir ###
