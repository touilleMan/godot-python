PYTHON_KEYWORDS = {
    # Python
    "False",
    "await",
    "else",
    "import",
    "pass",
    "None",
    "break",
    "except",
    "in",
    "raise",
    "True",
    "class",
    "finally",
    "is",
    "return",
    "and",
    "continue",
    "for",
    "lambda",
    "try",
    "as",
    "def",
    "from",
    "nonlocal",
    "while",
    "assert",
    "del",
    "global",
    "not",
    "with",
    "async",
    "elif",
    "if",
    "or",
    "yield",
    # Cython
    "char",
}


GD_SCALAR_TYPES = {"Nil", "bool", "int", "float"}


def correct_name(name: str) -> str:
    if name in PYTHON_KEYWORDS:
        return f"{name}_"
    else:
        return name


def correct_type_name(type_name: str) -> str:
    if type_name == "Nil":
        return "None"
    if type_name in GD_SCALAR_TYPES:
        # By chance Godot's scalar types have the same name than Python's ones
        return type_name
    elif type_name == "Object":
        # `Object` is too similar than Python's `object`
        return "GDObject"
    elif type_name == "String":
        # `String` is too similar than Python's `str`
        return "GDString"
    elif type_name == "Variant":
        return "GDVariant"
    else:
        return type_name


def assert_api_consistency(datacls, api: dict) -> None:
    # Ensure the fields are as expected, in theory we should also check typing
    # but it's cumbersome and it's very likely bad typing will lead anyway to a
    # runtime error in this script or a compilation error on the generated code
    if api.keys() != datacls.__dataclass_fields__.keys():
        missings = datacls.__dataclass_fields__.keys() - api.keys()
        unknowns = api.keys() - datacls.__dataclass_fields__.keys()
        raise RuntimeError(
            f"Invalid extension_api.json format\nmissings: {missings or ''}\nunknowns: {unknowns or ''}"
        )
