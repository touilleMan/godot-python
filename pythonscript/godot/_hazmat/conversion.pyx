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
from godot.rect2 cimport Rect2
from godot.vector3 cimport Vector3
from godot.transform2d cimport Transform2D
from godot.plane cimport Plane
from godot.quat cimport Quat
from godot.aabb cimport AABB
from godot.basis cimport Basis
from godot.transform cimport Transform
from godot.color cimport Color
from godot.node_path cimport NodePath
from godot.rid cimport RID
from godot.dictionary cimport Dictionary
from godot.array cimport Array
from godot.gdstring cimport GDString
from godot.pool_arrays cimport (
    PoolByteArray,
    PoolIntArray,
    PoolRealArray,
    PoolStringArray,
    PoolVector2Array,
    PoolVector3Array,
    PoolColorArray,
)

from warnings import warn


GD_PY_TYPES = (
    (godot_variant_type.GODOT_VARIANT_TYPE_NIL, type(None)),
    (godot_variant_type.GODOT_VARIANT_TYPE_BOOL, bool),
    (godot_variant_type.GODOT_VARIANT_TYPE_INT, int),
    (godot_variant_type.GODOT_VARIANT_TYPE_REAL, float),
    (godot_variant_type.GODOT_VARIANT_TYPE_STRING, GDString),
    (godot_variant_type.GODOT_VARIANT_TYPE_OBJECT, Object),
    (godot_variant_type.GODOT_VARIANT_TYPE_VECTOR2, Vector2),
    (godot_variant_type.GODOT_VARIANT_TYPE_RECT2, Rect2),
    (godot_variant_type.GODOT_VARIANT_TYPE_VECTOR3, Vector3),
    (godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM2D, Transform2D),
    (godot_variant_type.GODOT_VARIANT_TYPE_PLANE, Plane),
    (godot_variant_type.GODOT_VARIANT_TYPE_QUAT, Quat),
    (godot_variant_type.GODOT_VARIANT_TYPE_AABB, AABB),
    (godot_variant_type.GODOT_VARIANT_TYPE_BASIS, Basis),
    (godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM, Transform),
    (godot_variant_type.GODOT_VARIANT_TYPE_COLOR, Color),
    (godot_variant_type.GODOT_VARIANT_TYPE_NODE_PATH, NodePath),
    (godot_variant_type.GODOT_VARIANT_TYPE_RID, RID),
    (godot_variant_type.GODOT_VARIANT_TYPE_DICTIONARY, Dictionary),
    (godot_variant_type.GODOT_VARIANT_TYPE_ARRAY, Array),
    (
        godot_variant_type.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY,
        PoolByteArray,
    ),
    (godot_variant_type.GODOT_VARIANT_TYPE_POOL_INT_ARRAY, PoolIntArray),
    (
        godot_variant_type.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY,
        PoolRealArray,
    ),
    (godot_variant_type.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY, PoolStringArray),
    (
        godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY,
        PoolVector2Array,
    ),
    (
        godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY,
        PoolVector3Array,
    ),
    (
        godot_variant_type.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY,
        PoolColorArray,
    ),
)


cdef object godot_type_to_pyobj(godot_variant_type gdtype):
    cdef pytype = next((py for gd, py in GD_PY_TYPES if gd == gdtype), None)
    if pytype is None:
        warn(f"No Python equivalent for Godot type `{gdtype}`")
        return None

    return pytype


