import re
from typing import List, Dict
import argparse
from pathlib import Path
from pycparser import CParser, c_ast
from autopxd import AutoPxd


# List the includes to the stdlib we are expecting. This is needed to hack
# around them given they are needed for pycparser, but should endup in the pxd
# as `from libc.stdint cimport uint8_t` instead of being inside the `cdef extern`
# describing the whole header stuff.
STDLIB_INCLUDES = {
    "stdbool.h": ["bool"],
    "stdint.h": [
        "uint8_t",
        "int8_t",
        "uint16_t",
        "int16_t",
        "uint32_t",
        "int32_t",
        "uint64_t",
        "int64_t",
    ],
    "wchar.h": ["wchar_t", "size_t"],
}
STDLIB_TYPES = {t for m in STDLIB_INCLUDES.values() for t in m}


class CCCP:
    """
    CCCP: the Cheap&Coarse C Preprocessor
    PyCParser needs to get passed preprocessed C code, but we don't want to
    use a real one:
    - different OS have different preprocessors (msvc vs clang vs gcc)
    - we can control which #include to follow given we don't care about stdlibs ones
    - we can easily tweak the behavior of #ifdef parts to ignore platform specificities

    In the end remember that we are not compiling a C program, but creating a
    .pxd file that will (in conjuction with a .pyx) be used to generate a .c
    file that will include the godot api headers. So there is no need to handle
    platform specific (or even opaque structure size !) detail here: they will
    be ignored by cython and left to the final C compilation.
    """

    def __init__(
        self, include_dirs: List[str], forced_defined_vars: Dict[str, str], debug: bool = False
    ):
        self.source = []
        self.source_cursor = 0
        self.forced_defined_vars = forced_defined_vars.keys()
        self.defined_vars = {**forced_defined_vars}
        self.include_dirs = [Path(p) for p in include_dirs]
        self.ingnored_includes = set()
        self.debug = debug

    @staticmethod
    def source_to_lines(src: str) -> List[str]:
        # First remove all comments
        src = re.sub(r"(//.*$)", "", src, flags=re.MULTILINE)
        src = re.sub(r"/\*.*?\*/", "", src, flags=re.DOTALL)

        # Split lines, taking care of backslashes
        lines = []
        multi_lines = ""
        for line in src.splitlines():
            line = line.rstrip()
            if line.endswith("\\"):
                multi_lines += line[:-1]
                continue
            lines.append(multi_lines + line)
            multi_lines = ""

        return lines

    def debug_explain(self, msg):
        if self.debug:
            print(msg)

    def error_occurred(self, msg):
        extract = "\n".join(self.source[max(0, self.source_cursor - 5) : self.source_cursor + 5])
        raise RuntimeError(f"{msg}\n\nOccurred around:\n{extract}")

    def handle_include(self, line):
        match_include = re.match(r"^\s*#\s*include\s+[<\"]([a-zA-Z0-9_./]+)[>\"]$", line)
        if not match_include:
            return None
        include_name = match_include.group(1)
        if include_name in STDLIB_INCLUDES.keys():
            self.debug_explain(f"INCLUDE INGNORED {include_name}")
            self.source.pop(self.source_cursor)
            return 0
        for include_dir in self.include_dirs:
            include_path = include_dir / include_name
            try:
                included_source = include_path.read_text()
                # Remove #include line and replace it by included source
                self.source = (
                    self.source[: self.source_cursor]
                    + self.source_to_lines(included_source)
                    + self.source[self.source_cursor + 1 :]
                )
                self.debug_explain(f"INCLUDE {include_name}")
                return 0
            except FileNotFoundError:
                pass
        self.error_occurred(f"Cannot resolve import `{line}`")

    def handle_define(self, line):
        match_define = re.match(r"^\s*#\s*define\s+([a-zA-Z0-9_]+)(\s+|$)", line)
        if not match_define:
            return None
        define_name = match_define.group(1)
        define_value = line[len(match_define.group(0)) :]
        if define_name not in self.forced_defined_vars:
            self.defined_vars[define_name] = self.expand_macros(define_value)
            self.debug_explain(f"DEF {define_name}={define_value}")
        else:
            self.debug_explain(f"DEF IGNORED {define_name}={define_value}")
        self.source.pop(self.source_cursor)
        return 0

    def handle_define_macro(self, line):
        match_define_macro = re.match(r"^\s*#\s*define\s+([a-zA-Z0-9_]+)\(", line)
        if not match_define_macro:
            return None
        define_name = match_define_macro.group(1)
        define_value = line[len(match_define_macro.group(0)) :]
        # Macro are not supported, this is ok given they are not used
        # (but some are defined) in the gdnative headers.
        # As a sanity measure, we make sure the code generated if the macro
        # is used will cause the C parser to crash.
        self.defined_vars[define_name] = f"#error unsuported macro {define_name}"
        self.debug_explain(f"DEF MACRO {define_name}=__UNSUPORTED__")
        self.source.pop(self.source_cursor)
        return 0

    def handle_undef(self, line):
        match_undefine = re.match(r"^\s*#\s*undef\s+([a-zA-Z0-9_]+)$", line)
        if not match_undefine:
            return None
        define_name = match_undefine.group(1)
        if define_name not in self.forced_defined_vars:
            self.defined_vars.pop(define_name)
            self.debug_explain(f"UNDEF {define_name}")
        else:
            self.debug_explain(f"UNDEF INGNORED {define_name}")
        self.source.pop(self.source_cursor)
        return 0

    def handle_if(self, line):
        # Replace ifdef/ifndef by generic if to simplify parsing
        line = re.sub(r"^\s*#\s*ifdef\s+([a-zA-Z0-9_]+)$", r"#if defined(\1)", line)
        line = re.sub(r"^\s*#\s*ifndef\s+([a-zA-Z0-9_]+)$", r"#if !defined(\1)", line)

        match_if = re.match(r"^\s*#\s*if\s+", line)
        if not match_if:
            return None

        def _eval_if_condition(condition):
            # Turn condition into Python code and eval it \o/
            expr = condition.replace("||", " or ")
            expr = expr.replace("&&", " and ")
            expr = expr.replace("!", " not ")
            expr = re.sub(r"defined\(([a-zA-Z0-9_]+)\)", r"defined('\1')", expr)
            try:
                return eval(
                    expr, {"defined": lambda key: key in self.defined_vars}, self.defined_vars
                )
            except Exception as exc:
                self.error_occurred(
                    f"Error {exc} while evaluating `{expr}` (generated from `{condition}`)"
                )

        def _keep_until_next_condition(offset):
            nested_count = 0
            kept_body = []
            while True:
                try:
                    line = self.source[self.source_cursor + offset]
                except IndexError:
                    self.error_occurred("Reach end of file without #endif")
                if re.match(r"^\s*#\s*(if|ifdef|ifndef)(\s+|$)", line):
                    # Nested #if
                    nested_count += 1
                else_match = re.match(r"^\s*#\s*(else$|elif\s+)", line)
                if else_match:
                    if nested_count == 0:
                        condition_type = else_match.group(1).strip()
                        condition = line[len(else_match.group(1)) :]
                        return kept_body, condition_type, condition, offset + 1
                if re.match(r"^\s*#\s*endif$", line):
                    if nested_count == 0:
                        return kept_body, "endif", "", offset + 1
                    else:
                        nested_count -= 1
                offset += 1
                kept_body.append(line)

        def _retreive_kept_body(condition, offset):
            if _eval_if_condition(condition):
                kept_body, condition_type, condition, offset = _keep_until_next_condition(offset)
                # Skip other else/elif body parts until the matching endif
                while condition_type != "endif":
                    _, condition_type, _, offset = _keep_until_next_condition(offset)
                return kept_body, offset
            else:
                # Ignore the if body part
                _, condition_type, condition, offset = _keep_until_next_condition(offset)
                if condition_type == "elif":
                    return _retreive_kept_body(condition, offset)
                elif condition_type == "else":
                    return _retreive_kept_body("True", offset)
                else:  # endif
                    return [], offset

        if_condition = line[len(match_if.group()) :]
        body, offset = _retreive_kept_body(if_condition, offset=1)

        if_starts = self.source_cursor
        if_ends = self.source_cursor + offset
        self.source[if_starts:if_ends] = body

        self.debug_explain(f"IF ({line}) ==> {if_starts} {if_ends}")

        return 0  # 0 is not equivalent to None !

    def handle_unknown(self, line):
        match_unknown = re.match(r"^\s*#", line)
        if not match_unknown:
            return None
        self.error_occurred(f"Unknown preprocessor command `{line}`")

    def expand_macros(self, line):
        # Simple optim to discard most of the lines given regex search is cpu heavy
        if not line or all(key not in line for key in self.defined_vars.keys()):
            return line
        expanded_line = line
        # Recursive expansion given a macro can reference another one
        while True:
            for key, value in self.defined_vars.items():
                expanded_line = re.sub(
                    f"(^|[^a-zA-Z0-9_]){key}([^a-zA-Z0-9_]|$)",
                    f"\\g<1>{value}\\g<2>",
                    expanded_line,
                )
            if expanded_line == line:
                break
            line = expanded_line
        return line

    def parse(self, src: str) -> str:
        self.source = self.source_to_lines(src)

        cpp_handlers = (
            self.handle_define,
            self.handle_define_macro,
            self.handle_if,
            self.handle_include,
            self.handle_undef,
            self.handle_unknown,
        )
        while True:
            try:
                source_line = self.source[self.source_cursor]
            except IndexError:
                # Parsing is done
                break

            for cpp_handler in cpp_handlers:
                eaten_lines = cpp_handler(source_line)
                if eaten_lines is not None:
                    self.source_cursor += eaten_lines
                    break
            else:
                # Not a preprocessor line
                self.source[self.source_cursor] = self.expand_macros(source_line)
                self.source_cursor += 1

        return "\n".join(self.source)


