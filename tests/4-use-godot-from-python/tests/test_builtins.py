import enum
import clodotest
from clodotest import assert_eq
import godot


def test_str():
    assert_eq(str(godot.GDString("foo")), "foo")
    assert_eq(str(godot.StringName("foo")), "foo")
    assert_eq(str(godot.NodePath("foo")), "foo")


def test_repr():
    assert_eq(repr(godot.GDString("foo")), "GDString('foo')")
    assert_eq(repr(godot.StringName("foo")), "StringName('foo')")
    assert_eq(repr(godot.NodePath("foo")), "NodePath('foo')")
    assert_eq(repr(godot.Vector2i(1, 2)), "Vector2i(x=1, y=2)")
    assert_eq(repr(godot.GDArray([1, 2])), "GDArray([1, 2])")
    assert_eq(repr(godot.GDDictionary({1: "foo"})), 'GDDictionary({ 1: "foo" })')


@clodotest.parametrize("type", ["Nil", "bool", "int", "float"])
def test_scalars_and_nil_not_exposed(type: str):
    assert not hasattr(godot, type)


@clodotest.parametrize(
    "kind",
    [
        "default",
        "String",
        "StringName",
        "NodePath",
        "Dictionary",
        "Array",
        "PackedArray",
    ],
)
def test_constructor(kind: str):
    match kind:
        case "default":
            v = godot.Vector2i()
            assert_eq(v.x, 0)
            assert_eq(v.y, 0)

            v = godot.Vector2i(1, 2)
            assert_eq(v.x, 1)
            assert_eq(v.y, 2)

            v = godot.Vector2i(1)
            assert_eq(v.x, 1)
            assert_eq(v.y, 0)

            v = godot.Vector2i(y=2)
            assert_eq(v.x, 0)
            assert_eq(v.y, 2)

            v = godot.Vector2i(x=1, y=2)
            assert_eq(v.x, 1)
            assert_eq(v.y, 2)

            # In Godot you would do `var v2 = Vector2(v1)`, but it's more Pythonic
            # to provide a clone method and do `v2 = v1.clone()` (and it simplifies
            # constructor implementation !)
            v = godot.Vector2i(1, 2).clone()
            assert_eq(v.x, 1)
            assert_eq(v.y, 2)

            for bad_type in (godot.GDString(), "42", b"42"):
                with clodotest.raises(TypeError):
                    godot.Vector2i(bad_type)

        case "String":
            s = godot.GDString()
            assert_eq(str(s), "")

            s = godot.GDString("foo")
            assert_eq(str(s), "foo")

            s2 = s.clone()
            assert_eq(str(s2), "foo")

            s = godot.GDString(godot.StringName("foo"))
            assert_eq(str(s), "foo")

            s = godot.GDString(godot.NodePath("/foo"))
            assert_eq(str(s), "/foo")

            for bad_type in (godot.Vector2i(), 42, b"foo"):
                with clodotest.raises(TypeError):
                    godot.GDString(bad_type)

        case "StringName":
            s = godot.StringName()
            assert_eq(str(s), "")

            s = godot.StringName("foo")
            assert_eq(str(s), "foo")

            s2 = s.clone()
            assert_eq(str(s2), "foo")

            s = godot.StringName(godot.GDString("foo"))
            assert_eq(str(s), "foo")

            for bad_type in (godot.Vector2i(), godot.NodePath("/foo"), 42, b"foo"):
                with clodotest.raises(TypeError):
                    godot.StringName(bad_type)

        case "NodePath":
            s = godot.NodePath()
            assert_eq(str(s), "")

            s = godot.NodePath("/foo")
            assert_eq(str(s), "/foo")

            s2 = s.clone()
            assert_eq(str(s2), "/foo")

            s = godot.NodePath(godot.GDString("/foo"))
            assert_eq(str(s), "/foo")

            s = godot.NodePath(godot.NodePath("/foo"))
            assert_eq(str(s), "/foo")

            for bad_type in (godot.Vector2i(), godot.StringName("/foo"), 42, b"foo"):
                with clodotest.raises(TypeError):
                    godot.NodePath(bad_type)

        case "Dictionary":
            d = godot.GDDictionary()
            assert_eq(d.is_empty(), True)

            d = godot.GDDictionary([(godot.GDString("a"), 1), (2, godot.GDString("b"))])
            assert_eq(d.is_empty(), False)
            assert_eq(d["a"], 1)
            assert_eq(d[2], godot.GDString("b"))

            d2 = d.clone()
            assert_eq(d2["a"], 1)
            assert_eq(d2[2], godot.GDString("b"))

            d = godot.GDDictionary([(godot.GDString("a"), 1), (2, godot.GDString("b"))])
            assert_eq(d["a"], 1)
            assert_eq(d[2], godot.GDString("b"))

            for bad_type in (godot.Vector2i(), 42, b"foo"):
                with clodotest.raises(TypeError):
                    godot.GDDictionary(bad_type)

        case "Array":
            a = godot.GDArray()
            assert_eq(a.is_empty(), True)

            for items in (
                [godot.GDString("a"), 2, godot.Vector2i(1, 2)],
                ["a", 2, godot.Vector2i(1, 2)],
                ("a", 2, godot.Vector2i(1, 2)),
                iter(["a", 2, godot.Vector2i(1, 2)]),
            ):
                a = godot.GDArray(items)
                assert_eq(a.is_empty(), False)
                assert_eq(a.size(), 3)
                assert_eq(a[0], godot.GDString("a"))
                assert_eq(a[1], 2)
                assert_eq(a[2], godot.Vector2i(1, 2))

            a1 = godot.GDArray(["a", 2, godot.Vector2i(1, 2)])
            a2 = godot.GDArray(a1)
            assert_eq(a2, a1)
            a3 = a1.clone()
            assert_eq(a3, a1)

            a3 = godot.GDArray(godot.PackedStringArray(["1", "2", "3"]))
            assert_eq(a3, godot.GDArray(["1", "2", "3"]))

            assert_eq(godot.GDArray(b"foo"), godot.GDArray([102, 111, 111]))

            for bad_type in (godot.Vector2i(), godot.StringName("/foo"), 42):
                with clodotest.raises(TypeError):
                    godot.GDArray(bad_type)

        case "PackedArray":
            a = godot.PackedStringArray()
            assert_eq(a.is_empty(), True)

            for items in (
                [godot.GDString("a"), godot.GDString("b")],
                ["a", "b"],
                ("a", "b"),
                iter(("a", "b")),
            ):
                a = godot.GDArray(items)
                assert_eq(a.is_empty(), False)
                assert_eq(a.size(), 2)
                assert_eq(a[0], godot.GDString("a"))
                assert_eq(a[1], godot.GDString("b"))

            a = godot.PackedStringArray(["a", "b"])
            a2 = a.clone()
            assert_eq(a2[0], godot.GDString("a"))
            assert_eq(a2[1], godot.GDString("b"))

            for bad_type in (godot.Vector2i(), godot.StringName("/foo"), 42, b"foo"):
                with clodotest.raises(TypeError):
                    godot.PackedStringArray(bad_type)

        case unknown:
            assert False, unknown


