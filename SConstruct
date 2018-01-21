from __future__ import print_function
import os, shutil
from datetime import datetime
from functools import partial
from SCons.Errors import UserError


EnsureSConsVersion(2, 3)


def SymLink(target, source, env):
    """
    Scons doesn't provide cross-platform symlink out of the box
    """
    try:
        os.unlink(str(target[0]))
    except Exception:
        pass
    os.symlink(os.path.abspath(str(source[0])), os.path.abspath(str(target[0])))


vars = Variables('custom.py', ARGUMENTS)
vars.Add(EnumVariable('platform', "Target platform", '', allowed_values=(
    'x11-64',
    'x11-32',
    'windows-64',
    'windows-32',
)))
vars.Add(BoolVariable('show_build_dir', "Display build dir and leave", False))
vars.Add('release_suffix', "Suffix to add to the release archive", 'wip')
vars.Add('godot_binary', "Path to Godot main binary", '')
vars.Add('debugger', "Run godot with given debugger", '')
vars.Add('gdnative_include_dir', "Path to GDnative include directory", '')
vars.Add('gdnative_wrapper_lib', "Path to GDnative wrapper library", '')
vars.Add('godot_release_base_url', 'URL to the godot builder release to use',
         'https://github.com/GodotBuilder/godot-builds/releases/download/master_20180119-1')
vars.Add(BoolVariable('dev_dyn', "Load at runtime *.inc.py files instead of "
                                 "embedding them (useful for dev)", False))
vars.Add(BoolVariable('compressed_stdlib', "Compress Python std lib as a zip"
                                           "to save space", False))
vars.Add(EnumVariable('backend', "Python interpreter to embed", 'cpython',
         allowed_values=('cpython', 'pypy')))
vars.Add('gdnative_parse_cpp', "Preprocessor to use for parsing GDnative includes", 'cpp')
vars.Add('PYTHON', "Python executable to use for scripts (a virtualenv will be"
                   " created with it in `tools/venv`)", 'python3')
vars.Add("CC", "C compiler")
vars.Add("CFLAGS", "Custom flags for the C compiler")
vars.Add("LINK", "linker")
vars.Add("LINKFLAGS", "Custom flags for the linker")

env = Environment(ENV=os.environ, variables=vars, MSVC_USE_SCRIPT=False)
# env.AppendENVPath('PATH', os.getenv('PATH'))
# env.Append('DISPLAY', os.getenv('DISPLAY'))
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



### Disply build dir (useful for CI) ###


if env['show_build_dir']:
    print(env['build_dir'])
    raise SystemExit()


### Save my eyes plz ###


if 'clang' in env.get('CC'):
    env.Append(CCFLAGS="-fcolor-diagnostics")
if 'gcc' in env.get('CC'):
    env.Append(CCFLAGS="-fdiagnostics-color=always")


### Build venv with CFFI for python scripts ###


venv_dir = Dir('tools/venv')


def _create_env_python_command(env, init_venv):
    def _python_command(targets, sources, command, pre_init=None):
        commands = [pre_init, init_venv, command]
        return env.Command(targets, sources, ' && '.join([x for x in commands if x]))
    env.PythonCommand = _python_command


if os.name == 'nt':
    _create_env_python_command(env, "%s\\Scripts\\activate.bat" % venv_dir.path)
else:
    _create_env_python_command(env, ". %s/bin/activate" % venv_dir.path)


env.PythonCommand(
    targets=venv_dir,
    sources=None,
    pre_init='${PYTHON} -m virtualenv ${TARGET}',
    command='${PYTHON} -m pip install "pycparser>=2.18" "cffi>=1.11.2"',
)


### Generate cdef and cffi C source ###


cdef_gen = env.PythonCommand(
    targets='pythonscript/cdef.gen.h',
    sources=(venv_dir, env['gdnative_include_dir']),
    command=('python ./tools/generate_gdnative_cffidefs.py ${SOURCES[1]} '
             '--output=${TARGET} --bits=${bits} --cpp="${gdnative_parse_cpp}"')
)
env.Append(HEADER=cdef_gen)


