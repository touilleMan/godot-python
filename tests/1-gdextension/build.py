import platform
from pathlib import Path
import subprocess


PROJECT_DIR = Path(__file__).resolve().parent
GDEXTENSION_DIR = PROJECT_DIR / "gdextension_api"


if platform.system() == "Windows":
    cmd = ["cl.exe", "/DEBUG", "/LD", "my.c", "/I", str(GDEXTENSION_DIR)]
    print(f"cd {PROJECT_DIR} && " + " ".join(cmd))
    subprocess.check_call(cmd, cwd=PROJECT_DIR)

else:
    assert platform.system() in ("Linux", "Darwin")

    cmd = [
        "cc",
        "-g",
        "-fPIC",
        "-c",
        "my.c",
        "-o",
        "my.o",
        "-I",
        str(GDEXTENSION_DIR),
    ]
    print(f"cd {PROJECT_DIR} && " + " ".join(cmd))
    subprocess.check_call(cmd, cwd=PROJECT_DIR)

    cmd = ["cc", "my.o", "-shared", "-o", "my.so"]
    print(f"cd {PROJECT_DIR} && " + " ".join(cmd))
    subprocess.check_call(cmd, cwd=PROJECT_DIR)
