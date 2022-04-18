from pathlib import Path
import shutil

import isengard


isg = isengard.get_parent()

isg.subdir("godot")


isg.rule_command(
    outputs=["{build_dir}/_pythonscript.c#", "{build_dir}/_pythonscript_api.h#"],
    inputs=[
        "_pythonscript.pyx#",
        # "_godot_editor.pxi",
        # "_godot_instance.pxi",
        # "_godot_profiling.pxi",
        # "_godot_script.pxi",
        # "_godot_io.pxi",
    ],
    cmd="cython -3 --fast-fail {inputs[0]} -o {output[0]}",
)


# libpyx_pythonscript = isg.static_library(
libpyx_pythonscript = isg.shared_library(
    libname="_pythonscript",
    sources=["{build_dir}/_pythonscript.c#"],
    dependencies=["libpython?"],
    build_dir_config_name="build_dir",
)


@isg.lazy_config
def libpythonscript_linkflags(host_platform, linkflags):
    if host_platform.startswith("osx"):
        # if we don't give the lib a proper install_name, macos won't be able to find it,
        # and will link the cython modules with a relative path
        extra_linkflags = (
            *linkflags,
            "-Wl,-rpath,'@loader_path/lib'",
            "-install_name",
            "@rpath/libpythonscript.dylib",
        )
    elif host_platform.startswith("linux"):
        extra_linkflags = ("-Wl,-rpath,'$$ORIGIN/lib'",)
    return frozenset((*linkflags, *extra_linkflags))


@isg.lazy_config
# def libpythonscript_cflags(cc_is_msvc, cflags, godot_api_version):
def libpythonscript_cflags(cc_is_msvc, cflags):
    extra_cflags = (
        # f"-DGODOT_VERSION_MAJOR={godot_api_version.major}",
        # f"-DGODOT_VERSION_MINOR={godot_api_version.minor}",
        f"-DGODOT_VERSION_MAJOR=4",
        f"-DGODOT_VERSION_MINOR=0",
    )
    if cc_is_msvc:
        return frozenset((*cflags, *extra_cflags))
    else:
        return frozenset((*cflags, *extra_cflags, "-Werror-implicit-function-declaration"))


libpythonscript = isg.shared_library(
    libname="pythonscript",
    sources=["pythonscript.c#", "{build_dir}/_pythonscript_api.h#"],
    dependencies=["libpython?", "libgodot?", libpyx_pythonscript],
    build_dir_config_name="build_dir",
    cflags_config_name="libpythonscript_cflags",
    linkflags_config_name="libpythonscript_linkflags",
)


@isg.rule(output="dist@", input=libpythonscript)
def dist(output, input):
    pass


@isg.rule(output="dist:libpythonscript?", input=libpythonscript)
def dist_libpythonscript(
    output: isengard.DeferredTarget[isg.CDependency],
    input: isengard.DeferredTarget[Path],
    dist_platform_dir: Path,
):
    input_path = input.resolved.path
    output_path = dist_platform_dir / input_path.name
    shutil.copyfile(input_path, output_path)
    output.resolve(output_path, discriminant="#")
