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


def godot_array_to_pyobj(p_gdarray):
    ret = []
    for i in range(lib.godot_array_size(p_gdarray)):
        raw = lib.godot_array_get(p_gdarray, i)
        ret.append(variant_to_pyobj(ffi.addressof(raw)))
    return ret


def godot_dictionary_to_pyobj(p_gddict):
    pydict = {}
    gdkeys = lib.godot_dictionary_keys(p_gddict)
    p_gdkeys = ffi.addressof(gdkeys)
    for i in range(lib.godot_array_size(p_gdkeys)):
        raw_key = lib.godot_array_get(p_gdkeys, i)
        var_key = lib.godot_variant_as_string(ffi.addressof(raw_key))
        key = godot_string_to_pyobj(ffi.addressof(var_key))
        raw_value = lib.godot_dictionary_get(p_gddict, ffi.addressof(raw_key))
        # Recursive conversion of dict values
        pydict[key] = variant_to_pyobj(ffi.addressof(raw_value))
    return pydict


def godot_string_to_pyobj(p_gdstring):
    raw_str = lib.godot_string_unicode_str(p_gdstring)
    return ffi.string(raw_str)


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
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        raw = lib.godot_variant_as_rect3(p_gdvar)
        return Rect3.build_from_gdobj(raw)
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


variant_new = ffi.new_allocator(alloc=lib.malloc, free=lib.godot_variant_destroy, should_clear_after_alloc=False)
def pyobj_to_variant(pyobj, p_gdvar=None):
    p_gdvar = p_gdvar if p_gdvar else variant_new('godot_variant*')
    # p_gdvar = p_gdvar if p_gdvar else ffi.new('godot_variant*')
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
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RECT3:
            lib.godot_variant_new_rect3(p_gdvar, pyobj._gd_ptr)
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
        # Must init the variant anyway to avoid segfault in it destructor
        lib.godot_variant_new_nil(p_gdvar)
        raise TypeError("Cannot convert `%s` to Godot's Variant" % pyobj)
    return p_gdvar


def new_uninitialized_gdobj(gdtype):
    # TODO: use dict to optimize this ?
    # It seems Godot encode Variant as type nil...
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        return ffi.new('godot_variant*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_BOOL:
        return ffi.new('godot_bool*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_INT:
        return ffi.new('godot_int*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        return ffi.new('godot_real*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_STRING:
        return ffi.new('godot_string*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        return ffi.new('godot_vector2*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        return ffi.new('godot_rect2*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        return ffi.new('godot_vector3*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        return ffi.new('godot_transform2d*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        return ffi.new('godot_plane*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        return ffi.new('godot_quat*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        return ffi.new('godot_rect3*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        return ffi.new('godot_basis*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        return ffi.new('godot_transform*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        return ffi.new('godot_color*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        return ffi.new('godot_node_path*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        return ffi.new('godot_rid*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        # TODO use malloc to prevent garbage collection on object
        return ffi.new('godot_object**')
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        return ffi.new('godot_dictionary*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        return ffi.new('godot_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        return ffi.new('godot_pool_byte_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        return ffi.new('godot_pool_int_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        return ffi.new('godot_pool_real_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        return ffi.new('godot_pool_string_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        return ffi.new('godot_pool_vector2_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        return ffi.new('godot_pool_vector3_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        return ffi.new('godot_pool_color_array*')
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
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        return Rect3.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        return Basis.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        return Transform.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        return Color.build_from_gdobj(p_gdobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        return Node_path.build_from_gdobj(p_gdobj, steal=steal_gdobj)
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
        return ffi.new("godot_bool*", 1 if pyobj else 0)
    elif isinstance(pyobj, int):
        return ffi.new("godot_int*", pyobj)
    elif isinstance(pyobj, float):
        return ffi.new("godot_real*", pyobj)
    elif isinstance(pyobj, str):
        gdobj = ffi.new("godot_string*")
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
    (lib.GODOT_VARIANT_TYPE_RECT3, Rect3),
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
        lib.GODOT_VARIANT_TYPE_RECT3: Rect3,
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
module.godot_array_to_pyobj = godot_array_to_pyobj
module.godot_dictionary_to_pyobj = godot_dictionary_to_pyobj
module.godot_string_to_pyobj = godot_string_to_pyobj


# Expose this for test
sys.modules["godot._tools"] = module
