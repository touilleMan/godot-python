# cython: c_string_type=unicode, c_string_encoding=utf8

from godot.hazmat cimport gdapi
from godot.hazmat.gdnative_api_struct cimport (
    godot_pluginscript_language_data,
    godot_string,
    godot_bool,
    godot_array,
    godot_pool_string_array,
    godot_object,
    godot_variant,
    godot_error,
    godot_string_name,
    godot_pluginscript_script_data,
    godot_pluginscript_script_manifest,
    GODOT_OK,
    GODOT_ERR_UNAVAILABLE
)

# from cpython.ref cimport PyObject 
# from libc.stddef cimport wchar_t

# cdef extern from "Python.h":
#     PyObject* PyUnicode_FromWideChar(wchar_t *w, Py_ssize_t size)


# cdef inline void py_to_gd_str(str pystr, godot_string *gd_str):
#     # TODO: this is probably broken for unicode...
#     gdapi.godot_string_new_with_wide_string(gd_str, pystr, len(pystr))


# cdef inline void py_to_gd_strname(str pystr, godot_string_name *gd_str):
#     gdapi.godot_string_name_new_data(gd_str, pystr)


# cdef inline str gd_to_py_strname(godot_string_name *gd_str):
#     cdef godot_string gdstr = gdapi.godot_string_name_get_name(p_gdstring)
#     return gd_to_py_str(gdstr)


# cdef inline str gd_to_py_str(godot_string_name *gd_str):
#     cdef wchar_t *raw_str = gdapi.godot_string_wide_str(p_gdstring)
#     return raw_str


cdef api godot_pluginscript_script_manifest pythonscript_script_init(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_path,
    const godot_string *p_source,
    godot_error *r_error
):
    cdef godot_pluginscript_script_manifest manifest
    manifest.data = NULL
    gdapi.godot_string_name_new_data(&manifest.name, "")
    manifest.is_tool = False
    gdapi.godot_string_name_new_data(&manifest.base, "")
    gdapi.godot_dictionary_new(&manifest.member_lines)
    gdapi.godot_array_new(&manifest.methods)
    gdapi.godot_array_new(&manifest.signals)
    gdapi.godot_array_new(&manifest.properties)

    r_error[0] = GODOT_OK

    # # cdef wchar_t *cpath = godot_string_wide_str(p_path)
    # # path = PyUnicode_FromWideChar(cpath, -1)
    # # print(f"Init script {path}")
    # print('Init script')
    # r_error[0] = GODOT_ERR_UNAVAILABLE

    return manifest


cdef api void pythonscript_script_finish(
    godot_pluginscript_script_data *p_data
):
    pass
