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
from godot.bindings cimport Object
from godot.vector2 cimport Vector2
# from godot.rect2 cimport Rect2
# from godot.vector3 cimport Vector3
# from godot.transform2d cimport Transform2D
# from godot.plane cimport Plane
# from godot.quat cimport Quat
# from godot.aabb cimport AABB
# from godot.basis cimport Basis
# from godot.transform cimport Transform
# from godot.color cimport Color
# from godot.nodepath cimport NodePath
# from godot.rid cimport RID
from godot.dictionary cimport Dictionary
from godot.array cimport (
    Array,
    # PoolByteArray,
    # PoolIntArray,
    # PoolRealArray,
    # PoolStringArray,
    # PoolVector2Array,
    # PoolVector3Array,
    # PoolColorArray,
)


GD_PY_TYPES = (
    (godot_variant_type.GODOT_VARIANT_TYPE_NIL, type(None)),
    (godot_variant_type.GODOT_VARIANT_TYPE_BOOL, bool),
    (godot_variant_type.GODOT_VARIANT_TYPE_INT, int),
    (godot_variant_type.GODOT_VARIANT_TYPE_REAL, float),
    (godot_variant_type.GODOT_VARIANT_TYPE_STRING, str),
    (godot_variant_type.GODOT_VARIANT_TYPE_OBJECT, Object),
    (godot_variant_type.GODOT_VARIANT_TYPE_VECTOR2, Vector2),
    # (godot_variant_type.GODOT_VARIANT_TYPE_RECT2, Rect2),
    # (godot_variant_type.GODOT_VARIANT_TYPE_VECTOR3, Vector3),
    # (godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM2D, Transform2D),
    # (godot_variant_type.GODOT_VARIANT_TYPE_PLANE, Plane),
    # (godot_variant_type.GODOT_VARIANT_TYPE_QUAT, Quat),
    # (godot_variant_type.GODOT_VARIANT_TYPE_AABB, AABB),
    # (godot_variant_type.GODOT_VARIANT_TYPE_BASIS, Basis),
    # (godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM, Transform),
    # (godot_variant_type.GODOT_VARIANT_TYPE_COLOR, Color),
    # (godot_variant_type.GODOT_VARIANT_TYPE_NODE_PATH, NodePath),
    # (godot_variant_type.GODOT_VARIANT_TYPE_RID, RID),
    (godot_variant_type.GODOT_VARIANT_TYPE_DICTIONARY, Dictionary),
    (godot_variant_type.GODOT_VARIANT_TYPE_ARRAY, Array),
    # (
    #     godot_variant_type.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY,
    #     PoolByteArray,
    # ),
    # (godot_variant_type.GODOT_VARIANT_TYPE_POOL_INT_ARRAY, PoolIntArray),
    # (
    #     godot_variant_type.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY,
    #     PoolRealArray,
    # ),
    # (
    #     godot_variant_type.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY,
    #     PoolStringArray,
    # ),
    # (
    #     godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY,
    #     PoolVector2Array,
    # ),
    # (
    #     godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY,
    #     PoolVector3Array,
    # ),
    # (
    #     godot_variant_type.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY,
    #     PoolColorArray,
    # ),
)


cdef object godot_type_to_pyobj(godot_variant_type gdtype):
    cdef pytype = next((py for gd, py in GD_PY_TYPES if gd == gdtype), None)
    if pytype is None:
        raise TypeError(f"No Python equivalent for Godot type `{gdtype}`")

    return pytype


cdef godot_variant_type pyobj_to_godot_type(object pytype):
    cdef gdtype = next((gd for gd, py in GD_PY_TYPES if py == pytype), None)
    if gdtype is None:
        raise TypeError("No Godot equivalent for Python type `{pytype}`")

    return gdtype


cdef object godot_variant_to_pyobj(const godot_variant *p_gdvar):
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

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_DICTIONARY:
        return _godot_variant_to_pyobj_dictionary(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_ARRAY:
        return _godot_variant_to_pyobj_array(p_gdvar)

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


cdef inline str _godot_variant_to_pyobj_string(const godot_variant *p_gdvar):
    cdef godot_string gdstr = gdapi.godot_variant_as_string(p_gdvar)
    try:
        return godot_string_to_pyobj(&gdstr)
    finally:
        gdapi.godot_string_destroy(&gdstr)


cdef inline Vector2 _godot_variant_to_pyobj_vector2(const godot_variant *p_gdvar):
    cdef Vector2 vect = Vector2.__new__(Vector2)
    vect._gd_data = gdapi.godot_variant_as_vector2(p_gdvar)
    return vect


cdef inline Dictionary _godot_variant_to_pyobj_dictionary(const godot_variant *p_gdvar):
    cdef Dictionary d = Dictionary.__new__(Dictionary)
    d._gd_data = gdapi.godot_variant_as_dictionary(p_gdvar)
    return d


cdef inline Array _godot_variant_to_pyobj_array(const godot_variant *p_gdvar):
    cdef Array a = Array.__new__(Array)
    a._gd_data = gdapi.godot_variant_as_array(p_gdvar)
    return a


cdef void pyobj_to_godot_variant(object pyobj, godot_variant *p_var):
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
        gdapi.godot_variant_new_vector2(p_var, &(<Vector2>pyobj)._gd_data)
    elif isinstance(pyobj, Dictionary):
        gdapi.godot_variant_new_dictionary(p_var, &(<Dictionary>pyobj)._gd_data)
    elif isinstance(pyobj, Array):
        gdapi.godot_variant_new_array(p_var, &(<Array>pyobj)._gd_data)

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
