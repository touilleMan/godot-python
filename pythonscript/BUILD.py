from os import link
from typing import Callable, List, Tuple
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
    inputs=["pythonscript.c", "python_cflags@"],
)
def compile_pythonscript_c(
    output: Path,
    inputs: Tuple[Path, Tuple[str]],
    cc: str,
    cflags: Tuple[str],
    godot_headers: Path,
    host_platform: str,
) -> None:
    src, python_cflags = inputs
    if host_platform.startswith("windows"):
        # cl
        #  /Fobuild\windows-64\pythonscript\pythonscript.obj
        #  /c build\windows-64\pythonscript\pythonscript.c
        #  /WX /W2
        #  -IC:\Users\gbleu\source\repos\godot\godot-python\build\windows-64\platforms\windows-64\cpython_build/include
        #  /nologo
        #  /Igodot_headers
        cmd = [
            cc,
            f"/Fo{output}",
            "/c",
            str(src),
            *cflags,
            *python_cflags,
            "/nologo",
            f"-I{godot_headers}",
            "-DGODOT_VERSION_MAJOR=4",
            "-DGODOT_VERSION_MINOR=0",
            "-DGODOT_VERSION_PATCH=0",
        ]
    elif host_platform.startswith("linux"):
        # clang
        #  -o build/x11-64/pythonscript/pythonscript.os
        #  -c
        #  -O2 -m64
        #  -I/home/emmanuel/projects/godot/godot-python/build/x11-64/platforms/x11-64/cpython_build/include/python3.8/
        #  -Werror-implicit-function-declaration
        #  -fcolor-diagnostics
        #  -fPIC
        #  -Igodot_headers
        #  build/x11-64/pythonscript/pythonscript.c
        cmd = [
            cc,
            "-o",
            str(output),
            "-c",
            *cflags,
            *python_cflags,
            "-fPIC",
            f"-I{godot_headers}",
            "-DGODOT_VERSION_MAJOR=4",
            "-DGODOT_VERSION_MINOR=0",
            "-DGODOT_VERSION_PATCH=0",
            str(src),
        ]
    else:
        raise NotImplementedError()

    print(" ".join(cmd))
    subprocess.check_call(cmd)


@isg.rule(
    output="{build_pythonscript_dir}/pytonscript.so",
    inputs=["{build_pythonscript_dir}/pytonscript.os", "python_linkflags@"],
)
def link_pythonscript_so(
    output: Path,
    inputs: Tuple[Path, Tuple[str]],
    link: str,
    linkflags: Tuple[str],
    host_platform: str,
) -> None:
    src, python_linkflags = inputs

    if host_platform.startswith("windows"):
        # link
        #  /nologo
        #  /LIBPATH:C:\Users\gbleu\source\repos\godot\godot-python\build\windows-64\platforms\windows-64\cpython_build/libs
        #  /dll
        #  /out:build\windows-64\pythonscript\pythonscript.dll
        #  /implib:build\windows-64\pythonscript\pythonscript.lib
        #  python38.lib
        #  build\windows-64\pythonscript\pythonscript.obj
        cmd = [
            link,
            "/nologo",
            "/dll",
            f"/out:{output}",
            # f"/implib:{}",  # TODO
            *python_linkflags,
            str(src),
        ]
    elif host_platform.startswith("linux"):
        # clang
        #  -o build/x11-64/pythonscript/libpythonscript.so
        #  -m64
        #  -L/home/emmanuel/projects/godot/godot-python/build/x11-64/platforms/x11-64/cpython_build/lib
        #  -Wl,-rpath,'$ORIGIN/lib'
        #  -shared
        #  build/x11-64/pythonscript/pythonscript.os
        #  -lpython3.8
        cmd = [
            link,
            "-o",
            str(output),
            *linkflags,
            "-Wl,-rpath,'$ORIGIN/lib'",
            "--shared",
            *python_linkflags,
            str(src),
        ]
    else:
        raise NotImplementedError()

    # cmd = [link, "-o", str(output), str(src), *linkflags, *python_linkflags]

    # if host_platform.startswith("linux"):
    #     cmd += ("-Wl,-rpath,'$ORIGIN/lib'", "--shared")
    # TODO: handle other platforms

    print(" ".join(cmd))
    subprocess.check_call(cmd)


# @isg.lazy_config
# def pythonscript_cflags(cflags, host_platform):
#     if host_platform.startswith("linux"):
#         cmd += ("-Wl,-rpath,'$ORIGIN/lib'", "--shared")
#     # TODO: handle other platforms


# @isg.lazy_rule
# def pythonscript_rule(
#     register_rule: Callable, host_platform: str, cflags: Tuple[str], linkflags: Tuple[str]
# ):
#     cflags = list(cflags)
#     linkflags = list(linkflags)
#     libs = []
#     if host_platform.startswith("windows"):
#         libs.append("python38")
#         outputs = ["{build_pythonscript_dir}/pytonscript.os"]

#     elif host_platform.startswith("linux"):
#         libs.append("python3.8")
#         linkflags += ["-Wl,-rpath,'$$ORIGIN/lib'"]
#         cflags += ["-Werror-implicit-function-declaration"]

#     elif host_platform.startswith("osx"):
#         libs.append("python3.8")
#         # if we don't give the lib a proper install_name, macos won't be able to find it,
#         # and will link the cython modules with a relative path
#         linkflags += [
#             "-Wl,-rpath,'@loader_path/lib'",
#             "-install_name",
#             "@rpath/libpythonscript.dylib",
#         ]
#         cflags += ["-Werror-implicit-function-declaration"]

#     libpythonscript, *libpythonscript_extra = c_env.SharedLibrary(
#         "pythonscript", ["pythonscript.c"]
#     )


# c_env.Depends("pythonscript.c", env["cpython_build"])


# # cmd += ("-Wl,-rpath,'$ORIGIN/lib'", "--shared")


# outputs = isg.shared_library(
#     "pythonscript",
#     inputs=["pythonscript.c"],
#     overwrite_cflags="pythonscript_cflags",
#     overwrite_linkflags="pythonscript_linkflags",
# )


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
