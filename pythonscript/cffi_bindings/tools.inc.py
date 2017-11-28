import sys
import imp
from pythonscriptcffi import ffi, lib

# A bit of naming:
# pyobj is a regular Python Object
# gdobj is a pointer on memory where is stored the data of a Godot object
# variant is a pointer on memory where is stored a Godot Variant
#
# Pay attention not to mix pointers and actual memory (given the latter
# doesn't exist in Python)


def godot_string_to_pyobj(p_gdstring):
    raw_str = lib.godot_string_unicode_str(p_gdstring)
    return ffi.string(raw_str)


def godot_string_from_pyobj(pystr):
    if isinstance(pystr, str):
        gdstr = godot_string_alloc()
        lib.godot_string_new_unicode_data(gdstr, pystr, len(pystr))
    elif isinstance(pystr, bytes):
        gdstr = godot_string_alloc()
        lib.godot_string_new_data(gdstr, pystr, len(pystr))
    else:
        raise TypeError('`pystr` must be `str` or `bytes`')
    return gdstr


def variant_to_pyobj(p_gdvar):
    """
    Convert Godot variant to regular Python object
    :param p_gdvar: Godot variant as ``<cdata 'struct godot_variant *'>`` (note the pointer)
    """
    gdtype = lib.godot_variant_get_type(p_gdvar)
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        return None
    elif gdtype == lib.GODOT_VARIANT_TYPE_BOOL:
        return bool(lib.godot_variant_as_bool(p_gdvar))
    elif gdtype == lib.GODOT_VARIANT_TYPE_INT:
        return int(lib.godot_variant_as_int(p_gdvar))
    elif gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        return float(lib.godot_variant_as_real(p_gdvar))
    elif gdtype == lib.GODOT_VARIANT_TYPE_STRING:
        raw = lib.godot_variant_as_string(p_gdvar)
        return godot_string_to_pyobj(ffi.addressof(raw))
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        raw = lib.godot_variant_as_vector2(p_gdvar)
        return Vector2.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        raw = lib.godot_variant_as_rec2(p_gdvar)
        return Rect2.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        raw = lib.godot_variant_as_vector3(p_gdvar)
        return Vector3.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        raw = lib.godot_variant_as_transform2d(p_gdvar)
        return Transform2D.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        raw = lib.godot_variant_as_plane(p_gdvar)
        return Plane.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        raw = lib.godot_variant_as_quat(p_gdvar)
        return Quat.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_AABB:
        raw = lib.godot_variant_as_aabb(p_gdvar)
        return AABB.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        raw = lib.godot_variant_as_basis(p_gdvar)
        return Basis.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        raw = lib.godot_variant_as_transform(p_gdvar)
        return Transform.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        raw = lib.godot_variant_as_color(p_gdvar)
        return Color.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raw = lib.godot_variant_as_node_path(p_gdvar)
        return NodePath.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raw = lib.godot_variant_as_rid(p_gdvar)
        return RID.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        p_raw = lib.godot_variant_as_object(p_gdvar)
        # TODO: optimize this
        tmpobj = godot_bindings_module.Object(p_raw)
        return getattr(godot_bindings_module, tmpobj.get_class())(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        raw = lib.godot_variant_as_dictionary(p_gdvar)
        return Dictionary.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        raw = lib.godot_variant_as_array(p_gdvar)
        return Array.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        raw = lib.godot_variant_as_pool_byte_array(p_gdvar)
        return PoolByteArray.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        raw = lib.godot_variant_as_pool_int_array(p_gdvar)
        return PoolIntArray.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        raw = lib.godot_variant_as_pool_real_array(p_gdvar)
        return PoolRealArray.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        raw = lib.godot_variant_as_pool_string_array(p_gdvar)
        return PoolStringArray.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        raw = lib.godot_variant_as_pool_vector2_array(p_gdvar)
        return PoolVector2Array.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        raw = lib.godot_variant_as_pool_vector3_array(p_gdvar)
        return PoolVector3Array.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        raw = lib.godot_variant_as_pool_color_array(p_gdvar)
        return PoolColorArray.build_from_gdobj(raw)
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)


