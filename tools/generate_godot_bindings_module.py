#! /usr/bin/env python3

import os
import keyword
import json
import argparse
from collections import OrderedDict

import jinja2
import black


BASEDIR = os.path.dirname(os.path.abspath(__file__))
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("%s/templates" % BASEDIR), autoescape=False
)


def fix_name(name):
    if not name:
        return name

    # Yep ! Some names contain this...
    name = name.replace("/", "_")
    # Python keywords are invalid names
    return name + "_" if name in keyword.kwlist else name


env.filters["fix_name"] = fix_name


def retrieve_docstring(key):
    # TODO
    return None


env.globals["retrieve_docstring"] = retrieve_docstring


def constant_is_enum(enums, constant):
    for enum in enums:
        if constant in enum["values"]:
            return True

    return False


env.globals["constant_is_enum"] = constant_is_enum


def sort_classes_by_inheritance(classes):
    """
    Python is sensitive to order of classes when doing inheritance, this function makes sure it's all ordered by
    inheritance.
    """
    classes_by_name = {klass["name"]: klass for klass in classes}
    ordered_classes = OrderedDict()

    for klass in classes:
        current_class = klass
        inheritance_list = [klass]

        while True:
            base_class = current_class.get("base_class")

            if base_class:
                current_class = classes_by_name[base_class]
                inheritance_list.append(current_class)
            else:
                break

        for klass in reversed(inheritance_list):
            ordered_classes[klass["name"]] = klass

    return list(ordered_classes.values())


def generate_godot_bindings(api, pretty=True, no_docstring=False):

    print("Generating bindings...")

    # Cook api first
    constants = []
    singletons = []
    classes = []
    for cls_api in api["content"]:
        if cls_api["name"] == "GlobalConstants":
            constants = cls_api["constants"]
        else:
            if cls_api["singleton"]:
                singletons.append(cls_api)
            classes.append(cls_api)

    classes = sort_classes_by_inheritance(classes)

    # Render module
    rendered = env.get_template("module.j2").render(
        godot_api_version=api["version"],
        constants=constants,
        singletons=singletons,
        classes=classes,
        no_docstring=no_docstring,
    )

    if pretty:
        print("Prettifying...")
        rendered = black.format_str(rendered, 80)

    return rendered


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("godot_api", help="Path to Godot api json file")
    parser.add_argument("--output", "-o", default="godot_bindings.gen.py")
    parser.add_argument("--pretty", "-p", action="store_true")
    parser.add_argument("--no-docstring", "-N", action="store_true")
    args = parser.parse_args()

    with open(args.godot_api) as fd:
        api = json.load(fd)
    generated = generate_godot_bindings(api, args.pretty, args.no_docstring)
    with open(args.output, "w") as fd:
        fd.write(generated)
