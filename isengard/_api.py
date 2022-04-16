from contextvars import ContextVar
from pathlib import Path
from typing import (
    Dict,
    Tuple,
    List,
    Sequence,
    Callable,
    Union,
    Optional,
    Union,
    TypeVar,
)

from ._const import ConstTypes
from ._rule import Rule, RULE_RESERVED_PARAMS, LAZY_RULE_RESERVED_REGISTER_PARAM

from ._dump import dump_graph
from ._runner import Runner
from ._target import (
    ResolvedTargetID,
    TargetHandlersBundle,
    BaseTargetHandler,
    FileTargetHandler,
    FolderTargetHandler,
    VirtualTargetHandler,
    DeferredTargetHandler,
)
from ._collector import Collector
from ._exceptions import (
    IsengardError,
    IsengardStateError,
    IsengardConsistencyError,
)


RESERVED_CONFIG_NAMES = {
    *RULE_RESERVED_PARAMS,
    LAZY_RULE_RESERVED_REGISTER_PARAM,
    "rootdir",  # Entrypoint script's directory
    "ruledir",  # Directory of the script the current rule was defined in
}


DEFAULT_DEFAULT_TARGET_HANDLER = FileTargetHandler()
DEFAULT_TARGET_HANDLERS = [
    DEFAULT_DEFAULT_TARGET_HANDLER,
    FolderTargetHandler(),
    VirtualTargetHandler(),
    DeferredTargetHandler(),
]


C = TypeVar("C", bound=Callable[..., None])


_parent: ContextVar["Isengard"] = ContextVar("context")


def get_parent() -> "Isengard":
    try:
        return _parent.get()
    except LookupError as exc:
        raise IsengardError("Not in a subdir !") from exc