class PatchedAutoPxd(AutoPxd):
    def visit_TypeDecl(self, node):
        # Ignore types from stdlib (will be provided by the
        # `from libc.stdint cimport uint8_t` syntax)
        if node.declname in STDLIB_TYPES:
            return
        else:
            return super().visit_TypeDecl(node)

    def visit_ArrayDecl(self, node):
        # autopxd doesn't support array with an expression as size, but in:
        #   typedef struct {uint8_t _dont_touch_that[GODOT_VECTOR3_SIZE];} godot_vector3;
        # `GODOT_VECTOR3_SIZE` gets resolved as `sizeof(void*)` :(
        if node.type.declname == "_dont_touch_that":
            # Of course the 0 size is wrong, but it's not an issue given
            # we don't touch this array in Cython code (hence the name ^^)
            node.dim = c_ast.Constant(type="int", value="0")
        return super().visit_ArrayDecl(node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert gdnative_api_struct.gen.h into Cython .pxd"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="GODOT_HEADERS_PATH",
        help="Path to Godot GDNative headers",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=argparse.FileType("w", encoding="utf8"),
        metavar="GDNATIVE_API_STRUCT_PXD",
        help="Path to store the generated gdnative_api_struct.pxd file",
    )
    args = parser.parse_args()

    # Step 1: preprocessing
    header_name = "gdnative_api_struct.gen.h"
    with open(f"{args.input}/{header_name}", "r") as fd:
        source = fd.read()

    # салют товарищ !
    cccp = CCCP(
        include_dirs=[args.input],
        forced_defined_vars={"GDAPI": "", "GDN_EXPORT": "", "GDCALLINGCONV": ""},
    )

    preprocessed = ""
    # pycparser requires each symbol must be defined, hence provide a dummy
    # definition of the needed stdlib types.
    # Note those definitions will then be detected and ignored by PatchedAutoPxd.
    for stdtype in STDLIB_TYPES:
        preprocessed += f"typedef int {stdtype};\n"
    preprocessed += cccp.parse(source)

    with open("output.preprocessed.c", "w") as fd:
        fd.write(preprocessed)

    # Step 2: C parsing
    parser = CParser()
    ast = parser.parse(preprocessed)

    # Step 3: .pxd generation
    p = PatchedAutoPxd(header_name)
    p.visit(ast)

    pxd_cdef = p.lines()
    # Remove the cdef part given we want to add the `nogil` option and
    # we also want to add the `godot_method_flags` C inline code
    assert pxd_cdef[0].startswith("cdef extern from")
    pxd_cdef_body = "\n".join(pxd_cdef[1:])

    pxd = f"""\
# /!\\ Autogenerated code, modifications will be lost /!\\
# see `generation/generate_gdnative_api_struct.py`


from libc.stddef cimport wchar_t, size_t
from libc.stdint cimport {', '.join(STDLIB_INCLUDES['stdint.h'])}

cdef extern from "{header_name}" nogil:

    \"\"\"
    typedef enum {{
        GODOT_METHOD_FLAG_NORMAL = 1,
        GODOT_METHOD_FLAG_EDITOR = 2,
        GODOT_METHOD_FLAG_NOSCRIPT = 4,
        GODOT_METHOD_FLAG_CONST = 8,
        GODOT_METHOD_FLAG_REVERSE = 16,
        GODOT_METHOD_FLAG_VIRTUAL = 32,
        GODOT_METHOD_FLAG_FROM_SCRIPT = 64,
        GODOT_METHOD_FLAG_VARARG = 128,
        GODOT_METHOD_FLAGS_DEFAULT = GODOT_METHOD_FLAG_NORMAL
    }} godot_method_flags;
    \"\"\"

    ctypedef enum godot_method_flags:
        GODOT_METHOD_FLAG_NORMAL = 1
        GODOT_METHOD_FLAG_EDITOR = 2
        GODOT_METHOD_FLAG_NOSCRIPT = 4
        GODOT_METHOD_FLAG_CONST = 8
        GODOT_METHOD_FLAG_REVERSE = 16  # used for events
        GODOT_METHOD_FLAG_VIRTUAL = 32
        GODOT_METHOD_FLAG_FROM_SCRIPT = 64
        GODOT_METHOD_FLAG_VARARG = 128
        GODOT_METHOD_FLAGS_DEFAULT = 1  # METHOD_FLAG_NORMAL

    ctypedef bint bool

{pxd_cdef_body}
"""
    args.output.write(pxd)
