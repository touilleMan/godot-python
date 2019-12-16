import pytest
import json

from godot import (
Dictionary,
Vector2,
Array,
GDString,
)
from godot.bindings import Node, Resource


def test_base():
    v = Dictionary()
    assert type(v) == Dictionary

@pytest.mark.xfail(
    reason="Godot Dictionary equal does lame comparison by pointer so far..."
)
def test_equal():
    arr = Dictionary()
    other = Dictionary()
    for key, value in [("a", 1), ("b", "foo"), ("c", Node()), ("d", Vector2())]:
        other[key] = arr[key] = value
    assert arr == other
    bad = Dictionary({"a": 1})
    assert not arr == bad  # Force use of __eq__

@pytest.mark.parametrize(
    "arg", [None, 0, "foo", Vector2(), {"a": 1}, Dictionary({"b": 2})]
)
def test_bad_equal(arg):
    arr = Dictionary({"a": 1})
    assert arr != arg

def test_repr():
    v = Dictionary()
    assert repr(v) == "<Dictionary({})>"
    v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
    assert repr(v).startswith("<Dictionary({")
    for item in ["'a': 1", "2: 'foo'", "0.5: <Vector2(x=0.0, y=0.0)>"]:
        assert item in repr(v)

@pytest.mark.parametrize(
    "arg",
    [42, "dummy", Vector2(), [object()], {object(): 1}, {1: object()}],
)
def test_bad_instantiate(arg):
    with pytest.raises((TypeError, ValueError)):
        Dictionary(arg)

@pytest.mark.parametrize(
    "arg",
    [
        Dictionary(),
        {},
        {"a": 1, 2: "foo", 0.5: Vector2()},
        Dictionary({"a": 1, 2: "foo", 0.5: Vector2()}),
    ],
)
def test_instantiate_from_copy(arg):
    arr = Dictionary(arg)
    if hasattr(arg, "_gd_ptr"):
        assert arr._gd_ptr != arg._gd_ptr

def test_len():
    v = Dictionary()
    assert len(v) == 0
    v["foo"] = "bar"
    assert len(v) == 1

def test_getitem():
    v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
    assert v["a"] == 1
    assert v[0.5] == Vector2()
    # Missing items are stored as None
    assert v["dummy"] is None
    # Cannot store non Godot types
    with pytest.raises(TypeError):
        v[object()]

def test_setitem():
    v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
    v[0] = GDString("bar")
    assert len(v) == 4
    assert v[0] == GDString("bar")
    v["a"] = 4
    assert len(v) == 4
    assert v["a"] == 4
    # Cannot store non Godot types
    with pytest.raises(TypeError):
        v[object()] = 4
    with pytest.raises(TypeError):
        v[4] = object()

def test_delitem():
    v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
    del v["a"]
    assert len(v) == 2
    del v[0.5]
    assert len(v) == 1
    v[2] == GDString("foo")
    # Delete on missing items should raise error
    with pytest.raises(KeyError):
        del v["missing"]
    # Cannot store non Godot types
    with pytest.raises(TypeError):
        del v[object()]

def test_update():
    v = Dictionary({"a": 1, "b": 2, "c": 3})
    v.update({"a": "one", "d": "four"})
    v.update(Dictionary({"b": "two", "e": "five"}))
    assert list(v.keys()) == [GDString("a"), GDString("b"), GDString("c"), GDString("d"), GDString("e")]
    assert list(v.values()) == [GDString("one"), GDString("two"), 3, GDString("four"), GDString("five")]

def test_iter():
    v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
    items = [GDString("a"), 2, 0.5]
    items_from_v = [x for x in v]
    assert items_from_v == items

def test_keys():
    v = Dictionary({"a": 1, 2: "foo", 0.5: Vector2()})
    keys = v.keys()
    assert list(keys) == [GDString("a"), 2, 0.5]

def test_values():
    v = Dictionary({"a": 1, 2: "foo"})
    values = v.values()
    assert list(values) == [1, GDString("foo")]

def test_items():
    v = Dictionary({"a": 1, 2: "foo"})
    items = v.items()
    assert list(items) == [(GDString("a"), 1), (2, GDString("foo"))]

def test_empty_and_clear():
    v = Dictionary({"a": 1, 2: "foo"})
    assert not v.empty()
    v.clear()
    assert len(v) == 0
    assert v.empty()

def test_in():
    v = Dictionary({"a": 1, 2: "foo"})
    assert "a" in v
    assert 2 in v
    assert "dummy" not in v

def test_hash():
    v = Dictionary({"a": 1, 2: "foo"})
    h1 = v.hash()
    h2 = v.hash()
    assert h1 == h2
    v['b'] = 42
    h3 = v.hash()
    assert h3 != h2

def test_has_all():
    v = Dictionary({"a": 1, 2: "foo", None: None})
    elems = Array(["a", None])
    assert v.has_all(elems)
    bad_elems = Array(["a", 42])
    assert not v.has_all(bad_elems)

def test_to_json():
    v = Dictionary({"a": 1, "b": "foo"})
    jsoned = v.to_json()
    v2 = json.loads(str(jsoned))
    assert v2 == {"a": 1, "b": "foo"}
    assert json
