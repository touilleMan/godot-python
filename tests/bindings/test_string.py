import pytest

from godot import Basis, Vector2, Vector3, Quat, GDString

def test_default():
  assert GDString().empty()
  # Todo later: GDString creation from GD types: Vector2/3, Transform, Plane, Quat, AABB, Color, ...
  s = GDString("12")
  assert s.begins_with(GDString("1"))
  assert s.bigrams().size() == 1
  assert GDString("\ta").dedent() == GDString("a")
  assert s.ends_with(GDString("2"))
  abc = GDString("abc")
  abc.erase(1,1)
  assert abc == GDString("ac")
  assert GDString("abc").capitalize() == GDString("Abc")
  assert GDString("abc").find(GDString("b")) == 1
  assert GDString("file.ext").get_extension() == GDString("ext")
  assert GDString("127.0.0.1").is_valid_ip_address()
  assert GDString("abc").length() == 3
  assert GDString("€").length() == 1
  assert int(GDString("3.14").to_float() * 100) == 314
