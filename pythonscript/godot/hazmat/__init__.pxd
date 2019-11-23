from godot.hazmat cimport gdnative_api_struct
from godot.hazmat cimport convert
# Re-expose Godot API with better names
from godot.hazmat._gdapi cimport (
    pythonscript_gdapi as gdapi,
    pythonscript_gdapi11 as gdapi11,
    pythonscript_gdapi12 as gdapi12,
    pythonscript_gdapi_ext_nativescript as gdapi_ext_nativescript,
    pythonscript_gdapi_ext_pluginscript as gdapi_ext_pluginscript,
    pythonscript_gdapi_ext_android as gdapi_ext_android,
    pythonscript_gdapi_ext_arvr as gdapi_ext_arvr,
)
