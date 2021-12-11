import os
import sys
import re
import struct
import shutil
from SCons.Platform.virtualenv import ImportVirtualenv
from SCons.Errors import UserError


EnsurePythonVersion(3, 7)
EnsureSConsVersion(4, 0)


def extract_version():
    # Hold my beer...
    gl = {}
    exec(open("pythonscript/godot/_version.py").read(), gl)
    return gl["__version__"]


def godot_binary_converter(val, env):
    file = File(val)
    if file.exists():
        # Note here `env["godot_binary_download_version"]` is not defined, this is ok given
        # this variable shouldn't be needed if Godot doesn't have to be downloaded
        return file
    # Provided value is version information with format <major>.<minor>.<patch>[-<extra>]
    match = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-(\w+))?$", val)
    if match:
        major, minor, patch, extra = match.groups()
    else:
        raise UserError(
            f"`{val}` is neither an existing file nor a valid <major>.<minor>.<patch>[-<extra>] Godot version format"
        )
    env["godot_binary_download_version"] = (major, minor, patch, extra or "stable")
    # `godot_binary` is set to None to indicate it should be downloaded
    return None


vars = Variables("custom.py")
vars.Add(
    EnumVariable(
        "platform",
        "Target platform",
        default="default",
        allowed_values=("default", "linux", "windows", "osx"),
    )
)
vars.Add(EnumVariable("bits", "Target platform bits", default="default", allowed_values=("default", "32", "64")))
vars.Add("pytest_args", "Pytest arguments passed to tests functions", "")
vars.Add(
    "godot_args", "Additional arguments passed to godot binary when running tests&examples", ""
)
vars.Add("release_suffix", "Suffix to add to the release archive", extract_version())
vars.Add(
    "godot_binary",
    "Path to Godot binary or version of Godot to use",
    default="3.2.2",
    converter=godot_binary_converter,
)
vars.Add("godot_headers", "Path to Godot GDnative headers", "")
vars.Add("debugger", "Run test with a debugger", "")
vars.Add(BoolVariable("debug", "Compile with debug symbols", False))
vars.Add(BoolVariable("headless", "Run tests in headless mode", False))
vars.Add(BoolVariable("compressed_stdlib", "Compress Python std lib as a zip to save space", True))
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
    BoolVariable(
        "MSVC_USE_SCRIPT",
        (
            "Set to True to let SCons find compiler (with MSVC_VERSION and TARGET_ARCH), "
            "False to use cmd.exe env (MSVC_VERSION and TARGET_ARCH will be ignored), "
            "or vcvarsXY.bat script name to use."
        ),
        True,
    )
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
    tools=["default", "cython", "symlink", "virtual_target", "download"],
    ENV=os.environ,
    # ENV = {'PATH' : os.environ['PATH']},
)


if env["platform"] == "default":
    if sys.platform == "linux":
        env["platform"] = "linux"
    elif sys.platform == "darwin":
        env["platform"] = "osx"
    elif sys.platform == "win32":
        env["platform"] = "windows"
    else:
        raise RuntimeError("Cannot detect platform automatically.")


if env["bits"] == "default":
    version = struct.calcsize("P") * 8
    if version == 64:
        env["bits"] =  "64"
    elif version == 32:
        env["bits"] = "32"
    else:
        raise RuntimeError("Cannot detect bits automatically.")


env["platform_bits"] = f"{env['platform']}-{env['bits']}"
print(f"platform={env['platform']}, bits={env['bits']}")


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


if env["godot_headers"]:
    env["godot_headers"] = Dir(env["godot_headers"])
else:
    env["godot_headers"] = Dir("godot_headers")
env.AppendUnique(CPPPATH=["$godot_headers"])
# TODO: not sure why, but CPPPATH scan result for cython modules change between
# first and subsequent runs of scons (module is considered to no longer depend
# on godot_headers on subsequent run, so the build redone)
SetOption("implicit_cache", 1)


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
        env.Append(CFLAGS=["/DEBUG:FULL"])
        env.Append(LINKFLAGS=["/DEBUG:FULL"])
    else:
        env.Append(CFLAGS=["/WX", "/W2"])


env["DIST_ROOT"] = Dir(f"build/dist")
env["DIST_PLATFORM"] = Dir(f"{env['DIST_ROOT']}/addons/pythonscript/{env['platform_bits']}")
VariantDir(f"build/{env['platform_bits']}/platforms", f"platforms")
VariantDir(f"build/{env['platform_bits']}/pythonscript", "pythonscript")


### Load sub scons scripts ###


Export(env=env)
SConscript(
    [
        f"build/{env['platform_bits']}/platforms/SConscript",  # Must be kept first
        f"build/{env['platform_bits']}/pythonscript/SConscript",
        "tests/SConscript",
        "examples/SConscript",
    ]
)


### Define default target ###


env.Default(env["DIST_ROOT"])
env.Alias("build", env["DIST_ROOT"])


### Static files added to dist ###


# env.VanillaInstallAs(
env.InstallAs(
    target="$DIST_ROOT/pythonscript.gdextension", source="#/misc/release_pythonscript.gdextension"
)
# env.VanillaInstallAs(
env.InstallAs(
    target="$DIST_ROOT/addons/pythonscript/LICENSE.txt", source="#/misc/release_LICENSE.txt"
)
env.Command(target="$DIST_ROOT/addons/pythonscript/.gdignore", source=None, action=Touch("$TARGET"))
# SCons install on directory doesn't check for file changes
for item in env.Glob("addons/pythonscript_repl/*"):
    # env.VanillaInstall(target="$DIST_ROOT/addons/pythonscript_repl", source=item)
    env.Install(target="$DIST_ROOT/addons/pythonscript_repl", source=item)


### Release archive ###


def generate_release(target, source, env):
    for suffix, format in [(".zip", "zip"), (".tar.bz2", "bztar")]:
        if target[0].name.endswith(suffix):
            base_name = target[0].abspath[: -len(suffix)]
            break
    shutil.make_archive(base_name, format, root_dir=source[0].abspath)


# Zip format doesn't support symlinks that are needed for Linux&macOS
if env["platform"].startswith("windows"):
    release_target = "build/godot-python-${release_suffix}-${platform}.zip"
else:
    release_target = "build/godot-python-${release_suffix}-${platform}.tar.bz2"
release = env.Command(release_target, env["DIST_ROOT"], generate_release)
env.Alias("release", release)
env.AlwaysBuild("release")
