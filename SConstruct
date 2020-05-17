import os
import shutil
from datetime import datetime
from SCons.Platform.virtualenv import ImportVirtualenv


EnsurePythonVersion(3, 6)
EnsureSConsVersion(3, 0)


def boolean_converter(val, env):
    """Allowed values are True, False, and a script path"""
    if val in ("False", "false", "0"):
        return False

    if val in ("True", "true", "1"):
        return True

    return val


def extract_version():
    # Hold my beer...
    gl = {}
    exec(open("pythonscript/godot/_version.py").read(), gl)
    return gl["__version__"]


vars = Variables("custom.py")
vars.Add(
    EnumVariable(
        "platform",
        "Target platform",
        "",
        allowed_values=("x11-64", "x11-32", "windows-64", "windows-32", "osx-64"),
    )
)
vars.Add("pytest_args", "Pytest arguments passed to tests functions", "")
vars.Add(
    "godot_args", "Additional arguments passed to godot binary when running tests&examples", ""
)
vars.Add("release_suffix", "Suffix to add to the release archive", extract_version())
vars.Add(
    "godot_binary", "Path to Godot main binary", "", converter=lambda x: File(x) if x else None
)
vars.Add("gdnative_include_dir", "Path to GDnative include directory", "")
vars.Add("debugger", "Run test with a debugger", "")
vars.Add(BoolVariable("debug", "Compile with debug symbols", False))
vars.Add(
    BoolVariable(
        "bindings_generate_sample",
        "Generate only a subset of the bindings (faster build time)",
        False,
    )
)
vars.Add("CC", "C compiler")
vars.Add("CFLAGS", "Custom flags for the C compiler")
vars.Add("LINK", "linker")
vars.Add("LINKFLAGS", "Custom flags for the linker")
vars.Add("CPYTHON_CFLAGS", "Custom flags for the C compiler used to compile CPython")
vars.Add("CPYTHON_LINKFLAGS", "Custom flags for the linker used to compile CPython")
vars.Add("OPENSSL_PATH", "Path to the root of openssl installation to link CPython against")
vars.Add(
    "MSVC_VERSION",
    "MSVC version to use (Windows only) -- version num X.Y. Default: highest installed.",
)
vars.Add(
    "MSVC_USE_SCRIPT",
    "Set to True to let SCons find compiler (with MSVC_VERSION and TARGET_ARCH), "
    "False to use cmd.exe env (MSVC_VERSION and TARGET_ARCH will be ignored), "
    "or vcvarsXY.bat script name to use.",
    default=True,
    converter=boolean_converter,
)


# Set Visual Studio arch according to platform target
vanilla_vars_update = vars.Update


def _patched_vars_update(env, args=None):
    vanilla_vars_update(env, args=None)
    if env["platform"] == "windows-64":
        env["TARGET_ARCH"] = "x86_64"
    elif env["platform"] == "windows-32":
        env["TARGET_ARCH"] = "x86"


vars.Update = _patched_vars_update


env = Environment(
    variables=vars,
    tools=["default", "cython", "symlink", "virtual_target"],
    ENV=os.environ,
    # ENV = {'PATH' : os.environ['PATH']},
)


# Detect compiler
env["CC_IS_MSVC"] = env.get("CC") in ("cl", "cl.exe")
env["CC_IS_GCC"] = "gcc" in env.get("CC")
env["CC_IS_CLANG"] = "clang" in env.get("CC")


Help(vars.GenerateHelpText(env))
# if env["HOST_OS"] == "win32":
#   # Fix ImportVirtualenv raising error if PATH make reference to other drives
#   from SCons.Platform import virtualenv
#   vanilla_IsInVirtualenv = virtualenv.IsInVirtualenv
#   def patched_IsInVirtualenv(path):
#       try:
#           return vanilla_IsInVirtualenv(path)
#       except ValueError:
#           return False
#   virtualenv.IsInVirtualenv = patched_IsInVirtualenv
# ImportVirtualenv(env)


if env["gdnative_include_dir"]:
    env["gdnative_include_dir"] = Dir(env["gdnative_include_dir"])
else:
    env["gdnative_include_dir"] = Dir("godot_headers")
env.AppendUnique(CPPPATH=["$gdnative_include_dir"])


### Save my eyes plz ###

env["ENV"]["TERM"] = os.environ.get("TERM", "")
if env["CC_IS_CLANG"]:
    env.Append(CCFLAGS=["-fcolor-diagnostics"])
if env["CC_IS_GCC"]:
    env.Append(CCFLAGS=["-fdiagnostics-color=always"])


### Default compile flags ###

if not env["CC_IS_MSVC"]:
    if env["debug"]:
        env.Append(CFLAGS=["-g", "-ggdb"])
        env.Append(LINKFLAGS=["-g", "-ggdb"])
    else:
        env.Append(CFLAGS=["-O2"])
else:
    if env["debug"]:
        env.Append(CFLAGS=["/DEBUG"])
        env.Append(LINKFLAGS=["/DEBUG"])
    else:
        env.Append(CFLAGS=["/WX", "/W2"])


env["DIST_ROOT"] = Dir(f"build/dist")
env["DIST_PLATFORM"] = Dir(f"{env['DIST_ROOT']}/pythonscript/{env['platform']}")
VariantDir(f"build/{env['platform']}/platforms", f"platforms")
VariantDir(f"build/{env['platform']}/pythonscript", "pythonscript")


### Static files added to dist ###


env.Command(
    target=f"$DIST_ROOT/pythonscript.gdnlib",
    source=f"#/misc/release_pythonscript.gdnlib",
    action=Copy("$TARGET", "$SOURCE"),
)
env.Command(
    target=f"$DIST_ROOT/pythonscript/LICENSE.txt",
    source=f"#/misc/release_LICENSE.txt",
    action=Copy("$TARGET", "$SOURCE"),
)
env.Command(target="$DIST_ROOT/pythonscript/.gdignore", source=None, action=Touch("$TARGET"))


### Load sub scons scripts ###


Export(env=env)
SConscript(
    [
        f"build/{env['platform']}/platforms/SConscript",  # Must be kept first
        f"build/{env['platform']}/pythonscript/SConscript",
        "tests/SConscript",
        "examples/SConscript",
    ]
)


### Define default target ###


env.Default(env["DIST_ROOT"])
env.Alias("build", env["DIST_ROOT"])


### Release archive ###


def generate_release(target, source, env):
    base_name, format = target[0].abspath.rsplit(".", 1)
    shutil.make_archive(base_name, format, root_dir=source[0].abspath)


release = env.Command(
    "build/godot-python-${release_suffix}-${platform}.zip", env["DIST_ROOT"], generate_release
)
env.Alias("release", release)
env.AlwaysBuild("release")
