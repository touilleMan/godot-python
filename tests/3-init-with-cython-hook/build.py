import os
import sys
from pathlib import Path
import subprocess


PROJECT_DIR = Path(__file__).resolve().parent
SKIP_EXTENSION_BUILD = "SKIP_EXTENSION_BUILD" in os.environ
if SKIP_EXTENSION_BUILD:
    print("`SKIP_EXTENSION_BUILD` is set, skipping `my.pyx` extension build")
    raise SystemExit(0)


# # Here we run the build with the Python from the host development environment
# # (i.e. not the embedded Python that will run the extension).
# #
# # The reason for this is the embedded Python has issues building native extensions
# # since it has been compiled in a totally different environment that the one
# # it runs on, leading to incorrect flags passed during extension compilation
# # (see https://github.com/indygreg/python-build-standalone/issues/152).
# #
# # So instead we have to rely on the Python from the development environment, which
# # of course means its version (and platform !) must be the same to preserve ABI
# # compatibility.

# match platform.machine().lower():
#     case "x86" | "x86_64" as cpu:
#         pass
#     case "amd64" | "x64":
#         cpu = "x86_64"
#     case unknown:
#         raise SystemExit(f"Unknown CPU architecture {unknown}")


# match platform.system():
#     case "Windows":
#         embedded_platform_path = PROJECT_DIR / f"addons/gdpy/windows-{cpu}"
#         embedded_libgdpy_path = embedded_platform_path / "libgdpy.dll"
#         embedded_python_path = embedded_platform_path / "python.exe"
#         lib_pattern = "my.*.pyd"

#     case "Linux":
#         embedded_platform_path = PROJECT_DIR / f"addons/gdpy/linux-{cpu}"
#         embedded_libgdpy_path = embedded_platform_path / "libgdpy.so"
#         embedded_python_path = embedded_platform_path / "bin/python3"
#         lib_pattern = "my.*.so"

#     case "iOS":
#         embedded_platform_path = PROJECT_DIR / f"addons/gdpy/macos-{cpu}"
#         embedded_libgdpy_path = embedded_platform_path / "libgdpy.dylib"
#         embedded_python_path = embedded_platform_path / "bin/python3"
#         lib_pattern = "my.*.dylib"

#     case unknown:
#         raise SystemExit(f"Unknown platform `{unknown}`")


# embedded_version = subprocess.check_output([str(embedded_python_path), "--version"]).decode().strip()
# host_version = subprocess.check_output([sys.executable, "--version"]).decode().strip()
# if embedded_version != host_version:
#     BOLD_RED = "\x1b[1;31m"
#     NO_COLOR = "\x1b[0;0m"
#     print(
#         f"{BOLD_RED}"
#         "WARNING: Python extension loading may fail: host and embedded versions differ"
#         f" (host: {host_version}, embedded: {embedded_version})"
#         f"{NO_COLOR}"
#     )


# match platform.system():
#     case "Windows":
#         embedded_site_packages_path = embedded_platform_path / "Lib/site-packages/"
#     case "Linux" | "iOS":
#         # `"Python 3.12.1"` -> `3, 12`
#         embedded_version_major, embedded_version_minor = map(
#             int, embedded_version.removeprefix("Python ").split(".")[:2]
#         )
#         embedded_site_packages_path = (
#             embedded_platform_path
#             / f"lib/python{embedded_version_major}.{embedded_version_minor}/site-packages/"
#         )
#     case unknown:
#         raise SystemExit(f"Unknown platform `{unknown}`")


cmd = [sys.executable, "setup.py", "build_ext", "--build-lib", str(PROJECT_DIR)]
print(" ".join(cmd))
subprocess.check_call(
    cmd,
    cwd=PROJECT_DIR,
    # env={
    #     **os.environ,
    #     "EMBEDDED_PLATFORM_PATH": str(embedded_platform_path),
    #     "EMBEDDED_SITE_PACKAGES_PATH": str(embedded_site_packages_path),
    # },
)


# # Finally remove the platform info from the shared library, this is to avoid
# # annoying update everytime we change CPython embedded version.
# lib_candidates = list(PROJECT_DIR.glob(lib_pattern))
# assert len(lib_candidates) == 1, lib_candidates
# lib = lib_candidates[0]
# lib_new_name = f"my{lib.suffix}"
# print(f"renaming {lib.name} -> {lib_new_name}")
# shutil.move(lib, lib.parent / lib_new_name)
