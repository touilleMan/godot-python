# Public low-level APIs are exposed here

from godot._hazmat cimport gdnative_api_struct
# Re-expose Godot API with better names
from godot._hazmat.gdapi cimport (
    pythonscript_gdapi10 as gdapi10,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
    pythonscript_gdapi_ext_nativescript as gdapi_ext_nativescript,
    pythonscript_gdapi_ext_pluginscript as gdapi_ext_pluginscript,
    pythonscript_gdapi_ext_android as gdapi_ext_android,
    pythonscript_gdapi_ext_arvr as gdapi_ext_arvr,
)
from godot._hazmat.conversion cimport (
	godot_string_to_pyobj,
	pyobj_to_godot_string,
	godot_variant_to_pyobj,
	pyobj_to_godot_variant,
)
