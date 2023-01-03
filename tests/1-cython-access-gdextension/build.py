import platform
from pathlib import Path
import subprocess
import shutil
import zipfile
import tempfile

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


# with tempfile.TemporaryDirectory() as wheeldir:

#     # 1) Build the project into a wheel
#     # This is needed to have a build that takes the `pyproject.toml` into account
#     # and install the correct build depedencies beforehand.
#     cmd = [str(python_path), "-m", "pip", "wheel", "--wheel-dir", wheeldir, "."]
#     print(" ".join(cmd))
#     subprocess.check_call(cmd, cwd=PROJECT_DIR)

#     outputs = list(Path(wheeldir).iterdir())
#     if len(outputs) != 1:
#         raise RuntimeError(f"Target dir unexpectedly contains multiple or no files: {outputs}")
#     wheel_path = outputs[0]

#     # 2) Extract the .so from the wheel (only thing we care about).
#     with zipfile.ZipFile(wheel_path) as wheel:
#         for info in wheel.infolist():
#             info.filename.rsplit("/", 1)[-1].startswith("my.")
#             wheel.extract(info.filename, path=PROJECT_DIR)
#             break

# # 3) Finally remove the platform info from the shared library, this is to avoid
# # annoying update everytime we change CPython embedded version.
# lib_candidates = list(PROJECT_DIR.glob(lib_pattern))
# assert len(lib_candidates) == 1, lib_candidates
# lib = lib_candidates[0]
# lib_new_name = f"my{lib.suffix}"
# print(f"rename {lib.name} -> {lib_new_name}")
# shutil.move(lib, lib.parent / lib_new_name)