if env['dev_dyn']:
    print("\033[0;32mPython .inc.py files are dynamically loaded (dev_dyn=True), don't share the binary !\033[0m\n")


python_embedded_srcs = env.Glob('pythonscript/embedded/*.inc.py')


(cffi_bindings_gen, ) = env.PythonCommand(
    targets='pythonscript/cffi_bindings.gen.c',
    sources=[venv_dir] + cdef_gen + python_embedded_srcs,
    command=('python ./pythonscript/generate_cffi_bindings.py '
             '--cdef=${SOURCES[1]} --output=${TARGET}' +
             (" --dev-dyn" if env['dev_dyn'] else ""))
)


### Main compilation stuff ###

env.Alias('backend', env['backend_dir'])

env.Append(CPPPATH=env['gdnative_include_dir'])
env.Append(LIBS=env['gdnative_wrapper_lib'])

env.Append(CFLAGS='-I' + env.Dir('pythonscript').path)
# env.Append(CFLAGS='-std=c11')
# env.Append(CFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
#     '-g -Wdate-time -D_FORTIFY_SOURCE=2 '
#     '-Bsymbolic-functions -Wformat -Werror=format-security'.split())

sources = [
    "pythonscript/pythonscript.c",
    cffi_bindings_gen,
]
libpythonscript = env.SharedLibrary('pythonscript/pythonscript', sources)[0]


### Generate build dir ###


def extract_version():
    with open('pythonscript/embedded/godot/__init__.py') as fd:
        versionline = next(l for l in fd.readlines() if l.startswith('__version__ = '))
        return eval(versionline[14:])


def generate_build_dir_hook(path):
    shutil.copy('extras/pythonscript.gdnlib', os.path.join(path, 'pythonscript.gdnlib'))
    shutil.copy('extras/release_LICENSE.txt', os.path.join(path, 'LICENSE.txt'))
    with open('extras/release_README.txt') as fd:
        readme = fd.read().format(
            version=extract_version(),
            date=datetime.utcnow().strftime('%Y-%m-%d')
        )
    with open(os.path.join(path, 'README.txt'), 'w') as fd:
        fd.write(readme)

env['generate_build_dir_hook'] = generate_build_dir_hook


def do_or_die(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise UserError('ERROR: %s' % exc)

python_godot_module_srcs = env.Glob('pythonscript/embedded/**/*.py')
env.Command(
    env['build_dir'],
    [env['backend_dir'], libpythonscript, Dir('#pythonscript/embedded/godot')] + python_godot_module_srcs,
    partial(do_or_die, env['generate_build_dir'])
)
env.Clean(env['build_dir'], env['build_dir'].path)


### Symbolic link used by test and examples projects ###


install_build_symlink, = env.Command('build/main', env['build_dir'], SymLink)
env.Clean(install_build_symlink, 'build/main')
env.AlwaysBuild(install_build_symlink)

env.Default(install_build_symlink)


### Run tests ###


if env['debugger']:
    test_cmd = "${debugger} -- ${SOURCE} --path tests/bindings"
else:
    test_cmd = "${SOURCE} --path tests/bindings"


env.Command('test', [env['godot_binary'], install_build_symlink], test_cmd)
env.AlwaysBuild('test')
env.Alias('tests', 'test')


### Run example ###


env.Command('example', [env['godot_binary'], install_build_symlink],
    "${SOURCE} --path examples/pong"
)
env.AlwaysBuild('example')


### Release (because I'm scare to do that with windows cmd on appveyor...) ###

def generate_release(target, source, env):
    base_name, format = target[0].abspath.rsplit('.', 1)
    shutil.make_archive(
        base_name,
        format,
        base_dir='pythonscript',
        root_dir=source[0].abspath
    )

release = env.Command(
    '#godot-python-${release_suffix}-${platform}-${backend}.zip',
    env['build_dir'],
    generate_release
)
env.Alias('release', release)
env.AlwaysBuild('release')