@clodotest.parametrize(
    "kind",
    [
        "no",
        "keyed",
        "not_keyed",
    ],
)
def test_indexing(kind: str):
    match kind:
        case "no":
            f = godot.StringName("foo")

            # Get

            with clodotest.raises(TypeError):
                f[0]

            with clodotest.raises(TypeError):
                f[godot.GDString("key")]

            # Set

            with clodotest.raises(TypeError):
                f[0] = 1

            with clodotest.raises(TypeError):
                f[godot.GDString("key")] = godot.GDString("key")

            # Del

            with clodotest.raises(TypeError):
                del f[1]

            with clodotest.raises(TypeError):
                del f[godot.GDString("key")]

        case "keyed":
            # TODO: store a class instance
            d = godot.GDDictionary(
                [(0, "a"), ("b", 2), (godot.Vector2i(1, 2), godot.Vector2i(3, 4))]
            )

            # Get

            assert_eq(d[0], godot.GDString("a"))
            assert_eq(d["b"], 2)
            assert_eq(d[godot.Vector2i(1, 2)], godot.Vector2i(3, 4))

            clodotest.skip(reason="TODO: out of range is not handled yet !")

            with clodotest.raises(KeyError):
                d[godot.GDString("dummy")]
            with clodotest.raises(KeyError):
                d[99]

            with clodotest.raises(TypeError):
                d[object()]  # object cannot be converted to a Godot type

            # Set

            d[0] = godot.GDString("xx")
            d["11"] = "yy"
            d[godot.Vector2i(1, 2)] = godot.GDString("yy")
            # TODO: store a class instance

            assert_eq(
                d,
                godot.GDDictionary(
                    [(0, "xx"), ("b", 2), ("11", "yy"), (godot.Vector2i(1, 2), "zz")]
                ),
            )

            with clodotest.raises(TypeError):
                d[object()] = 1  # object cannot be converted to a Godot type
            with clodotest.raises(TypeError):
                d[1] = object()  # object cannot be converted to a Godot type

            # Del

            del d[0]
            del d["11"]
            del d[godot.Vector2i(1, 2)]
            # TODO: delete a class instance

            assert_eq(d, godot.GDDictionary([("b", 2)]))

            with clodotest.raises(KeyError):
                del d[godot.GDString("dummy")]
            with clodotest.raises(KeyError):
                del d[99]

            with clodotest.raises(TypeError):
                del d[object()]  # object cannot be converted to a Godot type

        case "not_keyed":
            # TODO: store a class instance
            a = godot.GDArray((1, "b", godot.Vector2i(1, 2)))

            # Get

            assert_eq(a[0], 1)
            assert_eq(a[1], godot.GDString("b"))
            assert_eq(a[2], godot.Vector2i(1, 2))

            clodotest.skip(reason="TODO: out of range is not handled yet !")

            with clodotest.raises(IndexError):
                a[3]

            with clodotest.raises(TypeError):
                a[godot.GDString("dummy")]
            with clodotest.raises(TypeError):
                a[object()]  # object cannot be converted to a Godot type

            # Set

            a[0] = godot.Vector2i(3, 4)
            a[1] = "xx"
            assert_eq(a, godot.GDArray((godot.Vector2i(3, 4), "xx", godot.Vector2i(1, 2))))

            with clodotest.raises(IndexError):
                a[3] = 1

            with clodotest.raises(TypeError):
                a[godot.GDString("dummy")] = 1
            with clodotest.raises(TypeError):
                a[object()] = 1  # object cannot be converted to a Godot type
            with clodotest.raises(TypeError):
                a[1] = object()  # object cannot be converted to a Godot type

            # Del

            del a[0]
            del a[1]
            assert_eq(a, godot.GDArray([godot.Vector2i(1, 2)]))

            with clodotest.raises(IndexError):
                del a[3]

            with clodotest.raises(TypeError):
                a[godot.GDString("dummy")] = 1
            with clodotest.raises(TypeError):
                a[object()] = 1  # object cannot be converted to a Godot type
            with clodotest.raises(TypeError):
                a[1] = object()  # object cannot be converted to a Godot type


