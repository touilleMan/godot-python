#! /usr/bin/env python3

import argparse
from typing import List, Dict, Tuple
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from extension_api_parser import BuildConfig, parse_extension_api_json


BASEDIR = Path(__file__).parent
GODOT_DIR = BASEDIR / "../src/godot"
HAZMAT_DIR = GODOT_DIR / "hazmat"
TARGETS: Dict[str, Tuple[bool, Path]] = {
    "gdnative_ptrs.pxd": (False, HAZMAT_DIR),
    "gdnative_ptrs.pyx": (False, HAZMAT_DIR),
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


# Subset of tlasses to use when generating the project for test&debug purpose,
# this makes compilation much faster !
GODOT_CLASSES_SAMPLE = {
    "ArrayMesh",
    "CallbackTweener",
    "Camera2D",
    "Camera3D",
    "CameraAttributes",
    "CanvasItem",
    "ClassDB",
    "ConcavePolygonShape3D",
    "Control",
    "ConvexPolygonShape3D",
    "Engine",
    "Environment",
    "Font",
    "Image",
    "InputEvent",
    "IntervalTweener",
    "MainLoop",
    "Material",
    "Mesh",
    "MethodTweener",
    "MultiMesh",
    "MultiplayerAPI",
    "MultiplayerPeer",
    "Node",
    "Node2D",
    "Node3D",
    "Node3DGizmo",
    "OS",
    "Object",
    "PackedScene",
    "PacketPeer",
    "PhysicsDirectSpaceState2D",
    "PhysicsDirectSpaceState3D",
    "PhysicsPointQueryParameters2D",
    "PhysicsPointQueryParameters3D",
    "PhysicsRayQueryParameters2D",
    "PhysicsRayQueryParameters3D",
    "PhysicsShapeQueryParameters2D",
    "PhysicsShapeQueryParameters3D",
    "ProjectSettings",
    "PropertyTweener",
    "RefCounted",
    "Resource",
    "ResourceFormatLoader",
    "ResourceFormatSaver",
    "ResourceImporter",
    "SceneState",
    "SceneTree",
    "SceneTreeTimer",
    "Script",
    "ScriptExtension",
    "ScriptLanguage",
    "Shape2D",
    "Shape3D",
    "Sky",
    "StyleBox",
    "TextServer",
    "Texture",
    "Texture2D",
    "Theme",
    "TriangleMesh",
    "Tween",
    "Tweener",
    "Viewport",
    "ViewportTexture",
    "Window",
    "World2D",
    "World3D",
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

    todo: List[Tuple[Path, str, Path]] = []
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
        todo.append((output, template_name, template_home))

    if need_classes:
        if args.classes_sample:
            filter_classes = GODOT_CLASSES_SAMPLE
        else:
            filter_classes = False  # keep all classes
    else:
        filter_classes = True

    api = parse_extension_api_json(
        path=args.input, build_config=BuildConfig(args.build_config), filter_classes=filter_classes
    )

    for todo_output, todo_template_name, todo_template_home in todo:
        env = make_jinja_env(todo_template_home)
        template = env.get_template(todo_template_name)
        code = template.render(api=api)
        todo_output.write_text(code, encoding="utf8")
