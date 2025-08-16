import sys
import clodotest

from godot import GDString

# TODO:
# Since the builtins are generated from the Godot's `extension_api.json`, we don't
# need to test every method, however we should test each flavor of generated stuff:
# - Initialization
# - No leak on destructor
# - Compatibility with Python types
# - operators (equality, comparison, bracket)
# - property
# - constant
# - static method
# - method call
# - method call with parameter
# - method call with parameter provided out-of-order by name
# - method call with parameter with a default value


def test_base():
    assert GDString().is_empty()
    # Todo later: GDString creation from GD types: Vector2/3, Transform, Plane, Quat, AABB, Color, ...
    s = GDString("12")
    assert s.begins_with(GDString("1"))
    assert s.bigrams().size() == 1
    # TODO: == operator no yet supported
    # assert GDString("\ta").dedent() == GDString("a")
    assert s.ends_with(GDString("2"))
    abc = GDString("abc")
    abc.erase(1, 1)
    # TODO: == operator no yet supported
    # assert abc == GDString("ac")
    # TODO: == operator no yet supported
    # assert GDString("abc").capitalize() == GDString("Abc")
    # TODO: `from` parameter should not be needed since the default value is passed
    assert GDString("abc").find(GDString("b"), 0) == 1
    # TODO: == operator no yet supported
    # assert GDString("file.ext").get_extension() == GDString("ext")
    assert GDString("127.0.0.1").is_valid_ip_address()
    assert not GDString("127.0.0.1.xxx").is_valid_ip_address()
    assert GDString("abc").length() == 3
    clodotest.assert_approx_eq(GDString("3.14").to_float(), 3.14)
    assert GDString("42").to_int() == 42
    # GDString.humanize_size is a static method
    # TODO: == operator no yet supported
    # assert GDString.humanize_size(133790307) == GDString("127.5 MiB")


@clodotest.parametrize("char", ["e", "é", "€", "蛇", "🐍"])
def test_unicode(char):
    # Godot supports UCS2 on Windows and UCS4 on other platforms
    if len(char.encode("utf8")) > 2 and sys.platform == "win32":
        clodotest.skip("Windows only supports UCS2")

    gdchar = GDString(char)
    assert str(gdchar) == char
    assert gdchar.length() == len(char)
