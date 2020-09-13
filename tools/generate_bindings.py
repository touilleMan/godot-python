import os
import argparse
import json
import re
from warnings import warn
from keyword import iskeyword
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, replace
from typing import Optional, Dict, List


BASEDIR = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(f"{BASEDIR}/bindings_templates"), trim_blocks=True, lstrip_blocks=True
)


@dataclass
class Type:
    # Type used when calling C api functions
    c_type: str
    # Type used in Cython, basically similar to c_type for scalars&enums
    # and to py_type for Godot objects&builtins
    cy_type: str
    # Type used for PEP 484 Python typing
    py_type: str = None
    # Type is a Godot object (i.e. defined in api.json)
    is_object: bool = False
    # Type is a Godot builtin (e.g. Vector2)
    is_builtin: bool = False
    # Type is a scalar (e.g. int, float) or void
    is_base_type: bool = False
    # Type doesn't use the heap (hence no need for freeing it)
    is_stack_only: bool = False
    # Type is an enum (e.g. godot_error, Camera::KeepAspect)
    is_enum: bool = False

    def __post_init__(self):
        self.py_type = self.py_type or self.cy_type
        if self.is_object:
            assert not self.is_builtin
            assert not self.is_base_type
            assert not self.is_stack_only
        if self.is_builtin:
            assert not self.is_base_type


@dataclass
class PropertyInfo:
    name: str
    type: Type
    getter: str
    setter: str
    index: Optional[int]


@dataclass
class ArgumentInfo:
    name: str
    type: Type
    default_value: Optional[str]

    @property
    def has_default_value(self):
        return self.default_value is not None


@dataclass
class SignalInfo:
    name: str
    arguments: List[ArgumentInfo]


@dataclass
class MethodInfo:
    name: str
    return_type: Type
    is_editor: bool
    is_noscript: bool
    is_const: bool
    is_reverse: bool
    is_virtual: bool
    has_varargs: bool
    is_from_script: bool
    arguments: List[ArgumentInfo]


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


