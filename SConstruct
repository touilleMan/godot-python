from __future__ import print_function
import re
import os
import shutil
import glob
from datetime import datetime
from functools import partial
from SCons.Errors import UserError


EnsureSConsVersion(3, 0)


def script_converter(val, env):
    """Allowed values are True, False, and a script path"""
    if val in ("False", "false", "0"):
        return False

    if val in ("True", "true", "1"):
        return True

    return val


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
vars.Add(
    "godot_release_base_url",
    "URL to the godot builder release to use",
    "https://github.com/GodotBuilder/godot-builds/releases/download/3.0_20180303-1",
)
vars.Add(
    BoolVariable(
        "dev_dyn",
        "Load at runtime *.inc.py files instead of embedding them (useful for dev)",
        False,
    )
)
vars.Add(
    BoolVariable(
        "sample", "Generate only a subset of the bindings (faster build time)", False
    )
)
vars.Add(
    BoolVariable(
        "compressed_stdlib", "Compress Python std lib as a zip to save space", False
    )
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
vars.Add(
    BoolVariable(
        "symlink_cp_fallback",
        "Symlink are poorly supported on Windows, fallback to copy instead",
        False,
    )
)


env = Environment(ENV=os.environ, variables=vars)
# env.AppendENVPath('PATH', os.getenv('PATH'))
# env.Append('DISPLAY', os.getenv('DISPLAY'))
Help(vars.GenerateHelpText(env))


env["shitty_compiler"] = env.get("CC") in ("cl", "cl.exe")


def compiler_opts(opts, msvc=None):
    cooked = []
    for opt in opts.split():
        opt = opt.strip()
        if env.get("CC") in ("cl", "cl.exe") and opt.startswith("-"):
            cooked.append(msvc or f"/{opt[1:]}")
        else:
            cooked.append(opt)
    return " ".join(cooked)


def SymLink(target, source, env):
    """
    Scons doesn't provide cross-platform symlink out of the box
    """
    abs_src = os.path.abspath(str(source[0]))
    abs_trg = os.path.abspath(str(target[0]))
    if env["symlink_cp_fallback"]:
        try:
            if os.path.isdir(abs_trg):
                shutil.rmtree(abs_trg)
            else:
                os.unlink(abs_trg)
        except Exception:
            pass
        try:
            if os.path.isdir(abs_src):
                shutil.copytree(abs_src, abs_trg)
            else:
                shutil.copy(abs_src, abs_trg)
        except Exception as e:
            raise UserError(
                f"Can't do copy as symlink fallback ({abs_src} -> {abs_trg}): {e}"
            )

    else:
        try:
            os.unlink(abs_trg)
        except Exception:
            pass
        try:
            os.symlink(abs_src, abs_trg)
        except Exception as e:
            raise UserError(f"Can't create symlink ({abs_src} -> {abs_trg}): {e}")


env.Append(BUILDERS={"SymLink": SymLink})


def Glob(env, pattern):
    """
    Scons Glob is rather limited
    """
    return [File(x) for x in glob.glob(pattern, recursive=True)]


env.AddMethod(Glob, "Glob")


if env["dev_dyn"]:
    print(
        "\033[0;32mBuild with a symlink on `pythonsript/godot` module"
        " (dev_dyn=True), don't share the binary !\033[0m\n"
    )


if env["godot_binary"]:
    env["godot_binary"] = File(env["godot_binary"])
if env["gdnative_include_dir"]:
    env["gdnative_include_dir"] = Dir(env["gdnative_include_dir"])
else:
    env["gdnative_include_dir"] = Dir("godot_headers")

env["build_name"] = f"pythonscript-{env['platform']}"
env["build_dir"] = Dir(f"#build/{env['build_name']}")


### Plaform-specific stuff ###


Export("env")
SConscript(f"platforms/{env['platform']}/SCsub")


### Display build dir (useful for CI) ###


if env["show_build_dir"]:
    print(env["build_dir"])
    raise SystemExit()


### Save my eyes plz ###

env["ENV"]["TERM"] = os.environ.get("TERM", "")
if "clang" in env.get("CC"):
    env.Append(CCFLAGS="-fcolor-diagnostics")
if "gcc" in env.get("CC"):
    env.Append(CCFLAGS="-fdiagnostics-color=always")


### Setup Cython builder ###


def _append_html_target(target, source, env):
    def _html(file):
        no_suffix = file.get_path().rsplit(".")[0]
        return f"{no_suffix}.html"

    return target + [_html(x) for x in target if x.get_suffix() == ".c"], source


env.Append(
    BUILDERS={
        "CythonToC": Builder(
            action="cython --fast-fail -3 $SOURCE",
            suffix=".c",
            src_suffix=".pyx",
            # emitter = _append_html_target
        )
    }
)


def cython_compile(env, source):
    def _strip_extension(item):
        for extension in (".gen.c", ".c"):
            if item.endswith(extension):
                return item[: -len(extension)]

    libs = [_strip_extension(x.abspath) for x in source]
    return env.SharedLibrary(libs, source, LIBPREFIX="")


def cythonizer(env, source):
    c_source = env.CythonToC(source)
    return cython_compile(env, c_source)


env.AddMethod(cython_compile, "CythonCompile")
env.AddMethod(cythonizer, "Cython")


### Default C flags ###


env.AppendUnique(CPPPATH=["#", "$gdnative_include_dir"])

# TODO: choose right flag
if not env["shitty_compiler"]:
    env.Append(CFLAGS="-std=c11")
    env.Append(CFLAGS="-Werror -Wall")
else:
    env.Append(CFLAGS="/WX /W2")

# env.Append(CFLAGS='-pthread -DDEBUG=1 -fwrapv -Wall '
#     '-g -Wdate-time -D_FORTIFY_SOURCE=2 '
#     '-Bsymbolic-functions -Wformat -Werror=format-security'.split())


### Generate godot api .h -> gdnative_api_struct.pxd ###


gdnative_api_struct_pxd = File("pythonscript/godot/gdnative_api_struct.pxd")
# TODO: autopxd doesn't work out of the box, hence
# `gdnative_api_struct.pxd` has been customized after generation
generate_gdnative_api_struct = env.Command(
    # target="pythonscript/godot/gdnative_api_struct.pxd",
    target="__dummy__",  # Avoid this rule to be triggered by a dependency
    source=(
        env["gdnative_include_dir"],
        "%s/gdnative_api_struct.gen.h" % env["gdnative_include_dir"],
    ),
    action=("autopxd -I ${SOURCES[0]} ${SOURCES[1]} > ${TARGET}"),
)
env.Alias("generate_gdnative_api_struct", generate_gdnative_api_struct)
env.AlwaysBuild("generate_gdnative_api_struct")


### Generate pythonscript/godot/bindings.pyx ###

sample_opt = "--sample" if env["sample"] else ""
godot_bindings_pyx, godot_bindings_pxd = env.Command(
    target=("pythonscript/godot/bindings.pyx", "pythonscript/godot/bindings.pxd"),
    source=("%s/api.json" % env["gdnative_include_dir"],),
    action=(
        "python tools/generate_bindings.py  -i ${SOURCES} -o ${TARGET} " + sample_opt
    ),
)
env.Depends(
    godot_bindings_pyx,
    ["tools/generate_bindings.py", env.Glob("tools/bindings_templates/*")],
)
env.Alias("generate_godot_bindings", godot_bindings_pyx)


### Collect and build `pythonscript/godot` module ###

cython_env = env.Clone()
# C code generated by Cython is not *that* clean
if not env["shitty_compiler"]:
    cython_env.Append(CFLAGS="-Wno-unused")

# `bindings.pyx` is a special snowflake given it size and autogeneration
cython_bindings_env = cython_env.Clone()
if not env["shitty_compiler"]:
    cython_bindings_env.Append(CFLAGS="-Os")
    cython_bindings_env.Append(LINKFLAGS="-Wl,--strip-all")
else:
    cython_bindings_env.Append(CFLAGS="/Os")

pythonscript_godot_pyx_compiled = [
    *[
        cython_env.Cython(src)
        for src in env.Glob("pythonscript/godot/*.pyx")
        if src != godot_bindings_pyx
    ],
    cython_bindings_env.Cython(godot_bindings_pyx),
]
env.Depends(pythonscript_godot_pyx_compiled, gdnative_api_struct_pxd)
env.Depends(pythonscript_godot_pyx_compiled, godot_bindings_pxd)
pythonscript_godot_targets = [
    *env.Glob("pythonscript/godot/*.py"),
    *env.Glob("pythonscript/godot/*.pxd"),
    *pythonscript_godot_pyx_compiled,
]


### Build `pythonscript/_godot` module ###

# pythonscript_godot_bootstrap = env.Cython("pythonscript/_godot.pyx")
pythonscript__godot_c_scrs = env.CythonToC(
    source="pythonscript/_godot.pyx",
    target=("pythonscript/_godot.c", "pythonscript/_godot_api.h"),
)
env.Depends(pythonscript__godot_c_scrs, gdnative_api_struct_pxd)
env.Depends(pythonscript__godot_c_scrs, env.Glob("pythonscript/*.pxi"))
pythonscript__godot_c, pythonscript__godot_api_h, *_ = pythonscript__godot_c_scrs
pythonscript__godot_targets = cython_env.CythonCompile(source=[pythonscript__godot_c])


### Compile libpythonscript.so ###


env.Alias("backend", "$backend_dir")

libpythonscript = env.SharedLibrary(
    "pythonscript/pythonscript", "pythonscript/pythonscript.c"
)[0]
env.Depends("pythonscript/pythonscript.c", pythonscript__godot_api_h)


### Generate build dir ###


def extract_version():
    # Hold my beer...
    gl = {}
    exec(open("pythonscript/godot/_version.py").read(), gl)
    return gl["__version__"]


def generate_build_dir_hook(path):
    with open("misc/single_build_pythonscript.gdnlib") as fd:
        gdnlib = fd.read().replace(env["build_name"], "")
        # Single platform vs multi-platform one have not the same layout
        gdnlib = re.sub(
            r"(res://pythonscript/)(x11|windows|osx)-(64|32)-(cpython|pypy)/",
            r"\1",
            gdnlib,
        )
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


env.Command(
    "$build_dir",
    [
        "$backend_dir",
        libpythonscript,
        Dir("#pythonscript/godot"),
        *pythonscript__godot_targets,
        *pythonscript_godot_targets,
    ],
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
env.Command(
    "tests/helloworld",
    ["$godot_binary", install_build_symlink],
    test_base_cmd + "helloworld",
)
env.AlwaysBuild("tests/helloworld")
env.AlwaysBuild("tests")
env.Alias("test", "tests")


### Run example ###


env.Command(
    "example",
    ["$godot_binary", install_build_symlink],
    "${SOURCE} --path ${Dir('#').abspath}/examples/pong",
)
env.AlwaysBuild("example")


### Release (because I'm scared to do that with windows cmd on appveyor...) ###


def generate_release(target, source, env):
    base_name, format = target[0].abspath.rsplit(".", 1)
    shutil.make_archive(base_name, format, root_dir=source[0].abspath)


release = env.Command(
    "#godot-python-${release_suffix}-${platform}-${backend}.zip",
    "$build_dir",
    generate_release,
)
env.Alias("release", release)
env.AlwaysBuild("release")


### Auto-format codebase ###


black_cmd = "black pythonscript tools/*.py tests/*/*.py SConstruct platforms/*/SCsub"
autoformat = env.Command("autoformat", [], black_cmd)
env.Alias("black", autoformat)
env.Command("checkstyle", [], black_cmd + " --check")
