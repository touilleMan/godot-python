from clodotest import assert_eq
import godot


def test_global_enum():
    assert_eq(godot.Error.OK.value, 0)
    assert_eq(godot.Error.FAILED.value, 1)

    # We expect the enum values not to leak outside of their enum type
    assert not hasattr(godot, "OK")

    # Special case for KEY_[A-Z0-9]
    assert_eq(godot.Key.K_Z.value, 90)
    assert_eq(godot.Key.K_0.value, 48)

    # Ensure the special case doesn't leak on similar types
    assert_eq(godot.JoyButton.A.value, 0)
    assert not hasattr(godot.JoyButton, "K_A")

    # Special case for METHOD_FLAG_xxx vs METHOD_FLAGS_DEFAULT
    assert_eq(godot.MethodFlags.NORMAL.value, 1)
    assert_eq(godot.MethodFlags.EDITOR.value, 2)
    assert_eq(godot.MethodFlags.FLAGS_DEFAULT.value, 1)

    # Since `Variant` is not defined in `extension_api.json`, it's enums
    # are defined among the global ones...
    assert godot.VariantType.NIL.value == 0
    assert godot.VariantOperator.ADD.value == 6

    # Max special value is omitted since it is not an actual valid value
    assert not hasattr(godot.PropertyHint, "MAX")
    assert not hasattr(godot.VariantOperator, "MAX")


def test_global_constant():
    # Nothing to do: `extension_api.json`'s `global_constants` entry is empty so far...
    pass