@clodotest.parametrize(
    "kind",
    [
        # comparison
        "equal",
        "not_equal",
        "less",
        "less_equal",
        "greater",
        "greater_equal",
        # mathematic
        "add",
        "subtract",
        "multiply",
        "divide",
        "negate",
        "positive",
        "module",
        "power",
        # bitwise
        "shift_left",
        "shift_right",
        "bit_and",
        "bit_or",
        "bit_xor",
        "bit_negate",
        # logic
        "and",
        "or",
        "xor",
        "not",
        # containment
        "in",
    ],
)
def test_operator(kind: str):
    match kind:
        # comparison

        case "equal":
            assert_eq(godot.GDString("foo") == godot.GDString("foo"), True)
            assert_eq(godot.GDString("foo") == godot.GDString("bar"), False)

            assert_eq(godot.Vector2i(1, 2) == godot.Vector2i(1, 2), True)
            assert_eq(godot.Vector2i(1, 0) == godot.Vector2i(1, 2), False)

            assert_eq(godot.GDArray() == godot.GDArray(), True)
            assert_eq(
                godot.GDArray((1, godot.GDString("foo")))
                == godot.GDArray((1, godot.GDString("foo"))),
                True,
            )
            assert_eq(godot.GDArray() == godot.GDArray((1,)), False)

            assert_eq(godot.GDDictionary() == godot.GDDictionary(), True)
            assert_eq(
                godot.GDDictionary([(1, godot.GDString("foo")), (godot.GDString("bar"), 2)])
                == godot.GDDictionary([(1, godot.GDString("foo")), (godot.GDString("bar"), 2)]),
                True,
            )
            assert_eq(godot.GDDictionary() == godot.GDDictionary([(1, 2)]), False)

        case "not_equal":
            assert_eq(godot.GDString("foo") != godot.GDString("bar"), True)
            assert_eq(godot.GDString("foo") != godot.GDString("foo"), False)

        case "less":
            assert_eq(godot.Vector2i(0, 0) < godot.Vector2i(1, 1), True)
            assert_eq(godot.Vector2i(1, 1) < godot.Vector2i(1, 1), False)

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 1) < 2

        case "less_equal":
            assert_eq(godot.Vector2i(1, 1) <= godot.Vector2i(1, 1), True)
            assert_eq(godot.Vector2i(2, 2) <= godot.Vector2i(1, 1), False)

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 1) <= 2

        case "greater":
            assert_eq(godot.Vector2i(1, 1) > godot.Vector2i(0, 0), True)
            assert_eq(godot.Vector2i(1, 1) > godot.Vector2i(1, 1), False)

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 1) > 2

        case "greater_equal":
            assert_eq(godot.Vector2i(1, 1) >= godot.Vector2i(1, 1), True)
            assert_eq(godot.Vector2i(1, 1) >= godot.Vector2i(2, 2), False)

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 1) >= 2

        # mathematic

        case "add":
            assert_eq(godot.GDString("foo") + godot.GDString("bar"), godot.GDString("foobar"))
            assert_eq(godot.Vector2i(1, 1) + godot.Vector2i(2, 3), godot.Vector2i(3, 4))

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 2) + 1

            with clodotest.raises(TypeError):
                _ = godot.GDString("a") + godot.Vector2i(1, 2)

        case "subtract":
            assert_eq(godot.Vector2i(4, 3) - godot.Vector2i(1, 2), godot.Vector2i(3, 1))

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 2) - 1

        case "multiply":
            assert_eq(godot.Vector2i(4, 3) * godot.Vector2i(2, 3), godot.Vector2i(8, 9))
            assert_eq(godot.Vector2i(4, 3) * 2, godot.Vector2i(8, 6))

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 2) * godot.GDString()

        case "divide":
            assert_eq(godot.Vector2i(4, 3) / godot.Vector2i(2, 3), godot.Vector2i(2, 1))
            assert_eq(godot.Vector2i(4, 3) / 2, godot.Vector2i(2, 1))

            with clodotest.raises(TypeError):
                _ = godot.Vector2i(1, 2) / godot.GDString()

        case "negate":
            assert_eq(-godot.Vector2i(1, 2), godot.Vector2i(-1, -2))

        case "positive":
            assert_eq(+godot.Vector2i(1, 2), godot.Vector2i(1, 2))

        case "module":
            assert_eq(godot.Vector2i(2, 3) % 2, godot.Vector2i(0, 1))
            assert_eq(godot.Vector2i(2, 3) % godot.Vector2i(3, 1), godot.Vector2i(2, 0))

            # TODO: Godot currently returns `gd_string_op_module_nil` when requesting `gd_string_op_module_variant`
            # (see: https://github.com/godotengine/godot/issues/109861)

            # assert_eq(godot.GDString("foo %s") % godot.GDString("bar"), godot.GDString("foo bar"))
            # assert_eq(godot.GDString("foo %s") % "bar", godot.GDString("foo bar"))
            # assert_eq(
            #     godot.GDString("foo %s") % godot.Vector2i(1, 2),
            #     godot.GDString("foo Vector2i(1, 2)"),
            # )

            # assert_eq(
            #     godot.StringName("foo %s") % godot.StringName("bar"), godot.StringName("foo bar")
            # )
            # assert_eq(
            #     godot.StringName("foo %s") % godot.GDString("bar"), godot.StringName("foo bar")
            # )
            # assert_eq(
            #     godot.StringName("foo %s %s")
            #     % [godot.GDString("bar"), godot.StringName("spam")],
            #     godot.StringName("foo bar spam"),
            # )

            with clodotest.raises(TypeError):
                _ = godot.StringName("foo %s %s") % object()

        case "power":
            # Nothing to do: currently only `int`&`float` implements `**` in Godot, but
            # they are not exposed to Python since we already have our own `int`&`float`!
            pass

        # bitwise

        case "shift_left":
            # Nothing to do: currently only `int` implements `<<` in Godot, but
            # it is not exposed to Python since we already have our own `int`!
            pass

        case "shift_right":
            # Nothing to do: currently only `int` implements `>>` in Godot, but
            # it is not exposed to Python since we already have our own `int`!
            pass

        case "bit_and":
            # Nothing to do: currently only `int` implements `&` in Godot, but
            # it is not exposed to Python since we already have our own `int`!
            pass

        case "bit_or":
            # Nothing to do: currently only `int` implements `|` in Godot, but
            # it is not exposed to Python since we already have our own `int`!
            pass

        case "bit_xor":
            # Nothing to do: currently only `int` implements `^` in Godot, but
            # it is not exposed to Python since we already have our own `int`!
            pass

        case "bit_negate":
            # Nothing to do: currently only `int` implements `~` in Godot, but
            # it is not exposed to Python since we already have our own `int`!
            pass

        # logic

        case "and":
            # Nothing to do: currently only `int/float/Nil` implements `and`
            # in Godot, but they are not exposed to Python since we already have
            # our own `int/float/None`!
            pass

        case "or":
            # Nothing to do: currently only `int/float/Nil` implements `or`
            # in Godot, but they are not exposed to Python since we already have
            # our own `int/float/None`!
            pass

        case "xor":
            # Nothing to do: currently only `int/float/Nil` implements `xor`
            # in Godot, but they are not exposed to Python since we already have
            # our own `int/float/None`!
            pass

        case "not":
            # In Python, `not x` is always defined as the invert of `bool(x)`,
            # so we test the bool operator here.
            assert_eq(bool(godot.GDString("")), False)
            assert_eq(bool(godot.GDString("foo")), True)
            assert_eq(bool(godot.Vector2i(0, 0)), False)
            assert_eq(bool(godot.Vector2i(1, 2)), True)
            assert_eq(bool(godot.GDArray()), False)
            assert_eq(bool(godot.GDArray([0])), True)
            assert_eq(bool(godot.GDDictionary()), False)
            assert_eq(bool(godot.GDDictionary([(0, 0)])), True)
            assert_eq(bool(godot.PackedStringArray()), False)
            assert_eq(bool(godot.PackedStringArray([godot.GDString("")])), True)

        # containment

        case "in":
            assert_eq(godot.GDString("foo") in godot.GDString("barfoospam"), True)
            # assert_eq("foo" in godot.GDString("barfoospam"), True)  # TODO: `GDString.contains` currently only accepts `GDString`...
            assert_eq(godot.GDString("foo") in godot.GDString("bar"), False)

            a = godot.GDArray((godot.Vector2i(0, 0), godot.Vector2i(1, 2), 3))
            assert_eq(godot.Vector2i(1, 2) in a, True)
            assert_eq(godot.Vector2i(1, 1) in a, False)
            assert_eq(2 in a, False)
            assert_eq(3 in a, True)

            d = godot.GDDictionary([(godot.Vector2i(0, 0), 1), (2, godot.Vector2i(1, 1))])
            assert_eq(godot.Vector2i(0, 0) in d, True)
            assert_eq(godot.Vector2i(1, 1) in d, False)
            assert_eq(2 in d, True)
            assert_eq(1 in d, False)

        case unknown:
            assert False, unknown


