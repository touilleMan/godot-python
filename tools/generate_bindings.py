import os
import argparse
import json
import re
from keyword import iskeyword
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


BASEDIR = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(f"{BASEDIR}/bindings_templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)


GD_TYPES = {
    "void": "void",
    "bool": "godot_bool",
    "int": "godot_int",
    "float": "godot_real",
    "enum.Error": "godot_error",
    "enum.Vector3::Axis": "godot_vector3_axis",
    "Variant": "godot_variant",
    "String": "godot_string",
    "Transform2D": "godot_transform2d",
}


SAMPLE_CLASSES = {
    "Object",
    # "Input",
    # "InputMap",
    # "MainLoop",
    # "Node",
    "Reference",
    "ARVRInterface",
    "ARVRInterfaceGDNative",
    # "MultiplayerAPI",
    # "SceneTree",
    # "Viewport",
    # "_ClassDB",
    # "_Engine",
    # "_Geometry",
    # "_JSON",
    "_OS",
    # "_ResourceLoader",
    # "_ResourceSaver",
    # "_VisualScriptEditor",
}

SUPPORTED_TYPES = {"void", "godot_bool", "godot_int"}


def strip_unsupported_stuff(classes):
    for klass in classes:
        methods = []
        for meth in klass["methods"]:
            if meth["is_editor"]:
                continue
            if meth["is_noscript"]:
                continue
            if meth["is_const"]:
                continue
            if meth["is_reverse"]:
                continue
            if meth["is_virtual"]:
                continue
            if meth["has_varargs"]:
                continue
            if meth["is_from_script"]:
                continue
            if meth["return_type"] not in SUPPORTED_TYPES:
                continue
            if [arg for arg in meth["arguments"] if arg["type"] not in SUPPORTED_TYPES]:
                continue
            methods.append(meth)
        klass["methods"] = methods

        properties = []
        for prop in klass["properties"]:
            if prop["type"] not in SUPPORTED_TYPES:
                continue
            properties.append(prop)
        klass["properties"] = properties

        signals = []
        for signal in klass["signals"]:
            if [
                arg for arg in signal["arguments"] if arg["type"] not in SUPPORTED_TYPES
            ]:
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
        if item["singleton"] and not old_name.startswith('_'):
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
            return (True, class_renames[type_])
        except KeyError:
            try:
                return (False, GD_TYPES[type_])
            except KeyError:
                if type_.startswith("enum."):
                    return (False, "godot_int")
                else:
                    return (False, f"godot_{camel_to_snake(type_)}")

    def _cook_name(name):
        if iskeyword(name) or name in ("char", "bool", "int", "float", "short"):
            return f"{name}_"
        else:
            return name

    for item in data:
        if item["name"] == "GlobalConstants":
            constants = item["constants"]
            continue

        item["base_class"] = class_renames[item["base_class"]]
        item["name"] = class_renames[item["name"]]

        if item["singleton"]:
            # Strip the leading underscore
            item["singleton_name"] = item["name"][1:]

        for meth in item["methods"]:
            meth["name"] = _cook_name(meth["name"])
            meth["return_type_is_binding"], meth["return_type"] = _cook_type(
                meth["return_type"]
            )
            for arg in meth["arguments"]:
                arg["name"] = _cook_name(arg["name"])
                arg["type_is_binding"], arg["type"] = _cook_type(arg["type"])

        for prop in item["properties"]:
            prop["name"] = _cook_name(prop["name"])
            prop["type_is_binding"], prop["type"] = _cook_type(prop["type"])

        for signal in item["signals"]:
            signal["name"] = _cook_name(signal["name"])
            for arg in signal["arguments"]:
                arg["name"] = _cook_name(arg["name"])
                arg["type_is_binding"], arg["type"] = _cook_type(arg["type"])

        classes.append(item)

    # Order classes by inheritance
    inheritances = defaultdict(list)
    for klass in classes:
        inheritances[klass['base_class']].append(klass)
    sorted_classes = [*inheritances[""]]
    todo_base_classes = [*inheritances[""]]
    while todo_base_classes:
        base_class = todo_base_classes.pop()
        children_classes = inheritances[base_class['name']]
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
