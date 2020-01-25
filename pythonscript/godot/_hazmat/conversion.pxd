from libc.stddef cimport wchar_t
from libc.stdio cimport printf

from godot._hazmat.gdapi cimport pythonscript_gdapi10 as gdapi10
from godot._hazmat.gdnative_api_struct cimport (
    godot_string,
    godot_string_name,
    godot_int,
    godot_vector2,
    godot_variant,
    godot_variant_type,
)
from godot.builtins cimport GDString, NodePath


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
    cdef char *raw = <char*>gdapi10.godot_string_wide_str(p_gdstr)
    cdef godot_int length = gdapi10.godot_string_length(p_gdstr)
    return raw[:length * _STRING_CODEPOINT_LENGTH].decode(_STRING_ENCODING)

    # cdef char *raw = <char*>gdapi10.godot_string_wide_str(p_gdstr)
    # cdef godot_int length = gdapi10.godot_string_length(p_gdstr)
    # printf("==========> godot_string_to_pyobj ")
    # cdef int i
    # for i in range(length):
    #     printf("%c ", raw[i * 4]);
    # printf("\n")
    # cdef object ret = raw[:length * _STRING_CODEPOINT_LENGTH].decode(_STRING_ENCODING)
    # print('==>ret: %r' % ret)
    # return ret


cdef inline void pyobj_to_godot_string(str pystr, godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    cdef bytes raw = pystr.encode(_STRING_ENCODING)
    gdapi10.godot_string_new_with_wide_string(
        p_gdstr, (<wchar_t*><char*>raw), len(pystr)
    )


cdef inline str godot_string_name_to_pyobj(const godot_string_name *p_gdname):
    cdef godot_string strname = gdapi10.godot_string_name_get_name(p_gdname)
    cdef ret = godot_string_to_pyobj(&strname)
    gdapi10.godot_string_destroy(&strname)
    return ret


cdef inline void pyobj_to_godot_string_name(str pystr, godot_string_name *p_gdname):
    cdef godot_string strname
    pyobj_to_godot_string(pystr, &strname)
    gdapi10.godot_string_name_new(p_gdname, &strname)
    gdapi10.godot_string_destroy(&strname)


cdef object godot_variant_to_pyobj(const godot_variant *p_gdvar)
cdef bint pyobj_to_godot_variant(object pyobj, godot_variant *p_var)

cdef bint is_pytype_compatible_with_godot_variant(object pytype)
cdef object godot_type_to_pytype(godot_variant_type gdtype)
cdef godot_variant_type pytype_to_godot_type(object pytype)

cdef GDString ensure_is_gdstring(object gdstring_or_pystr)
cdef NodePath ensure_is_nodepath(object nodepath_or_pystr)


# TODO: finish this...

# cdef inline object cook_slice(slice slice_, godot_int size, godot_int *r_start, godot_int *r_stop, godot_int *r_step, godot_int *r_items):
#     cdef godot_int start
#     cdef godot_int stop
#     cdef godot_int step

#     step = slice_.step if slice_.step is not None else 1
#     if step == 0:
#         raise ValueError("range() arg 3 must not be zero")
#     elif step > 0:
#         start = slice_.start if slice_.start is not None else 0
#         stop = slice_.stop if slice_.stop is not None else size
#     else:
#         start = slice_.start if slice_.start is not None else size
#         stop = slice_.stop if slice_.stop is not None else -size - 1

#     r_start[0] = cook_slice_start(size, start)
#     r_stop[0] = cook_slice_stop(size, stop)
#     r_step[0] = step
#     r_items[0] = cook_slice_get_items(size, start, stop, step)

#     return None


# cdef inline godot_int cook_slice_start(godot_int size, godot_int start):
#     if start > size - 1:
#         return size - 1
#     elif start < 0:
#         start += size
#         if start < 0:
#             return 0
#     return start


# cdef inline godot_int cook_slice_stop(godot_int size, godot_int stop):
#     if stop > size:
#         return size
#     elif stop < -size:
#         return -1
#     elif stop < 0:
#         stop += size
#     return stop


# cdef inline godot_int cook_slice_get_items(godot_int size, godot_int start, godot_int stop, godot_int step):
#     cdef godot_int items
#     if step > 0:
#         if start >= stop:
#             return 0
#         items = 1 + (stop - start - 1) // step
#     else:
#         if start <= stop:
#             return 0
#         items = 1 + (stop - start + 1) // step
#     return items if items > 0 else 0