cdef godot_variant_type pyobj_to_godot_type(object pytype):
    cdef gdtype = next((gd for gd, py in GD_PY_TYPES if py == pytype), None)
    if gdtype is None:
        warn(f"No Godot equivalent for Python type `{pytype}`")
        return godot_variant_type.GODOT_VARIANT_TYPE_NIL

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

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_RECT2:
        return _godot_variant_to_pyobj_rect2(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_VECTOR3:
        return _godot_variant_to_pyobj_vector3(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM2D:
        return _godot_variant_to_pyobj_transform2d(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_PLANE:
        return _godot_variant_to_pyobj_plane(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_QUAT:
        return _godot_variant_to_pyobj_quat(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_AABB:
        return _godot_variant_to_pyobj_aabb(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_BASIS:
        return _godot_variant_to_pyobj_basis(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_TRANSFORM:
        return _godot_variant_to_pyobj_transform(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_COLOR:
        return _godot_variant_to_pyobj_color(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_NODE_PATH:
        return _godot_variant_to_pyobj_node_path(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_RID:
        return _godot_variant_to_pyobj_rid(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_OBJECT:
        return _godot_variant_to_pyobj_object(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_DICTIONARY:
        return _godot_variant_to_pyobj_dictionary(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_ARRAY:
        return _godot_variant_to_pyobj_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        return _godot_variant_to_pyobj_pool_byte_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        return _godot_variant_to_pyobj_pool_int_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        return _godot_variant_to_pyobj_pool_real_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        return _godot_variant_to_pyobj_pool_string_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        return _godot_variant_to_pyobj_pool_vector2_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        return _godot_variant_to_pyobj_pool_vector3_array(p_gdvar)

    elif gdtype == godot_variant_type.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        return _godot_variant_to_pyobj_pool_color_array(p_gdvar)

    else:
        warn(f"Unknown Variant type `{gdtype}` (this should never happen !)")
        return None


cdef inline GDString _godot_variant_to_pyobj_string(const godot_variant *p_gdvar):
    cdef GDString ret = GDString.__new__(GDString)
    ret._gd_data = gdapi.godot_variant_as_string(p_gdvar)
    return ret


cdef inline Vector2 _godot_variant_to_pyobj_vector2(const godot_variant *p_gdvar):
    cdef Vector2 ret = Vector2.__new__(Vector2)
    ret._gd_data = gdapi.godot_variant_as_vector2(p_gdvar)
    return ret


cdef inline Rect2 _godot_variant_to_pyobj_rect2(const godot_variant *p_gdvar):
    cdef Rect2 ret = Rect2.__new__(Rect2)
    ret._gd_data = gdapi.godot_variant_as_rect2(p_gdvar)
    return ret


cdef inline Vector3 _godot_variant_to_pyobj_vector3(const godot_variant *p_gdvar):
    cdef Vector3 ret = Vector3.__new__(Vector3)
    ret._gd_data = gdapi.godot_variant_as_vector3(p_gdvar)
    return ret


cdef inline Transform2D _godot_variant_to_pyobj_transform2d(const godot_variant *p_gdvar):
    cdef Transform2D ret = Transform2D.__new__(Transform2D)
    ret._gd_data = gdapi.godot_variant_as_transform2d(p_gdvar)
    return ret


cdef inline Transform _godot_variant_to_pyobj_transform(const godot_variant *p_gdvar):
    cdef Transform ret = Transform.__new__(Transform)
    ret._gd_data = gdapi.godot_variant_as_transform(p_gdvar)
    return ret


cdef inline Plane _godot_variant_to_pyobj_plane(const godot_variant *p_gdvar):
    cdef Plane ret = Plane.__new__(Plane)
    ret._gd_data = gdapi.godot_variant_as_plane(p_gdvar)
    return ret


cdef inline Quat _godot_variant_to_pyobj_quat(const godot_variant *p_gdvar):
    cdef Quat ret = Quat.__new__(Quat)
    ret._gd_data = gdapi.godot_variant_as_quat(p_gdvar)
    return ret


cdef inline AABB _godot_variant_to_pyobj_aabb(const godot_variant *p_gdvar):
    cdef AABB ret = AABB.__new__(AABB)
    ret._gd_data = gdapi.godot_variant_as_aabb(p_gdvar)
    return ret


cdef inline Basis _godot_variant_to_pyobj_basis(const godot_variant *p_gdvar):
    cdef Basis ret = Basis.__new__(Basis)
    ret._gd_data = gdapi.godot_variant_as_basis(p_gdvar)
    return ret


cdef inline Color _godot_variant_to_pyobj_color(const godot_variant *p_gdvar):
    cdef Color ret = Color.__new__(Color)
    ret._gd_data = gdapi.godot_variant_as_color(p_gdvar)
    return ret


cdef inline NodePath _godot_variant_to_pyobj_node_path(const godot_variant *p_gdvar):
    cdef NodePath ret = NodePath.__new__(NodePath)
    ret._gd_data = gdapi.godot_variant_as_node_path(p_gdvar)
    return ret


cdef inline RID _godot_variant_to_pyobj_rid(const godot_variant *p_gdvar):
    cdef RID ret = RID.__new__(RID)
    ret._gd_data = gdapi.godot_variant_as_rid(p_gdvar)
    return ret


cdef inline Object _godot_variant_to_pyobj_object(const godot_variant *p_gdvar):
    return Object.from_ptr(gdapi.godot_variant_as_object(p_gdvar), owner=False)


cdef inline Dictionary _godot_variant_to_pyobj_dictionary(const godot_variant *p_gdvar):
    cdef Dictionary d = Dictionary.__new__(Dictionary)
    d._gd_data = gdapi.godot_variant_as_dictionary(p_gdvar)
    return d


cdef inline Array _godot_variant_to_pyobj_array(const godot_variant *p_gdvar):
    cdef Array a = Array.__new__(Array)
    a._gd_data = gdapi.godot_variant_as_array(p_gdvar)
    return a


cdef inline PoolByteArray _godot_variant_to_pyobj_pool_byte_array(const godot_variant *p_gdvar):
    cdef PoolByteArray a = PoolByteArray.__new__(PoolIntArray)
    a._gd_data = gdapi.godot_variant_as_pool_byte_array(p_gdvar)
    return a


cdef inline PoolIntArray _godot_variant_to_pyobj_pool_int_array(const godot_variant *p_gdvar):
    cdef PoolIntArray a = PoolIntArray.__new__(PoolIntArray)
    a._gd_data = gdapi.godot_variant_as_pool_int_array(p_gdvar)
    return a


cdef inline PoolRealArray _godot_variant_to_pyobj_pool_real_array(const godot_variant *p_gdvar):
    cdef PoolRealArray a = PoolRealArray.__new__(PoolRealArray)
    a._gd_data = gdapi.godot_variant_as_pool_real_array(p_gdvar)
    return a


cdef inline PoolStringArray _godot_variant_to_pyobj_pool_string_array(const godot_variant *p_gdvar):
    cdef PoolStringArray a = PoolStringArray.__new__(PoolStringArray)
    a._gd_data = gdapi.godot_variant_as_pool_string_array(p_gdvar)
    return a


cdef inline PoolVector2Array _godot_variant_to_pyobj_pool_vector2_array(const godot_variant *p_gdvar):
    cdef PoolVector2Array a = PoolVector2Array.__new__(PoolVector2Array)
    a._gd_data = gdapi.godot_variant_as_pool_vector2_array(p_gdvar)
    return a


cdef inline PoolVector3Array _godot_variant_to_pyobj_pool_vector3_array(const godot_variant *p_gdvar):
    cdef PoolVector3Array a = PoolVector3Array.__new__(PoolVector3Array)
    a._gd_data = gdapi.godot_variant_as_pool_vector3_array(p_gdvar)
    return a


cdef inline PoolColorArray _godot_variant_to_pyobj_pool_color_array(const godot_variant *p_gdvar):
    cdef PoolColorArray a = PoolColorArray.__new__(PoolColorArray)
    a._gd_data = gdapi.godot_variant_as_pool_color_array(p_gdvar)
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
    elif isinstance(pyobj, GDString):
        gdapi.godot_variant_new_string(p_var, &(<GDString>pyobj)._gd_data)
    elif isinstance(pyobj, Vector2):
        gdapi.godot_variant_new_vector2(p_var, &(<Vector2>pyobj)._gd_data)
    elif isinstance(pyobj, Vector3):
        gdapi.godot_variant_new_vector3(p_var, &(<Vector3>pyobj)._gd_data)
    elif isinstance(pyobj, Plane):
        gdapi.godot_variant_new_plane(p_var, &(<Plane>pyobj)._gd_data)
    elif isinstance(pyobj, Quat):
        gdapi.godot_variant_new_quat(p_var, &(<Quat>pyobj)._gd_data)
    elif isinstance(pyobj, AABB):
        gdapi.godot_variant_new_aabb(p_var, &(<AABB>pyobj)._gd_data)
    elif isinstance(pyobj, Basis):
        gdapi.godot_variant_new_basis(p_var, &(<Basis>pyobj)._gd_data)
    elif isinstance(pyobj, Color):
        gdapi.godot_variant_new_color(p_var, &(<Color>pyobj)._gd_data)
    elif isinstance(pyobj, NodePath):
        gdapi.godot_variant_new_node_path(p_var, &(<NodePath>pyobj)._gd_data)
    elif isinstance(pyobj, RID):
        gdapi.godot_variant_new_rid(p_var, &(<RID>pyobj)._gd_data)
    elif isinstance(pyobj, Rect2):
        gdapi.godot_variant_new_rect2(p_var, &(<Rect2>pyobj)._gd_data)
    elif isinstance(pyobj, Transform2D):
        gdapi.godot_variant_new_transform2d(p_var, &(<Transform2D>pyobj)._gd_data)
    elif isinstance(pyobj, Transform):
        gdapi.godot_variant_new_transform(p_var, &(<Transform>pyobj)._gd_data)
    elif isinstance(pyobj, Dictionary):
        gdapi.godot_variant_new_dictionary(p_var, &(<Dictionary>pyobj)._gd_data)
    elif isinstance(pyobj, Array):
        gdapi.godot_variant_new_array(p_var, &(<Array>pyobj)._gd_data)
    elif isinstance(pyobj, PoolByteArray):
        gdapi.godot_variant_new_pool_byte_array(p_var, &(<PoolByteArray>pyobj)._gd_data)
    elif isinstance(pyobj, PoolIntArray):
        gdapi.godot_variant_new_pool_int_array(p_var, &(<PoolIntArray>pyobj)._gd_data)
    elif isinstance(pyobj, PoolRealArray):
        gdapi.godot_variant_new_pool_real_array(p_var, &(<PoolRealArray>pyobj)._gd_data)
    elif isinstance(pyobj, PoolStringArray):
        gdapi.godot_variant_new_pool_string_array(p_var, &(<PoolStringArray>pyobj)._gd_data)
    elif isinstance(pyobj, PoolVector2Array):
        gdapi.godot_variant_new_pool_vector2_array(p_var, &(<PoolVector2Array>pyobj)._gd_data)
    elif isinstance(pyobj, PoolVector3Array):
        gdapi.godot_variant_new_pool_vector3_array(p_var, &(<PoolVector3Array>pyobj)._gd_data)
    elif isinstance(pyobj, PoolColorArray):
        gdapi.godot_variant_new_pool_color_array(p_var, &(<PoolColorArray>pyobj)._gd_data)
    elif isinstance(pyobj, Object):
        gdapi.godot_variant_new_object(p_var, (<Object>pyobj)._gd_ptr)
    else:
        warn(f"Cannot convert `{type(pyobj)}` to Godot's Variant")
        gdapi.godot_variant_new_nil(p_var)


# Needed to define gdstr in it own scope
cdef inline void _pyobj_to_godot_variant_convert_string(object pyobj, godot_variant *p_var):
    cdef godot_string gdstr
    pyobj_to_godot_string(pyobj, &gdstr)
    try:
        gdapi.godot_variant_new_string(p_var, &gdstr)
    finally:
        gdapi.godot_string_destroy(&gdstr)
