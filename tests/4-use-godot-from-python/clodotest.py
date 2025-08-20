from functools import partial, wraps
from traceback import print_exception
from typing import Callable, Iterator, Any
import itertools
from contextlib import contextmanager
import pkgutil
import re
from pathlib import Path
import dataclasses


@dataclasses.dataclass(slots=True)
class Parametrize[X: tuple[Any, ...]]:
    param: list[str] | str
    values: list[X]
    ids: Callable[[X], str | Any]


RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NO_COLOR = "\033[0m"


def _ensure_repr(x: Any) -> str:
    return x if isinstance(x, str) else repr(x)


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

        assert module.__file__ is not None
        for name, fn in module.__dict__.items():
            if not callable(fn) or not name.startswith("test_"):
                continue

            parametrized: list[Parametrize] | None = getattr(fn, "_clodo_parametrized", None)
            if parametrized:
                all_parametrizes: list[Parametrize] = parametrized
                for all_parametrizes_values_product in itertools.product(
                    *(p.values for p in all_parametrizes)
                ):

                    def _parametrized_fn(
                        fn: Callable,
                        all_parametrizes: list[Parametrize],
                        all_parametrizes_values_product: tuple[Any, ...],
                    ):
                        params = {}
                        for parametrize, parametrize_value in zip(
                            all_parametrizes, all_parametrizes_values_product
                        ):
                            if isinstance(parametrize.param, list):
                                assert len(parametrize.param) == len(parametrize_value)
                                for param, value in zip(parametrize.param, parametrize_value):
                                    params[param] = value
                            else:
                                params[parametrize.param] = parametrize_value
                        return fn(**params)

                    params_display = ",".join(
                        _ensure_repr(parametrize.ids(parametrize_value))
                        for parametrize, parametrize_value in zip(
                            all_parametrizes, all_parametrizes_values_product
                        )
                    )

                    test_path = (
                        f"{Path(module.__file__).relative_to(path)}::{name}[{params_display}]"
                    )
                    if filter and not filter.search(test_path):
                        continue
                    tests.append(
                        (
                            test_path,
                            partial(
                                _parametrized_fn,
                                fn,
                                all_parametrizes,
                                all_parametrizes_values_product,
                            ),
                        )
                    )

            else:
                test_path = f"{Path(module.__file__).relative_to(path)}::{name}"
                if filter and not filter.match(test_path):
                    continue
                tests.append((test_path, fn))

    return tests


def run_tests(path: Path, filter: re.Pattern | None, stop_on_failure: bool, verbose: bool) -> bool:
    tests = _collect_tests(path, filter)

    tests_success = 0
    for test_full_name, test_fn in tests:
        if verbose:
            print(test_full_name, end="", flush=False)
        try:
            test_fn()
        except SkipTest as exc:
            tests_success += 1
            if verbose:
                print(f"{YELLOW} Skipped: {exc.reason}{NO_COLOR}", flush=True)
        except BaseException as exc:
            if not verbose:
                print(test_full_name, end="", flush=False)
            print(f"{RED} ✘ ERROR !!!{NO_COLOR}\n", flush=True)
            print_exception(exc)
            if stop_on_failure:
                return False
        else:
            tests_success += 1
            if verbose:
                print(f"{GREEN} ✔{NO_COLOR}", flush=True)

    if len(tests) == tests_success:
        print(f"{GREEN}{tests_success}/{len(tests)} tests passed{NO_COLOR}")
        return True
    else:
        print(f"{RED}{tests_success}/{len(tests)} tests passed{NO_COLOR}")
        return False


def run_tests_with_argv(path: Path, argv: list[str]) -> bool:
    verbose = False
    stop_on_failure = False
    raw_filters = []

    args = iter(argv)
    for arg in args:
        match arg:
            case "-v":
                verbose = True
            case "-x":
                stop_on_failure = True
            case "-k":
                raw_filters.append(rf"({re.escape(next(args))})")
            case "-h":
                print("Allowed options: [PATH] [-v] [-x] [-k FILTER]")
                raise SystemExit(-1)
            case unknown:
                if not unknown.startswith("-"):
                    raw_filters.append(rf"(^{re.escape(unknown)})")
                    continue

                raise SystemExit(f"Unknown option `{unknown}`")

    filter = re.compile(r"|".join(raw_filters))
    return run_tests(path=path, filter=filter, stop_on_failure=stop_on_failure, verbose=verbose)


@contextmanager
def raises(expected_exc_type: type) -> Iterator[None]:
    try:
        yield
    except BaseException as exc:
        assert isinstance(exc, expected_exc_type), (
            f"Invalid exception, expected type {expected_exc_type!r}, got `{exc!r}`"
        )
    else:
        assert False, "No exception occured !"


def xfail[F: Callable](reason: str) -> Callable[[F], F]:
    def _xfail(fn: F) -> F:
        @wraps(fn)
        def _wrapper(**kwargs):
            try:
                fn(**kwargs)
                assert False, "Expected error, got none !"
            except BaseException:
                # As expected
                raise SkipTest(reason=f"XFAIL ({reason})")

        return _wrapper  # type: ignore

    return _xfail


def parametrize[F: Callable, P: Any | tuple[Any, ...]](
    param: str,
    values: list[P],
    ids: Callable[[P], str | Any] = lambda x: x if isinstance(x, str) else repr(x),
) -> Callable[[F], F]:
    if "," in param:
        cooked_param = param.split(",")
    else:
        cooked_param = param

    def _wrapper(
        param: str | list[str], values: list[P], ids: Callable[[P], str | Any], fn: F
    ) -> F:
        parametrized = getattr(fn, "_clodo_parametrized", None)
        if parametrized is None:
            parametrized = []
            setattr(fn, "_clodo_parametrized", parametrized)
        parametrized.append(Parametrize(param=param, values=values, ids=ids))
        return fn

    return partial(_wrapper, cooked_param, values, ids)


class SkipTest(BaseException):
    def __init__(self, reason: str):
        self.reason = reason


def skip(reason: str) -> None:
    raise SkipTest(reason=reason)


def assert_approx_eq(a: float, b: float, max_relative_diff: float = 0.001):
    diff = abs(a - b)
    if diff == 0:
        return
    base = a if a != 0 else b
    relative_diff = diff / base
    if relative_diff > max_relative_diff:
        raise AssertionError(
            f"{a} and {b} are too far appart ({relative_diff * 100:.2f}%, max allowed is {max_relative_diff * 100:.2f}%)"
        )


def assert_eq(got: Any, expected: Any):
    if got != expected:
        raise AssertionError(f"Expected {expected!r}, got {got!r}")


def assert_is(got: Any, expected: Any):
    if got is expected:
        raise AssertionError(f"Expected {expected!r}, got {got!r}")
