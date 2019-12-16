# import pytest

# from godot import Array, Dictionary
# from godot.hazmat.tools import (
#     variant_to_pyobj,
#     pyobj_to_variant,
#     gdobj_to_pyobj,
#     pyobj_to_gdobj,
#     gd_to_py_type,
#     py_to_gd_type,
#     godot_string_to_pyobj,
# )
# from pythonscriptcffi import lib

# # @pytest.mark.parametrize('arg', [
# #     None,
# #     0,
# #     42,
# #     0.0,
# #     42.5,
# #     '',
# #     'test',
# #     Dictionary(),
# #     Dictionary({'foo': 1, 2: 'bar'}),
# #     Array(),
# #     Array(['foo', 2]),
# # ])
# # def test_pyobj_variant_conversion(arg):
# #     variant = pyobj_to_variant(arg)
# #     ret_arg = variant_to_pyobj(variant)
# #     assert ret_arg == arg


# # @pytest.mark.parametrize('arg', [
# #     None,
# #     0,
# #     42,
# #     0.0,
# #     42.5,
# #     '',
# #     'test',
# #     Dictionary(),
# #     Dictionary({'foo': 1, 2: 'bar'}),
# #     Array(),
# #     Array(['foo', 2]),
# # ])
# # def test_pyobj_raw_conversion(arg):
# #     variant = pyobj_to_gdobj(arg)
# #     ret_arg = gdobj_to_pyobj(variant, )
# #     assert ret_arg == arg


# @pytest.mark.parametrize("arg", ["", "foo", "l" + "o" * 25000 + "ong"])
# def test_godot_string_to_pyobj(arg):
#     gdstr = pyobj_to_gdobj(arg)
#     ret_arg = godot_string_to_pyobj(gdstr)
#     assert ret_arg == arg


# @pytest.mark.parametrize(
#     "args",
#     [
#         (lib.GODOT_VARIANT_TYPE_NIL, type(None)),
#         (lib.GODOT_VARIANT_TYPE_REAL, float),
#         (lib.GODOT_VARIANT_TYPE_STRING, str),
#         (lib.GODOT_VARIANT_TYPE_DICTIONARY, Dictionary),
#     ],
# )
# def test_gd_py_type_translation(args):
#     gdtype, pytype = args

#     rettype = gd_to_py_type(gdtype)
#     assert rettype == pytype

#     rettype = py_to_gd_type(pytype)
#     assert rettype == gdtype


# # @pytest.mark.parametrize('args', [
# #     (None, lib.GODOT_VARIANT_TYPE_NIL),
# #     (0, lib.GODOT_VARIANT_TYPE_INT),
# #     (42, lib.GODOT_VARIANT_TYPE_INT),
# #     (0.0, lib.GODOT_VARIANT_TYPE_REAL),
# #     (42.5, lib.GODOT_VARIANT_TYPE_REAL),
# #     ('', lib.GODOT_VARIANT_TYPE_STRING),
# #     ('test', lib.GODOT_VARIANT_TYPE_STRING),
# #     (Dictionary(), lib.GODOT_VARIANT_TYPE_DICTIONARY),
# #     (Dictionary({'foo': 1, 2: 'bar'}), lib.GODOT_VARIANT_TYPE_DICTIONARY),
# #     (Array(), lib.GODOT_VARIANT_TYPE_ARRAY),
# #     (Array(['foo', 2]), lib.GODOT_VARIANT_TYPE_ARRAY),
# # ])
# # def test_new_raw_initialized(args):
# #     pyobj, gdtype = args
# #     new_raw()
# #     raw = pyobj_to_gdobj(pyobj)
# #     ret_pyobj = gdobj_to_pyobj(gdtype, raw)
# #     assert ret_pyobj == pyobj


# @pytest.mark.parametrize(
#     "args",
#     [
#         (None, lib.GODOT_VARIANT_TYPE_NIL),
#         (0, lib.GODOT_VARIANT_TYPE_INT),
#         (42, lib.GODOT_VARIANT_TYPE_INT),
#         (0.0, lib.GODOT_VARIANT_TYPE_REAL),
#         (42.5, lib.GODOT_VARIANT_TYPE_REAL),
#         ("", lib.GODOT_VARIANT_TYPE_STRING),
#         ("test", lib.GODOT_VARIANT_TYPE_STRING),
#         (Dictionary(), lib.GODOT_VARIANT_TYPE_DICTIONARY),
#         (Dictionary({"foo": 1, 2: "bar"}), lib.GODOT_VARIANT_TYPE_DICTIONARY),
#         (Array(), lib.GODOT_VARIANT_TYPE_ARRAY),
#         (Array(["foo", 2]), lib.GODOT_VARIANT_TYPE_ARRAY),
#     ],
# )
# def test_pyobj_raw_conversion(args):
#     pyobj, gdtype = args
#     raw = pyobj_to_gdobj(pyobj)
#     ret_pyobj = gdobj_to_pyobj(gdtype, raw)
#     assert ret_pyobj == pyobj
