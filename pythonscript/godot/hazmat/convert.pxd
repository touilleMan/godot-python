from libc.stddef cimport wchar_t
from libc.stdio cimport printf
from godot.hazmat._gdapi cimport pythonscript_gdapi as gdapi
from godot.hazmat.gdnative_api_struct cimport (
    godot_string,
    godot_int
)

# Godot string are basically a vector of wchar_t, each wchar_t representing
# a single unicode character (i.e. there is no surrogates support).
# The sad part is wchar_t is not portable: it is 16bits long on Windows and
# 32bits long on Linux and MacOS...
# So we end up with a UCS2 encoding on Windows and UCS4 everywhere else :'(


cdef inline object godot_string_to_pyobj(const godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    cdef char *raw = <char*>gdapi.godot_string_wide_str(p_gdstr)
    cdef godot_int length = gdapi.godot_string_length(p_gdstr)
    IF UNAME_SYSNAME == "Windows":
        return raw[:length * 2].decode("UTF-16")
    ELSE:
        return raw[:length * 4].decode("UTF-32")


cdef inline godot_string pyobj_to_godot_string(object pystr):
    cdef godot_string gdstr;
    # TODO: unicode&windows support is most likely broken...
    IF UNAME_SYSNAME == "Windows":
        raw = pystr.encode("UTF-16")
    ELSE:
        raw = pystr.encode("UTF-32")
    gdapi.godot_string_new_with_wide_string(
        &gdstr, <wchar_t*><char*>raw, len(pystr)
    )
    return gdstr
