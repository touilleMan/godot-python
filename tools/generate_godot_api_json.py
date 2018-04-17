#! /usr/bin/env python3

import argparse
import json
import subprocess
import tempfile


def generate_json_api(godot_bin, output):
    with tempfile.NamedTemporaryFile() as x:
        ret = subprocess.call([godot_bin, "--gdnative-generate-json-api", x.name])
        assert ret == 0
        data = json.loads(x.read())
    try:
        subprocess.check_output([godot_bin, "--version"])
    except subprocess.CalledProcessError as exc:
        assert exc.returncode == 255  # Godot is supposed to return this...
        version = exc.output.decode().strip()
    return {"version": version, "content": data}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract the Godot api as a JSON with version"
    )
    parser.add_argument("godot_bin", help="Path to Godot binary")
    parser.add_argument("--output", "-o", default="godot_api.gen.json")
    args = parser.parse_args()

    api = generate_json_api(args.godot_bin, args.output)
    with open(args.output, "w") as fd:
        json.dump(api, fd, indent=True)