TYPES = {
    # Base types
    "void": Type("void", "None", is_base_type=True, is_stack_only=True),
    "bool": Type("godot_bool", "bool", is_base_type=True, is_stack_only=True),
    "int": Type("godot_int", "int", is_base_type=True, is_stack_only=True),
    "float": Type("godot_real", "float", is_base_type=True, is_stack_only=True),
    "enum.Error": Type(
        "godot_error",
        "godot_error",
        py_type="Error",
        is_base_type=True,
        is_stack_only=True,
        is_enum=True,
    ),
    "enum.Vector3::Axis": Type(
        "godot_vector3_axis",
        "godot_vector3_axis",
        py_type="Vector3.Axis",
        is_base_type=True,
        is_stack_only=True,
        is_enum=True,
    ),
    "enum.Variant::Type": Type(
        "godot_variant_type",
        "godot_variant_type",
        py_type="VariantType",
        is_base_type=True,
        is_stack_only=True,
        is_enum=True,
    ),
    "enum.Variant::Operator": Type(
        "godot_variant_operator",
        "godot_variant_operator",
        py_type="VariantOperator",
        is_base_type=True,
        is_stack_only=True,
        is_enum=True,
    ),
    # Stack&heap types
    "Variant": Type("godot_variant", "object", is_builtin=True),
    "String": Type("godot_string", "GDString", py_type="Union[str, GDString]", is_builtin=True),
    # Stack only types
    "AABB": Type("godot_aabb", "AABB", is_builtin=True, is_stack_only=True),
    "Array": Type("godot_array", "Array", is_builtin=True, is_stack_only=True),
    "Basis": Type("godot_basis", "Basis", is_builtin=True, is_stack_only=True),
    "Color": Type("godot_color", "Color", is_builtin=True, is_stack_only=True),
    "Dictionary": Type("godot_dictionary", "Dictionary", is_builtin=True, is_stack_only=True),
    "NodePath": Type(
        "godot_node_path",
        "NodePath",
        py_type="Union[str, NodePath]",
        is_builtin=True,
        is_stack_only=True,
    ),
    "Plane": Type("godot_plane", "Plane", is_builtin=True, is_stack_only=True),
    "Quat": Type("godot_quat", "Quat", is_builtin=True, is_stack_only=True),
    "Rect2": Type("godot_rect2", "Rect2", is_builtin=True, is_stack_only=True),
    "RID": Type("godot_rid", "RID", is_builtin=True, is_stack_only=True),
    "Transform": Type("godot_transform", "Transform", is_builtin=True, is_stack_only=True),
    "Transform2D": Type("godot_transform2d", "Transform2D", is_builtin=True, is_stack_only=True),
    "Vector2": Type("godot_vector2", "Vector2", is_builtin=True, is_stack_only=True),
    "Vector3": Type("godot_vector3", "Vector3", is_builtin=True, is_stack_only=True),
    "PoolByteArray": Type(
        "godot_pool_byte_array", "PoolByteArray", is_builtin=True, is_stack_only=True
    ),
    "PoolIntArray": Type(
        "godot_pool_int_array", "PoolIntArray", is_builtin=True, is_stack_only=True
    ),
    "PoolRealArray": Type(
        "godot_pool_real_array", "PoolRealArray", is_builtin=True, is_stack_only=True
    ),
    "PoolStringArray": Type(
        "godot_pool_string_array", "PoolStringArray", is_builtin=True, is_stack_only=True
    ),
    "PoolVector2Array": Type(
        "godot_pool_vector2_array", "PoolVector2Array", is_builtin=True, is_stack_only=True
    ),
    "PoolVector3Array": Type(
        "godot_pool_vector3_array", "PoolVector3Array", is_builtin=True, is_stack_only=True
    ),
    "PoolColorArray": Type(
        "godot_pool_color_array", "PoolColorArray", is_builtin=True, is_stack_only=True
    ),
}


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
    "godot_pool_int_array",
    "godot_pool_string_array",
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

    kept_classes = []
    for klass in classes:
        methods = []
        for meth in klass.methods:
            # TODO: handle default param values
            # TODO: handle those flags
            if meth.is_editor:
                # warn(f"Ignoring `{klass.name}.{meth.name}` (attribute `is_editor=True` not supported)")
                continue
            if meth.is_reverse:
                warn(
                    f"Ignoring `{klass.name}.{meth.name}` (attribute `is_reverse=True` not supported)"
                )
                continue
            if meth.is_virtual:
                # warn(f"Ignoring `{klass.name}.{meth.name}` (attribute `is_virtual=True` not supported)")
                continue
            if meth.has_varargs:
                # warn(f"Ignoring `{klass.name}.{meth.name}` (attribute `has_varargs=True` not supported)")
                continue
            if not _is_supported_type(meth.return_type):
                warn(
                    f"Ignoring `{klass.name}.{meth.name}` (return type {meth.return_type} not supported)"
                )
                continue
            bad_arg = next(
                (arg for arg in meth.arguments if not _is_supported_type(arg.type)), None
            )
            if bad_arg:
                warn(f"Ignoring `{klass.name}.{meth.name}` (argument type {bad_arg} not supported)")
                continue
            methods.append(meth)
        klass.methods = methods

        properties = []
        for prop in klass.properties:
            if not _is_supported_type(prop.type):
                warn(
                    f"Ignoring property `{klass.name}.{prop.name}` (property type {prop.type} not supported)"
                )
                continue
            properties.append(prop)
        klass.properties = properties

        signals = []
        for signal in klass.signals:
            bad_arg = next(
                (arg for arg in signal.arguments if not _is_supported_type(arg.type)), None
            )
            if bad_arg:
                warn(
                    f"Ignoring signal `{klass.name}.{signal.name}` (argument type {bad_arg} not supported)"
                )
                continue
            signals.append(signal)
        klass.signals = signals

        kept_classes.append(klass)

    return kept_classes


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
                return Type(
                    "godot_int",
                    "godot_int",
                    py_type=f"{class_renames[pcls]}.{ecls}",
                    is_base_type=True,
                    is_stack_only=True,
                    is_enum=True,
                )

            # TODO: improve handling of resources
            if "," in type_:
                return Type(
                    "godot_object",
                    "Resource",
                    py_type=f"Union[{','.join([class_renames[x] for x in type_.split(',')])}]",
                    is_object=True,
                )
            else:
                return Type("godot_object", class_renames[type_], is_object=True)

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


def generate_bindings(output_path, input_path, sample):
    with open(input_path, "r") as fd:
        raw_data = json.load(fd)
    pre_cook_patch_stuff(raw_data)
    classes, constants = cook_data(raw_data)
    if sample:
        strip_sample_stuff(classes)
    strip_unsupported_stuff(classes)
    post_cook_patch_stuff(classes)

    template = env.get_template("bindings.tmpl.pyx")
    out = template.render(classes=classes, constants=constants)
    with open(output_path, "w") as fd:
        fd.write(out)

    pyi_output_path = output_path.rsplit(".", 1)[0] + ".pyi"
    template = env.get_template("bindings.tmpl.pyi")
    out = template.render(classes=classes, constants=constants)
    with open(pyi_output_path, "w") as fd:
        fd.write(out)

    pxd_output_path = output_path.rsplit(".", 1)[0] + ".pxd"
    template = env.get_template("bindings.tmpl.pxd")
    out = template.render(classes=classes, constants=constants)
    with open(pxd_output_path, "w") as fd:
        fd.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate godot api bindings file")
    parser.add_argument("--input", "-i", help="Path to Godot api.json file", default="api.json")
    parser.add_argument("--output", "-o", default="godot_bindings_gen.pyx")
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()
    generate_bindings(args.output, args.input, args.sample)
