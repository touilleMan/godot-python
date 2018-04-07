import sys

from pythonscriptcffi import ffi, lib

from godot.hazmat.profiler import Profiler
from godot.hazmat.tools import godot_string_from_pyobj
from godot.bindings import Dictionary


profiler = Profiler()


@ffi.def_extern()
def pybind_profiling_start(handle):
    profiler.reset()
    profiler.enabled = True
    sys.setprofile(profiler.get_profilefunc())


@ffi.def_extern()
def pybind_profiling_stop(handle):
    profiler.enabled = False
    sys.setprofile(None)


@ffi.def_extern()
def pybind_profiling_get_accumulated_data(handle, info, info_max):
    print("get_frame_accumulated_data")
    info = Dictionary.build_from_gdobj(info, steal=True)
    # Sort function to make sure we can display the most consuming ones
    sorted_and_limited = sorted(
        profiler.per_meth_profiling.items(), key=lambda x: -x[1].self_time
    )[
        :info_max
    ]
    for signature, profile in sorted_and_limited:
        info[signature] = Dictionary(
            call_count=profile.call_count,
            total_time=int(profile.total_time * 1e6),
            self_time=int(profile.self_time * 1e6),
        )
    return len(sorted_and_limited)


@ffi.def_extern()
def pybind_profiling_get_frame_data(handle, info, info_max):
    print("get_frame_data")
    # Sort function to make sure we can display the most consuming ones
    sorted_and_limited = sorted(
        profiler.per_meth_profiling.items(), key=lambda x: -x[1].last_frame_self_time
    )[
        :info_max
    ]
    for i, item in enumerate(sorted_and_limited):
        signature, profile = item
        # TODO: should be able to use lib.godot_string_new_with_wide_string directly
        lib.godot_string_name_new(
            ffi.addressof(info[i].signature), godot_string_from_pyobj(signature)
        )
        info[i].call_count = profile.last_frame_call_count
        info[i].total_time = int(profile.last_frame_total_time * 1e6)
        info[i].self_time = int(profile.last_frame_self_time * 1e6)
    return len(sorted_and_limited)


@ffi.def_extern()
def pybind_profiling_frame(handle):
    if profiler.enabled:
        profiler.next_frame()
