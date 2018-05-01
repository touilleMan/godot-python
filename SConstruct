from __future__ import print_function
import re
import os
import shutil
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
    try:
        os.symlink(os.path.abspath(str(source[0])), os.path.abspath(str(target[0])))
    except Exception as e:
        raise UserError(
            "Can't create symlink (%s -> %s): %s"
            % (str(source[0]), os.path.abspath(str(target[0])), e)
        )


def script_converter(str, env):
    """Allowed values are True, False, and a script path"""
    if str in ("False", "false", "0"):
        return False

    if str in ("True", "true", "1"):
        return True

    return str


vars = Variables("custom.py", ARGUMENTS)
vars.Add(
    EnumVariable(
        "platform",
        "Target platform",
        "",
        allowed_values=("x11-64", "x11-32", "windows-64", "windows-32", "osx-64"),
    )
)
vars.Add(BoolVariable("show_build_dir", "Display build dir and leave", False))
vars.Add("release_suffix", "Suffix to add to the release archive", "wip")
vars.Add("godot_binary", "Path to Godot main binary", "")
vars.Add("debugger", "Run godot with given debugger", "")
vars.Add("gdnative_include_dir", "Path to GDnative include directory", "")
vars.Add("gdnative_wrapper_lib", "Path to GDnative wrapper library", "")
vars.Add(
    "godot_release_base_url",
    "URL to the godot builder release to use",
    "https://github.com/GodotBuilder/godot-builds/releases/download/3.0_20180303-1",
)
vars.Add(
    BoolVariable(
        "dev_dyn",
        "Load at runtime *.inc.py files instead of " "embedding them (useful for dev)",
        False,
    )
)
vars.Add(
    BoolVariable(
        "compressed_stdlib", "Compress Python std lib as a zip" "to save space", False
    )
)
vars.Add(
    EnumVariable(
        "backend",
        "Python interpreter to embed",
        "cpython",
        allowed_values=("cpython", "pypy"),
    )
)
vars.Add(
    "gdnative_parse_cpp", "Preprocessor to use for parsing GDnative includes", "cpp"
)
vars.Add(
    "PYTHON",
    "Python executable to use for scripts (a virtualenv will be"
    " created with it in `tools/venv`)",
    "python3",
)
vars.Add("CC", "C compiler")
vars.Add("CFLAGS", "Custom flags for the C compiler")
vars.Add("LINK", "linker")
vars.Add("LINKFLAGS", "Custom flags for the linker")
vars.Add(
    "TARGET_ARCH",
    "Target architecture (Windows only) -- x86, x86_64, ia64. Default: host arch.",
)
vars.Add(
    "MSVC_VERSION",
    "MSVC version to use (Windows only) -- version num X.Y. Default: highest installed.",
)
vars.Add(
    "MSVC_USE_SCRIPT",
    "Set to True to let SCons find compiler (with MSVC_VERSION and TARGET_ARCH), "
    "False to use cmd.exe env (MSVC_VERSION and TARGET_ARCH will be ignored), "
    "or vcvarsXY.bat script name to use.",
    default=False,
    converter=script_converter,
)

env = Environment(ENV=os.environ, variables=vars)
# env.AppendENVPath('PATH', os.getenv('PATH'))
# env.Append('DISPLAY', os.getenv('DISPLAY'))
Help(vars.GenerateHelpText(env))


if env["godot_binary"]:
    env["godot_binary"] = File(env["godot_binary"])
if env["gdnative_include_dir"]:
    env["gdnative_include_dir"] = Dir(env["gdnative_include_dir"])
if env["gdnative_wrapper_lib"]:
    env["gdnative_wrapper_lib"] = File(env["gdnative_wrapper_lib"])

env["build_name"] = '%s-%s' % (env['platform'], env["backend"])
env["build_dir"] = Dir("#build/%s" % env["build_name"])


### Plaform-specific stuff ###


Export("env")
SConscript("platforms/%s/SCsub" % env["platform"])


### Disply build dir (useful for CI) ###


if env["show_build_dir"]:
    print(env["build_dir"])
    raise SystemExit()


### Save my eyes plz ###


if "clang" in env.get("CC"):
    env.Append(CCFLAGS="-fcolor-diagnostics")
if "gcc" in env.get("CC"):
    env.Append(CCFLAGS="-fdiagnostics-color=always")


### Build venv with CFFI for python scripts ###


venv_dir = Dir("tools/venv")


def _create_env_python_command(env, init_venv):

    def _python_command(targets, sources, command, pre_init=None):
        commands = [pre_init, init_venv, command]
        return env.Command(targets, sources, " && ".join([x for x in commands if x]))

    env.PythonCommand = _python_command


if os.name == "nt":
    _create_env_python_command(env, "%s\\Scripts\\activate.bat" % venv_dir.path)
else:
    _create_env_python_command(env, ". %s/bin/activate" % venv_dir.path)


env.PythonCommand(
    targets=venv_dir,
    sources=None,
    pre_init="${PYTHON} -m virtualenv ${TARGET}",
    command='${PYTHON} -m pip install "pycparser>=2.18" "cffi>=1.11.2"',
)


### Generate cdef and cffi C source ###


cdef_gen = env.PythonCommand(
    targets="pythonscript/cdef.gen.h",
    sources=(venv_dir, "$gdnative_include_dir"),
    command=(
        "python ./tools/generate_gdnative_cffidefs.py ${SOURCES[1]} "
        '--output=${TARGET} --bits=${bits} --cpp="${gdnative_parse_cpp}"'
    ),
)
env.Append(HEADER=cdef_gen)


