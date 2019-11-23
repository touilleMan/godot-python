# cython: c_string_type=unicode, c_string_encoding=utf8

from godot.hazmat cimport gdapi
from godot.hazmat.convert cimport godot_string_to_pyobj, pyobj_to_godot_string
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
    GODOT_ERR_UNAVAILABLE,
    GODOT_ERR_FILE_BAD_PATH,
    GODOT_ERR_PARSE_ERROR,
)
from godot.hazmat._internal cimport (
    get_pythonscript_verbose,
    get_exposed_class_per_module,
    destroy_exposed_classes,
)

import traceback


cdef inline _init_empty_manifest(godot_pluginscript_script_manifest *manifest):
    manifest.data = NULL
    gdapi.godot_string_name_new_data(&manifest.name, "")
    manifest.is_tool = False
    gdapi.godot_string_name_new_data(&manifest.base, "")
    gdapi.godot_dictionary_new(&manifest.member_lines)
    gdapi.godot_array_new(&manifest.methods)
    gdapi.godot_array_new(&manifest.signals)
    gdapi.godot_array_new(&manifest.properties)


cdef api godot_pluginscript_script_manifest pythonscript_script_init(
    godot_pluginscript_language_data *p_data,
    const godot_string *p_path,
    const godot_string *p_source,
    godot_error *r_error
):
    cdef godot_pluginscript_script_manifest manifest
    cdef object path = godot_string_to_pyobj(p_path)
    if get_pythonscript_verbose():
        print(f"Loading python script from {path}")

    if not path.startswith("res://") or not path.rsplit(".", 1)[-1] in (
        "py",
        "pyc",
        "pyo",
        "pyd",
    ):
        print(
            f"Bad python script path `{path}`, must starts by `res://` and ends with `.py/pyc/pyo/pyd`"
        )
        r_error[0] = GODOT_ERR_FILE_BAD_PATH
        # Obliged to return the structure, but no need in init it
        return manifest

    # TODO: possible bug if res:// is not part of PYTHONPATH
    # Remove `res://`, `.py` and replace / by .
    modname = path[6:].rsplit(".", 1)[0].replace("/", ".")
    try:
        __import__(modname)  # Force lazy loading of the module
        # TODO: make sure script reloading works
        cls = get_exposed_class_per_module(modname)
    except BaseException:
        # If we are here it could be because the file doesn't exists
        # or (more possibly) the file content is not a valid python (or
        # miss an exposed class)
        print(
            f"Got exception loading {path} ({modname}): {traceback.format_exc()}"
        )
        r_error[0] = GODOT_ERR_PARSE_ERROR
        # Obliged to return the structure, but no need in init it
        return manifest

    r_error[0] = GODOT_OK
    _init_empty_manifest(&manifest)
    return manifest
    # return _build_script_manifest(cls)[0]


cdef api void pythonscript_script_finish(
    godot_pluginscript_script_data *p_data
):
    destroy_exposed_classes()