def pyobj_to_variant(pyobj, p_gdvar=None):
    # `initialized=False` means we MUST manually init this by hand no matter what
    p_gdvar = p_gdvar if p_gdvar else godot_variant_alloc(initialized=False)
    try:
        if pyobj is None:
            lib.godot_variant_new_nil(p_gdvar)
        elif (isinstance(pyobj, bool)):
            lib.godot_variant_new_bool(p_gdvar, pyobj)
        elif (isinstance(pyobj, int)):
            lib.godot_variant_new_int(p_gdvar, pyobj)
        elif (isinstance(pyobj, float)):
            lib.godot_variant_new_real(p_gdvar, pyobj)
        elif (isinstance(pyobj, str)):
            gdstr = ffi.new("godot_string*")
            pyobj_as_bytes = pyobj.encode()
            lib.godot_string_new_data(gdstr, pyobj_as_bytes, len(pyobj_as_bytes))
            lib.godot_variant_new_string(p_gdvar, gdstr)
        elif (isinstance(pyobj, bytes)):
            gdstr = ffi.new("godot_string*")
            lib.godot_string_new_data(gdstr, pyobj, len(pyobj))
            lib.godot_variant_new_string(p_gdvar, gdstr)
        elif isinstance(pyobj, BaseBuiltin):
            if pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_VECTOR2:
                lib.godot_variant_new_vector2(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RECT2:
                lib.godot_variant_new_rect2(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_VECTOR3:
                lib.godot_variant_new_vector3(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
                lib.godot_variant_new_transform2d(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_PLANE:
                lib.godot_variant_new_plane(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_QUAT:
                lib.godot_variant_new_quat(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_AABB:
                lib.godot_variant_new_aabb(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_BASIS:
                lib.godot_variant_new_basis(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_TRANSFORM:
                lib.godot_variant_new_transform(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_COLOR:
                lib.godot_variant_new_color(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_NODE_PATH:
                lib.godot_variant_new_nodepath(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RID:
                lib.godot_variant_new_rid(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_OBJECT:
                lib.godot_variant_new_object(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_DICTIONARY:
                lib.godot_variant_new_dictionary(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_ARRAY:
                lib.godot_variant_new_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLBYTEARRAY:
                lib.godot_variant_new_poolbytearray(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLINTARRAY:
                lib.godot_variant_new_poolintarray(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLREALARRAY:
                lib.godot_variant_new_poolrealarray(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLSTRINGARRAY:
                lib.godot_variant_new_poolstringarray(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLVECTOR2ARRAY:
                lib.godot_variant_new_poolvector2array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLVECTOR3ARRAY:
                lib.godot_variant_new_poolvector3array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLCOLORARRAY:
                lib.godot_variant_new_poolcolorarray(p_gdvar, pyobj._gd_ptr)
        elif isinstance(pyobj, BaseObject):
            lib.godot_variant_new_object(p_gdvar, pyobj._gd_ptr)
        else:
            raise TypeError("Cannot convert `%s` to Godot's Variant" % pyobj)
    except:
        # Must init the variant anyway to avoid segfault in it destructor
        lib.godot_variant_new_nil(p_gdvar)
        raise
    return p_gdvar


def new_uninitialized_gdobj(gdtype):
    # TODO: use dict to optimize this ?
    # It seems Godot encode Variant as type nil...
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        return godot_variant_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_BOOL:
        return godot_bool_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_INT:
        return godot_int_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        return godot_real_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_STRING:
        return godot_string_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        return godot_vector2_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        return godot_rect2_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        return godot_vector3_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        return godot_transform2d_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        return godot_plane_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        return godot_quat_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_AABB:
        return godot_aabb_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        return godot_basis_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        return godot_transform_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        return godot_color_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        return godot_node_path_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        return godot_rid_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        return godot_object_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        return godot_dictionary_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        return godot_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        return godot_pool_byte_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        return godot_pool_int_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        return godot_pool_real_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        return godot_pool_string_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        return godot_pool_vector2_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        return godot_pool_vector3_array_alloc()
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        return godot_pool_color_array_alloc()
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)


def gdobj_to_pyobj(gdtype, p_gdobj, steal_gdobj=True):
    # It seems Godot encode Variant as type nil...
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        if p_gdobj == ffi.NULL:
            return None
        else:
            return variant_to_pyobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_BOOL:
        return bool(p_gdobj[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_INT:
        return int(p_gdobj[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        return float(p_gdobj[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_STRING:
        return godot_string_to_pyobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        return Vector2.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        return Rect2.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        return Vector3.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        return Transform2d.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        return Plane.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        return Quat.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_AABB:
        return AABB.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        return Basis.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        return Transform.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        return Color.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        return NodePath.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        return RID.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        # TODO: optimize this
        tmpobj = godot_bindings_module.Object(p_gdobj[0])
        return getattr(godot_bindings_module, tmpobj.get_class())(p_gdobj[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        return Dictionary.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        return Array.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        return PoolByteArray.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        return PoolIntArray.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        return PoolRealArray.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        return PoolStringArray.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        return PoolVector2Array.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        return PoolVector3Array.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        return PoolColorArray.build_from_gdobj(p_gdobj, steal=steal_gdobj)
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)


def pyobj_to_gdobj(pyobj, steal_gdobj=True):
    if pyobj is None:
        return ffi.NULL
    elif isinstance(pyobj, bool):
        return godot_bool_alloc(1 if pyobj else 0)
    elif isinstance(pyobj, int):
        return godot_int_alloc(pyobj)
    elif isinstance(pyobj, float):
        return godot_real_alloc(pyobj)
    elif isinstance(pyobj, str):
        gdobj = godot_string_alloc()
        lib.godot_string_new_unicode_data(gdobj, pyobj, -1)
        return gdobj
    elif isinstance(pyobj, BaseBuiltinWithGDObjOwnership):
        if steal_gdobj:
            return pyobj._gd_ptr
        else:
            return pyobj._copy_gdobj(pyobj._gd_ptr)
    elif isinstance(pyobj, BaseBuiltin):
        return pyobj._gd_ptr
    elif isinstance(pyobj, BaseObject):
        # TODO: copy ptr box ?
        return pyobj._gd_ptr
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)


GD_PY_TYPES = (
    (lib.GODOT_VARIANT_TYPE_NIL, type(None)),
    (lib.GODOT_VARIANT_TYPE_BOOL, bool),
    (lib.GODOT_VARIANT_TYPE_INT, int),
    (lib.GODOT_VARIANT_TYPE_REAL, float),
    (lib.GODOT_VARIANT_TYPE_STRING, str),
    (lib.GODOT_VARIANT_TYPE_VECTOR2, Vector2),
    (lib.GODOT_VARIANT_TYPE_RECT2, Rect2),
    (lib.GODOT_VARIANT_TYPE_VECTOR3, Vector3),
    (lib.GODOT_VARIANT_TYPE_TRANSFORM2D, Transform2D),
    (lib.GODOT_VARIANT_TYPE_PLANE, Plane),
    (lib.GODOT_VARIANT_TYPE_QUAT, Quat),
    (lib.GODOT_VARIANT_TYPE_AABB, AABB),
    (lib.GODOT_VARIANT_TYPE_BASIS, Basis),
    (lib.GODOT_VARIANT_TYPE_TRANSFORM, Transform),
    (lib.GODOT_VARIANT_TYPE_COLOR, Color),
    (lib.GODOT_VARIANT_TYPE_NODE_PATH, NodePath),
    (lib.GODOT_VARIANT_TYPE_RID, RID),
    # (lib.GODOT_VARIANT_TYPE_OBJECT, BaseObject),  # TODO: recursive import error ?
    (lib.GODOT_VARIANT_TYPE_DICTIONARY, Dictionary),
    (lib.GODOT_VARIANT_TYPE_ARRAY, Array),
    (lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY, PoolByteArray),
    (lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY, PoolIntArray),
    (lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY, PoolRealArray),
    (lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY, PoolStringArray),
    (lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY, PoolVector2Array),
    (lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY, PoolVector3Array),
    (lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY, PoolColorArray),
)


def gd_to_py_type(gdtype):
    pytype = next((py for gd, py in GD_PY_TYPES if gd == gdtype), None)
    if pytype is None:
        raise RuntimeError('No Python equivalent for Godot type `%s`' % gdtype)
    return pytype


def py_to_gd_type(pytype):
    gdtype = next((gd for gd, py in GD_PY_TYPES if py == pytype), None)
    if gdtype is None:
        raise RuntimeError('No Godot equivalent for Python type `%s`' % pytype)
    return gdtype


def convert_arg(gdtype, argname, arg, to_variant=False):
    gdtype_to_pytype = {
        # lib.GODOT_VARIANT_TYPE_NIL: type(None),
        lib.GODOT_VARIANT_TYPE_BOOL: bool,
        lib.GODOT_VARIANT_TYPE_INT: int,
        # lib.GODOT_VARIANT_TYPE_REAL: (int, float),
        lib.GODOT_VARIANT_TYPE_STRING: str,
        lib.GODOT_VARIANT_TYPE_VECTOR2: Vector2,
        lib.GODOT_VARIANT_TYPE_RECT2: Rect2,
        lib.GODOT_VARIANT_TYPE_VECTOR3: Vector3,
        lib.GODOT_VARIANT_TYPE_TRANSFORM2D: Transform2D,
        lib.GODOT_VARIANT_TYPE_PLANE: Plane,
        lib.GODOT_VARIANT_TYPE_QUAT: Quat,
        lib.GODOT_VARIANT_TYPE_AABB: AABB,
        lib.GODOT_VARIANT_TYPE_BASIS: Basis,
        lib.GODOT_VARIANT_TYPE_TRANSFORM: Transform,
        lib.GODOT_VARIANT_TYPE_COLOR: Color,
        # lib.GODOT_VARIANT_TYPE_NODE_PATH: NodePath,
        lib.GODOT_VARIANT_TYPE_RID: RID,
        lib.GODOT_VARIANT_TYPE_OBJECT: BaseObject,
        lib.GODOT_VARIANT_TYPE_DICTIONARY: Dictionary,
        lib.GODOT_VARIANT_TYPE_ARRAY: Array,
        lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY: PoolByteArray,
        lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY: PoolIntArray,
        lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY: PoolRealArray,
        lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY: PoolStringArray,
        lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY: PoolVector2Array,
        lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY: PoolVector3Array,
        lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY: PoolColorArray
    }
    if gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        try:
            arg = float(arg)
        except ValueError:
            raise TypeError('`%s` must be of type float or int' % argname)
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        if not isinstance(arg, NodePath):
            if isinstance(arg, str):
                return str_to_gd_node_path(arg, to_variant=to_variant)
            else:
                raise TypeError('`%s` must be of type NodePath or str' % argname)
    elif gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        # NIL type is used by Godot to represent variant...
        return pyobj_to_variant(arg)
    else:
        pytype = gdtype_to_pytype[gdtype]
        if not isinstance(arg, pytype):
            raise TypeError('`%s` must be of type %s' % (argname, pytype))
    if to_variant:
        return pyobj_to_variant(arg)
    else:
        return pyobj_to_gdobj(arg)


module = imp.new_module("godot._tools")
module.variant_to_pyobj = variant_to_pyobj
module.pyobj_to_variant = pyobj_to_variant
module.new_uninitialized_gdobj = new_uninitialized_gdobj
module.gdobj_to_pyobj = gdobj_to_pyobj
module.pyobj_to_gdobj = pyobj_to_gdobj
module.gd_to_py_type = gd_to_py_type
module.py_to_gd_type = py_to_gd_type
module.godot_string_to_pyobj = godot_string_to_pyobj
module.godot_string_from_pyobj = godot_string_from_pyobj


# Expose this for test
sys.modules["godot._tools"] = module