if env["dev_dyn"]:
    print(
        "\033[0;32mPython .inc.py files are dynamically loaded (dev_dyn=True), don't share the binary !\033[0m\n"
    )


python_embedded_srcs = env.Glob("pythonscript/embedded/*.inc.py")


(cffi_bindings_gen,) = env.PythonCommand(
    targets="pythonscript/cffi_bindings.gen.c",
    sources=[venv_dir] + cdef_gen + python_embedded_srcs,
    command=(
        "python ./pythonscript/generate_cffi_bindings.py "
        "--cdef=${SOURCES[1]} --output=${TARGET}"
        + (" --dev-dyn" if env["dev_dyn"] else "")
    ),
)


### Main compilation stuff ###


env.Alias("backend", "$backend_dir")

env.AppendUnique(CPPPATH=["#", "$gdnative_include_dir"])
env.Append(LIBS=env["gdnative_wrapper_lib"])

# env.Append(CFLAGS='-std=c11')
# env.Append(CFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
#     '-g -Wdate-time -D_FORTIFY_SOURCE=2 '
#     '-Bsymbolic-functions -Wformat -Werror=format-security'.split())

sources = ["pythonscript/pythonscript.c", cffi_bindings_gen]
libpythonscript = env.SharedLibrary("pythonscript/pythonscript", sources)[0]


### Generate build dir ###


def extract_version():
    with open("pythonscript/embedded/godot/__init__.py") as fd:
        versionline = next(l for l in fd.readlines() if l.startswith("__version__ = "))
        return eval(versionline[14:])


def generate_build_dir_hook(path):
    with open("misc/single_build_pythonscript.gdnlib") as fd:
        gdnlib = fd.read().replace(env['build_name'], '')
        # Single platform vs multi-platform one have not the same layout
        gdnlib = re.sub(r'(res://pythonscript/)(x11|windows|osx)-(64|32)-(cpython|pypy)/', r'\1', gdnlib)
    with open(os.path.join(path, "pythonscript.gdnlib"), "w") as fd:
        fd.write(gdnlib)

    shutil.copy("misc/release_LICENSE.txt", os.path.join(path, "LICENSE.txt"))

    with open("misc/release_README.txt") as fd:
        readme = fd.read().format(
            version=extract_version(), date=datetime.utcnow().strftime("%Y-%m-%d")
        )
    with open(os.path.join(path, "README.txt"), "w") as fd:
        fd.write(readme)


env["generate_build_dir_hook"] = generate_build_dir_hook


def do_or_die(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)

    except Exception as exc:
        import traceback

        traceback.print_exc()
        raise UserError("ERROR: %s" % exc)


python_godot_module_srcs = env.Glob("pythonscript/embedded/**/*.py")
env.Command(
    "$build_dir",
    ["$backend_dir", libpythonscript, Dir("#pythonscript/embedded/godot")]
    + python_godot_module_srcs,
    Action(
        partial(do_or_die, env["generate_build_dir"]),
        "Generating build dir $TARGET from $SOURCES",
    ),
)
env.Clean("$build_dir", env["build_dir"].path)


### Symbolic link used by test and examples projects ###


install_build_symlink, = env.Command(
    "build/main", "$build_dir", Action(SymLink, "Symlinking $SOURCE -> $TARGET")
)
env.Clean(install_build_symlink, "build/main")
env.AlwaysBuild(install_build_symlink)

env.Default(install_build_symlink)


### Download godot binary ###


godot_binary, = env.Command(
    "build/godot", "$godot_binary", Action(SymLink, "Symlinking $SOURCE -> $TARGET")
)
env.Alias("godot_binary", godot_binary)


### Run tests ###


# Note: passing absolute path is only really needed on Mac with Godot.app
if env["debugger"]:
    test_base_cmd = "${debugger} -- ${SOURCE} --path ${Dir('#').abspath}/tests/"
else:
    test_base_cmd = "${SOURCE} --path ${Dir('#').abspath}/tests/"


env.Command(
    "tests/bindings",
    ["$godot_binary", install_build_symlink],
    test_base_cmd + "bindings",
)
env.AlwaysBuild("tests/bindings")
env.Command(
    "tests/work_with_gdscript",
    ["$godot_binary", install_build_symlink],
    test_base_cmd + "work_with_gdscript",
)
env.AlwaysBuild("tests/work_with_gdscript")
env.AlwaysBuild("tests")
env.Alias("test", "tests")


### Run example ###


env.Command(
    "example",
    ["$godot_binary", install_build_symlink],
    "${SOURCE} --path ${Dir('#').abspath}/examples/pong",
)
env.AlwaysBuild("example")


### Release (because I'm scare to do that with windows cmd on appveyor...) ###


def generate_release(target, source, env):
    base_name, format = target[0].abspath.rsplit(".", 1)
    shutil.make_archive(
        base_name, format, root_dir=source[0].abspath
    )


release = env.Command(
    "#godot-python-${release_suffix}-${platform}-${backend}.zip",
    "$build_dir",
    generate_release,
)
env.Alias("release", release)
env.AlwaysBuild("release")


### Auto-format codebase ###


black_cmd = "pip install -U black && black pythonscript tools/*.py tests/*/*.py SConstruct platforms/*/SCsub"
autoformat = env.PythonCommand("autoformat", [venv_dir], black_cmd)
env.Alias("black", autoformat)
env.PythonCommand("checkstyle", [venv_dir], black_cmd + " --check")
