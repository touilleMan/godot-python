import clodotest
import godot


@clodotest.xfail(reason="TODO: Godot enum from Python is still WIP")
def test_global_enum():
    assert godot.Error.OK == 0
    assert godot.Error.FAILED == 1

    # Since `Variant` is not defined in `extension_api.json`, it's enums
    # are defined among the global ones...
    assert godot.Variant.Type.NIL == 0
    assert godot.Variant.Operator.OP_MAX == 25


def test_global_constant():
    # Nothing to do: `extension_api.json`'s `global_constants` entry is empty so far...
    pass
