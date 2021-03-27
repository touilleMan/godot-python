import os
import argparse
import json
import re
from warnings import warn
from keyword import iskeyword
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, replace
from typing import Optional, Dict, List, Tuple

from type_specs import TypeSpec, ALL_TYPES_EXCEPT_OBJECTS


BASEDIR = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(f"{BASEDIR}/bindings_templates"), trim_blocks=True, lstrip_blocks=True
)


@dataclass
class PropertyInfo:
    name: str
    type: TypeSpec
    getter: str
    setter: str
    index: Optional[int]

    # If using feature we don't support yet
    unsupported_reason: Optional[str] = None

    @property
    def is_supported(self) -> bool:
        return self.unsupported_reason is None


@dataclass
class ArgumentInfo:
    name: str
    type: TypeSpec
    default_value: Optional[str]

    @property
    def has_default_value(self):
        return self.default_value is not None


@dataclass
class SignalInfo:
    name: str
    arguments: List[ArgumentInfo]

    # If using feature we don't support yet
    unsupported_reason: Optional[str] = None

    @property
    def is_supported(self) -> bool:
        return self.unsupported_reason is None


@dataclass
class MethodInfo:
    name: str
    return_type: TypeSpec
    is_editor: bool
    is_noscript: bool
    is_const: bool
    is_reverse: bool
    is_virtual: bool
    has_varargs: bool
    is_from_script: bool
    arguments: List[ArgumentInfo]

    # If using feature we don't support yet
    unsupported_reason: Optional[str] = None

    @property
    def is_supported(self) -> bool:
        return self.unsupported_reason is None


@dataclass
class EnumInfo:
    name: str
    values: Dict[str, int]


@dataclass
class ClassInfo:
    # Cleaned up name (mainly ensure singleton classes have a leading underscore)
    name: str
    # Name as provided in api.json (needed to use GDNative's ClassDB)
    bind_register_name: str
    # Parent class name (also cleaned up)
    base_class: str
    singleton: Optional[str]
    instantiable: bool
    is_reference: bool
    constants: Dict[str, int]
    properties: List[PropertyInfo]
    signals: List[SignalInfo]
    methods: List[MethodInfo]
    enums: List[EnumInfo]


TYPES = {t.gdapi_type: t for t in ALL_TYPES_EXCEPT_OBJECTS}


# Basically provide enough to run the tests and the pong demo
SAMPLE_CLASSES = {
    "Object",
    "_ProjectSettings",
    "_Input",
    "_InputMap",
    "MainLoop",
    "SceneTree",
    "Node",
    "CanvasItem",
    "Node2D",
    "Reference",
    "Resource",
    "OpenSimplexNoise",
    "CollisionObject2D",
    "Area2D",
    "ARVRInterface",
    "ARVRInterfaceGDNative",
    "Environment",
    "Viewport",
    "Script",
    "PluginScript",
    "GDScript",
    "Control",
    "Label",
    # "_ClassDB",
    # "_Engine",
    # "_Geometry",
    # "_JSON",
    "_OS",
    "_ResourceLoader",
    # "_ResourceSaver",
    # "_VisualScriptEditor",
    "SurfaceTool",
    "Mesh",
    "ArrayMesh",
    "Spatial",
    "VisualInstance",
    "GeometryInstance",
    "MeshInstance",
    # For REPL editor plugin
    "GlobalConstants",
    "EditorPlugin",
    "PackedScene",
    "BaseButton",
    "Button",
    "ToolButton",
    "Panel",
    "Container",
    "BoxContainer",
    "VBoxContainer",
    "HBoxContainer",
    "RichTextLabel",
    "LineEdit",
    "Font",
    "BitmapFont",
    "DynamicFont",
    "DynamicFontData",
    # Input event & friends stuff
    "InputEvent",
    "InputEventAction",
    "InputEventJoypadButton",
    "InputEventJoypadMotion",
    "InputEventMIDI",
    "InputEventScreenDrag",
    "InputEventScreenTouch",
    "InputEventWithModifiers",
    "InputEventGesture",
    "InputEventMagnifyGesture",
    "InputEventPanGesture",
    "InputEventKey",
    "InputEventMouse",
    "InputEventMouseButton",
    "InputEventMouseMotion",
}

