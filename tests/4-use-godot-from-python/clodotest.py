from traceback import print_exception
from typing import Callable
from inspect import signature
import pkgutil
import re
from pathlib import Path


RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NO_COLOR = "\033[0m"


def _collect_tests(path: Path, filter: re.Pattern | None) -> list[tuple[str, Callable]]:
    tests = []

    for loader, name, _ in pkgutil.walk_packages([str(path)]):
        match loader.find_spec(name, None):
            case None:
                continue
            case spec:
                if spec.loader is None:
                    continue
                module = spec.loader.load_module(name)

        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith("test_"):
                assert module.__file__ is not None
                test_path = f"{Path(module.__file__).relative_to(path)}::{name}"
                if filter and not filter.match(test_path):
                    continue
                tests.append((test_path, obj))

    return tests


def run_tests(path: Path, filter: re.Pattern | None, stop_on_failure: bool, quiet: bool) -> bool:
    tests = _collect_tests(path, filter)

    tests_success = 0
    for test_full_name, test_fn in tests:
        if not quiet:
            print(test_full_name, end="", flush=False)
        try:
            test_fn()
        except BaseException as exc:
            if quiet:
                print(test_full_name, end="", flush=False)
            print("{RED} ✘ ERROR !!!{NO_COLOR}\n")
            print_exception(exc)
            if stop_on_failure:
                return False
        else:
            tests_success += 1
            if not quiet:
                print(f"{GREEN} ✔{NO_COLOR}")

    if len(tests) == tests_success:
        print(f"{GREEN}{tests_success}/{len(tests)} tests passed{NO_COLOR}")
        return True
    else:
        print(f"{RED}{tests_success}/{len(tests)} tests passed{NO_COLOR}")
        return False
