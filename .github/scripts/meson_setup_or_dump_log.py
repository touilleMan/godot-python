import sys
import subprocess

cmd = ["meson", "setup", *sys.argv[1:]]
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as exc:
    print()
    print("### meson-logs/meson-log.txt ###")
    try:
        print(open("build/meson-logs/meson-log.txt").read())
    except FileNotFoundError:
        pass
    sys.exit(exc.returncode)