SUPPORTED_TYPES = {
    "void",
    "godot_bool",
    "godot_int",
    "godot_real",
    "godot_string",
    "godot_variant",
    "godot_object",
    "godot_aabb",
    "godot_array",
    "godot_basis",
    "godot_color",
    "godot_dictionary",
    "godot_node_path",
    "godot_plane",
    "godot_quat",
    "godot_rect2",
    "godot_rid",
    "godot_transform",
    "godot_transform2d",
    "godot_vector2",
    "godot_vector3",
    "godot_pool_byte_array",
    "godot_pool_int_array",
    "godot_pool_real_array",
    "godot_pool_string_array",
    "godot_pool_vector2_array",
    "godot_pool_vector3_array",
    "godot_pool_color_array",
}


def pre_cook_patch_stuff(raw_data):
    for klass in raw_data:
        # see https://github.com/godotengine/godot/pull/40386
        if klass["name"] == "Reference":
            klass["is_reference"] = True
        for prop in klass["properties"]:
            prop["name"] = prop["name"].replace("/", "_")
            # see https://github.com/godotengine/godot/pull/40383
            if prop["type"] == "17/17:RichTextEffect":
                prop["type"] = "Array"
        for meth in klass["methods"]:
            if meth["is_noscript"]:
                warn(
                    f"`{klass['name']}.{meth['name']}` has `is_noscript=True`"
                    " (should never be the case...)"
                )
            if meth["is_from_script"]:
                warn(
                    f"`{klass['name']}.{meth['name']}` has `is_from_script=True`"
                    " (should never be the case...)"
                )


def post_cook_patch_stuff(classes):
    for klass in classes:
        # See https://github.com/godotengine/godot/issues/34254
        if klass.name == "_OS":
            for meth in klass.methods:
                if meth.name in (
                    "get_static_memory_usage",
                    "get_static_memory_peak_usage",
                    "get_dynamic_memory_usage",
                ):
                    meth.return_type.c_type = "uint64_t"


def strip_unsupported_stuff(classes):
    supported_classes = {k.name for k in classes}

    def _is_supported_type(specs):
        if specs.is_builtin:
            return specs.c_type in SUPPORTED_TYPES
        elif specs.is_object:
            return specs.cy_type in supported_classes
        else:
            return True

    for klass in classes:
        for meth in klass.methods:
            unsupported_reason = None
            # TODO: handle default param values
            # TODO: handle those flags
            if meth.is_editor:
                unsupported_reason = "attribute `is_editor=True` not supported"
            if meth.is_reverse:
                unsupported_reason = "attribute `is_reverse=True` not supported"
            if meth.has_varargs:
                unsupported_reason = "attribute `has_varargs=True` not supported"
            if not _is_supported_type(meth.return_type):
                unsupported_reason = f"return type {meth.return_type} not supported"
            bad_arg = next(
                (arg for arg in meth.arguments if not _is_supported_type(arg.type)), None
            )
            if bad_arg:
                unsupported_reason = f"argument type {bad_arg} not supported"

            if unsupported_reason:
                warn(f"Ignoring `{klass.name}.{meth.name}` ({unsupported_reason})")
                meth.unsupported_reason = unsupported_reason

        for prop in klass.properties:
            if not _is_supported_type(prop.type):
                unsupported_reason = f"property type {prop.type} not supported"
                warn(f"Ignoring property `{klass.name}.{prop.name}` ({unsupported_reason})")
                prop.unsupported_reason = unsupported_reason

        for signal in klass.signals:
            bad_arg = next(
                (arg for arg in signal.arguments if not _is_supported_type(arg.type)), None
            )
            if bad_arg:
                unsupported_reason = f"argument type {bad_arg} not supported"
                warn(f"Ignoring signal `{klass.name}.{signal.name}` ({unsupported_reason})")
                signal.unsupported_reason = unsupported_reason


def strip_sample_stuff(classes):
    def _is_supported(type):
        return not type.is_object or type.cy_type in SAMPLE_CLASSES

    classes2 = [klass for klass in classes if klass.name in SAMPLE_CLASSES]
    for klass in classes2:
        klass.methods = [
            meth
            for meth in klass.methods
            if all(_is_supported(arg.type) for arg in meth.arguments)
            and _is_supported(meth.return_type)
        ]
        klass.signals = [
            signal
            for signal in klass.signals
            if all(_is_supported(arg.type) for arg in signal.arguments)
        ]
        klass.properties = [prop for prop in klass.properties if _is_supported(prop.type)]

    classes[:] = classes2


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def build_class_renames(data):
    renames = {"": ""}
    for item in data:
        old_name = item["name"]
        # In api.json, some singletons have underscore and others don't (
        # e.g. ARVRServer vs _OS). But to access them with `get_singleton_object`
        # we always need the name without underscore...
        if item["singleton"] and not old_name.startswith("_"):
            new_name = f"_{old_name}"
        else:
            new_name = old_name
        renames[old_name] = new_name
    return renames


