import re
import platform
from multiprocessing.sharedctypes import Value
import sys
from pathlib import Path
from typing import Callable, Optional, Tuple
import argparse

import isengard


# class IsengardCMixin:
#     def shared_library(self, name: str, sources: List[str], extra_cflags=None, extra_linkflags=None):
#         for source in sources:
#             assert sources.endswith()
#         @self.rule()
#         def _shared_library():
#             pass

# clang -o build/x11-64/pythonscript/pythonscript.os -c -O2 -m64 -I/home/emmanuel/projects/godot/godot-python/build/x11-64/platforms/x11-64/cpython_build/include/python3.8/ -Werror-implicit-function-declaration -fcolor-diagnostics -fPIC -Igodot_headers build/x11-64/pythonscript/pythonscript.c
# clang -o build/x11-64/pythonscript/libpythonscript.so -m64 -L/home/emmanuel/projects/godot/godot-python/build/x11-64/platforms/x11-64/cpython_build/lib -Wl,-rpath,'$ORIGIN/lib' -shared build/x11-64/pythonscript/pythonscript.os -lpython3.8


# class IsengardCythonMixin:
#     pass


# class CustomizedIsengard(isengard.Isengard, IsengardCMixin, IsengardCythonMixin):
#     pass


# isg = CustomizedIsengard(__file__, subdir_default_filename="BUILD.py")
isg = isengard.Isengard(__file__, subdir_default_filename="BUILD.py")


# @isg.lazy_config()
# def release_format_ext(host_platform: str) -> str:
#     # Zip format doesn't support symlinks that are needed for Linux&macOS
#     if host_platform == "windows":
#         return "zip"
#     else:
#         return "tar.bz2"


# @isg.rule(output="{build_dir}/godot-python-{release_suffix}-{host_platform}.{release_format_ext}", input="{build_dir}/dist/")
# def generate_release(output: Path, input: Path) -> None:
#     for suffix, format in [(".zip", "zip"), (".tar.bz2", "bztar")]:
#         if output.name.endswith(suffix):
#             base_name = str(output)[: -len(suffix)]
#             break

#     from shutil import make_archive
#     make_archive(base_name, format, root_dir=input)


# libfoo = isg.cython_module("foo.pyx")
# isg.install(libfoo)

# pythonscript_pyx_src, pythonscript_pyx_header = isg.cython_to_c("_pythonscript.pyx")
# pythonscript_lib = isg.shared_library("_pythonscript", ["pythonscript.c", pythonscript_pyx_src, pythonscript_pyx_header])
# isg.install(pythonscript_lib)


# def _customize_cflags(cflags, *args):
#     return [[*cflags, "-O2"], *args]

# isg.c("foo.c", config_hook=_customize_cflags)


# @isg.meta_rule
# def cython(source: str, config_hook: Optional[Callable]=None):
#     name, ext = source.rsplit(".")
#     if ext != "pyx":
#         raise ValueError("Expects .pyx file as source")
#     output = f"{name}.so"

#     @isg.rule(output=f"{{__DST__}}/{name}.so", input=source)
#     def _cython_rule(output: Path, input: Path, cflags: List[str], linkflags: List[str]):
#         if config_hook:
#             cflags, linkflags = config_hook(cflags, linkflags)
#         pass

#     return isengard.Rule(f"cythonize_{source}", outputs=[output], inputs=[source], fn=_cython)

# @isg.meta_rule
# def shared_library(libname, sources):
#     def _shared_library():
#         pass

#     return _shared_library


isg.subscript("build_tools/dist.py")
isg.subscript("build_tools/godot_binary.py")
isg.subscript("build_tools/python_distrib.py")
isg.subdir("pythonscript")
isg.subdir("tests")


@isg.lazy_config
def build_dir(rootdir: Path) -> Path:
    build_dir = rootdir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    return build_dir


