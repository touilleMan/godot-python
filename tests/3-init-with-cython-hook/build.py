import os
import sys
from pathlib import Path
import subprocess


PROJECT_DIR = Path(__file__).resolve().parent
SKIP_EXTENSION_BUILD = "SKIP_EXTENSION_BUILD" in os.environ
if SKIP_EXTENSION_BUILD:
    print("`SKIP_EXTENSION_BUILD` is set, skipping `my.pyx` extension build")
    raise SystemExit(0)


cmd = [sys.executable, "setup.py", "build_ext", "--build-lib", str(PROJECT_DIR)]
print(" ".join(cmd))
subprocess.check_call(
    cmd,
    cwd=PROJECT_DIR,
)