def cook_data(data):
    classes = []
    constants = {}

    class_renames = build_class_renames(data)

    def _cook_type(type_):
        try:
            return TYPES[type_]
        except KeyError:
            if type_.startswith("enum."):
                # typically somethin like ``enum.AnimationTree::AnimationProcessMode``
                pcls, ecls = re.match(r"enum.(\w+)::(\w+)", type_).groups()
                return TypeSpec(
                    gdapi_type=type_,
                    c_type="godot_int",
                    cy_type="godot_int",
                    py_type=f"{class_renames[pcls]}.{ecls}",
                    is_base_type=True,
                    is_stack_only=True,
                    is_enum=True,
                )

            # TODO: improve handling of resources
            if "," in type_:
                return TypeSpec(
                    gdapi_type=type_,
                    c_type="godot_object",
                    cy_type="Resource",
                    py_type=f"Union[{','.join([class_renames[x] for x in type_.split(',')])}]",
                    is_object=True,
                )
            else:
                return TypeSpec(
                    gdapi_type=type_,
                    c_type="godot_object",
                    cy_type=class_renames[type_],
                    is_object=True,
                )

    def _cook_name(name):
        if iskeyword(name) or name in ("char", "bool", "int", "float", "short", "type"):
            return f"{name}_"
        else:
            return name

    def _cook_default_value(type, value, has_default_value):
        if not has_default_value:
            return None
        # Mostly ad-hoc stuff given default values format in api.json is broken
        if type in ("godot_bool", "godot_int", "godot_real", "godot_variant"):
            if value == "Null":
                return "None"
            else:
                return value
        elif type == "godot_string":
            return f'"{value}"'
        elif type == "godot_object" and value in ("[Object:null]", "Null"):
            return "None"
        elif type == "godot_dictionary" and value == "{}":
            return "Dictionary()"
        elif type == "godot_vector2":
            return f"Vector2{value}"
        elif type == "godot_rect2":
            return f"Rect2{value}"
        elif type == "godot_vector3":
            return f"Vector3{value}"
        elif type == "godot_transform" and value == "1, 0, 0, 0, 1, 0, 0, 0, 1 - 0, 0, 0":
            return (
                "Transform(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))"
            )
        elif type == "godot_transform2d" and value == "((1, 0), (0, 1), (0, 0))":
            return "Transform2D(Vector2(1, 0), Vector2(0, 1), Vector2(0, 0))"
        elif value == "[RID]":
            return "RID()"
        elif type == "godot_color":
            return f"Color({value})"
        elif type == "godot_pool_color_array" and value == "[PoolColorArray]":
            return "PoolColorArray()"
        elif type == "godot_array" and value == "[]":
            return f"Array()"
        elif type == "godot_pool_vector2_array" and value == "[]":
            return f"PoolVector2Array()"
        elif type == "godot_pool_vector3_array" and value == "[]":
            return f"PoolVector3Array()"
        elif type == "godot_pool_int_array" and value == "[]":
            return f"PoolIntArray()"
        elif type == "godot_pool_real_array" and value == "[]":
            return f"PoolRealArray()"
        elif type == "godot_pool_string_array" and value == "[]":
            return f"PoolStringArray()"
        elif value == "Null":
            return "None"
        else:
            warn(f"Unknown default arg value: type=`{type}`, value=`{value}`")
            return "None"

    for cls_data in data:
        if cls_data["name"] == "GlobalConstants":
            constants = cls_data["constants"]
            continue

        cls_info = {
            "bind_register_name": cls_data["name"],
            "name": class_renames[cls_data["name"]],
            "base_class": class_renames[cls_data["base_class"]],
            "instantiable": cls_data["instanciable"],
            "is_reference": cls_data["is_reference"],
            "constants": cls_data["constants"],
            "properties": [],
            "signals": [],
            "methods": [],
            "enums": [],
        }

        if cls_data["singleton"]:
            # Strip the leading underscore
            cls_info["singleton"] = cls_info["name"][1:]
        else:
            cls_info["singleton"] = None

        for prop_data in cls_data["properties"]:
            cls_info["properties"].append(
                PropertyInfo(
                    name=_cook_name(prop_data["name"]),
                    type=_cook_type(prop_data["type"]),
                    getter=prop_data["getter"],
                    setter=prop_data["setter"],
                    index=prop_data["index"] if prop_data["index"] != -1 else None,
                )
            )

        for signal_data in cls_data["signals"]:
            args_info = [
                ArgumentInfo(
                    name=_cook_name(arg_data["name"]),
                    type=_cook_type(arg_data["type"]),
                    default_value=None,
                )
                for arg_data in signal_data["arguments"]
            ]
            if any(arg_data["default_value"] != "" for arg_data in signal_data["arguments"]):
                warn(
                    f"{cls_info['name']}.{signal_data['name']}: default value are not supported for signals"
                )
            cls_info["signals"].append(
                SignalInfo(name=_cook_name(signal_data["name"]), arguments=args_info)
            )

        for meth_data in cls_data["methods"]:
            args_info = [
                ArgumentInfo(
                    name=_cook_name(arg_data["name"]),
                    type=_cook_type(arg_data["type"]),
                    default_value=_cook_default_value(
                        _cook_type(arg_data["type"]).c_type,
                        arg_data["default_value"],
                        arg_data["has_default_value"],
                    ),
                )
                for arg_data in meth_data["arguments"]
            ]
            meth_info = {
                "name": _cook_name(meth_data["name"]),
                "return_type": _cook_type(meth_data["return_type"]),
                "is_editor": meth_data["is_editor"],
                "is_noscript": meth_data["is_noscript"],
                "is_const": meth_data["is_const"],
                "is_reverse": meth_data["is_reverse"],
                "is_virtual": meth_data["is_virtual"],
                "has_varargs": meth_data["has_varargs"],
                "is_from_script": meth_data["is_from_script"],
                "arguments": args_info,
            }
            cls_info["methods"].append(MethodInfo(**meth_info))

        for enum_data in cls_data["enums"]:
            cls_info["enums"].append(
                EnumInfo(name=_cook_name(enum_data["name"]), values=enum_data["values"])
            )

        classes.append(ClassInfo(**cls_info))

    # Order classes by inheritance
    inheritances = defaultdict(list)
    for klass in classes:
        inheritances[klass.base_class].append(klass)
    sorted_classes = [*inheritances[""]]
    todo_base_classes = [*inheritances[""]]
    while todo_base_classes:
        base_class = todo_base_classes.pop()
        children_classes = inheritances[base_class.name]
        todo_base_classes += children_classes
        sorted_classes += children_classes

    return sorted_classes, constants


