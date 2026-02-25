from godot import gddataclass, classes, Vector2, StringName, GDString


@gddataclass(init=False)
class DummyBuiltinsPython(classes.Node):
    """Python node stressing Godot builtin type creation and operations.

    Each _process() call exercises:
    - Vector2 construction, arithmetic (operator dispatch through Godot), and methods
      that return builtins (normalized, length, distance_to)
    - StringName construction and equality comparison
    - GDString construction and a method call (to_lower)

    This measures the cost of wrapping/unwrapping Godot builtin values on the
    Python side, including any object allocation and type-conversion round-trips.
    """

    def _process(self, delta: float) -> None:
        # --- Vector2: create, arithmetic, method returning builtin ---
        v = Vector2(1.0, 2.0)
        v2 = v + Vector2(0.5, 0.5)  # operator goes through Godot
        _n = v2.normalized()  # Godot method → new Vector2
        _l = v2.length()  # Godot method → float

        v3 = Vector2(3.0, 4.0)
        _d = v3.distance_to(v2)  # takes a builtin, returns float
        _dot = v3.dot(v2)  # another builtin → float

        # --- StringName: construction and comparison ---
        s1 = StringName("benchmark")
        s2 = StringName("godot_python")
        _eq = s1 == s2

        # --- GDString: construction and method returning new GDString ---
        gs = GDString("Benchmark_Test_String")
        _lower = gs.to_lower()  # Godot method → new GDString
