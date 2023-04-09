import platform
from pathlib import Path
import subprocess
import shutil


PROJECT_DIR = Path(__file__).resolve().parent


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

cmd = [str(python_path), "setup.py", "build_ext", "--build-lib", str(PROJECT_DIR)]
print(" ".join(cmd))
subprocess.check_call(cmd, cwd=PROJECT_DIR)


# Finally remove the platform info from the shared library, this is to avoid
# annoying update everytime we change CPython embedded version.
lib_candidates = list(PROJECT_DIR.glob(lib_pattern))
assert len(lib_candidates) == 1, lib_candidates
lib = lib_candidates[0]
lib_new_name = f"my{lib.suffix}"
print(f"rename {lib.name} -> {lib_new_name}")
shutil.move(lib, lib.parent / lib_new_name)
