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
vars.Add("pytest_args", "Pytest arguments passed to tests functions", "")
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
        "Provide godot/_godot modules through symlinks instead of copying them in the build (useful for dev)",
        False,
    )
)
vars.Add(BoolVariable("debug", "Compile with debug symbols", False))
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
vars.Add("BINDINGS_CFLAGS", "Custom flags for the C compiler (for bindings.c only)", "")
vars.Add("LINK", "linker")
vars.Add("LINKFLAGS", "Custom flags for the linker")
vars.Add("BINDINGS_LINKFLAGS", "Custom flags for the linker (for bindings.c only)", "")
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


def SymLinkAction(target, source, env):
    """
    Scons doesn't provide cross-platform symlink out of the box due to Windows...
    """
    abs_src = os.path.abspath(str(source[0]))
    abs_trg = os.path.abspath(str(target[0]))

    try:
        os.unlink(abs_trg)
    except Exception:
        pass

    if env["HOST_OS"] == "win32":
        if os.path.isdir(abs_src):
            try:
                import _winapi

                _winapi.CreateJunction(abs_src, abs_trg)
            except Exception as e:
                raise UserError(
                    f"Can't do a NTFS junction as symlink fallback ({abs_src} -> {abs_trg}): {e}"
                )
        else:
            try:
                shutil.copy(abs_src, abs_trg)
            except Exception as e:
                raise UserError(
                    f"Can't do a file copy as symlink fallback ({abs_src} -> {abs_trg}): {e}"
                )

    else:
        try:
            os.symlink(abs_src, abs_trg)
        except Exception as e:
            raise UserError(f"Can't create symlink ({abs_src} -> {abs_trg}): {e}")


def SymLink(env, target, source, action=SymLinkAction):
    results = env.Command(target, source, action)
    abs_trg = os.path.abspath(str(target[0]))
    if env["PLATFORM"] == "win32":

        def _rm(env, target, source):
            # assert len(target) == 1
            try:
                os.unlink(abs_trg)
                # os.unlink(target[0])
            except FileNotFoundError:
                pass
            except Exception as e:
                # raise UserError(f"Can't remove NTFS junction {target[0]}")
                raise UserError(f"Can't remove NTFS junction {abs_trg}: {e}")

        env.CustomClean(
            target,
            # RemoveSymLink
            Action(_rm, f"Removing symlink {abs_trg}"),
        )
    return results


env.Append(BUILDERS={"SymLink": SymLink})


def CustomClean(env, targets, action):
    # Inspired by https://github.com/SCons/scons/wiki/CustomCleanActions

    if not env.GetOption("clean"):
        return

    # normalize targets to absolute paths
    targets = [env.Entry(target).abspath for target in env.Flatten(targets)]
    launchdir = env.GetLaunchDir()
    topdir = env.Dir("#").abspath
    cl_targets = COMMAND_LINE_TARGETS

    if not cl_targets:
        cl_targets.append(".")

    for cl_target in cl_targets:
        if cl_target.startswith("#"):
            full_target = os.path.join(topdir, cl_target[:1])
        else:
            full_target = os.path.join(launchdir, cl_target)
        full_target = os.path.normpath(full_target)
        for target in targets:
            if target.startswith(full_target):
                env.Execute(action)
                return


env.AddMethod(CustomClean, "CustomClean")


def Glob(env, pattern):
    """
    Scons Glob is rather limited
    """
    return sorted([File(x) for x in glob.glob(pattern, recursive=True)])


env.AddMethod(Glob, "Glob")