class Isengard:
    def __init__(
        self,
        self_file: Union[str, Path],
        db: Union[str, Path] = ".isengard.sqlite",
        subdir_default_filename: Optional[str] = None,
        target_handlers: Sequence[BaseTargetHandler] = DEFAULT_TARGET_HANDLERS,
        default_target_handler: Optional[BaseTargetHandler] = DEFAULT_DEFAULT_TARGET_HANDLER,
    ):
        entrypoint_path = Path(self_file).resolve()
        self._entrypoint_dir = entrypoint_path.parent
        self._entrypoint_name = entrypoint_path.name
        self._subdir_default_filename = subdir_default_filename or self._entrypoint_name
        self._workdir = self._entrypoint_dir  # Modified when reading subdir

        if not isinstance(db, Path):
            db = Path(db)
        if not db.is_absolute():
            db = self._entrypoint_dir / db
        self._db_path = db

        self._target_handlers_bundle = TargetHandlersBundle(
            target_handlers=target_handlers,
            default_target_handler=default_target_handler,
        )
        self._collector = Collector(target_handlers=self._target_handlers_bundle)

        # Defined when configured is called
        self._config: Optional[Dict[str, ConstTypes]] = None
        self._runner: Optional[Runner] = None

    @property
    def rootdir(self) -> Path:
        return self._entrypoint_dir

    def subscript(self, subscript: Union[str, Path]) -> None:
        if not isinstance(subscript, Path):
            subscript = self._workdir / subscript

        try:
            relative_subscript = subscript.relative_to(self._entrypoint_dir)
        except ValueError:
            raise IsengardConsistencyError(
                f"Subscript must be within the root folder `{self._entrypoint_dir}`"
            )

        assert not relative_subscript.is_absolute()
        modname = ".".join([*relative_subscript.parent.parts, relative_subscript.stem])

        previous_workdir = self._workdir
        token = _parent.set(self)
        try:
            # Temporary self modification is not a very clean approach
            # but at least it's fast&simple ;-)
            self._workdir = subscript.parent

            self._load_file_as_module(modname, subscript)

        finally:
            self._workdir = previous_workdir
            _parent.reset(token)

    def subdir(self, subdir: str, filename: Optional[str] = None) -> None:
        subscript_path = self._workdir / subdir / (filename or self._subdir_default_filename)
        self.subscript(subscript_path)

    def configure(self, **config: ConstTypes) -> None:
        """
        Note passing configuration as function arguments limit the name you can use
        (e.g. `compiler.c.flags` is not a valid name). This is intended to work
        well with dependency injection in the rule where configuration is requested
        by using it name as function argument.
        """
        if self._config:
            raise IsengardStateError("`configure` has already been called !")

        setted = config.setdefault("rootdir", self._entrypoint_dir)
        if setted is not self._entrypoint_dir:
            raise IsengardConsistencyError(f"Config `rootdir` is a reserved name")
        self._rules, self._config = self._collector.configure(**config)
        self._runner = Runner(
            rules=self._rules,
            config=self._config,
            target_handlers=self._target_handlers_bundle,
            db_path=self._db_path,
        )

    def lazy_config(self, fn: C) -> C:
        if self._config is not None:
            raise IsengardStateError(
                "Cannot create new lazy configuration value once `configure` has been called !"
            )

        config_name = fn.__name__
        if config_name in RESERVED_CONFIG_NAMES:
            raise IsengardConsistencyError(f"Config `{config_name}` is a reserved name")

        self._collector.add_lazy_config(config_name, fn)

        return fn

    def lazy_rule(self, fn: C) -> C:
        if self._config is not None:
            raise IsengardStateError(
                "Cannot create new lazy rule generator once `configure` has been called !"
            )

        self._collector.add_lazy_rule(fn.__name__, fn, self._workdir)

        return fn

    def rule(
        self,
        outputs: Optional[Sequence[str]] = None,
        output: Optional[str] = None,
        inputs: Optional[Sequence[str]] = None,
        input: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Callable[[C], C]:
        def wrapper(fn: C) -> C:
            if self._config is not None:
                raise IsengardStateError(
                    "Cannot create new rules once `configure` has been called !"
                )

            rule = Rule(
                workdir=self._workdir,
                fn=fn,
                outputs=outputs,
                output=output,
                inputs=inputs,
                input=input,
                id=id,
            )
            self._collector.add_rule(rule)

            return fn

        return wrapper

    def run(self, target: Union[str, Path]) -> bool:
        """
        Raises:
            IsengardUnknownTargetError
            IsengardConsistencyError
            IsengardRunError
        """
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        resolved = self.resolve_target(target)
        return self._runner.run(target=resolved)

    def clean(self, target: Union[str, Path]) -> None:
        """
        Raises:
            IsengardUnknownTargetError
            IsengardConsistencyError
            IsengardRunError
        """
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        resolved = self.resolve_target(target)
        self._runner.clean(resolved)

    def resolve_target(self, target: Union[str, Path]) -> ResolvedTargetID:
        if isinstance(target, Path):
            # Identifying a target by it Path on the FS is convenient for the user,
            # but not for us given we use the `ResolvedTagetID` instead precisely to
            # unify Virtual and on-disk targets...
            # So we consider only the targets from the default handler can be
            # represented as Path.
            if not target.is_absolute():
                target = self._workdir / target
            resolved_without_suffix = target.resolve().as_posix()
            return ResolvedTargetID(
                resolved_without_suffix
                + self._target_handlers_bundle.default_target_handler.DISCRIMINANT_SUFFIX
            )

        else:
            resolved, _ = self._target_handlers_bundle.resolve_target(
                target, self._config, workdir=self._entrypoint_dir
            )
            return resolved

    def list_targets(self) -> List[Tuple[str, ResolvedTargetID]]:
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        targets = []
        for rule in self._rules.values():
            targets += list(zip(rule.outputs, rule.resolved_outputs))

        return targets

    def dump_graph(
        self,
        target: Optional[Union[str, Path]] = None,
        display_resolved: bool = False,
    ) -> str:
        """
        Graph example:
            a.out#
            ├─rule:link_c
            ├─config:linkflags
            ├─x.o#
            │ ├─rule:compile_c
            │ ├─config:cflags
            │ ├─x.c#
            │ └─headers/
            │   ├─rule:generate_headers
            │   └─config:headers_config
            └─y.o#
              ├─rule:compile_c
              ├─config:cflags
              ├─y.c#
              └─headers/
                ├─rule:generate_headers
                └─…
        """
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        if target is not None:
            resolved = self.resolve_target(target)
        else:
            resolved = None

        return dump_graph(
            rules=list(self._rules.values()),
            target_filter=resolved,
            display_resolved=display_resolved,
        )
