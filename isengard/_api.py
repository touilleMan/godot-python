import sys
from importlib.util import spec_from_file_location, module_from_spec
from types import ModuleType
from contextvars import ContextVar
from pathlib import Path
from typing import (
    Dict,
    Tuple,
    List,
    Set,
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
    RawTargetID,
    TargetDiscriminant,
    ConfiguredTargetID,
    TargetHandlersBundle,
    BaseTargetHandler,
    FileTargetHandler,
    FolderTargetHandler,
    VirtualTargetHandler,
)
from ._collector import Collector
from ._exceptions import (
    IsengardError,
    IsengardStateError,
    IsengardConsistencyError,
)


RESERVED_CONFIG_IDS = {
    *RULE_RESERVED_PARAMS,
    LAZY_RULE_RESERVED_REGISTER_PARAM,
    "rootdir",  # Entrypoint script's directory
    "ruledir",  # Directory of the script the current rule was defined in
}


C = TypeVar("C", bound=Callable[..., None])


_parent: ContextVar["Isengard"] = ContextVar("context")


def get_parent() -> "Isengard":
    try:
        return _parent.get()
    except LookupError as exc:
        raise IsengardError("Not in a subdir !") from exc


class Isengard:

    DEFAULT_TARGET_HANDLERS = [
        FileTargetHandler(),
        FolderTargetHandler(),
        VirtualTargetHandler(),
        # Not `DeferredTargetHandler` is automatically added by the target bundle
    ]

    def __init__(
        self,
        self_file: Union[str, Path],
        db: Union[str, Path] = ".isengard.sqlite",
        subdir_default_filename: Optional[str] = None,
        target_handlers: Sequence[BaseTargetHandler] = DEFAULT_TARGET_HANDLERS,
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
        )
        self._collector = Collector(target_handlers=self._target_handlers_bundle)

        # Defined when configured is called
        self._config: Optional[Dict[str, ConstTypes]] = None
        self._runner: Optional[Runner] = None

    @property
    def rootdir(self) -> Path:
        return self._entrypoint_dir

    def _load_file_as_module(self, name: str, path: Path) -> None:
        spec = spec_from_file_location(name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[name] = module
        # Ensure the module's parents are loaded to avoid loading the wrong parent when
        # doing "import foo.bar" while only "foo.bar" is declared as helper module
        child_module = module
        parent_name = name
        while True:
            try:
                parent_name, child_name = parent_name.rsplit(".", 1)
            except ValueError:
                break
            try:
                parent_module = sys.modules[parent_name]
            except KeyError:
                parent_module = ModuleType(parent_name)
                sys.modules[parent_name] = parent_module
            setattr(parent_module, child_name, child_module)

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

    def lazy_config(self, fn: C, id: Optional[str] = None, kwargs_params: Set[str] = set()) -> C:
        if self._config is not None:
            raise IsengardStateError(
                "Cannot create new lazy configuration value once `configure` has been called !"
            )

        config_id = id or fn.__name__
        if config_id in RESERVED_CONFIG_IDS:
            raise IsengardConsistencyError(f"Config `{config_id}` is a reserved name")

        self._collector.add_lazy_config(config_id, fn, kwargs_params)

        return fn

    def lazy_rule(self, fn: C, id: Optional[str] = None, kwargs_params: Set[str] = set()) -> C:
        if self._config is not None:
            raise IsengardStateError(
                "Cannot create new lazy rule generator once `configure` has been called !"
            )

        self._collector.add_lazy_rule(id or fn.__name__, fn, self._workdir, kwargs_params)

        return fn

    def rule(
        self,
        outputs: Optional[Sequence[RawTargetID]] = None,
        output: Optional[RawTargetID] = None,
        inputs: Optional[Sequence[RawTargetID]] = None,
        input: Optional[RawTargetID] = None,
        id: Optional[str] = None,
        kwargs_params: Set[str] = set(),
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
                kwargs_params=kwargs_params,
            )
            self._collector.add_rule(rule)

            return fn

        return wrapper

    def run(self, target: Union[RawTargetID, Path]) -> bool:
        """
        Raises:
            IsengardUnknownTargetError
            IsengardConsistencyError
            IsengardRunError
        """
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        configured = self.configure_target(target)
        return self._runner.run(target=configured)

    def clean(self, target: Union[RawTargetID, Path]) -> None:
        """
        Raises:
            IsengardUnknownTargetError
            IsengardConsistencyError
            IsengardRunError
        """
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        configured = self.configure_target(target)
        self._runner.clean(configured)

    def configure_target(
        self,
        target: Union[RawTargetID, Path],
        path_discriminant: TargetDiscriminant = FileTargetHandler.DISCRIMINANT,
    ) -> ConfiguredTargetID:
        if isinstance(target, Path):
            # Identifying a target by it Path on the FS is convenient for the user,
            # but not for us given we use the `ConfiguredTargetID` instead precisely to
            # unify virtual and on-disk targets...
            # So we consider only the targets from the default handler can be
            # represented as Path.
            if not target.is_absolute():
                target = self._workdir / target
            configured_without_discriminant = target.resolve().as_posix()
            return ConfiguredTargetID(configured_without_discriminant + path_discriminant)

        else:
            configured, _ = self._target_handlers_bundle.configure_target(
                target, self._config, workdir=self._entrypoint_dir
            )
            return configured

    # TODO: it should be possible to return the list of cooked element (which is useful to
    # retreive a target from a given path) by loading previous fingerprint for deferred targets
    def list_targets(self) -> List[Tuple[RawTargetID, ConfiguredTargetID]]:
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        targets = []
        for rule in self._rules.values():
            targets += list(zip(rule.outputs, rule.configured_outputs))

        return targets

    def dump_graph(
        self,
        target: Optional[Union[RawTargetID, Path]] = None,
        display_configured: bool = False,
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
            configured = self.configure_target(target)
        else:
            configured = None

        return dump_graph(
            rules=list(self._rules.values()),
            target_filter=configured,
            display_configured=display_configured,
        )
