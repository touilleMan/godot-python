from string import ascii_uppercase


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


def correct_name(name: str) -> str:
    if name in PYTHON_KEYWORDS:
        return f"{name}_"
    else:
        return name


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


def camel_to_snake(name):
    snake = ""
    for c in name:
        if c in ascii_uppercase and snake and snake[-1] not in ascii_uppercase:
            snake += "_"
        snake += c
    return snake.lower()