def load_bindings_specs_from_api_json(
    api_json: dict, sample: bool
) -> Tuple[List[ClassInfo], Dict[str, int]]:
    pre_cook_patch_stuff(api_json)
    classes, constants = cook_data(api_json)
    if sample:
        strip_sample_stuff(classes)
    strip_unsupported_stuff(classes)
    post_cook_patch_stuff(classes)
    return classes, constants


def generate_bindings(
    no_suffix_output_path: str, classes_specs: List[ClassInfo], constants_specs: Dict[str, int]
):
    pyx_output_path = f"{no_suffix_output_path}.pyx"
    print(f"Generating {pyx_output_path}")
    template = env.get_template("bindings.tmpl.pyx")
    out = template.render(classes=classes_specs, constants=constants_specs)
    with open(pyx_output_path, "w") as fd:
        fd.write(out)

    pyi_output_path = f"{no_suffix_output_path}.pyi"
    print(f"Generating {pyi_output_path}")
    template = env.get_template("bindings.tmpl.pyi")
    out = template.render(classes=classes_specs, constants=constants_specs)
    with open(pyi_output_path, "w") as fd:
        fd.write(out)

    pxd_output_path = f"{no_suffix_output_path}.pxd"
    print(f"Generating {pxd_output_path}")
    template = env.get_template("bindings.tmpl.pxd")
    out = template.render(classes=classes_specs, constants=constants_specs)
    with open(pxd_output_path, "w") as fd:
        fd.write(out)


if __name__ == "__main__":

    def _parse_output(val):
        suffix = ".pyx"
        if not val.endswith(suffix):
            raise argparse.ArgumentTypeError(f"Must have a `{suffix}` suffix")
        return val[: -len(suffix)]

    parser = argparse.ArgumentParser(description="Generate godot api bindings bindings files")
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="API_PATH",
        type=argparse.FileType("r", encoding="utf8"),
        help="Path to Godot api.json file",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        metavar="BINDINGS_PYX",
        type=_parse_output,
        help="Path to store the generated bindings.pyx (also used to determine .pxd/.pyi output path)",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Generate a subset of the bindings (faster to build, useful for dev)",
    )
    args = parser.parse_args()
    api_json = json.load(args.input)
    classes_specs, constants_specs = load_bindings_specs_from_api_json(api_json, args.sample)
    generate_bindings(args.output, classes_specs, constants_specs)
