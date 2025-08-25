from clodotest import assert_isinstance
import godot


def test_access():
    from godot.classes import OS as _OS
    from godot.singletons import OS

    assert_isinstance(OS, _OS)
    assert_isinstance(OS.delta_smoothing, bool)
    assert_isinstance(OS.get_config_dir(), godot.GDString)
