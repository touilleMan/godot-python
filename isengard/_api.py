from contextvars import ContextVar
from dis import dis
from distutils.command.config import config
from multiprocessing.sharedctypes import Value
from pathlib import Path
from typing import Dict, List, Sequence, Set, Callable, Union, Optional, Any, Union, TypeVar, Type
import inspect

from ._utils import ConstTypes, validate_const_data
from ._target import (
    Target,
    VirtualTarget,
    FileTarget,
    FolderTarget,
    ConfiguredTarget,
    ConfiguredVirtualTarget,
    VirtualTargetResolver,
    StablePath,
)
from ._rule import Rule, _INPUT_OUTPUT_CONFIG_NAMES
from ._exceptions import (
    IsengardError,
    IsengardStateError,
    IsengardDefinitionError,
    IsengardConsistencyError,
    IsengardRunError,
)


C = TypeVar("C", bound=Callable[..., None])
TargetLike = Union[str, Target]


_RESERVED_CONFIG_NAMES = {
    *_INPUT_OUTPUT_CONFIG_NAMES,
    "rootdir",  # Entrypoint script's directory
    "ruledir",  # Directory of the script the current rule was defined in
}


_parent: ContextVar["Isengard"] = ContextVar("context")


def get_parent() -> "Isengard":
    try:
        return _parent.get()
    except LookupError as exc:
        raise IsengardError("Not in a subdir !") from exc


def extract_params_from_signature(fn: Callable) -> Set[str]:
    config = set()
    signature = inspect.signature(fn)
    for param in signature.parameters.values():
        if not param.empty:
            raise TypeError(f"Default value to parameters not allowed")
        if param.kind == param.VAR_POSITIONAL:
            raise TypeError(f"*args parameter not allowed")
        if param.kind == param.VAR_KEYWORD:
            raise TypeError(f"**kwargs parameter not allowed")
        config.add(param.name)
    return config


