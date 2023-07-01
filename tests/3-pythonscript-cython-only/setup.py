import os
import platform
from setuptools import setup
from Cython.Build import cythonize
from pathlib import Path


# Retrieve `Python.h`'s include dir.
# In theory setuptools rely on `sysconfig` to find this information, `sysconfig` being
# generated when Python is installed (typically `make install` after it compilation).
# However we use python-build-standalone which (as it name imply) provide us with a
# standalone Python distribution, hence the install step is part of the build process
# and `sysconfig` provide irrelevant include paths (e.g. on Linux it is done on Docker
# with install in `/install`)
# See:
# - https://github.com/indygreg/python-build-standalone/issues/152
# - https://gregoryszorc.com/docs/python-build-standalone/main/quirks.html#references-to-build-time-paths
if platform.system() in ("Linux", "Darwin"):
    python_include_dir = next(Path(".").parent.glob("addons/pythonscript/*-*/include/python*"))
elif platform.system() == "Windows":
    python_include_dir = next(Path(".").parent.glob("addons/pythonscript/*-*/include"))
else:
    raise RuntimeError(f"Unsupported platform `{platform.system()}`")
# Same idea: `sysconfig` defines CC=clang, but who knows if the current machine has it !
os.environ.setdefault("CC", "cc")


# Work around cythonize's `include_path` parameter not configuring the C compiler
# (see: https://github.com/cython/cython/issues/1480)
gdextension_api_include_dir = Path("gdextension_api")


ext_modules = cythonize("my.pyx")
ext_modules[0].include_dirs = [
    python_include_dir,
    gdextension_api_include_dir,
]
setup(
    ext_modules=ext_modules,
)
