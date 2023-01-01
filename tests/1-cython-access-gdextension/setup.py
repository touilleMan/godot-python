from setuptools import setup
from Cython.Build import cythonize

ext_modules = cythonize("my.pyx")
# ext_modules[0].extra_compile_args=['/Zi', '/Od'], # generate PDB, disable optimization
# ext_modules[0].extra_link_args=['/DEBUG'], # preserve debug info
# Work around cythonize's `include_path` parameter not configuring the C compiler
# (see: https://github.com/cython/cython/issues/1480)
ext_modules[0].include_dirs = ["./godot_headers"]
setup(
    ext_modules=ext_modules,
)
