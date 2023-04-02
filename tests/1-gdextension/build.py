import platform
from pathlib import Path
import subprocess
import shutil


PROJECT_DIR = Path(__file__).resolve().parent
GDEXTENSION_DIR = PROJECT_DIR / "gdextension_api"


if platform.system() == "Windows":
    if not shutil.which("cl.exe"):
        raise SystemExit(
            "`cl.exe` command is missing, have you run `<Visual Studio Path>/vcvarsall.bat` ?"
        )

    cmd = ["cl.exe", "/DEBUG", "/LD", "my.c", "/I", str(GDEXTENSION_DIR)]
    print(f"cd {PROJECT_DIR} && " + " ".join(cmd))
    subprocess.check_call(cmd, cwd=PROJECT_DIR)

else:
    assert platform.system() in ("Linux", "Darwin")
    if not shutil.which("cc"):
        raise SystemExit("`cc` command is missing")

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