if env["dev_dyn"]:
    print(
        "\033[0;32mBuild with a symlink on `pythonscript/godot` module"
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
    env.Append(CCFLAGS=["-fcolor-diagnostics"])
if "gcc" in env.get("CC"):
    env.Append(CCFLAGS=["-fdiagnostics-color=always"])


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
    # Python native module must have .pyd suffix on windows and .so on POSIX
    if env["platform"].startswith("windows"):
        suffix = ".pyd"
    else:
        suffix = ".so"
    return env.SharedLibrary(libs, source, LIBPREFIX="", SHLIBSUFFIX=suffix)


def cythonizer(env, source):
    c_source = env.CythonToC(source)
    return cython_compile(env, c_source)


env.AddMethod(cython_compile, "CythonCompile")


### Default C flags ###


env.AppendUnique(CPPPATH=["#", "$gdnative_include_dir"])

# TODO: choose right flag
if not env["shitty_compiler"]:
    env.Append(CFLAGS=["-std=c11"])
    env.Append(CFLAGS=["-Werror", "-Wall"])
    if env["debug"]:
        env.Append(CFLAGS=["-g", "-ggdb"])
        env.Append(LINKFLAGS=["-g", "-ggdb"])
else:
    env.Append(CFLAGS=["/WX", "/W2"])

# env.Append(CFLAGS=['-pthread -DDEBUG=1 -fwrapv -Wall '
#     '-g -Wdate-time -D_FORTIFY_SOURCE=2 '
#     '-Bsymbolic-functions -Wformat -Werror=format-security'.split()])


### Generate godot api .h -> gdnative_api_struct.pxd ###


gdnative_api_struct_pxd = File("pythonscript/godot/_hazmat/gdnative_api_struct.pxd")
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


### Generate pythonscript/godot/pool_arrays.pyx&pxd ###

godot_pool_arrays_pyx, godot_pool_arrays_pxd = env.Command(
    target=("pythonscript/godot/pool_arrays.pyx", "pythonscript/godot/pool_arrays.pxd"),
    source=("pythonscript/godot/builtins.pxd"),
    action=("python tools/generate_pool_arrays.py  -o ${TARGET}"),
)
env.Depends(
    godot_pool_arrays_pyx,
    ["tools/generate_pool_arrays.py", env.Glob("tools/pool_arrays_templates/*")],
)
env.Alias("generate_pool_arrays", godot_pool_arrays_pyx)


### Generate pythonscript/godot/builtins.pyx&pxd ###

godot_builtins_pyx, godot_builtins_pxd = env.Command(
    target=("pythonscript/godot/builtins.pyx", "pythonscript/godot/builtins.pxd"),
    source=(),
    action=("python tools/generate_builtins.py  -o ${TARGET}"),
)
env.Depends(
    godot_builtins_pyx,
    ["tools/generate_builtins.py", env.Glob("tools/builtins_templates/*")],
)
env.Alias("generate_builtins", godot_builtins_pyx)


### Generate pythonscript/godot/bindings.pyx&pxd ###

sample_opt = "--sample" if env["sample"] else ""
godot_bindings_pyx, godot_bindings_pxd = env.Command(
    target=("pythonscript/godot/bindings.pyx", "pythonscript/godot/bindings.pxd"),
    source=(
        "%s/api.json" % env["gdnative_include_dir"],
        "pythonscript/godot/builtins.pxd",
    ),
    action=(
        "python tools/generate_bindings.py  -i ${SOURCE} -o ${TARGET} " + sample_opt
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
    cython_env.Append(CFLAGS=["-Wno-unused"])

# Godot api struct pointers used in the cython modules are defined
# in the pythonscript shared library. Unlink on UNIX, Windows
# requires to have those symboles resolved at compile time.
if env["platform"].startswith("windows"):
    cython_env.Append(LIBPATH=["#pythonscript"])
    cython_env.Append(LIBS=["pythonscript"])

# `bindings.pyx` is a special snowflake given it size and autogeneration
cython_bindings_env = cython_env.Clone()
if env["BINDINGS_LINKFLAGS"]:
    cython_bindings_env.Append(CFLAGS=env["BINDINGS_LINKFLAGS"])
elif not env["sample"]:
    if not env["shitty_compiler"]:
        cython_bindings_env.Append(LINKFLAGS=["-Wl,--strip-all"])
if env["BINDINGS_CFLAGS"]:
    cython_bindings_env.Append(CFLAGS=env["BINDINGS_CFLAGS"])
elif env["sample"]:
    if not env["shitty_compiler"]:
        cython_bindings_env.Append(CFLAGS=["-O0"])
    else:
        cython_bindings_env.Append(CFLAGS=["/O0"])
else:
    if not env["shitty_compiler"]:
        cython_bindings_env.Append(CFLAGS=["-Os", "-Wno-misleading-indentation"])
    else:
        cython_bindings_env.Append(CFLAGS=["/Os"])
godot_bindings_pyx_to_c = cython_bindings_env.CythonToC(godot_bindings_pyx)
godot_bindings_pyx_compiled = cython_bindings_env.CythonCompile(godot_bindings_pyx_to_c)

# Now the other common folks
pythonscript_godot_pyxs_except_bindings = [
    godot_builtins_pyx,
    godot_pool_arrays_pyx,
    # Keep glob last to avoid changing deps order depending of the other entries
    # being already generated or not
    *[src for src in env.Glob("pythonscript/godot/*.pyx") if src != godot_bindings_pyx],
    *env.Glob("pythonscript/godot/_hazmat/*.pyx"),
]
pythonscript_godot_pyxs_except_bindings_to_c = [
    cython_env.CythonToC(src) for src in pythonscript_godot_pyxs_except_bindings
]
pythonscript_godot_pyxs_except_bindings_compiled = [
    cython_env.CythonCompile(src)
    for src in pythonscript_godot_pyxs_except_bindings_to_c
]

# Define dependencies on .pxd files
pythonscript_godot_pyxs = [pythonscript_godot_pyxs_except_bindings, godot_bindings_pyx]
pythonscript_godot_pxds = [
    godot_pool_arrays_pxd,
    godot_builtins_pxd,
    gdnative_api_struct_pxd,
    godot_bindings_pxd,
    # Keep glob last to avoid changing deps order depending of the other entries
    # being already generated or not
    *env.Glob("pythonscript/godot/*.pxd"),
    *env.Glob("pythonscript/godot/_hazmat/*.pxd"),
]
pythonscript_godot_pyxs_to_c = [
    pythonscript_godot_pyxs_except_bindings_to_c,
    godot_bindings_pyx_to_c,
]
pythonscript_godot_pyxs_compiled = [
    pythonscript_godot_pyxs_except_bindings_compiled,
    godot_bindings_pyx_compiled,
]
env.Depends(pythonscript_godot_pyxs_to_c, pythonscript_godot_pxds)

# Final target
pythonscript_godot_targets = [
    *pythonscript_godot_pxds,
    *pythonscript_godot_pyxs_compiled,
    # Keep glob last to avoid changing deps order depending of the other entries
    # being already generated or not
    *env.Glob("pythonscript/godot/*.py"),
    *env.Glob("pythonscript/godot/_hazmat/*.py"),
]


### Build `pythonscript/_godot` module ###

# pythonscript_godot_bootstrap = env.Cython("pythonscript/_godot.pyx")
pythonscript__godot_c_scrs = env.CythonToC(
    source="pythonscript/_godot.pyx",
    target=("pythonscript/_godot.c", "pythonscript/_godot_api.h"),
)
env.Depends(pythonscript__godot_c_scrs, pythonscript_godot_pxds)
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


def generate_build_dir(target, source, env):
    target = target[0]
    cpython_build = source[0]
    libpythonscript = source[1]
    godot_module = source[2]
    _godot_module = source[3]

    if os.path.isdir(target.path):
        if env["dev_dyn"]:
            print(f"dev_dyn: {target.path} already exist, reusing it")
        else:
            print(f"Removing old build {target.path}")
            shutil.rmtree(target.path)

    if not os.path.isdir(target.path):
        print(f"Generating build {target.path}")
        os.mkdir(target.path)
        env["add_cpython_to_build_dir"](env, target, cpython_build)

    env["add_pythonscript_stuff_to_build_dir"](
        env, target, libpythonscript, _godot_module, godot_module
    )

    with open("misc/single_build_pythonscript.gdnlib") as fd:
        gdnlib = fd.read().replace(env["build_name"], "")
        # Single platform vs multi-platform one have not the same layout
        gdnlib = re.sub(
            r"(res://pythonscript/)(x11|windows|osx)-(64|32)-(cpython|pypy)/",
            r"\1",
            gdnlib,
        )
    with open(os.path.join(target.path, "pythonscript.gdnlib"), "w") as fd:
        fd.write(gdnlib)

    shutil.copy("misc/release_LICENSE.txt", os.path.join(target.path, "LICENSE.txt"))

    with open("misc/release_README.txt") as fd:
        readme = fd.read().format(
            version=extract_version(), date=datetime.utcnow().strftime("%Y-%m-%d")
        )
    with open(os.path.join(target.path, "README.txt"), "w") as fd:
        fd.write(readme)


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
        partial(do_or_die, generate_build_dir),
        "Generating build dir $TARGET from $SOURCES",
    ),
)
env.Clean("$build_dir", env["build_dir"].path)


### Symbolic link used by test and examples projects ###


(install_build_symlink,) = env.SymLink("build/main", "$build_dir")
env.AlwaysBuild(install_build_symlink)

env.Default(install_build_symlink)


### Download godot binary ###


(godot_binary,) = env.SymLink("build/godot", "$godot_binary")
env.Alias("godot_binary", godot_binary)


### Run tests ###


# Note: passing absolute path is only really needed on Mac with Godot.app
if env["pytest_args"]:
    pytest_args = " ".join(f"--pytest={arg}" for arg in env["pytest_args"].split())
else:
    pytest_args = ""
if env["debugger"]:
    test_base_cmd = (
        "${debugger} ${SOURCE} -- --path ${Dir('#').abspath}/tests/%s " + pytest_args
    )
else:
    test_base_cmd = "${SOURCE} --path ${Dir('#').abspath}/tests/%s " + pytest_args


if env["HOST_OS"] == "win32":

    def init_pythonscript_build_symlinks(target_dir):
        # Under Windows, symlinks in a git repository are not resolved, hence
        # we must force their creation (using junction/file copy fallback)
        symlinks = []
        for item in ("pythonscript", "pythonscript.gdnlib"):
            trg = (f"{target_dir}/{item}",)
            src = f"{install_build_symlink}/{item}"
            (symlink,) = env.SymLink(
                trg,
                install_build_symlink,
                action=Action(
                    # Using {install_build_symlink}/{item} as SOURCE creates
                    # recursive dependency build/main -> build/main/pythonscript -> build/main.
                    # On top of that the for loop force us to store in captured_src
                    # the value to use in the call.
                    lambda target, source, env, captured_src=src: SymLinkAction(
                        target, [captured_src, *source], env
                    ),
                    f"Symlinking {src} -> $TARGET",
                ),
            )
            symlinks.append(symlink)

        return symlinks


else:

    def init_pythonscript_build_symlinks(target_dir):
        # Under POSIX, symlinks just works, so we only need to make sure
        # the build dir they point to has been generated
        return install_build_symlink


env.Command(
    "tests/bindings",
    ["$godot_binary", init_pythonscript_build_symlinks("tests/bindings")],
    test_base_cmd % "bindings",
)
env.AlwaysBuild("tests/bindings")
env.Command(
    "tests/work_with_gdscript",
    ["$godot_binary", init_pythonscript_build_symlinks("tests/work_with_gdscript")],
    test_base_cmd % "work_with_gdscript",
)
env.AlwaysBuild("tests/work_with_gdscript")
env.Command(
    "tests/helloworld",
    ["$godot_binary", init_pythonscript_build_symlinks("tests/helloworld")],
    test_base_cmd % "helloworld",
)
env.AlwaysBuild("tests/helloworld")
env.AlwaysBuild("tests")
env.Alias("test", "tests")


### Run example ###


env.Command(
    "examples/pong",
    ["$godot_binary", init_pythonscript_build_symlinks("examples/pong")],
    "${SOURCE} --path ${Dir('#').abspath}/examples/pong",
)
env.AlwaysBuild("examples/pong")
env.Alias("example", "examples/pong")


env.Command(
    "examples/pong_multiplayer",
    ["$godot_binary", init_pythonscript_build_symlinks("examples/pong_multiplayer")],
    "${SOURCE} --path ${Dir('#').abspath}/examples/pong_multiplayer",
)
env.AlwaysBuild("examples/pong_multiplayer")


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