@isg.lazy_config
def build_platform_dir(build_dir: Path, host_platform: str) -> Path:
    build_platform_dir = build_dir / host_platform
    build_platform_dir.mkdir(parents=True, exist_ok=True)
    return build_platform_dir


@isg.lazy_config
def cflags(host_platform: str) -> Tuple[str, ...]:
    if host_platform.startswith("windows"):
        return ("/WX", "/W2")
    else:
        return (
            "-O2",
            "-m64",
            "-Werror-implicit-function-declaration",
            "-fcolor-diagnostics",
        )


@isg.lazy_config
def linkflags(host_platform: str):
    return ("-m64",)


if __name__ == "__main__":

    def _parse_host_cypthon_version_argument(val):
        if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", val):
            raise ValueError(f"`{val}` doesn't respect the <major>.<minor>.<patch> version format")
        return val

    def _parse_godot_binary_argument(val):
        file = Path(val)
        if file.exists():
            return file
        # Provided value is version information with format <major>.<minor>.<patch>[-<extra>]
        match = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-(\w+))?$", val)
        if match:
            major, minor, patch, extra = match.groups()
        else:
            raise ValueError(
                f"`{val}` is neither an existing file nor a valid <major>.<minor>.<patch>[-<extra>] Godot version format"
            )
        return (major, minor, patch, extra or "stable")

    parser = argparse.ArgumentParser(description="Build the project")
    parser.add_argument("target")
    parser.add_argument(
        "--host-cpython-version",
        help="Version of CPython that will be shipped in the extension (default: 3.9.7)",
        default="3.9.7",
        type=_parse_host_cypthon_version_argument,
    )
    parser.add_argument(
        "--godot-binary",
        help="Path to Godot binary or version of Godot to use (default: 4.0.0-alpha1)",
        default="4.0.0-alpha1",
        type=_parse_godot_binary_argument,
    )
    parser.add_argument(
        "--godot-headers",
        help="Path to Godot headers directory",
        default="./godot_headers",
        type=lambda x: Path(x).resolve().absolute(),
    )
    parser.add_argument(
        "--dump-graph",
        help="Display dependency graph",
        action="store_true",
    )
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    def get_build_platform():
        build_platform = ""

        # TODO: support Apple M1 ?

        system = platform.system()
        if system == "Linux":
            build_platform += "linux"
        elif system == "Windows":
            build_platform += "windows"
        elif system == "Darwin":
            build_platform += "osx"
        else:
            raise RuntimeError(f"Unsupported system {system}")

        machine = platform.machine()
        if machine in ("i386", "x86"):
            build_platform += "-x86"
        elif machine in ("AMD64", "x86_64"):
            build_platform += "-x86_64"
        else:
            raise RuntimeError(f"Unknown machine {machine}")

        return build_platform

    build_platform = get_build_platform()
    host_platform = build_platform  # No cross-compilation
    isg.configure(
        build_platform=build_platform,
        host_platform=host_platform,
        godot_binary_hint=args.godot_binary,
        godot_headers=args.godot_headers,
        cpython_compressed_stdlib=True,
        host_cpython_version=args.host_cpython_version,
        godot_args=(),
        pytest_args=(),
        debugger="",
        headless=False,
        cc_is_msvc=host_platform.startswith("windows"),
        cc="cl.exe" if host_platform.startswith("windows") else "clang",
        link="link.exe" if host_platform.startswith("windows") else "clang",
    )

    if args.target == "targets":
        for target in isg.list_configured_targets():
            if isinstance(target, Path):
                target = target.relative_to(isg.rootdir)
            print(target)
    else:
        try:
            if args.dump_graph:
                print(
                    isg.dump_graph(args.target, display_configured=True, display_relative_path=True)
                )
            isg.run(args.target)
        except isengard.IsengardRunError as exc:
            if args.debug:
                raise
            else:
                raise SystemExit(f"Run has failed: {exc}")
