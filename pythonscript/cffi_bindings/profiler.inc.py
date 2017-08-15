import sys
import threading
from collections import defaultdict
from time import perf_counter


class MethProfile:
    __slots__ = ('call_count', 'self_time', 'total_time',
                 'cur_frame_call_count', 'cur_frame_self_time', 'cur_frame_total_time',
                 'last_frame_call_count', 'last_frame_self_time', 'last_frame_total_time')

    def __init__(self):
        self.call_count = 0
        self.self_time = 0
        self.total_time = 0
        self.cur_frame_call_count = 0
        self.cur_frame_self_time = 0
        self.cur_frame_total_time = 0
        self.last_frame_call_count = 0
        self.last_frame_self_time = 0
        self.last_frame_total_time = 0


class FuncCallProfile:
    __slots__ = ('signature', 'start', 'end', 'out_of_func_time')

    def __init__(self, signature):
        self.signature = signature
        self.start = perf_counter()
        self.end = None
        # Time spend calling another function
        self.out_of_func_time = 0

    def add_out_of_func(self, time):
        self.out_of_func_time += time

    def get_self_time(self):
        return self.get_total_time() - self.out_of_func_time

    def done(self):
        self.end = perf_counter()

    def get_total_time(self):
        return self.end - self.start


class Profiler:
    def __init__(self):
        self.enabled = False
        self.per_meth_profiling = defaultdict(MethProfile)
        self._profile_stack = []

    @property
    def _per_thread_profile_stack(self):
        return self._profile_stack
        # TODO: Make this thread safe
        # Not sure if multithreading is supported by sys.setprofile anyway...
        # loc = threading.local()
        # key = 'profile_stack_%s' % id(self)
        # stack = getattr(loc, key, None)
        # if not stack:
        #     stack = []
        #     setattr(loc, key, stack)
        # return stack

    def reset(self):
        self.per_meth_profiling.clear()
        self._profile_stack.clear()

    def next_frame(self):
        for meth_profile in self.per_meth_profiling.values():
            meth_profile.call_count = meth_profile.cur_frame_call_count
            meth_profile.self_time = meth_profile.cur_frame_self_time
            meth_profile.total_time = meth_profile.cur_frame_total_time
            meth_profile.last_frame_call_count = meth_profile.cur_frame_call_count
            meth_profile.last_frame_self_time = meth_profile.cur_frame_self_time
            meth_profile.last_frame_total_time = meth_profile.cur_frame_total_time
            meth_profile.cur_frame_call_count = 0
            meth_profile.cur_frame_self_time = 0
            meth_profile.cur_frame_total_time = 0

    def get_profilefunc(self):

        def profilefunc(frame, event, arg):
            # TODO: improve this hack to avoid profiling builtins functions
            if frame.f_code.co_filename.startswith('<'):
                return
            if event in ('call', 'c_call'):
                signature = '{path}::{line}::{name}'.format(
                    path=frame.f_code.co_filename,
                    line=frame.f_lineno, name=frame.f_code.co_name)
                self.per_meth_profiling[signature].cur_frame_call_count += 1
                self._per_thread_profile_stack.append(FuncCallProfile(signature))
            else:
                try:
                    callprof = self._per_thread_profile_stack.pop()
                except IndexError:
                    # `pybind_profiling_start` has been called before the
                    # profiler was enable, so _per_thread_profile_stack lacks
                    # it representation
                    return
                callprof.done()
                signature = callprof.signature
                prof = self.per_meth_profiling[signature]
                prof.cur_frame_total_time += callprof.get_total_time()
                prof.cur_frame_self_time += callprof.get_self_time()
                if self._per_thread_profile_stack:
                    self._per_thread_profile_stack[-1].add_out_of_func(callprof.get_total_time())

        return profilefunc


profiler = Profiler()


@ffi.def_extern()
def pybind_profiling_start():
    profiler.reset()
    profiler.enabled = True
    sys.setprofile(profiler.get_profilefunc())


@ffi.def_extern()
def pybind_profiling_stop():
    profiler.enabled = False
    sys.setprofile(None)


@ffi.def_extern()
def pybind_profiling_get_accumulated_data(info, info_max):
    print('get_frame_accumulated_data')
    info = Dictionary.build_from_gdobj(info, steal=True)
    # Sort function to make sure we can display the most consuming ones
    sorted_and_limited = sorted(profiler.per_meth_profiling.items(),
                                key=lambda x: -x[1].self_time)[:info_max]
    for signature, profile in sorted_and_limited:
        info[signature] = Dictionary(
            call_count=profile.call_count,
            total_time=int(profile.total_time * 1e6),
            self_time=int(profile.self_time * 1e6)
        )
    return len(sorted_and_limited)


@ffi.def_extern()
def pybind_profiling_get_frame_data(info, info_max):
    print('get_frame_data')
    info = Dictionary.build_from_gdobj(info, steal=True)
    count = 0
    for signature, profile in profiler.per_meth_profiling.items():
        if profile.last_frame_call_count:
            info[signature] = Dictionary(
                call_count=profile.last_frame_call_count,
                total_time=int(profile.last_frame_total_time * 1e6),
                self_time=int(profile.last_frame_self_time * 1e6)
            )
            count += 1
    return count


@ffi.def_extern()
def pybind_profiling_frame():
    if profiler.enabled:
        profiler.next_frame()
