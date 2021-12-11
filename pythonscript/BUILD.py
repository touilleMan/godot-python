from typing import List, Tuple
from pathlib import Path
import subprocess
import isengard


isg = isengard.get_parent()

isg.subdir("godot")


@isg.lazy_config
def build_pythonscript_dir(build_platform_dir: Path):
    build_pythonscript_dir = build_platform_dir / "pythonscript"
    build_pythonscript_dir.mkdir(parents=True, exist_ok=True)
    return build_pythonscript_dir


@isg.rule(
    output="{build_pythonscript_dir}/pytonscript.os",
    inputs=["pythonscript.c", "python_headers_dir@"],
)
def compile_pythonscript_c(
    output: Path,
    inputs: Tuple[Path, Path],
    cc: str,
    cflags: Tuple[str],
    godot_headers: Path,
) -> None:
    import subprocess
    src, python_headers = inputs
    extra_cflags = [
        f"-I{python_headers}",
        "-fPIC",
        f"-I{godot_headers}",
    ]
    cmd = f"{cc} {' '.join(cflags)} {' '.join(extra_cflags)} -o {output} -c {src}"
    print(cmd)
    subprocess.check_call(
        cmd.split()
    )


# clang -o build/x11-64/pythonscript/pythonscript.os -c -O2 -m64 -I/home/emmanuel/projects/godot/godot-python/build/x11-64/platforms/x11-64/cpython_build/include/python3.8/ -Werror-implicit-function-declaration -fcolor-diagnostics -fPIC -Igodot_headers build/x11-64/pythonscript/pythonscript.c
# clang -o build/x11-64/pythonscript/libpythonscript.so -m64 -L/home/emmanuel/projects/godot/godot-python/build/x11-64/platforms/x11-64/cpython_build/lib -Wl,-rpath,'$ORIGIN/lib' -shared build/x11-64/pythonscript/pythonscript.os -lpython3.8

# pythonscript_lib = isg.shared_library("pythonscript", ["pythonscript.c"])
# isg.copy(src=pythonscript_lib, dst="{DIST_SITE_PACKAGES}")


# @isg.lazy_config()
# def pythonscript_cflags(host_platform: str, cflags: List[str]) -> str:
#     if host_platform == "windows":
#         cflags.append("")

#     elif:
#     return [*cflags, ]


# Import("env")

# c_env = env.Clone()
# if env["platform"].startswith("windows"):
#     c_env.AppendUnique(LIBS=["python38"])

# elif env["platform"].startswith("osx"):
#     c_env.AppendUnique(LIBS=["python3.8"])
#     # if we don't give the lib a proper install_name, macos won't be able to find it,
#     # and will link the cython modules with a relative path
#     c_env.AppendUnique(
#         LINKFLAGS=["-Wl,-rpath,'@loader_path/lib'", "-install_name", "@rpath/libpythonscript.dylib"]
#     )
#     c_env.AppendUnique(CFLAGS=["-Werror-implicit-function-declaration"])

# else:  # x11
#     c_env.AppendUnique(LIBS=["python3.8"])
#     c_env.AppendUnique(LINKFLAGS=["-Wl,-rpath,'$$ORIGIN/lib'"])
#     c_env.AppendUnique(CFLAGS=["-Werror-implicit-function-declaration"])
# c_env.Depends("pythonscript.c", env["cpython_build"])


# libpythonscript, *libpythonscript_extra = c_env.SharedLibrary("pythonscript", ["pythonscript.c"])
# env.Install("$DIST_PLATFORM", [libpythonscript, *libpythonscript_extra])


# # Cython modules depend on libpythonscript
# env.AppendUnique(LIBPATH=[Dir(".")])
# env.AppendUnique(CYTHON_COMPILE_DEPS=[libpythonscript])


# SConscript(["godot/SConscript"])

# def cython_module(isg, name, sources=None):
#     sources = sources or [f"{name}.pyx"]
#     output = "{build_dir}/godot-python-{release_suffix}-{host_platform}.{release_format_ext}"

#     @isg.rule(
#         name=f"cython_module: {name}",
#         output=output,
#         input="{build_dir}/dist/",
#     )
#     def rule(output: Path, input: Path, basedir: Path) -> None:
#         input_relative = input.relative_to(basedir)

#     return output


# mods = isg.cython_module("_pythonscript", [
#     "_pythonscript.pyx",
#     "_godot_editor.pxi",
#     "_godot_instance.pxi",
#     "_godot_profiling.pxi",
#     "_godot_script.pxi",
#     "_godot_io.pxi",
# ])
# isg.copy(src=mods, dst="{DIST_SITE_PACKAGES}")
# # `_pythonscript_api.h` is only for internal use between _godot and pythonscript
# # libraries, hence no need to provide it as part of the release
# isg.side_effect("_pythonscript_api.h", mods[0])
