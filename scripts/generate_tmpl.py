#! /usr/bin/env python3

import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from extension_api_parser import BuildConfig, parse_extension_api_json, ExtensionApi


BASEDIR = Path(__file__).parent


def make_jinja_env(import_dir: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(import_dir),
        trim_blocks=True,
        lstrip_blocks=False,
        extensions=["jinja2.ext.loopcontrols"],
        undefined=StrictUndefined,
    )
    env.filters["merge"] = lambda x, **kwargs: {**x, **kwargs}
    return env


def generate_gdapi_pxd(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot/hazmat")
    template = env.get_template("gdapi.pxd.j2")
    return template.render(api=api)


def generate_gdapi_ptrs(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot/hazmat")
    template = env.get_template("gdapi_ptrs.pxi.j2")
    return template.render(api=api)


def generate_builtins_pxd(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot")
    template = env.get_template("builtins.pxd.j2")
    return template.render(api=api)


def generate_builtins_pyx(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot")
    template = env.get_template("builtins.pyx.j2")
    return template.render(api=api)


def generate_builtins_pyi(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot")
    template = env.get_template("builtins.pyi.j2")
    return template.render(api=api)


def generate_classes_pxd(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot")
    template = env.get_template("classes.pxd.j2")
    return template.render(api=api)


def generate_classes_pyx(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot")
    template = env.get_template("classes.pyx.j2")
    return template.render(api=api)


def generate_classes_pyi(api: ExtensionApi) -> str:
    env = make_jinja_env(BASEDIR / "../src/godot")
    template = env.get_template("classes.pyi.j2")
    return template.render(api=api)


OUTPUT_TO_FN = {
    "gdapi.pxd": generate_gdapi_pxd,
    "gdapi_ptrs.pxi": generate_gdapi_ptrs,
    "builtins.pxd": generate_builtins_pxd,
    "builtins.pyx": generate_builtins_pyx,
    "builtins.pyi": generate_builtins_pyi,
    "classes.pxd": generate_classes_pxd,
    "classes.pyx": generate_classes_pyx,
    "classes.pyi": generate_classes_pyi,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code from templates")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="EXTENSION_API_PATH",
        type=Path,
        help="Path to Godot extension_api.json file",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
        help=f"pyx/pxd/pyi to generate (choices: {', '.join(OUTPUT_TO_FN.keys())})",
    )
    parser.add_argument(
        "--build-config",
        required=True,
        choices=[x.value for x in BuildConfig],
        metavar="CONFIG",
    )

    args = parser.parse_args()

    api = parse_extension_api_json(path=args.input, build_config=BuildConfig(args.build_config))

    # We use # in the name to simulate folder hierarchy in the meson build
    *_, name = args.output.name.rsplit("#", 1)
    code = OUTPUT_TO_FN[name](api)
    args.output.write_text(code, encoding="utf8")