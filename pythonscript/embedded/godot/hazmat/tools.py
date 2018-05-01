from pythonscriptcffi import ffi, lib

from godot.hazmat.base import BaseBuiltin, BaseObject, BaseBuiltinWithGDObjOwnership
from godot.hazmat.allocator import (
    godot_variant_alloc,
    godot_bool_alloc,
    godot_int_alloc,
    godot_real_alloc,
    godot_string_alloc,
    godot_vector2_alloc,
    godot_rect2_alloc,
    godot_vector3_alloc,
    godot_transform2d_alloc,
    godot_plane_alloc,
    godot_quat_alloc,
    godot_aabb_alloc,
    godot_basis_alloc,
    godot_transform_alloc,
    godot_color_alloc,
    godot_node_path_alloc,
    godot_rid_alloc,
    godot_object_alloc,
    godot_dictionary_alloc,
    godot_array_alloc,
    godot_pool_byte_array_alloc,
    godot_pool_int_array_alloc,
    godot_pool_real_array_alloc,
    godot_pool_string_array_alloc,
    godot_pool_vector2_array_alloc,
    godot_pool_vector3_array_alloc,
    godot_pool_color_array_alloc,
)
from godot.hazmat.recursive import godot_bindings_module


# A bit of naming:
# pyobj is a regular Python Object
# gdobj is a pointer on memory where is stored the data of a Godot object
# variant is a pointer on memory where is stored a Godot Variant
#
# Pay attention not to mix pointers and actual memory (given the latter
# doesn't exist in Python)


def godot_string_to_pyobj(p_gdstring):
    raw_str = lib.godot_string_wide_str(p_gdstring)
    return ffi.string(raw_str)


def godot_string_from_pyobj_for_ffi_return(pystr):
    """
    /!\ Don't use me unless you have good reason /!\
    Resulting godot_string object will not call godot_string_destroy
    when garbage collected. This is useful when a copy of this object is
    passed as a return value to Godot (which will be then responsible to
    actually call the destructor).
    """
    gdstr = ffi.new("godot_string*")
    lib.godot_string_new_with_wide_string(gdstr, pystr, len(pystr))
    return gdstr


