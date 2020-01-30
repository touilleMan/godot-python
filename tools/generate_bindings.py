import os
import argparse
import json
import re
from warnings import warn
from keyword import iskeyword
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


BASEDIR = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(f"{BASEDIR}/bindings_templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)


BASE_TYPES = {
    "void": "void",
    "bool": "godot_bool",
    "int": "godot_int",
    "float": "godot_real",
    "enum.Error": "godot_error",
    "enum.Vector3::Axis": "godot_vector3_axis",
}
STACK_AND_HEAP_BUILTINS_TYPES = {"Variant": "godot_variant", "String": "godot_string"}
STACK_ONLY_BUILTINS_TYPES = {
    "AABB": "godot_aabb",
    "Array": "godot_array",
    "Basis": "godot_basis",
    "Color": "godot_color",
    "Dictionary": "godot_dictionary",
    "NodePath": "godot_node_path",
    "Plane": "godot_plane",
    "Quat": "godot_quat",
    "Rect2": "godot_rect2",
    "RID": "godot_rid",
    "Transform": "godot_transform",
    "Transform2D": "godot_transform2d",
    "Vector2": "godot_vector2",
    "Vector3": "godot_vector3",
    "PoolByteArray": "godot_pool_byte_array",
    "PoolIntArray": "godot_pool_int_array",
    "PoolRealArray": "godot_pool_real_array",
    "PoolStringArray": "godot_pool_string_array",
    "PoolVector2Array": "godot_pool_vector2_array",
    "PoolVector3Array": "godot_pool_vector3_array",
    "PoolColorArray": "godot_pool_color_array",
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
    "CollisionObject2D",
    "Area2D",
    "ARVRInterface",
    "ARVRInterfaceGDNative",
    "Resource",
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
    # "_ResourceLoader",
    # "_ResourceSaver",
    # "_VisualScriptEditor",
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


def patch_stuff(classes):
    # See https://github.com/godotengine/godot/issues/34254
    for klass in classes:
        if klass["name"] != "_OS":
            continue
        for meth in klass["methods"]:
            if meth["name"] in (
                "get_static_memory_usage",
                "get_static_memory_peak_usage",
                "get_dynamic_memory_usage",
            ):
                meth["return_type"] = "uint64_t"
                meth["return_type_specs"]["binding_type"] = "uint64_t"


def strip_unsupported_stuff(classes):
    supported_classes = {k["name"] for k in classes}

    def _is_supported_type(specs):
        if specs["is_builtin"]:
            return specs["type"] in SUPPORTED_TYPES
        elif specs["is_object"]:
            return specs["binding_type"] in supported_classes
        else:
            return True

    for klass in classes:
        methods = []
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
            # TODO: handle default param values
            # TODO: handle those flags
            if meth["is_editor"]:
                continue
            if meth["is_reverse"]:
                continue
            if meth["is_virtual"]:
                continue
            if meth["has_varargs"]:
                continue
            if not _is_supported_type(meth["return_type_specs"]):
                continue
            if any(
                arg
                for arg in meth["arguments"]
                if not _is_supported_type(arg["type_specs"])
            ):
                continue
            methods.append(meth)
        klass["methods"] = methods

        properties = []
        for prop in klass["properties"]:
            if not _is_supported_type(prop["type_specs"]):
                continue
            properties.append(prop)
        klass["properties"] = properties

        signals = []
        for signal in klass["signals"]:
            if any(
                arg
                for arg in signal["arguments"]
                if not _is_supported_type(arg["type_specs"])
            ):
                continue
            signals.append(signal)
        klass["signals"] = signals


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def patch_data(data):
    for item in data:
        # TODO: BulletPhysicsServer is not marked as a singleton but inherits PhysicsServer
        if item["name"] == "BulletPhysicsServer":
            item["singleton"] = True
    return data


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
            return {
                "type": "godot_object",
                "binding_type": class_renames[type_],
                "is_object": True,
                "is_builtin": False,
                "is_base_type": False,
                "stack_only": False,
            }
        except KeyError:
            pass
        try:
            return {
                "type": STACK_ONLY_BUILTINS_TYPES[type_],
                "binding_type": type_,
                "is_object": False,
                "is_builtin": True,
                "is_base_type": False,
                "stack_only": True,
            }
        except KeyError:
            pass
        try:
            spec = {
                "type": STACK_AND_HEAP_BUILTINS_TYPES[type_],
                "is_object": False,
                "is_builtin": True,
                "is_base_type": False,
                "stack_only": False,
            }
            if spec["type"] == "godot_variant":
                spec["binding_type"] = "object"
            elif spec["type"] == "godot_string":
                spec["binding_type"] = "GDString"
            return spec
        except KeyError:
            pass
        try:
            specs = {
                "is_object": False,
                "is_builtin": False,
                "stack_only": True,
                "is_base_type": True,
            }
            if type_.startswith("enum."):
                specs["binding_type"] = specs["type"] = "godot_int"
            else:
                specs["binding_type"] = specs["type"] = BASE_TYPES[type_]
            return specs
        except KeyError:
            pass
        warn(f"Unknown type: {type_!r}")
        return {
            "type": type_,
            "binding_type": type_,
            "is_object": False,
            "is_builtin": False,
            "stack_only": False,
        }

    def _cook_name(name):
        if iskeyword(name) or name in ("char", "bool", "int", "float", "short", "type"):
            return f"{name}_"
        else:
            return name

    def _cook_default_arg(type, value):
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
        elif (
            type == "godot_transform" and value == "1, 0, 0, 0, 1, 0, 0, 0, 1 - 0, 0, 0"
        ):
            return "Transform(Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1), Vector3(0, 0, 0))"
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

    for item in data:
        if item["name"] == "GlobalConstants":
            constants = item["constants"]
            continue

        item["bind_register_name"] = item["name"]
        item["base_class"] = class_renames[item["base_class"]]
        item["name"] = class_renames[item["name"]]

        if item["singleton"]:
            # Strip the leading underscore
            item["singleton_name"] = item["name"][1:]

        for meth in item["methods"]:
            meth["name"] = _cook_name(meth["name"])
            specs = _cook_type(meth["return_type"])
            meth["return_type_specs"] = specs
            meth["return_type"] = specs["type"]
            for arg in meth["arguments"]:
                arg["name"] = _cook_name(arg["name"])
                specs = _cook_type(arg["type"])
                arg["type_specs"] = specs
                arg["type"] = specs["type"]
                if arg["has_default_value"]:
                    arg["default_value"] = _cook_default_arg(
                        arg["type"], arg["default_value"]
                    )

        for prop in item["properties"]:
            prop["name"] = _cook_name(prop["name"])
            specs = _cook_type(prop["type"])
            prop["type_specs"] = specs
            prop["type"] = specs["type"]

        for signal in item["signals"]:
            signal["name"] = _cook_name(signal["name"])
            for arg in signal["arguments"]:
                arg["name"] = _cook_name(arg["name"])
                specs = _cook_type(arg["type"])
                arg["type_specs"] = specs
                arg["type"] = specs["type"]

        classes.append(item)

    # Order classes by inheritance
    inheritances = defaultdict(list)
    for klass in classes:
        inheritances[klass["base_class"]].append(klass)
    sorted_classes = [*inheritances[""]]
    todo_base_classes = [*inheritances[""]]
    while todo_base_classes:
        base_class = todo_base_classes.pop()
        children_classes = inheritances[base_class["name"]]
        todo_base_classes += children_classes
        sorted_classes += children_classes

    return sorted_classes, constants


def generate_bindings(output_path, input_path, sample):
    with open(input_path, "r") as fd:
        raw_data = json.load(fd)
    classes, constants = cook_data(raw_data)
    if sample:
        classes = [klass for klass in classes if klass["name"] in SAMPLE_CLASSES]
    strip_unsupported_stuff(classes)
    patch_stuff(classes)

    template = env.get_template("bindings.tmpl.pyx")
    out = template.render(classes=classes, constants=constants)
    with open(output_path, "w") as fd:
        fd.write(out)

    pxd_output_path = output_path.rsplit(".", 1)[0] + ".pxd"
    template = env.get_template("bindings.tmpl.pxd")
    out = template.render(classes=classes, constants=constants)
    with open(pxd_output_path, "w") as fd:
        fd.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate godot api bindings file")
    parser.add_argument(
        "--input", "-i", help="Path to Godot api.json file", default="api.json"
    )
    parser.add_argument("--output", "-o", default="godot_bindings_gen.pyx")
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()
    generate_bindings(args.output, args.input, args.sample)
