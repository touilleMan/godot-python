from __future__ import print_function
import os, glob
from SCons.Errors import UserError


EnsureSConsVersion(2, 3)

vars = Variables('custom.py', ARGUMENTS)
vars.Add(EnumVariable('platform', "Target platform", '', allowed_values=(
    'x11-64',
    'windows-64',
)))
vars.Add('godot_binary', "Path to Godot main binary", '')
vars.Add('debugger', "Run godot with given debugger", '')
vars.Add('gdnative_include_dir', "Path to GDnative include directory", '')
vars.Add('gdnative_wrapper_lib', "Path to GDnative wrapper library", '')
vars.Add(BoolVariable('dev_dyn', "Load at runtime *.inc.py files instead of "
                                 "embedding them (useful for dev)", False))
vars.Add(BoolVariable('compressed_stdlib', "Compress Python std lib as a zip"
                                           "to save space", False))
vars.Add(EnumVariable('backend', "Python interpreter to embed", 'cpython',
         allowed_values=('cpython', 'pypy')))
vars.Add('PYTHON', "Python executable to use for scripts (a virtualenv will be"
                   " created with it in `tools/venv`)", 'python3')
vars.Add("CC", "C compiler")
vars.Add("CFLAGS", "Custom flags for the C compiler")
vars.Add("LINKFLAGS", "Custom flags for the linker")

env = Environment(variables=vars)
Help(vars.GenerateHelpText(env))


if env['godot_binary']:
    env['godot_binary'] = File(env['godot_binary'])
if env['gdnative_include_dir']:
    env['gdnative_include_dir'] = Dir(env['gdnative_include_dir'])
if env['gdnative_wrapper_lib']:
    env['gdnative_wrapper_lib'] = File(env['gdnative_wrapper_lib'])


### Plaform-specific stuff ###


Export('env')
SConscript('platforms/%s/SCsub' % env['platform'])


### Save my eyes plz ###


if 'clang' in env.get('CC'):
    env.Append(CCFLAGS="-fcolor-diagnostics")
if 'gcc' in env.get('CC'):
    env.Append(CCFLAGS="-fdiagnostics-color=always")


### Build venv with CFFI for python scripts ###


venv_dir = Dir('tools/venv')
env.Command(venv_dir, None,
    "${PYTHON} -m virtualenv ${TARGET} && " +
    ". ${TARGET}/bin/activate && " +
    "python -m pip install 'pycparser>=2.18' 'cffi>=1.11.2'")


### Generate cdef and cffi C source ###


cdef_gen = env.Command('pythonscript/cffi_bindings/cdef.gen.h', (venv_dir, env['gdnative_include_dir']),
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

env.Append(CPPPATH=env['gdnative_include_dir'])
env.Append(LIBS=env['gdnative_wrapper_lib'])

env.Append(CFLAGS='-I' + env.Dir('pythonscript').path)
env.Append(CFLAGS='-std=c11')
env.Append(CFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
    '-g -Wformat '
    '-Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 '
    '-Bsymbolic-functions -Wformat -Werror=format-security'.split())

sources = [
    "pythonscript/pythonscript.c",
    pythonscriptcffi_gen,
]
pythonscript, = env.SharedLibrary('%s/pythonscript' % env['build_dir'].path, sources)


### Symbolic link used by test and examples projects ###


env.Clean(pythonscript, env['build_dir'])
def SymLink(target, source, env):
    try:
        os.unlink(str(target[0]))
    except Exception:
        pass
    os.symlink(os.path.abspath(str(source[0])), os.path.abspath(str(target[0])))
install_build_symlink, = env.Command('build/main', env['build_dir'], SymLink)
env.Clean(install_build_symlink, 'build/main')
env.AlwaysBuild(install_build_symlink)

env.Depends(install_build_symlink, pythonscript)

env.Default(install_build_symlink)


### Run tests ###
if env['debugger']:
    test_cmd = "DISPLAY=:0.0 ${debugger} -- ${SOURCE} --path tests/bindings"
else:
    test_cmd = "DISPLAY=:0.0 ${SOURCE} --path tests/bindings"

env.Command('test', [env['godot_binary'], install_build_symlink], test_cmd)
env.AlwaysBuild('test')
env.Alias('tests', 'test')


### Run example ###

env.Command('example', [env['godot_binary'], install_build_symlink],
    "DISPLAY=0.0 ${SOURCE} --path examples/pong"
)
env.AlwaysBuild('example')
