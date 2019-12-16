# import pytest
# import json

# from godot import (
#     Dictionary,
#     Vector2,
#     Array,
# )
# from godot.bindings import Node, Resource


# class TestDictionary:
#     def test_base(self):
#         v = Dictionary()
#         assert type(v) == Dictionary

#     @pytest.mark.xfail(
#         reason="Godot Dictionary equal does lame comparison by pointer so far..."
#     )
#     def test_equal(self):
#         arr = Dictionary()
#         other = Dictionary()
#         for key, value in [("a", 1), ("b", "foo"), ("c", Node()), ("d", Vector2())]:
#             other[key] = arr[key] = value
#         assert arr == other
#         bad = Dictionary({"a": 1})
#         assert not arr == bad  # Force use of __eq__

#     @pytest.mark.parametrize(
#         "arg", [None, 0, "foo", Vector2(), Node(), {"a": 1}, Dictionary({"b": 2})]
#     )
#     def test_bad_equal(self, arg):
#         arr = Dictionary({"a": 1})
#         assert arr != arg

#     def test_repr(self):
#         v = Dictionary()
#         assert repr(v) == "<Dictionary({})>"
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         assert repr(v).startswith("<Dictionary({")
#         for item in ["'a': 1", "2: 'foo'", "0.5: <Vector2(x=0.0, y=0.0)>"]:
#             assert item in repr(v)

#     @pytest.mark.parametrize(
#         "arg",
#         [42, "dummy", Node(), Vector2(), [object()], {object(): 1}, {1: object()}],
#     )
#     def test_bad_instantiate(self, arg):
#         with pytest.raises(TypeError):
#             Dictionary(arg)

#     @pytest.mark.parametrize(
#         "arg",
#         [
#             Dictionary(),
#             {},
#             {"a": 1, 2: "foo", 0.5: Vector2()},
#             Dictionary({"a": 1, 2: "foo", 0.5: Vector2()}),
#         ],
#     )
#     def test_instantiate_from_copy(self, arg):
#         arr = Dictionary(arg)
#         if hasattr(arg, "_gd_ptr"):
#             assert arr._gd_ptr != arg._gd_ptr

#     def test_len(self):
#         v = Dictionary()
#         assert len(v) == 0
#         v["foo"] = "bar"
#         assert len(v) == 1

#     def test_getitem(self):
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         assert v["a"] == 1
#         assert v[0.5] == Vector2()
#         # Missing items are stored as None
#         assert v["dummy"] is None
#         # Cannot store non Godot types
#         with pytest.raises(TypeError):
#             v[object()]

#     def test_setitem(self):
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         v[0] = "bar"
#         assert len(v) == 4
#         assert v[0] == "bar"
#         v["a"] = 4
#         assert len(v) == 4
#         assert v["a"] == 4
#         # Cannot store non Godot types
#         with pytest.raises(TypeError):
#             v[object()] = 4
#         with pytest.raises(TypeError):
#             v[4] = object()

#     def test_delitem(self):
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         del v["a"]
#         assert len(v) == 2
#         del v[0.5]
#         assert len(v) == 1
#         v[2] == "foo"
#         # Missing items can be deleted without error
#         del v["missing"]
#         # Cannot store non Godot types
#         with pytest.raises(TypeError):
#             del v[object()]

#     def test_update(self):
#         v = Dictionary({"a": 1, "b": 2, "c": 3})
#         v.update({"a": "one", "d": "four"})
#         v.update(Dictionary({"b": "two", "e": "five"}))
#         assert set(v.keys()) == {"a", "b", "c", "d", "e"}
#         assert set(v.values()) == {"one", "two", 3, "four", "five"}

#     def test_contains(self):
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         assert "a" in v
#         assert "dummy" not in v

#     def test_iter(self):
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         items = ["a", 2, 0.5]
#         items_from_v = [x for x in v]
#         assert set(items_from_v) == set(items)

#     def test_keys(self):
#         v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
#         keys = v.keys()
#         assert set(keys) == set(["a", 2, 0.5])

#     def test_values(self):
#         v = Dictionary({"a": 1, 2: "foo"})
#         values = v.values()
#         assert set(values) == set([1, "foo"])

#     def test_items(self):
#         v = Dictionary({"a": 1, 2: "foo"})
#         items = v.items()
#         assert set(items) == set([("a", 1), (2, "foo")])

#     def test_empty_and_clear(self):
#         v = Dictionary({"a": 1, 2: "foo"})
#         assert not v.empty()
#         v.clear()
#         assert len(v) == 0
#         assert v.empty()

#     def test_in(self):
#         v = Dictionary({"a": 1, 2: "foo"})
#         assert "a" in v
#         assert "dummy" not in v

#     def test_hash(self):
#         v = Dictionary({"a": 1, 2: "foo"})
#         v.hash()

#     def test_has_all(self):
#         v = Dictionary({"a": 1, 2: "foo", None: None})
#         elems = Array(["a", None])
#         assert v.has_all(elems)
#         bad_elems = Array(["a", 42])
#         assert not v.has_all(bad_elems)

#     def test_to_json(self):
#         v = Dictionary({"a": 1, "b": "foo"})
#         jsoned = v.to_json()
#         v2 = json.loads(jsoned)
#         assert v2 == {"a": 1, "b": "foo"}
#         assert json
