#! /usr/bin/env python3

import argparse
from pathlib import Path
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--godot-headers", type=Path, required=True)
    args = parser.parse_args()

    config_path: Path = args.godot_headers / "extension_api.json"
    config = json.loads(config_path.read_text(encoding="utf8"))

    header = config["header"]
    prefix = "Godot Engine v"
    assert header["version_full_name"].startswith(prefix)
    print(header["version_full_name"][len(prefix) :])
    print(header["version_major"])
    print(header["version_minor"])
