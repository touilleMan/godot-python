import os
import sys
import platform
from pathlib import Path
import subprocess
import shutil


PROJECT_DIR = Path(__file__).resolve().parent
SKIP_EXTENSION_BUILD = "SKIP_EXTENSION_BUILD" in os.environ
if SKIP_EXTENSION_BUILD:
    print("`SKIP_EXTENSION_BUILD` is set, skipping `my.pyx` extension build")
    raise SystemExit(0)


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


if platform.system() == "Windows":
    python_path = PROJECT_DIR / "addons/pythonscript/windows-x86_64/python.exe"
    lib_pattern = "my.*.pyd"
elif platform.system() == "Darwin":
    python_path = PROJECT_DIR / "addons/pythonscript/macos-x86_64/bin/python3"
    lib_pattern = "my.*.dylib"
else:
    assert platform.system() == "Linux"
    python_path = PROJECT_DIR / "addons/pythonscript/linux-x86_64/bin/python3"
    lib_pattern = "my.*.so"


embedded_version = subprocess.check_output([str(python_path), "--version"]).strip()
host_version = subprocess.check_output([sys.executable, "--version"]).strip()
if embedded_version != host_version:
    BOLD_RED = "\x1b[1;31m"
    NO_COLOR = "\x1b[0;0m"
    print(
        f"{BOLD_RED}"
        "WARNING: Python extension loading may fail: host and embedded versions differ"
        f" (host: {host_version.decode().strip()}, embedded: {embedded_version.decode().strip()})"
        f"{NO_COLOR}"
    )


cmd = [sys.executable, "setup.py", "build_ext", "--build-lib", str(PROJECT_DIR)]
print(" ".join(cmd))
subprocess.check_call(cmd, cwd=PROJECT_DIR)


# Finally remove the platform info from the shared library, this is to avoid
# annoying update everytime we change CPython embedded version.
lib_candidates = list(PROJECT_DIR.glob(lib_pattern))
assert len(lib_candidates) == 1, lib_candidates
lib = lib_candidates[0]
lib_new_name = f"my{lib.suffix}"
print(f"renaming {lib.name} -> {lib_new_name}")
shutil.move(lib, lib.parent / lib_new_name)
