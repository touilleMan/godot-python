from clodotest import assert_eq
import godot


def test_global_enum():
    assert_eq(godot.Error.OK, 0)
    assert_eq(godot.Error.FAILED, 1)
    assert_eq(godot.Key.KEY_Z, 90)
    # We expect the enum values not to leak outside of their enum type
    assert not hasattr(godot, "OK")

    # Since `Variant` is not defined in `extension_api.json`, it's enums
    # are defined among the global ones...
    assert godot.VariantType.TYPE_NIL == 0
    assert godot.VariantOperator.OP_ADD == 6


def test_global_constant():
    # Nothing to do: `extension_api.json`'s `global_constants` entry is empty so far...
    pass
