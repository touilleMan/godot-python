from godot import GDString, GDArray, PackedByteArray
from godot.classes import WeakRef
import clodotest
from clodotest import assert_eq, assert_isinstance


@clodotest.parametrize(
    "kind",
    [
        "scalar_in_out",
        "none_in_object_out",
        "none_out",
        "variant_in_builtin_out",
        "builtin_in_variant_out",
        "default_param",
        "str_param_conversion",
        "bad_type_scalar",
        "bad_type_variant",
        "vararg_in_variant_out",
        "vararg_in_builtin_out",
        "vararg_in_none_out",
    ],
)
def test_call(kind: str):
    from godot import utils

    match kind:
        case "scalar_in_out":
            assert_eq(utils.cos(0), 1)
        case "none_in_object_out":
            obj = utils.weakref(None)
            try:
                assert_isinstance(obj, WeakRef)
                assert_eq(obj.get_ref(), None)
            finally:
                obj.free()
        case "none_out":
            assert_eq(utils.seed(42), None)
        case "variant_in_builtin_out":
            x = GDString("hello")
            ret = utils.var_to_bytes(x)
            assert_isinstance(ret, PackedByteArray)
            assert_eq(utils.bytes_to_var(ret), x)
        case "builtin_in_variant_out":
            assert_eq(utils.str_to_var(GDString("[1, 2]")), GDArray([1, 2]))
        case "default_param":
            # Nothing to do: currently there is not Godot utility function with default parameter value.
            pass
        case "str_param_conversion":
            assert_eq(utils.str_to_var("[1, 2]"), GDArray([1, 2]))
        case "bad_type_scalar":
            with clodotest.raises(TypeError):
                utils.cos(None)
        case "bad_type_variant":
            with clodotest.raises(TypeError):
                utils.str(object())
        case "vararg_in_variant_out":
            assert_eq(utils.max(0, 1.1), 1.1)
        case "vararg_in_builtin_out":
            assert_eq(utils.str(GDArray([1, 2])), GDString("[1, 2]"))
            assert_eq(utils.str(GDArray([1, 2]), 42), GDString("[1, 2]42"))
            # Also try with > 8 parameters (since we implement it as a special case)
            assert_eq(utils.str(0, 1, 2, 3, 4, 5, 6, 7, 8, 9), GDString("0123456789"))
        case "vararg_in_none_out":
            assert_eq(utils.print(GDArray(["hello", "world"])), None)
        case unknown:
            assert False, unknown
