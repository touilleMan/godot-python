import os
import argparse
import json
import re
from keyword import iskeyword
from jinja2 import Environment, FileSystemLoader


BASEDIR = os.path.dirname(__file__)
env = Environment(loader=FileSystemLoader(f"{BASEDIR}/bindings_templates"))


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
        if item["singleton"]:
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
            return class_renames[type_]
        except KeyError:
            try:
                return GD_TYPES[type_]
            except KeyError:
                if type_.startswith("enum."):
                    return "godot_int"
                else:
                    return f"godot_{camel_to_snake(type_)}"

    def _cook_name(name):
        if iskeyword(name) or name in ('char', 'bool', 'int', 'float', 'short'):
            return f"{name}_"
        else:
            return name

    for item in data:
        if item['name'] == 'GlobalConstants':
            constants = item["constants"]
            continue

        if item['singleton']:
            item['singleton_name'] = item['name']

        item["base_class"] = class_renames[item["base_class"]]
        item["name"] = class_renames[item["name"]]

        for meth in item["methods"]:
            meth["name"] = _cook_name(meth["name"])
            meth["return_type"] = _cook_type(meth["return_type"])
            for arg in meth["arguments"]:
                arg["name"] = _cook_name(arg["name"])
                arg["type"] = _cook_type(arg["type"])

        for prop in item["properties"]:
            prop["name"] = _cook_name(prop["name"])
            prop["type"] = _cook_type(prop["type"])

        for signal in item["signals"]:
            signal["name"] = _cook_name(signal["name"])
            for arg in signal["arguments"]:
                arg["name"] = _cook_name(arg["name"])
                arg["type"] = _cook_type(arg["type"])

        classes.append(item)

    return classes, constants


def generate_bindings(output_path, input_path):
    with open(input_path, "r") as fd:
        raw_data = json.load(fd)
    classes, constants = cook_data(raw_data)
    template = env.get_template("bindings.tmpl.pyx")
    out = template.render(classes=classes, constants=constants)
    with open(output_path, "w") as fd:
        fd.write(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate godot api bindings file")
    parser.add_argument(
        "--input", "-i", help="Path to Godot api.json file", default="api.json"
    )
    parser.add_argument("--output", "-o", default="godot_bindings_gen.pyx")
    args = parser.parse_args()
    generate_bindings(args.output, args.input)
