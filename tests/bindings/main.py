import os
import pytest

from godot import exposed
from godot.bindings import Node, OS


@exposed
class Main(Node):

    def _ready(self):
        # benchmark
        iterations = 10000000
        from pythonscriptcffi import lib, ffi
        v1 = ffi.new('godot_vector2*')
        v2 = ffi.new('godot_vector2*')
        lib.godot_vector2_new(v1, 0, 0)
        lib.godot_vector2_new(v2, 2, 3)
        from time import perf_counter
        start = perf_counter()
        for _ in range(iterations):
            lib.godot_vector2_distance_to(v1, v2)
        end = perf_counter()
        print('func: %s iterations in %s' % (iterations, end - start))
        start = perf_counter()
        for _ in range(iterations):
            lib.ptrfunc_godot_vector2_distance_to(v1, v2)
        end = perf_counter()
        print('ptrfunc: %s iterations in %s' % (iterations, end - start))
        start = perf_counter()
        for _ in range(iterations):
            lib.structfunc_godot_vector2_distance_to(v1, v2)
        end = perf_counter()
        print('structfunc: %s iterations in %s' % (iterations, end - start))
        start = perf_counter()
        for _ in range(iterations):
            lib.staticfunc_godot_vector2_distance_to(v1, v2)
        end = perf_counter()
        print('staticfunc: %s iterations in %s' % (iterations, end - start))
        start = perf_counter()
        for _ in range(iterations):
            lib.structfunc._godot_vector2_distance_to(v1, v2)
        end = perf_counter()
        print('ptr: %s iterations in %s' % (iterations, end - start))

        # Retrieve command line arguments passed through --pytest=...
        prefix = '--pytest='
        import pdb; pdb.set_trace()
        # Filter to avoid scanning `plugins` and `lib` directories
        pytest_args = [x for x in os.listdir() if x.startswith('test_')]
        for arg in OS.get_cmdline_args():
            if arg.startswith(prefix):
                pytest_args += arg[len(prefix):].split(',')
        # Run tests here
        if pytest.main(pytest_args):
            OS.set_exit_code(1)
        # Exit godot
        self.get_tree().quit()
