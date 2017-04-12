from pythonscriptcffi import ffi, lib


def godot_array_to_pyobj(p_gdarray):
    return [variant_to_pyobj(lib.godot_array_get(p_gdarray, i))
            for i in range(lib.godot_array_size(p_gdarray))]


def godot_dictionary_to_pyobj(p_gddict):
    pydict = {}
    gdkeys = lib.godot_dictionary_keys(p_gddict)
    p_gdkeys = ffi.new("godot_array*", gdkeys)
    for i in range(lib.godot_array_size(p_gdkeys)):
        p_key = lib.godot_array_get(p_gdkeys, i)
        keystr = lib.godot_variant_as_string(p_key)
        p_keystr = ffi.new("godot_string*", keystr)
        c_str = lib.godot_string_c_str(p_keystr)
        value = lib.godot_dictionary_operator_index(p_gddict, p_key)
        # Recursive conversion of dict values
        pydict[ffi.string(c_str)] = variant_to_pyobj(value)
    return pydict


def godot_string_to_pyobj(gdstring):
    p_gdstring = ffi.new("godot_string*", gdstring)
    c_str = lib.godot_string_c_str(p_gdstring)
    return ffi.string(c_str)


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
        return godot_string_to_pyobj(lib.godot_variant_as_string(p_gdvar))
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        raise TypeError("Variant type `Vector2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        raise TypeError("Variant type `Rect2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        raise TypeError("Variant type `Vector3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        raise TypeError("Variant type `Transform2d` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        raise TypeError("Variant type `Plane` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        raise TypeError("Variant type `Quat` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        raise TypeError("Variant type `Rect3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        raise TypeError("Variant type `Basis` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        raise TypeError("Variant type `Transform` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        raise TypeError("Variant type `Color` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_IMAGE:
        raise TypeError("Variant type `Image` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Variant type `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Variant type `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        raise TypeError("Variant type `Object` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_INPUT_EVENT:
        raise TypeError("Variant type `InputEvent` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        gddict = lib.godot_variant_as_dictionary(p_gdvar)
        return godot_dictionary_to_pyobj(ffi.addressof(gddict))
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        gdarray = lib.godot_variant_as_array(p_gdvar)
        return godot_array_to_pyobj(ffi.addressof(gdarray))
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        raise TypeError("Variant type `PoolByteArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        raise TypeError("Variant type `PoolIntArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        raise TypeError("Variant type `PoolRealArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        raise TypeError("Variant type `PoolStringArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        raise TypeError("Variant type `PoolVector2Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        raise TypeError("Variant type `PoolVector3Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        raise TypeError("Variant type `PoolColorArray` not implemented yet")
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
        raise TypeError("Type conversion `Vector2` not implemented yet")
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
    elif gdtype == lib.GODOT_VARIANT_TYPE_IMAGE:
        raise TypeError("Type conversion `Image` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Type conversion `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Type conversion `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        return ffi.new('godot_object**')
    elif gdtype == lib.GODOT_VARIANT_TYPE_INPUT_EVENT:
        raise TypeError("Type conversion `InputEvent` not implemented yet")
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
        return godot_string_to_pyobj(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        raise TypeError("Type conversion `Vector2` not implemented yet")
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
    elif gdtype == lib.GODOT_VARIANT_TYPE_IMAGE:
        raise TypeError("Type conversion `Image` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Type conversion `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Type conversion `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        return getattr(godot_bindings_module, hint_string)(p_raw[0])
    elif gdtype == lib.GODOT_VARIANT_TYPE_INPUT_EVENT:
        raise TypeError("Type conversion `InputEvent` not implemented yet")
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
            ret.append(godot_string_to_pyobj(lib.godot_pool_string_array_get(p_raw, i)))
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
        return
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
    elif hasattr(pyobj, "_gd_obj"):
        lib.godot_variant_new_object(gdvar, pyobj._gd_obj)
    else:
        raise TypeError("Cannot convert `%s` to Godot's Variant" % pyobj)
    return gdvar


def pyobj_to_raw(gdtype, pyobj):
    if gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        if pyobj is not None:
            raise TypeError("`%s` should be of type None" % pyobj)
        return ffi.NULL
    elif gdtype == lib.GODOT_VARIANT_TYPE_BOOL:
        if not isinstance(pyobj, bool):
            raise TypeError("`%s` should be of type bool" % pyobj)
        return ffi.new("godot_bool*", 1 if pyobj else 0)
    elif gdtype == lib.GODOT_VARIANT_TYPE_INT:
        if not isinstance(pyobj, int):
            raise TypeError("`%s` should be of type int" % pyobj)
        return ffi.new("godot_int*", pyobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        if not isinstance(pyobj, float):
            raise TypeError("`%s` should be of type float" % pyobj)
        return ffi.new("godot_real*", pyobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_STRING:
        if not isinstance(pyobj, str):
            raise TypeError("`%s` should be of type str" % pyobj)
        return ffi.new("wchar_t*", pyobj)
        # return ffi.new("char*", pyobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        raise TypeError("Variant type `Vector2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        raise TypeError("Variant type `Rect2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        raise TypeError("Variant type `Vector3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        raise TypeError("Variant type `Transform2d` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        raise TypeError("Variant type `Plane` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        raise TypeError("Variant type `Quat` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT3:
        raise TypeError("Variant type `Rect3` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        raise TypeError("Variant type `Basis` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        raise TypeError("Variant type `Transform` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        raise TypeError("Variant type `Color` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_IMAGE:
        raise TypeError("Variant type `Image` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Variant type `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Variant type `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        raise TypeError("Variant type `Object` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_INPUT_EVENT:
        raise TypeError("Variant type `InputEvent` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        if not isinstance(pyobj, dict):
            raise TypeError("`%s` should be of type dict" % pyobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        if not isinstance(pyobj, list):
            raise TypeError("`%s` should be of type list" % pyobj)
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        raise TypeError("Variant type `PoolByteArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        raise TypeError("Variant type `PoolIntArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        raise TypeError("Variant type `PoolRealArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        raise TypeError("Variant type `PoolStringArray` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        raise TypeError("Variant type `PoolVector2Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        raise TypeError("Variant type `PoolVector3Array` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        raise TypeError("Variant type `PoolColorArray` not implemented yet")
    else:
        raise TypeError("Unknown Variant type `%s` (this should never happen !)" % gdtype)