def godot_string_from_pyobj(pystr):
    gdstr = godot_string_alloc(initialized=False)
    lib.godot_string_new_with_wide_string(gdstr, pystr, len(pystr))
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
        ret = godot_string_to_pyobj(ffi.addressof(raw))
        lib.godot_string_destroy(ffi.addressof(raw))
        return ret

    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR2:
        raw = lib.godot_variant_as_vector2(p_gdvar)
        return godot_bindings_module.Vector2.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        raw = lib.godot_variant_as_rect2(p_gdvar)
        return godot_bindings_module.Rect2.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        raw = lib.godot_variant_as_vector3(p_gdvar)
        return godot_bindings_module.Vector3.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        raw = lib.godot_variant_as_transform2d(p_gdvar)
        return godot_bindings_module.Transform2D.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        raw = lib.godot_variant_as_plane(p_gdvar)
        return godot_bindings_module.Plane.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        raw = lib.godot_variant_as_quat(p_gdvar)
        return godot_bindings_module.Quat.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_AABB:
        raw = lib.godot_variant_as_aabb(p_gdvar)
        return godot_bindings_module.AABB.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        raw = lib.godot_variant_as_basis(p_gdvar)
        return godot_bindings_module.Basis.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        raw = lib.godot_variant_as_transform(p_gdvar)
        return godot_bindings_module.Transform.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        raw = lib.godot_variant_as_color(p_gdvar)
        return godot_bindings_module.Color.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        p_raw = godot_node_path_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_node_path(p_gdvar)
        return godot_bindings_module.NodePath.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        raw = lib.godot_variant_as_rid(p_gdvar)
        return godot_bindings_module.RID.build_from_gdobj(raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        p_raw = lib.godot_variant_as_object(p_gdvar)
        # TODO: optimize this
        tmpobj = godot_bindings_module.Object(p_raw)
        return getattr(godot_bindings_module, tmpobj.get_class())(p_raw)

    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        p_raw = godot_dictionary_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_dictionary(p_gdvar)
        return godot_bindings_module.Dictionary.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        p_raw = godot_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_array(p_gdvar)
        return godot_bindings_module.Array.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        p_raw = godot_pool_byte_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_byte_array(p_gdvar)
        return godot_bindings_module.PoolByteArray.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        p_raw = godot_pool_int_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_int_array(p_gdvar)
        return godot_bindings_module.PoolIntArray.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        p_raw = godot_pool_real_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_real_array(p_gdvar)
        return godot_bindings_module.PoolRealArray.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        p_raw = godot_pool_string_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_string_array(p_gdvar)
        return godot_bindings_module.PoolStringArray.build_from_gdobj(p_raw, steal=True)

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        p_raw = godot_pool_vector2_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_vector2_array(p_gdvar)
        return godot_bindings_module.PoolVector2Array.build_from_gdobj(
            p_raw, steal=True
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        p_raw = godot_pool_vector3_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_vector3_array(p_gdvar)
        return godot_bindings_module.PoolVector3Array.build_from_gdobj(
            p_raw, steal=True
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        p_raw = godot_pool_color_array_alloc(initialized=False)
        p_raw[0] = lib.godot_variant_as_pool_color_array(p_gdvar)
        return godot_bindings_module.PoolColorArray.build_from_gdobj(p_raw, steal=True)

    else:
        raise TypeError(
            "Unknown Variant type `%s` (this should never happen !)" % gdtype
        )


def pyobj_to_variant(pyobj, p_gdvar=None, for_ffi_return=False):
    """
    `initialized=False` means we MUST manually init this by hand no matter what

    `for_ffi_return=True` means the returned variant won't have it destructor called
    once it is garbage collected by python.
    This is typically what we want when we pass the variant object by copy as a
    return value to Godot (which is then in charge of calling the destructor itself).
    """
    if not p_gdvar:
        if for_ffi_return:
            p_gdvar = ffi.new("godot_variant*")
        else:
            p_gdvar = godot_variant_alloc(initialized=False)
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
            gdstr = godot_string_alloc(initialized=False)
            lib.godot_string_new_with_wide_string(gdstr, pyobj, len(pyobj))
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
                lib.godot_variant_new_node_path(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_RID:
                lib.godot_variant_new_rid(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_OBJECT:
                lib.godot_variant_new_object(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_DICTIONARY:
                lib.godot_variant_new_dictionary(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_ARRAY:
                lib.godot_variant_new_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
                lib.godot_variant_new_pool_byte_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
                lib.godot_variant_new_pool_int_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
                lib.godot_variant_new_pool_real_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
                lib.godot_variant_new_pool_string_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
                lib.godot_variant_new_pool_vector2_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
                lib.godot_variant_new_pool_vector3_array(p_gdvar, pyobj._gd_ptr)
            elif pyobj.GD_TYPE == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
                lib.godot_variant_new_pool_color_array(p_gdvar, pyobj._gd_ptr)
        elif isinstance(pyobj, BaseObject):
            lib.godot_variant_new_object(p_gdvar, pyobj._gd_ptr)
        else:
            raise TypeError("Cannot convert `%s` to Godot's Variant" % pyobj)

    except BaseException:
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
        raise TypeError(
            "Unknown Variant type `%s` (this should never happen !)" % gdtype
        )


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
        return godot_bindings_module.Vector2.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_RECT2:
        return godot_bindings_module.Rect2.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_VECTOR3:
        return godot_bindings_module.Vector3.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM2D:
        return godot_bindings_module.Transform2D.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_PLANE:
        return godot_bindings_module.Plane.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_QUAT:
        return godot_bindings_module.Quat.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_AABB:
        return godot_bindings_module.AABB.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_BASIS:
        return godot_bindings_module.Basis.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_TRANSFORM:
        return godot_bindings_module.Transform.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_COLOR:
        return godot_bindings_module.Color.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        return godot_bindings_module.NodePath.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_RID:
        return godot_bindings_module.RID.build_from_gdobj(p_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_OBJECT:
        # TODO: optimize this
        tmpobj = godot_bindings_module.Object(p_gdobj[0])
        return getattr(godot_bindings_module, tmpobj.get_class())(p_gdobj[0])

    elif gdtype == lib.GODOT_VARIANT_TYPE_DICTIONARY:
        return godot_bindings_module.Dictionary.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_ARRAY:
        return godot_bindings_module.Array.build_from_gdobj(p_gdobj, steal=steal_gdobj)

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY:
        return godot_bindings_module.PoolByteArray.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY:
        return godot_bindings_module.PoolIntArray.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY:
        return godot_bindings_module.PoolRealArray.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY:
        return godot_bindings_module.PoolStringArray.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY:
        return godot_bindings_module.PoolVector2Array.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY:
        return godot_bindings_module.PoolVector3Array.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    elif gdtype == lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY:
        return godot_bindings_module.PoolColorArray.build_from_gdobj(
            p_gdobj, steal=steal_gdobj
        )

    else:
        raise TypeError(
            "Unknown Variant type `%s` (this should never happen !)" % gdtype
        )


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
        gdobj = godot_string_alloc(initialized=False)
        lib.godot_string_new_with_wide_string(gdobj, pyobj, -1)
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
        raise TypeError("Cannot convert Python object `%s` into Godot object." % pyobj)


# Must do lazy evaluation to avoid circular dependency here
GD_PY_TYPES = None


def _get_gd_py_types():
    global GD_PY_TYPES
    if not GD_PY_TYPES:
        GD_PY_TYPES = (
            (lib.GODOT_VARIANT_TYPE_NIL, type(None)),
            (lib.GODOT_VARIANT_TYPE_BOOL, bool),
            (lib.GODOT_VARIANT_TYPE_INT, int),
            (lib.GODOT_VARIANT_TYPE_REAL, float),
            (lib.GODOT_VARIANT_TYPE_STRING, str),
            (lib.GODOT_VARIANT_TYPE_VECTOR2, godot_bindings_module.Vector2),
            (lib.GODOT_VARIANT_TYPE_RECT2, godot_bindings_module.Rect2),
            (lib.GODOT_VARIANT_TYPE_VECTOR3, godot_bindings_module.Vector3),
            (lib.GODOT_VARIANT_TYPE_TRANSFORM2D, godot_bindings_module.Transform2D),
            (lib.GODOT_VARIANT_TYPE_PLANE, godot_bindings_module.Plane),
            (lib.GODOT_VARIANT_TYPE_QUAT, godot_bindings_module.Quat),
            (lib.GODOT_VARIANT_TYPE_AABB, godot_bindings_module.AABB),
            (lib.GODOT_VARIANT_TYPE_BASIS, godot_bindings_module.Basis),
            (lib.GODOT_VARIANT_TYPE_TRANSFORM, godot_bindings_module.Transform),
            (lib.GODOT_VARIANT_TYPE_COLOR, godot_bindings_module.Color),
            (lib.GODOT_VARIANT_TYPE_NODE_PATH, godot_bindings_module.NodePath),
            (lib.GODOT_VARIANT_TYPE_RID, godot_bindings_module.RID),
            # (lib.GODOT_VARIANT_TYPE_OBJECT, BaseObject),  # TODO: recursive import error godot_bindings_module.?
            (lib.GODOT_VARIANT_TYPE_DICTIONARY, godot_bindings_module.Dictionary),
            (lib.GODOT_VARIANT_TYPE_ARRAY, godot_bindings_module.Array),
            (
                lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY,
                godot_bindings_module.PoolByteArray,
            ),
            (lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY, godot_bindings_module.PoolIntArray),
            (
                lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY,
                godot_bindings_module.PoolRealArray,
            ),
            (
                lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY,
                godot_bindings_module.PoolStringArray,
            ),
            (
                lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY,
                godot_bindings_module.PoolVector2Array,
            ),
            (
                lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY,
                godot_bindings_module.PoolVector3Array,
            ),
            (
                lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY,
                godot_bindings_module.PoolColorArray,
            ),
        )
    return GD_PY_TYPES


def gd_to_py_type(gdtype):
    pytype = next((py for gd, py in _get_gd_py_types() if gd == gdtype), None)
    if pytype is None:
        raise RuntimeError("No Python equivalent for Godot type `%s`" % gdtype)

    return pytype


def py_to_gd_type(pytype):
    gdtype = next((gd for gd, py in _get_gd_py_types() if py == pytype), None)
    if gdtype is None:
        raise RuntimeError("No Godot equivalent for Python type `%s`" % pytype)

    return gdtype


def convert_arg(gdtype, argname, arg, to_variant=False):
    gdtype_to_pytype = {
        # lib.GODOT_VARIANT_TYPE_NIL: type(None),
        lib.GODOT_VARIANT_TYPE_BOOL: bool,
        lib.GODOT_VARIANT_TYPE_INT: int,
        # lib.GODOT_VARIANT_TYPE_REAL: (int, float),
        lib.GODOT_VARIANT_TYPE_STRING: str,
        lib.GODOT_VARIANT_TYPE_VECTOR2: godot_bindings_module.Vector2,
        lib.GODOT_VARIANT_TYPE_RECT2: godot_bindings_module.Rect2,
        lib.GODOT_VARIANT_TYPE_VECTOR3: godot_bindings_module.Vector3,
        lib.GODOT_VARIANT_TYPE_TRANSFORM2D: godot_bindings_module.Transform2D,
        lib.GODOT_VARIANT_TYPE_PLANE: godot_bindings_module.Plane,
        lib.GODOT_VARIANT_TYPE_QUAT: godot_bindings_module.Quat,
        lib.GODOT_VARIANT_TYPE_AABB: godot_bindings_module.AABB,
        lib.GODOT_VARIANT_TYPE_BASIS: godot_bindings_module.Basis,
        lib.GODOT_VARIANT_TYPE_TRANSFORM: godot_bindings_module.Transform,
        lib.GODOT_VARIANT_TYPE_COLOR: godot_bindings_module.Color,
        # lib.GODOT_VARIANT_TYPE_NODE_PATH: godot_bindings_module.NodePath,
        lib.GODOT_VARIANT_TYPE_RID: godot_bindings_module.RID,
        lib.GODOT_VARIANT_TYPE_OBJECT: BaseObject,
        lib.GODOT_VARIANT_TYPE_DICTIONARY: godot_bindings_module.Dictionary,
        lib.GODOT_VARIANT_TYPE_ARRAY: godot_bindings_module.Array,
        lib.GODOT_VARIANT_TYPE_POOL_BYTE_ARRAY: godot_bindings_module.PoolByteArray,
        lib.GODOT_VARIANT_TYPE_POOL_INT_ARRAY: godot_bindings_module.PoolIntArray,
        lib.GODOT_VARIANT_TYPE_POOL_REAL_ARRAY: godot_bindings_module.PoolRealArray,
        lib.GODOT_VARIANT_TYPE_POOL_STRING_ARRAY: godot_bindings_module.PoolStringArray,
        lib.GODOT_VARIANT_TYPE_POOL_VECTOR2_ARRAY: godot_bindings_module.PoolVector2Array,
        lib.GODOT_VARIANT_TYPE_POOL_VECTOR3_ARRAY: godot_bindings_module.PoolVector3Array,
        lib.GODOT_VARIANT_TYPE_POOL_COLOR_ARRAY: godot_bindings_module.PoolColorArray,
    }
    if gdtype == lib.GODOT_VARIANT_TYPE_REAL:
        try:
            arg = float(arg)
        except ValueError:
            raise TypeError("`%s` must be of type float or int" % argname)

    elif gdtype == lib.GODOT_VARIANT_TYPE_NODE_PATH:
        from godot.node_path import NodePath, str_to_gd_node_path

        if not isinstance(arg, NodePath):
            if isinstance(arg, str):
                return str_to_gd_node_path(arg, to_variant=to_variant)

            else:
                raise TypeError("`%s` must be of type NodePath or str" % argname)

    elif gdtype == lib.GODOT_VARIANT_TYPE_NIL:
        # NIL type is used by Godot to represent variant...
        return pyobj_to_variant(arg)

    else:
        pytype = gdtype_to_pytype[gdtype]
        if not isinstance(arg, pytype):
            raise TypeError("`%s` must be of type %s" % (argname, pytype))

    if to_variant:
        return pyobj_to_variant(arg)

    else:
        return pyobj_to_gdobj(arg)


__all__ = (
    "variant_to_pyobj",
    "pyobj_to_variant",
    "new_uninitialized_gdobj",
    "gdobj_to_pyobj",
    "pyobj_to_gdobj",
    "gd_to_py_type",
    "py_to_gd_type",
    "godot_string_to_pyobj",
    "godot_string_from_pyobj",
)
