#! /usr/bin/env python3

from __future__ import annotations
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from extension_api_parser import BuildConfig, parse_extension_api_json


BASEDIR = Path(__file__).parent
SRC_DIR = BASEDIR / "../src"
GODOT_DIR = SRC_DIR / "godot"
HAZMAT_DIR = GODOT_DIR / "hazmat"
TARGETS: dict[str, tuple[bool, Path]] = {
    "pythonscript_gdextension_ptrs.c": (False, SRC_DIR),
    "gdptrs.pxd": (False, HAZMAT_DIR),
    "gdtypes.pxd": (False, HAZMAT_DIR),
    "gdapi.pxd": (False, HAZMAT_DIR),
    "builtins.pyi": (False, GODOT_DIR),
    "builtins.pxd": (True, GODOT_DIR),
    "builtins.pyx": (True, GODOT_DIR),
    "classes.pyi": (True, GODOT_DIR),
    "classes.pxd": (True, GODOT_DIR),
    "classes.pyx": (True, GODOT_DIR),
    "conversion.pyx": (False, GODOT_DIR),
    "conversion.pxd": (False, GODOT_DIR),
}


# Subset of classes to use when generating the project for test&debug purpose,
# this makes compilation much faster !
GODOT_CLASSES_SAMPLE = {
    "Camera2D",
    "CameraAttributes",
    "CanvasItem",
    "ClassDB",
    "Control",
    "Engine",
    "Environment",
    "Font",
    "Image",
    "InputEvent",
    "MainLoop",
    "Node",
    "Node2D",
    "OS",
    "Object",
    "ProjectSettings",
    "RefCounted",
    "Resource",
    "ResourceFormatLoader",
    "ResourceFormatSaver",
    "ResourceImporter",
    "SceneState",
    "SceneTree",
    "Script",
    "ScriptExtension",
    "ScriptLanguage",
    "Shape2D",
    "TextServer",
    "Texture",
    "Texture2D",
    "World2D",
}
GODOT_BUILTINS_SAMPLE = {
    "String",
    "StringName",
    "NodePath",
    "Vector2i",
    "Array",
    "Dictionary",
    "PackedStringArray",
    "Callable",
    "Signal",
}


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
        "--classes-sample",
        action="store_true",
    )
    parser.add_argument(
        "--builtins-sample",
        action="store_true",
    )
    parser.add_argument(
        "--build-config",
        required=True,
        choices=[x.value for x in BuildConfig],
        metavar="CONFIG",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
        nargs="+",
        help=f"pyx/pxd/pyi to generate (choices: {', '.join(TARGETS.keys())})",
    )

    args = parser.parse_args()

    items: list[tuple[Path, str, Path]] = []
    need_classes = False
    for output in args.output:
        # We use # in the name to simulate folder hierarchy in the meson build
        *_, name = output.name.rsplit("#", 1)
        try:
            template_need_classes, template_home = TARGETS[name]
        except KeyError:
            raise SystemExit(f"Unknown output, valid values: {', '.join(TARGETS.keys())}")
        need_classes |= template_need_classes
        template_name = f"{name}.j2"
        items.append((output, template_name, template_home))

    filter_builtins: set[str] | None
    if args.builtins_sample:
        filter_builtins = GODOT_BUILTINS_SAMPLE
    else:
        filter_builtins = None  # Keep all builtins

    filter_classes: bool | set[str]
    if need_classes:
        if args.classes_sample:
            filter_classes = GODOT_CLASSES_SAMPLE
        else:
            filter_classes = False  # Keep all classes
    else:
        filter_classes = True

    api = parse_extension_api_json(
        path=args.input,
        build_config=BuildConfig(args.build_config),
        filter_builtins=filter_builtins,
        filter_classes=filter_classes,
    )

    for item_output, item_template_name, item_template_home in items:
        env = make_jinja_env(item_template_home)
        template = env.get_template(item_template_name)
        code = template.render(api=api)
        item_output.write_text(code, encoding="utf8")
