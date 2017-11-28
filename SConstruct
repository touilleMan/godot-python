#!/usr/bin/env python
from __future__ import print_function
import os, glob
from SCons.Errors import UserError


EnsureSConsVersion(2, 3)

vars = Variables('custom.py', ARGUMENTS)
vars.Add(EnumVariable('bits', "Target platform bits", '64', allowed_values=('64', '32')))
vars.Add(BoolVariable('dev_dyn', "Load at runtime *.inc.py files instead of "
                                 "embedding them (useful for dev)", False))
vars.Add('gdnative_include_dir', "Path to GDnative include directory",
         './godot/modules/gdnative/include')
vars.Add('gdnative_wrapper_lib', "Path to GDnative wrapper library",
         './godot/bin/libgdnative_wrapper_code.*.a')
vars.Add(EnumVariable('backend', "Python interpreter to embed", 'cpython',
         allowed_values=('cpython', 'pypy')))
vars.Add('backend_path', "Path to Python interpreter to embed", 'cpython')
vars.Add('PYTHON', "Python executable to use for scripts (a virtualenv will be"
                   " created with it in `tools/venv`)", 'python3')
vars.Add("CC", "C compiler")
vars.Add("CFLAGS", "Custom flags for the C compiler")
vars.Add("LINKFLAGS", "Custom flags for the linker")

env = Environment(variables=vars)
Help(vars.GenerateHelpText(env))


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


try:
    backend_dir = env.Dir(glob.glob(env['backend_path'])[0])
except IndexError:
    raise UserError("Invalid backend_path var `%s`,  must point to "
                    "a Python build directory" % env['backend_path'])


if env['backend'] == 'cpython':
    # Retrieve path&file whose name depends on CPython version number
    orig_libpython_path = '%s/lib/libpython*.so.*' % backend_dir
    try:
        libpython = env.File(glob.glob(orig_libpython_path)[0])
    except IndexError:
        raise UserError("Cannot find `%s`, has CPython been compiled ?" % orig_libpython_path)
    orig_python_include_path = '%s/include/python*/' % backend_dir
    try:
        python_include = env.Dir(glob.glob(orig_python_include_path)[0])
    except IndexError:
        raise UserError("Cannot find `%s`, has CPython been compiled ?" % orig_python_include_path)
    env.Append(CFLAGS='-DBACKEND_CPYTHON')
else:  # pypy
    orig_libpython_path = '%s/bin/libpypy3-c.so' % backend_dir
    try:
        libpython = env.File(glob.glob(orig_libpython_path)[0])
    except IndexError:
        raise UserError("Cannot find `%s`, has Pypy been compiled ?" % orig_libpython_path)
    orig_python_include_path = '%s/include/' % backend_dir
    try:
        python_include = env.Dir(glob.glob(orig_python_include_path)[0])
    except IndexError:
        raise UserError("Cannot find `%s`, has Pypy been compiled ?" % orig_python_include_path)
    env.Append(CFLAGS='-DBACKEND_PYPY')

env.Append(CFLAGS='-I %s' % python_include)


### Build venv with CFFI for python scripts ###


venv_dir = Dir('tools/venv')
env.Command(venv_dir, None,
    "${PYTHON} -m virtualenv ${TARGET} && " +
    ". ${TARGET}/bin/activate && " +
    "python -m pip install pycparser>=2.18 cffi>=1.11.2")


### Generate cdef and cffi C source ###


cdef_gen = env.Command('pythonscript/cffi_bindings/cdef.gen.h', (venv_dir, gdnative_include_dir),
    ". ${SOURCES[0]}/bin/activate && " +
    "python ./tools/generate_gdnative_cffidefs.py ${SOURCES[1]} --output=${TARGET} --bits=${bits}")
env.Append(HEADER=cdef_gen)


if env['dev_dyn']:
    print("\033[0;32mPython .inc.py files are dynamically loaded (dev_dyn=True), don't share the binary !\033[0m\n")
python_inc_srcs = Glob('pythonscript/cffi_bindings/*.inc.py')
(pythonscriptcffi_gen, ) = env.Command(
    'pythonscript/cffi_bindings/pythonscriptcffi.gen.c',
    [venv_dir] + cdef_gen + python_inc_srcs,
    ". ${SOURCES[0]}/bin/activate && " +
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


if env['backend'] == 'cpython':
    # libpythonX.Ym.so.1.0 will be in the same directory as the godot binary,
    # hence we need to inform the binary to look there.
    env.Append(LINKFLAGS=["-Wl,-rpath,'$$ORIGIN/lib'"])
else:  # pypy
    env.Append(LINKFLAGS=["-Wl,-rpath,'$$ORIGIN/bin'"])

sources = [
    "pythonscript/pythonscript.c",
    pythonscriptcffi_gen,
]
# Dunno with, libcpython wants to be provided as `<path>/libcpython.so.xxx`
# and libpypy-c wants `-L<path> -lpypy-c.so.xxx`...
if env['backend'] == 'cpython':
    env.Append(LIBS=[libpython, 'util'])
else:  # pypy
    env.Append(LIBPATH=libpython.dir.path)
    env.Append(LIBS=[libpython.name, 'util'])
pythonscript, = env.SharedLibrary('pythonscript', sources)
env.Default(pythonscript)


### Generate build dir ###


build_dir_name = 'build-%s' % env['backend']
if env['dev_dyn']:
    build_dir_name += '-dev_dyn'
build_dir_name += '-linux%s' % env['bits']

env.Install(build_dir_name, pythonscript)
if env['backend'] == 'cpython':
    env.Install(build_dir_name, '%s/include' % backend_dir)
    env.Install(build_dir_name, '%s/lib' % backend_dir)
    # CPython standard library can be compressed to save *a lot* of space
else:  # pypy
    env.Install(build_dir_name, '%s/include' % backend_dir)
    env.Install(build_dir_name, '%s/lib' % backend_dir)
    env.Install(build_dir_name, '%s/lib_pypy' % backend_dir)
    env.Install(build_dir_name, '%s/lib-python' % backend_dir)
    env.Install('%s/lib' % build_dir_name, '%s/bin/libpypy3-c.so' % backend_dir)
env.Alias('build', build_dir_name)


env.Alias('install-build-symlink',
          env.Command('build-main', build_dir_name, "ln -s ${SOURCE} ${TARGET}"))
