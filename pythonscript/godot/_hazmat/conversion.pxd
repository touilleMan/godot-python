from libc.stddef cimport wchar_t
from libc.stdio cimport printf

from godot._hazmat.gdapi cimport pythonscript_gdapi as gdapi
from godot._hazmat.gdnative_api_struct cimport (
    godot_string,
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


cdef inline object godot_string_to_pyobj(const godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    cdef char *raw = <char*>gdapi.godot_string_wide_str(p_gdstr)
    cdef godot_int length = gdapi.godot_string_length(p_gdstr)
    return raw[:length * _STRING_CODEPOINT_LENGTH].decode(_STRING_ENCODING)


cdef inline pyobj_to_godot_string(object pystr, godot_string *p_gdstr):
    # TODO: unicode&windows support is most likely broken...
    cdef bytes raw = pystr.encode(_STRING_ENCODING)
    gdapi.godot_string_new_with_wide_string(
        p_gdstr, (<wchar_t*><char*>raw), len(pystr)
    )


cdef inline object godot_variant_to_pyobj(const godot_variant *p_gdvar):
    cdef godot_variant_type gdtype = gdapi.godot_variant_get_type(p_gdvar)

    if gdtype == godot_variant_type.GODOT_VARIANT_TYPE_NIL:
        return None

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_BOOL:
        return bool(gdapi.godot_variant_as_bool(p_gdvar))

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_INT:
        return int(gdapi.godot_variant_as_int(p_gdvar))

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_REAL:
        return float(gdapi.godot_variant_as_real(p_gdvar))

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_STRING:
        return _godot_variant_to_pyobj_string(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_VECTOR2:
        return _godot_variant_to_pyobj_vector2(p_gdvar)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_RECT2:
    #     raw = gdapi.godot_variant_as_rect2(p_gdvar)
    #     return godot_bindings_module.Rect2.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_VECTOR3:
    #     raw = gdapi.godot_variant_as_vector3(p_gdvar)
    #     return godot_bindings_module.Vector3.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM2D:
    #     raw = gdapi.godot_variant_as_transform2d(p_gdvar)
    #     return godot_bindings_module.Transform2D.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_PLANE:
    #     raw = gdapi.godot_variant_as_plane(p_gdvar)
    #     return godot_bindings_module.Plane.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_QUAT:
    #     raw = gdapi.godot_variant_as_quat(p_gdvar)
    #     return godot_bindings_module.Quat.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_AABB:
    #     raw = gdapi.godot_variant_as_aabb(p_gdvar)
    #     return godot_bindings_module.AABB.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_BASIS:
    #     raw = gdapi.godot_variant_as_basis(p_gdvar)
    #     return godot_bindings_module.Basis.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM:
    #     raw = gdapi.godot_variant_as_transform(p_gdvar)
    #     return godot_bindings_module.Transform.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_COLOR:
    #     raw = gdapi.godot_variant_as_color(p_gdvar)
    #     return godot_bindings_module.Color.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_NODE_PATH:
    #     p_raw = godot_node_path_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_node_path(p_gdvar)
    #     return godot_bindings_module.NodePath.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_RID:
    #     raw = gdapi.godot_variant_as_rid(p_gdvar)
    #     return godot_bindings_module.RID.build_from_gdobj(raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_OBJECT:
    #     p_raw = gdapi.godot_variant_as_object(p_gdvar)
    #     # TODO: optimize this
    #     tmpobj = godot_bindings_module.Object(p_raw)
    #     return getattr(godot_bindings_module, tmpobj.get_class())(p_raw)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_DICTIONARY:
    #     p_raw = godot_dictionary_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_dictionary(p_gdvar)
    #     return godot_bindings_module.Dictionary.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_ARRAY:
    #     p_raw = godot_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_array(p_gdvar)
    #     return godot_bindings_module.Array.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
    #     p_raw = godot_pool_byte_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_byte_array(p_gdvar)
    #     return godot_bindings_module.PoolByteArray.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
    #     p_raw = godot_pool_int_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_int_array(p_gdvar)
    #     return godot_bindings_module.PoolIntArray.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
    #     p_raw = godot_pool_real_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_real_array(p_gdvar)
    #     return godot_bindings_module.PoolRealArray.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
    #     p_raw = godot_pool_string_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_string_array(p_gdvar)
    #     return godot_bindings_module.PoolStringArray.build_from_gdobj(p_raw, steal=True)

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
    #     p_raw = godot_pool_vector2_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_vector2_array(p_gdvar)
    #     return godot_bindings_module.PoolVector2Array.build_from_gdobj(
    #         p_raw, steal=True
    #     )

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
    #     p_raw = godot_pool_vector3_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_vector3_array(p_gdvar)
    #     return godot_bindings_module.PoolVector3Array.build_from_gdobj(
    #         p_raw, steal=True
    #     )

    # elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
    #     p_raw = godot_pool_color_array_alloc(initialized=False)
    #     p_raw[0] = gdapi.godot_variant_as_pool_color_array(p_gdvar)
    #     return godot_bindings_module.PoolColorArray.build_from_gdobj(p_raw, steal=True)

    else:
        raise TypeError(
            f"Unknown Variant type `{gdtype}` (this should never happen !)"
        )


# Needed to define gdstr in it own scope
cdef inline object _godot_variant_to_pyobj_string(const godot_variant *p_gdvar):
    cdef godot_string gdstr = gdapi.godot_variant_as_string(p_gdvar)
    try:
        return godot_string_to_pyobj(&gdstr)
    finally:
        gdapi.godot_string_destroy(&gdstr)


# Needed to define gdvect2 in it own scope
cdef inline object _godot_variant_to_pyobj_vector2(const godot_variant *p_gdvar):
    cdef godot_vector2 gdvect2 = gdapi.godot_variant_as_vector2(p_gdvar)
    return Vector2.build_from_gdobj(gdvect2)


cdef inline void pyobj_to_godot_variant(object pyobj, godot_variant *p_var):
    if pyobj is None:
        gdapi.godot_variant_new_nil(p_var)
    elif isinstance(pyobj, bool):
        gdapi.godot_variant_new_bool(p_var, pyobj)
    elif isinstance(pyobj, int):
        gdapi.godot_variant_new_int(p_var, pyobj)
    elif isinstance(pyobj, float):
        gdapi.godot_variant_new_real(p_var, pyobj)
    elif isinstance(pyobj, str):
        _pyobj_to_godot_variant_convert_string(pyobj, p_var)
    elif isinstance(pyobj, Vector2):
        gdapi.godot_variant_new_vector2(p_var, (<Vector2>pyobj)._c_vector2_ptr())

    # TODO: finish other base types

    elif isinstance(pyobj, Object):
        gdapi.godot_variant_new_object(p_var, (<Object>pyobj)._ptr)
    else:
        raise TypeError(f"Cannot convert `{pyobj}` to Godot's Variant")


# Needed to define gdstr in it own scope
cdef inline void _pyobj_to_godot_variant_convert_string(object pyobj, godot_variant *p_var):
    cdef godot_string gdstr
    pyobj_to_godot_string(pyobj, &gdstr)
    try:
        gdapi.godot_variant_new_string(p_var, &gdstr)
    finally:
        gdapi.godot_string_destroy(&gdstr)
