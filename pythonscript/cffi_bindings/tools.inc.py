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
        p_raw = ffi.new('godot_vector2*')
        lib.godot_variant_as_vector2(p_gdvar, p_raw)
        return Vector2.build_from_gd_obj(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        raise TypeError("Variant type `Rect2` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        p_raw = ffi.new('godot_vector3*')
        lib.godot_variant_as_vector3(p_gdvar, p_raw)
        return Vector3.build_from_gd_obj(p_raw)
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
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Variant type `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Variant type `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        p_raw = lib.godot_variant_as_object(p_gdvar)
        return getattr(bindings, hint_string)(p_raw)
    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        p_raw = ffi.new('godot_dictionary*')
        raw = lib.godot_variant_as_dictionary(p_gdvar)
        return godot_dictionary_to_pyobj(ffi.addressof(raw))
    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        raw = lib.godot_variant_as_array(p_gdvar)
        return godot_array_to_pyobj(ffi.addressof(raw))
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
        return Vector2.build_from_gd_ptr(p_raw)
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
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_IMAGE:
            lib.godot_variant_new_image(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_NODEPATH:
            lib.godot_variant_new_nodepath(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RID:
            lib.godot_variant_new_rid(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_OBJECT:
            lib.godot_variant_new_object(gdvar, pyobj._gd_ptr)
        elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_INPUTEVENT:
            lib.godot_variant_new_inputevent(gdvar, pyobj._gd_ptr)
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
        gdobj = ffi.new("godot_string*")
        lib.godot_string_new_unicode_data(gdobj, pyobj, -1)
        return gdobj
    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        return pyobj._gd_ptr
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
    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        raise TypeError("Variant type `NodePath` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raise TypeError("Variant type `Rid` not implemented yet")
    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        raise TypeError("Variant type `Object` not implemented yet")
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


GD_PY_TYPES = (
    (lib.GODOT_VARIANT_TYPE_NIL, type(None)),
    (lib.GODOT_VARIANT_TYPE_BOOL, bool),
    (lib.GODOT_VARIANT_TYPE_INT, int),
    (lib.GODOT_VARIANT_TYPE_REAL, float),
    (lib.GODOT_VARIANT_TYPE_STRING, str),
    (lib.GODOT_VARIANT_TYPE_VECTOR2, Vector2),
    (lib.GODOT_VARIANT_TYPE_RECT2, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_VECTOR3, Vector3),
    (lib.GODOT_VARIANT_TYPE_TRANSFORM2D, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_PLANE, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_QUAT, Quat),
    (lib.GODOT_VARIANT_TYPE_RECT3, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_BASIS, Basis),
    (lib.GODOT_VARIANT_TYPE_TRANSFORM, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_COLOR, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_NODE_PATH, NodePath),
    (lib.GODOT_VARIANT_TYPE_RID, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_OBJECT, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_DICTIONARY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY, type(None)),  # TODO
    (lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY, type(None)),  # TODO
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
