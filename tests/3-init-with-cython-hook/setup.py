from setuptools import Extension, setup
from Cython.Build import cythonize
from pathlib import Path


gdextension_api_include_dir = Path("gdextension_api")
extensions = [
    Extension(
        "*",
        ["my.pyx"],
        # C/C++ includes
        include_dirs=[str(gdextension_api_include_dir.absolute())],
    ),
]
setup(
    name="My hello app",
    ext_modules=cythonize(extensions),
)
