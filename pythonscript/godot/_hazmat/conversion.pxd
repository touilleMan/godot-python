from libc.stddef cimport wchar_t
from libc.stdio cimport printf

from godot._hazmat.gdapi cimport pythonscript_gdapi as gdapi
from godot._hazmat.gdnative_api_struct cimport (
    godot_string,
    godot_string_name,
    godot_int,
    godot_vector2,
    godot_variant,
    godot_variant_type,
)
from godot.vector2 cimport Vector2
from godot.bindings cimport Object


# Godot string are basically a vector of wchar_t, each wchar_t representing
# a single unicode character (i.e. there is no surrogates support).
# The sad part is wchar_t is not portable: it is 16bits long on Windows and
# 32bits long on Linux and MacOS...
# So we end up with a UCS2 encoding on Windows and UCS4 everywhere else :'(
IF UNAME_SYSNAME == "Windows":
    # Specify endianess otherwise `encode` appends a BOM at the start of the converted string
    DEF _STRING_ENCODING = "UTF-16-LE"
    DEF _STRING_CODEPOINT_LENGTH = 2
ELSE:
    DEF _STRING_ENCODING = "UTF-32-LE"
    DEF _STRING_CODEPOINT_LENGTH = 4


cdef inline str godot_string_to_pyobj(const godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    cdef char *raw = <char*>gdapi.godot_string_wide_str(p_gdstr)
    cdef godot_int length = gdapi.godot_string_length(p_gdstr)
    return raw[:length * _STRING_CODEPOINT_LENGTH].decode(_STRING_ENCODING)


cdef inline void pyobj_to_godot_string(str pystr, godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    cdef bytes raw = pystr.encode(_STRING_ENCODING)
    gdapi.godot_string_new_with_wide_string(
        p_gdstr, (<wchar_t*><char*>raw), len(pystr)
    )


cdef inline str godot_string_name_to_pyobj(const godot_string_name *p_gdname):
    cdef godot_string strname = gdapi.godot_string_name_get_name(p_gdname)
    cdef ret = godot_string_to_pyobj(&strname)
    gdapi.godot_string_destroy(&strname)
    return ret


cdef inline void pyobj_to_godot_string_name(str pystr, godot_string_name *p_gdname):
    cdef godot_string strname
    pyobj_to_godot_string(pystr, &strname)
    gdapi.godot_string_name_new(p_gdname, &strname)
    gdapi.godot_string_destroy(&strname)


cdef object godot_variant_to_pyobj(const godot_variant *p_gdvar)
cdef void pyobj_to_godot_variant(object pyobj, godot_variant *p_var)

cdef object godot_type_to_pyobj(godot_variant_type gdtype)
cdef godot_variant_type pyobj_to_godot_type(object pytype)
