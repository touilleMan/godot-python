# Here we run the build with the Python from the host development environment
# (i.e. not the embedded Python that will run the extension).
#
# The reason for this is the embedded Python has issues building native extensions
# since it has been compiled in a totally different environment that the one
# it runs on, leading to incorrect flags passed during extension compilation
# (see https://github.com/indygreg/python-build-standalone/issues/152).
#
# So instead we have to rely on the Python from the development environment, which
# of course means its version (and platform !) must be the same to preserve ABI
# compatibility.


from setuptools import Extension, setup
from pathlib import Path
import platform
import subprocess
from Cython.Build import cythonize


PROJECT_DIR = Path(__file__).resolve().parent
GDEXTENSION_API_INCLUDE_DIR = PROJECT_DIR / "gdextension_api"


match platform.machine().lower():
    case "x86" | "x86_64" as cpu:
        pass
    case "amd64" | "x64":
        cpu = "x86_64"
    case unknown:
        raise SystemExit(f"Unknown CPU architecture {unknown}")


match platform.system():
    case "Windows":
        embedded_platform_path = PROJECT_DIR / f"addons/gdpy/windows-{cpu}"
        embedded_libgdpy_path = embedded_platform_path / "libgdpy.lib"
        embedded_python_path = embedded_platform_path / "python.exe"
        embedded_site_packages_path = embedded_platform_path / "Lib/site-packages/"
        # lib_pattern = "my.*.pyd"

    case "Linux":
        embedded_platform_path = PROJECT_DIR / f"addons/gdpy/linux-{cpu}"
        embedded_libgdpy_path = embedded_platform_path / "libgdpy.so"
        embedded_python_path = embedded_platform_path / "bin/python3"
        embedded_site_packages_path = next(embedded_platform_path.glob("lib/python*/site-packages"))
        # lib_pattern = "my.*.so"

    case "iOS":
        embedded_platform_path = PROJECT_DIR / f"addons/gdpy/macos-{cpu}"
        embedded_libgdpy_path = embedded_platform_path / "libgdpy.dylib"
        embedded_python_path = embedded_platform_path / "bin/python3"
        embedded_site_packages_path = next(embedded_platform_path.glob("lib/python*/site-packages"))
        # lib_pattern = "my.*.dylib"

    case unknown:
        raise SystemExit(f"Unknown platform `{unknown}`")


# Sanity check to ensure host and embedded Python are compatible
host_python_version = platform.python_version_tuple()
embedded_python_version = tuple(
    subprocess.check_output([str(embedded_python_path), "--version"])
    .decode()
    .strip()
    .removeprefix("Python ")
    .split(".")
)
if host_python_version == embedded_python_version:
    pass
elif host_python_version[:2] == embedded_python_version[:2]:  # Different
    BOLD_RED = "\x1b[1;31m"
    NO_COLOR = "\x1b[0;0m"
    print(
        f"{BOLD_RED}"
        "WARNING: Python extension loading may fail: host and embedded versions differ"
        f" (host: {host_python_version}, embedded: {embedded_python_version})"
        f"{NO_COLOR}"
    )
else:
    BOLD_RED = "\x1b[1;31m"
    NO_COLOR = "\x1b[0;0m"
    raise SystemExit(
        f"{BOLD_RED}"
        "Python extension loading may fail: host and embedded versions differ"
        f" (host: {host_python_version}, embedded: {embedded_python_version})"
        f"{NO_COLOR}"
    )


extensions = [
    Extension(
        "*",
        ["my.pyx"],
        # C/C++ includes
        include_dirs=[str(GDEXTENSION_API_INCLUDE_DIR)],
        # libgdpy contains the Godot C API's pointers, must link to it
        extra_link_args=[str(embedded_libgdpy_path)],
    ),
]
setup(
    name="My hello app",
    ext_modules=cythonize(
        extensions,
        # Cython .pxd includes (env var is defined in `build.py`)
        include_path=[str(embedded_site_packages_path)],
    ),
)
