from pythonscriptcffi import ffi, lib


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
        raw_value = lib.godot_dictionary_operator_index(p_gddict, ffi.addressof(raw_key))
        # Recursive conversion of dict values
        pydict[key] = variant_to_pyobj(ffi.addressof(raw_value))
    return pydict


def godot_string_to_pyobj(p_gdstring):
    raw_str = lib.godot_string_unicode_str(p_gdstring)
    return ffi.string(raw_str)


def variant_to_pyobj(p_gdvar, hint_string=None):
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
        return Transform2d.build_from_gdobj(raw)
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
        return Rid.build_from_gdobj(raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        p_raw = lib.godot_variant_as_object(p_gdvar)
        # TODO gdnative should have a way to get object type
        hint_string = hint_string or 'Object'
        return getattr(godot_bindings_module, hint_string)(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        raw = lib.godot_variant_as_dictionary(p_gdvar)
        return godot_dictionary_to_pyobj(ffi.addressof(raw))
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        raw = lib.godot_variant_as_array(p_gdvar)
        return godot_array_to_pyobj(ffi.addressof(raw))
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


def new_raw(gdtype):
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        return ffi.NULL
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
        raise TypeError("Type conversion `Rect2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        raise TypeError("Type conversion `Vector3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        raise TypeError("Type conversion `Transform2d` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        raise TypeError("Type conversion `Plane` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        raise TypeError("Type conversion `Quat` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        raise TypeError("Type conversion `Rect3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        raise TypeError("Type conversion `Basis` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        raise TypeError("Type conversion `Transform` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        raise TypeError("Type conversion `Color` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Type conversion `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Type conversion `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        # TODO use malloc to prevent garbage collection on object
        return ffi.new('godot_object**')
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        p_raw = ffi.new('godot_dictionary*')
        lib.godot_dictionary_new(p_raw)
        return p_raw
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        p_raw = ffi.new('godot_array*')
        lib.godot_array_new(p_raw)
        return p_raw
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        raise TypeError("Variant type `PoolByteArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        raise TypeError("Variant type `PoolIntArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        raise TypeError("Variant type `PoolRealArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        return ffi.new('godot_pool_string_array*')
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        raise TypeError("Variant type `PoolVector2Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        raise TypeError("Variant type `PoolVector3Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        raise TypeError("Variant type `PoolColorArray` not implemented yet")
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)


def raw_to_pyobj(gdtype, p_raw, hint_string=None):
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        return None
    elif gdtype == lib.GODOT_VARIANT_TYPE_BOOL:
        return bool(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_INT:
        return int(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        return float(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_STRING:
        return godot_string_to_pyobj(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        return Vector2.build_from_gdobj(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        raise TypeError("Type conversion `Rect2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        raise TypeError("Type conversion `Vector3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        raise TypeError("Type conversion `Transform2d` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        raise TypeError("Type conversion `Plane` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        raise TypeError("Type conversion `Quat` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        raise TypeError("Type conversion `Rect3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        raise TypeError("Type conversion `Basis` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        raise TypeError("Type conversion `Transform` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        raise TypeError("Type conversion `Color` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Type conversion `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Type conversion `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        return getattr(godot_bindings_module, hint_string)(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        return godot_dictionary_to_pyobj(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        return godot_array_to_pyobj(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        raise TypeError("Variant type `PoolByteArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        raise TypeError("Variant type `PoolIntArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        raise TypeError("Variant type `PoolRealArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        ret = []
        for i in range(lib.godot_pool_string_array_size(p_raw)):
            p_raw_value = ffi.new('godot_string*')
            raw_value = lib.godot_pool_string_array_get(p_raw, i)
            ret.append(godot_string_to_pyobj(ffi.addressof(raw_value)))
        return ret
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        raise TypeError("Variant type `PoolVector2Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        raise TypeError("Variant type `PoolVector3Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        raise TypeError("Variant type `PoolColorArray` not implemented yet")
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)


def pyobj_to_variant(pyobj, gdvar=None):
    gdvar = gdvar if gdvar else ffi.new('godot_variant*')
    if pyobj is None:
        lib.godot_variant_new_nil(gdvar)
    elif (isinstance(pyobj, bool)):
        lib.godot_variant_new_bool(gdvar, pyobj)
    elif (isinstance(pyobj, int)):
        lib.godot_variant_new_int(gdvar, pyobj)
    elif (isinstance(pyobj, float)):
        lib.godot_variant_new_real(gdvar, pyobj)
    elif (isinstance(pyobj, str)):
        gdstr = ffi.new("godot_string*")
        pyobj_as_bytes = pyobj.encode()
        lib.godot_string_new_data(gdstr, pyobj_as_bytes, len(pyobj_as_bytes))
        lib.godot_variant_new_string(gdvar, gdstr)
    elif (isinstance(pyobj, bytes)):
        gdstr = ffi.new("godot_string*")
        lib.godot_string_new_data(gdstr, pyobj, len(pyobj))
        lib.godot_variant_new_string(gdvar, gdstr)
    elif isinstance(pyobj, BaseBuiltin):
        if pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_VECTOR2:
            lib.godot_variant_new_vector2(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RECT2:
            lib.godot_variant_new_rect2(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_VECTOR3:
            lib.godot_variant_new_vector3(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
            lib.godot_variant_new_transform2d(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_PLANE:
            lib.godot_variant_new_plane(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_QUAT:
            lib.godot_variant_new_quat(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RECT3:
            lib.godot_variant_new_rect3(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_BASIS:
            lib.godot_variant_new_basis(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_TRANSFORM:
            lib.godot_variant_new_transform(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_COLOR:
            lib.godot_variant_new_color(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_NODEPATH:
            lib.godot_variant_new_nodepath(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RID:
            lib.godot_variant_new_rid(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_OBJECT:
            lib.godot_variant_new_object(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_DICTIONARY:
            lib.godot_variant_new_dictionary(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_ARRAY:
            lib.godot_variant_new_array(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLBYTEARRAY:
            lib.godot_variant_new_poolbytearray(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLINTARRAY:
            lib.godot_variant_new_poolintarray(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLREALARRAY:
            lib.godot_variant_new_poolrealarray(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLSTRINGARRAY:
            lib.godot_variant_new_poolstringarray(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLVECTOR2ARRAY:
            lib.godot_variant_new_poolvector2array(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLVECTOR3ARRAY:
            lib.godot_variant_new_poolvector3array(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOLCOLORARRAY:
            lib.godot_variant_new_poolcolorarray(gdvar, pyobj._gd_ptr)
    elif isinstance(pyobj, BaseObject):
        lib.godot_variant_new_object(gdvar, pyobj._gd_ptr)
    else:
        raise TypeError("Cannot convert `%s` to Godot's Variant" % pyobj)
    return gdvar


def pyobj_to_raw(pyobj):
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
    if isinstance(pyobj, (BaseObject, BaseBuiltin)):
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
    (lib.GODOT_VARIANT_TYPE_TRANSFORM2D, Transform2d),
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
