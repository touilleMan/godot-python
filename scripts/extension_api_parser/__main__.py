"""
Helper to debug the parser
"""

import os
import sys
from pathlib import Path

from . import parse_extension_api_json, BuildConfig


try:
    extension_api_path = Path(sys.argv[1])
except IndexError:
    extension_api_path = (
        (Path(__file__).parent / "../../godot_headers/extension_api.json")
        .resolve()
        .relative_to(os.getcwd())
    )


try:
    build_configs = [BuildConfig(sys.argv[2])]
except IndexError:
    build_configs = BuildConfig


for build_config in build_configs:
    print(f"Checking {extension_api_path} with config {build_config.value}")
    parse_extension_api_json(extension_api_path, build_config)