@clodotest.parametrize(
    "kind",
    [
        "static_method",
        "without_parameter_and_with_return_value",
        "without_return_value",
        "with_parameter_as_godot_value",
        "with_parameter_as_python_value",
        "with_parameter_passed_by_name",
        "with_parameter_with_default_value",
        "with_parameter_with_default_value_overwritten",
        "with_parameter_with_default_value_overwritten_and_passed_by_name",
        "bad_parameter_type",
    ],
)
def test_method(kind: str):
    match kind:
        case "static_method":
            clodotest.skip(reason="TODO: static method not supported yet!")  # TODO
            s = godot.GDString("foo.txt")
            assert_eq(godot.GDString.humanize_size(133790307), godot.GDString("127.5 MiB"))

        case "without_parameter_and_with_return_value":
            s = godot.GDString("foo.txt")

            # Return scalar
            assert_eq(s.length(), 7)
            assert_eq(s.is_empty(), False)

            # Return non-scalar builtin
            assert_eq(godot.Vector2i(-1, 2).sign(), godot.Vector2i(-1, 1))

            # Return Godot Variant
            a = godot.GDArray([s])
            assert_eq(a.front(), s)
            assert_eq(a.get(99), None)

            # TODO: Return Godot class instance

        case "without_return_value":
            a = godot.GDArray((1, 2))
            assert_eq(a.clear(), None)

        case "with_parameter_as_godot_value":
            s = godot.GDString("foo.txt")

            # Note we don't test scalar & Godot class instance here: those types
            # are always passed as Python values.

            # Method expecting a non-scalar builtin
            assert_eq(s.begins_with(godot.GDString("foo")), True)
            # Method expecting a Godot Variant
            assert_eq(s.format(godot.GDArray(["foo"])), godot.GDString("foo.txt"))
            assert_eq(
                s.format(godot.GDArray(["ar"]), placeholder=godot.GDString("oo")),
                godot.GDString("far.txt"),
            )

        case "with_parameter_as_python_value":
            s = godot.GDString("foo.txt")
            a = godot.GDArray()

            # Method expecting a scalar
            assert_eq(s.left(1), godot.GDString("f"))
            # Method expecting a non-scalar builtin
            assert_eq(s.begins_with("foo"), True)
            # TODO: Method expecting a Godot class instance
            # Method expecting a Godot Variant
            a.append("foo")
            assert_eq(a, godot.GDArray(["foo"]))

        case "with_parameter_passed_by_name":
            s = godot.GDString("foo.txt")

            assert_eq(s.begins_with(text="foo"), True)

        case "with_parameter_with_default_value":
            s = godot.GDString("foo.txt")

            assert_eq(s.count("o"), 2)

        case "with_parameter_with_default_value_overwritten":
            s = godot.GDString("foo.txt")

            assert_eq(s.count("o", 2), 1)
            assert_eq(s.count("o", 2, 2), 0)

        case "with_parameter_with_default_value_overwritten_and_passed_by_name":
            s = godot.GDString("foo.txt")

            assert_eq(s.count("o", from_=1), 2)
            assert_eq(s.count("o", to=2), 1)
            assert_eq(s.count("o", to=2, from_=2), 0)

        case "bad_parameter_type":
            s = godot.GDString("foo.txt")

            # Method expecting a scalar
            with clodotest.raises(TypeError):
                s.left(godot.GDString())  # Non-scalar builtin
            with clodotest.raises(TypeError):
                s.left(None)  # Wrong scalar type
            # TODO: test with a Godot class instance
            with clodotest.raises(TypeError):
                s.left(object())  # Incompatible Python type

            # Method expecting a non-scalar builtin
            with clodotest.raises(TypeError):
                s.begins_with(1)  # Scalar builtin
            with clodotest.raises(TypeError):
                s.begins_with(None)  # Scalar builtin
            with clodotest.raises(TypeError):
                s.begins_with(object())  # Incompatible Python type
            # TODO: test with a Godot class instance
            with clodotest.raises(TypeError):
                s.begins_with(godot.Vector2i())  # Wrong non-scalar builtin

            # Method expecting a Variant
            a = godot.GDArray()
            with clodotest.raises(TypeError):
                s.format(object())  # Incompatible Python type

            # TODO: Method expecting a Godot class instance


def test_member():
    v = godot.Vector2i(2, 3)
    assert_eq(v.x, 2)
    assert_eq(v.y, 3)

    v.x = 20
    assert_eq(v.x, 20)
    assert_eq(v.y, 3)

    v.y = 30
    assert_eq(v.x, 20)
    assert_eq(v.y, 30)

    # TODO: test property unrelated to the builtin internal structure
    # TODO: test subtype property (e.g. `rec2.position.x`)


def test_constant():
    # TODO: find a way to expose the constant as a class property ?
    assert_eq(godot.Vector2i.ZERO(), godot.Vector2i(0, 0))


@clodotest.xfail(reason="TODO: WIP")
def test_enum():
    assert isinstance(godot.Vector2i.AXIS, enum.Enum)
    assert_eq(godot.Vector2i.AXIS.X, 0)
    assert_eq(godot.Vector2i.AXIS.Y, 1)
