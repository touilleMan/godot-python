import platform
from pathlib import Path
import subprocess


PROJECT_DIR = Path(__file__).resolve().parent
GODOT_HEADERS_DIR = PROJECT_DIR / "godot_headers"


if platform.system() == "Windows":
    cmd = ["cl.exe", "/DEBUG", "/LD", "my.c", "/I", str(GODOT_HEADERS_DIR)]
elif platform.system() == "Darwin":
    cmd = [
        "cc",
        "-g",
        "-fPIC",
        "-shared",
        "-c",
        "my.c",
        "-o",
        "my.so",
        "-I",
        str(GODOT_HEADERS_DIR),
    ]
else:
    assert platform.system() == "Linux"
    cmd = [
        "cc",
        "-g",
        "-fPIC",
        "-shared",
        "-c",
        "my.c",
        "-o",
        "my.so",
        "-I",
        str(GODOT_HEADERS_DIR),
    ]

print(f"cd {PROJECT_DIR} && " + " ".join(cmd))
subprocess.check_call(cmd, cwd=PROJECT_DIR)
