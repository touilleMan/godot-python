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
    godot_string_wide_str,
    godot_pluginscript_script_data,
    godot_pluginscript_script_manifest,
    GODOT_ERR_UNAVAILABLE
)

# from cpython.ref cimport PyObject 
# from libc.stddef cimport wchar_t

# cdef extern from "Python.h":
#     PyObject* PyUnicode_FromWideChar(wchar_t *w, Py_ssize_t size)

cdef api godot_pluginscript_script_manifest pythonscript_script_init(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_path,
    const godot_string *p_source,
    godot_error *r_error
):
    # cdef wchar_t *cpath = godot_string_wide_str(p_path)
    # path = PyUnicode_FromWideChar(cpath, -1)
    # print(f"Init script {path}")
    print('Init script')
    r_error[0] = GODOT_ERR_UNAVAILABLE


cdef api void pythonscript_script_finish(
    godot_pluginscript_script_data *p_data
):
    pass
