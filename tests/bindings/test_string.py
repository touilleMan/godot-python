import sys
import pytest

from godot import GDString


def test_base():
    assert GDString().empty()
    # Todo later: GDString creation from GD types: Vector2/3, Transform, Plane, Quat, AABB, Color, ...
    s = GDString("12")
    assert s.begins_with(GDString("1"))
    assert s.bigrams().size() == 1
    assert GDString("\ta").dedent() == GDString("a")
    assert s.ends_with(GDString("2"))
    abc = GDString("abc")
    abc.erase(1, 1)
    assert abc == GDString("ac")
    assert GDString("abc").capitalize() == GDString("Abc")
    assert GDString("abc").find(GDString("b")) == 1
    assert GDString("file.ext").get_extension() == GDString("ext")
    assert GDString("127.0.0.1").is_valid_ip_address()
    assert not GDString("127.0.0.1.xxx").is_valid_ip_address()
    assert GDString("abc").length() == 3
    assert GDString("3.14").to_float() == pytest.approx(3.14)
    assert GDString("42").to_int() == 42
    # GDString.humanize_size is a static method
    assert GDString.humanize_size(133790307) == GDString("127.5 MiB")


@pytest.mark.parametrize("char", ["e", "é", "€", "蛇", "🐍"])
def test_unicode(char):
    # Godot supports UCS2 on Windows and UCS4 on other platforms
    if len(char.encode("utf8")) > 2 and sys.platform == "win32":
        pytest.skip("Windows only supports UCS2")

    gdchar = GDString(char)
    assert str(gdchar) == char
    assert gdchar.length() == len(char)
