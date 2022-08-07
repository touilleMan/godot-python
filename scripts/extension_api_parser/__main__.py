"""
Helper to debug the parser
"""

import sys
from pathlib import Path

from . import parse_extension_api_json, BuildConfig


parse_extension_api_json(Path(sys.argv[1]), BuildConfig.DOUBLE_64)
