from godot.hazmat.gdapi cimport *


cdef api gd_packed_string_array_t _pythonscript_get_reserved_words():
    cdef gd_packed_string_array_t arr = gd_packed_string_array_new()
    cdef gd_string_t string
    cdef (char*)[33] keywords = [
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    ]
    for keyword in keywords:
        string = gdstring_from_utf8(keyword, keyword.len())
        gd_packed_string_array_append(&arr, &string)
        gd_string_del(&string)
    return arr