class Isengard:
    def __init__(
        self,
        self_file: Union[str, Path],
        db: Union[str, Path] = ".isengard.sqlite",
        subdir_default_filename: Optional[str] = None,
    ):
        self._default_target_cooker = FileTarget
        self._target_cookers: Dict[str, Type[Target]] = {
            "#": FileTarget,
            "/": FolderTarget,
            "@": VirtualTarget,
        }

        entrypoint_path = Path(self_file).absolute()
        self._entrypoint_dir = entrypoint_path.parent
        self._entrypoint_name = entrypoint_path.name
        self._subdir_default_filename = subdir_default_filename or self._entrypoint_name
        self._workdir = self._entrypoint_dir  # Modified when reading subdir

        self._config: Optional[Dict[str, ConstTypes]] = None
        self._rules: List[Rule] = []
        self._lazy_configs: List[Callable] = []
        # self._target_to_rule: Dict[Target, Rule] = {}
        self._configured_target_to_rule: Dict[ConfiguredTarget, Rule] = {}
        self._configured_to_executed: Dict[ConfiguredTarget, ConstTypes] = {}

        if not isinstance(db, Path):
            db = Path(db)
        if not db.is_absolute():
            db = self._entrypoint_dir / db
        self._db_path = db

    @property
    def rootdir(self):
        return self._entrypoint_dir

    def register_target_cooker(self, suffix: str, target_cls: Type[Target]):
        self._target_cookers[suffix] = target_cls

    def _load_file_as_module(self, name: str, path: Path) -> None:
        import sys
        from types import ModuleType
        from importlib.util import spec_from_file_location, module_from_spec

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
            raise IsengardDefinitionError(
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

    def configure(self, **config: ConstTypes):
        """
        Note passing configuration as function arguments limit the name you can use
        (e.g. `compiler.c.flags` is not a valid name). This is intended to work
        well with dependency injection in the rule where configuration is requested
        by using it name as function argument.
        """
        if self._config:
            raise IsengardStateError("`configure` has already been called !")

        # Check provided config
        try:
            for k, v in config.items():
                validate_const_data(v)
        except TypeError as exc:
            raise TypeError(
                f"Invalid configuration `{k}`: value must be a Path/str/bytes/int/float/bool/None or a tuple of those"
            ) from exc

        invalid_config_names = config.keys() & _INPUT_OUTPUT_CONFIG_NAMES
        if invalid_config_names:
            raise IsengardConsistencyError(
                f"Invalid config name(s): {', '.join(invalid_config_names)}"
            )

        # Resolve lazy config
        config["rootdir"] = self.rootdir
        to_run = self._lazy_configs
        cannot_run_yet = []
        while to_run:
            for fn in to_run:
                kwargs = {}
                for k in extract_params_from_signature(fn):
                    try:
                        kwargs[k] = config[k]
                    except KeyError:
                        cannot_run_yet.append(fn)
                        break
                else:
                    if fn.__name__ in config:
                        raise IsengardConsistencyError(
                            f"Config `{fn.__name__}` is defined multiple times !"
                        )
                    config[fn.__name__] = fn(**kwargs)

            if to_run == cannot_run_yet:
                # Unknown config or recursive dependency between two lazy configs
                errors = []
                for fn in cannot_run_yet:
                    missings = "/".join(
                        f"`{x}`" for x in extract_params_from_signature(fn) - config.keys()
                    )
                    if missings:
                        errors.append(
                            f"Lazy config `{fn.__name__}` contains unknwon config item(s) {missings}"
                        )
                raise IsengardConsistencyError(f"Invalid lazy config: {', '.join(errors)}")
            else:
                to_run = cannot_run_yet
                cannot_run_yet = []

        self._config = config

        # Configured rules' output targets and check config
        for rule in self._rules:
            for target in rule.outputs:
                configured = target.configure(**config)
                assigned_rule = self._configured_target_to_rule.setdefault(configured, rule)
                if assigned_rule is not rule:
                    raise IsengardConsistencyError(
                        f"Multiple rules to produce `{configured}`: `{rule.name}` and `{assigned_rule.name}`"
                    )
            for config_name in rule.needed_config:
                if config_name not in self._config:
                    raise IsengardConsistencyError(
                        f"Rule `{rule.name}` contains unknwon config item `{config_name}`"
                    )

    def lazy_config(self, fn):
        if self._config is not None:
            raise IsengardStateError(
                "Cannot create new lazy configuration value once `configure` has been called !"
            )

        if fn.__name__ in _RESERVED_CONFIG_NAMES:
            raise IsengardDefinitionError(f"Config `{fn.__name__}` is a reserved name")

        params = extract_params_from_signature(fn)
        invalid_config_names = params & _INPUT_OUTPUT_CONFIG_NAMES
        if invalid_config_names:
            raise IsengardConsistencyError(
                f"Invalid config name(s): {', '.join(invalid_config_names)}"
            )

        self._lazy_configs.append(fn)

        return fn

    def rule(
        self,
        outputs: Optional[Sequence[TargetLike]] = None,
        output: Optional[TargetLike] = None,
        inputs: Optional[Sequence[TargetLike]] = None,
        input: Optional[TargetLike] = None,
        name: Optional[str] = None,
    ) -> Callable[[C], C]:
        def wrapper(fn: C) -> C:
            nonlocal outputs, inputs

            if self._config is not None:
                raise IsengardStateError(
                    "Cannot create new rules once `configure` has been called !"
                )

            fn_params = extract_params_from_signature(fn)

            if output is not None:
                if outputs is not None:
                    raise TypeError("Cannot define both `output` and `outputs` parameters")
                else:
                    outputs = [output]
                if "output" not in fn_params or "outputs" in fn_params:
                    raise TypeError("Function must have a `output` and no `outputs` parameter")
            elif outputs is not None:
                if "outputs" not in fn_params or "output" in fn_params:
                    raise TypeError("Function must have a `outputs` and no `output` parameter")
            else:
                raise TypeError("One of `output` or `outputs` parameters is mandatory")

            if input is not None:
                if inputs is not None:
                    raise TypeError("Cannot define both `input` and `inputs` parameters")
                else:
                    inputs = [input]
                if "input" not in fn_params or "inputs" in fn_params:
                    raise TypeError("Function must have an `input` and no `inputs` parameter")
            elif inputs is not None:
                if "inputs" not in fn_params or "input" in fn_params:
                    raise TypeError("Function must have an `inputs` and no `input` parameter")
            else:
                inputs = []

            cooked_name = name or fn.__name__
            try:
                cooked_outputs = [self._parse_target_like(x) for x in outputs]
                cooked_inputs = [self._parse_target_like(x) for x in inputs]
            except TypeError as exc:
                raise IsengardConsistencyError(f"Error in rule `{cooked_name}`: {exc}") from exc

            rule = Rule(
                name=cooked_name,
                fn_params=fn_params,
                outputs=cooked_outputs,
                inputs=cooked_inputs,
                fn=fn,
            )
            self._rules.append(rule)

            return fn

        return wrapper

    def _parse_target_like(self, raw: TargetLike) -> Target:
        if isinstance(raw, Target):
            return raw
        elif isinstance(raw, str):
            try:
                target_cls = self._target_cookers[raw[-1]]
                raw = raw[:-1]
            except (KeyError, IndexError):
                target_cls = self._default_target_cooker
            return target_cls(label=raw, workdir=self._workdir)
        else:
            raise TypeError(f"Invalid target value `{raw}`, expected str or Target object")

    def run(self, target: Union[TargetLike, Path]) -> None:
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        configured: ConfiguredTarget
        if isinstance(target, Path):
            if target.is_absolute():
                configured = StablePath(target)
            else:
                configured = StablePath((self.rootdir / target))
        else:
            target = self._parse_target_like(target)
            configured = target.configure(**self._config)

        try:
            rule = self._configured_target_to_rule[configured]
        except KeyError:
            raise IsengardConsistencyError(f"No rule has target `{target!r}` as output")

        self._run(rule, [])

    def _run(self, rule: Rule, parent_rules: Sequence[Rule]) -> None:
        assert self._config is not None

        # Now we can configure input targets
        inputs: List[ConstTypes] = []
        for target in rule.inputs:
            configured = target.configure(**self._config)

            try:
                sub_rule = self._configured_target_to_rule[configured]

            except KeyError:
                if isinstance(configured, ConfiguredVirtualTarget):
                    raise IsengardConsistencyError(
                        f"No rule has target `{target!r}` as output (needed by rule `{rule.name}`)"
                    )
                else:
                    # Consider the target is a prerequisit existing on disk
                    inputs.append(configured)

            else:
                sub_parent_rules = [*parent_rules, rule]
                if sub_rule in sub_parent_rules:
                    raise IsengardConsistencyError(
                        f"Recursion detection in rules {'->'.join(r.name for r in sub_parent_rules)}"
                    )

                try:
                    executed = self._configured_to_executed[configured]
                except KeyError:
                    self._run(sub_rule, sub_parent_rules)
                    executed = self._configured_to_executed[configured]
                inputs.append(executed)

        outputs: List[Union[ConstTypes, VirtualTargetResolver]] = []
        for target in rule.outputs:
            configured = target.configure(**self._config)
            if isinstance(configured, ConfiguredVirtualTarget):
                outputs.append(VirtualTargetResolver(configured))
            else:
                outputs.append(configured)

        kwargs: Dict[str, Any] = {}
        for k in rule.fn_params:
            if k == "output":
                kwargs["output"] = outputs[0]
            elif k == "outputs":
                kwargs["outputs"] = outputs
            elif k == "input":
                kwargs["input"] = inputs[0]
            elif k == "inputs":
                kwargs["inputs"] = inputs
            else:
                kwargs[k] = self._config[k]

        print(f"> {rule.name}")
        try:
            rule.fn(**kwargs)
        except Exception as exc:
            raise IsengardRunError(f"Error in rule `{rule.name}`: {exc}") from exc

        for output in outputs:
            if isinstance(output, VirtualTargetResolver):
                self._configured_to_executed[output.configured] = output._resolved
            else:
                self._configured_to_executed[output] = output

    def clean(self, target: Union[TargetLike, Path]) -> None:
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        configured: ConfiguredTarget
        if isinstance(target, Path):
            configured = StablePath(target.absolute())
            for rule in self._rules:
                for target in rule.outputs:
                    candidate_configured = target.configure(**self._config)
                    if candidate_configured == configured:
                        break
            else:
                raise IsengardConsistencyError("No rule has target as output")

        else:
            target = self._parse_target_like(target)
            configured = target.configure(**self._config)

        target.clean(configured)

    def list_configured_targets(self) -> Sequence[Union[Path, str]]:
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        configureds: List[Union[Path, str]] = []
        for configured in self._configured_target_to_rule.keys():
            if isinstance(configured, ConfiguredVirtualTarget):
                configureds.append(f"{configured}@")
            else:
                configureds.append(configured)
        return configureds

    def _target_like_to_configured(self, target: TargetLike) -> ConfiguredTarget:
        if isinstance(target, Path):
            if target.is_absolute():
                configured = StablePath(target)
            else:
                configured = StablePath((self.rootdir / target))
        else:
            target = self._parse_target_like(target)
            configured = target.configure(**self._config)
        return configured

    def dump_graph(
        self,
        target: Optional[TargetLike] = None,
        display_configured: bool = False,
        display_relative_path: bool = False,
    ):
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

        filter_by_configured = None
        if target:
            filter_by_configured = self._target_like_to_configured(target)

        # Order rules by dependencies
        to_order = self._rules.copy()
        ordered_rules: List[Rule] = []
        while to_order:
            to_order_rule = to_order.pop()
            if not ordered_rules:
                ordered_rules.append(to_order_rule)
            else:
                to_order_rule_configured_outputs = set(
                    t.configure(**self._config) for t in to_order_rule.outputs
                )
                for i, ordered_rule in enumerate(ordered_rules):
                    if to_order_rule_configured_outputs & set(
                        t.configure(**self._config) for t in ordered_rule.inputs
                    ):
                        # `to_order_rule` is a dependency of `ordered_rule`, it must be ordered before
                        ordered_rules.insert(i, to_order_rule)
                        break
                    else:
                        # Two possibilities:
                        # 1) both rules are independants
                        # 2) `to_order_rule` depends of `ordered_rule`
                        # In both case `to_order_rule` must be ordered after `ordered_rule`.
                        # However `to_order_rule` might depend of other rules,
                        # so we can't just insert it right after `ordered_rule`.
                        continue
                else:
                    # not rule depends of `to_order_rule` so far, we can insert it last
                    ordered_rules.append(to_order_rule)

        graph = ""
        already_dumped_rules = set()
        # Different targets can lead to the same configured value, hence we
        # we use the configured value as discriminant.
        already_dumped_configured = set()

        def _dump_rule(rule: Rule) -> str:
            depends = [f"─rule:{rule.name}"]
            if rule in already_dumped_rules:
                depends.append("…")

            else:
                already_dumped_rules.add(rule)

                if rule.needed_config:
                    depends.append("─configs:" + ", ".join(sorted(rule.needed_config)))
                for target in rule.inputs:
                    configured = target.configure(**self._config)
                    if display_configured:
                        if isinstance(target, VirtualTarget):
                            depend_target = f"{target.label}{target.discriminant}"
                        else:
                            depend_target = f"{configured}{target.discriminant}"
                            if display_relative_path:
                                try:
                                    relative_configured = configured.relative_to(
                                        self._entrypoint_dir
                                    )
                                    depend_target = f"{relative_configured}{target.discriminant}"
                                except ValueError:
                                    # Configured is not relative to root dir, just keep it absolute
                                    pass
                    else:  # Display targets without configuration
                        depend_target = f"{target.label}{target.discriminant}"
                    target_rule = self._configured_target_to_rule.get(configured)
                    if target_rule:
                        already_dumped_configured.add(configured)
                        depend_target += "\n"
                        depend_target += _dump_rule(target_rule)
                    depends.append(depend_target)

            def _multilines_paste(depend: str, next_line_suffix: str) -> str:
                first_line, *next_lines = depend.splitlines()
                dump = f"{first_line}\n"
                for next_line in next_lines:
                    dump += next_line_suffix
                    dump += next_line
                    dump += "\n"
                return dump

            dump = ""
            *all_but_last_depends, last_depend = depends
            for depend in all_but_last_depends:
                dump += "├─"
                dump += _multilines_paste(depend, next_line_suffix="│ ")
            dump += "└─"
            dump += _multilines_paste(last_depend, next_line_suffix="  ")
            return dump

        if filter_by_configured:
            filtered_ordered_rules = []
            for rule in reversed(ordered_rules):
                for target in rule.outputs:
                    configured = target.configure(**self._config)
                    if configured == filter_by_configured:
                        for target_to_ignore in rule.outputs:
                            configured_to_ignore = target_to_ignore.configure(**self._config)
                            if configured_to_ignore != configured:
                                already_dumped_configured.add(configured_to_ignore)
                        filtered_ordered_rules.append(rule)
            ordered_rules = filtered_ordered_rules

        for rule in reversed(ordered_rules):
            should_dump_rule = False
            for target in rule.outputs:
                configured = target.configure(**self._config)
                if configured not in already_dumped_configured:
                    graph += f"{target.label}{target.discriminant}\n"
                    should_dump_rule = True
                    already_dumped_configured.add(configured)
            if should_dump_rule:
                graph += _dump_rule(rule)

        return graph

    # def main(self, argv: str) -> Any:
    #     self.run(argv[1])
