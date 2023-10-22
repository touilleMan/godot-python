import sys
from pathlib import Path
from typing import Iterable

from . import parse_extension_api_json, BuildConfig
from .type_spec import TYPES_DB


try:
    extension_api_path = Path(sys.argv[1])
except IndexError:
    raise SystemExit(
        "Usage: python -m extension_api_parser <path/to/extension_api.json> [float_32|double_32|float_64|double_64]"
    )

build_configs: Iterable[BuildConfig]
try:
    build_configs = [BuildConfig(sys.argv[2])]
except IndexError:
    build_configs = BuildConfig


for build_config in build_configs:
    initial_types_db = TYPES_DB.copy()
    print(f"Checking {extension_api_path} with config {build_config.value}")
    parse_extension_api_json(extension_api_path, build_config, filter_classes=False)
    TYPES_DB.clear()
    TYPES_DB.update(initial_types_db)
