from contextvars import ContextVar
from pathlib import Path
from typing import Dict, List, Set, Callable, Union, Optional, Any, Union, TypeVar, Type
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
        self._target_to_rule: Dict[Target, Rule] = {}
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

    def subdir(self, subdir: str, filename: Optional[str] = None) -> None:
        previous_workdir = self._workdir
        token = _parent.set(self)
        try:
            # Temporary self modification is not a very clean approach
            # but at least it's fast&simple ;-)
            self._workdir /= subdir
            subscript_path = self._workdir / (filename or self._subdir_default_filename)

            # TODO: find the best way to do that...

            # import importlib.util
            # spec = importlib.util.spec_from_file_location(subscript_path, subscript_path)
            # mod = importlib.util.module_from_spec(spec)
            # spec.loader.exec_module(mod)
            # foo.MyClass()

            import sys
            sys.path.insert(0, str(subscript_path.parent))
            __import__(subscript_path.name.split('.', 1)[0])
            sys.path.pop(0)

            # code = compile(subscript_path.read_text(), subscript_path, "exec")
            # exec(code)

        finally:
            self._workdir = previous_workdir
            _parent.reset(token)

    def subscript(self, subscript: Union[str, Path]) -> None:
        if not isinstance(subscript, Path):
            subscript = self._workdir / subscript

        previous_workdir = self._workdir
        token = _parent.set(self)
        try:
            # Temporary self modification is not a very clean approach
            # but at least it's fast&simple ;-)
            self._workdir = subscript.parent
            subscript_path = subscript

            import sys
            sys.path.insert(0, str(subscript_path.parent))
            __import__(subscript_path.name.split('.', 1)[0])
            sys.path.pop(0)

        finally:
            self._workdir = previous_workdir
            _parent.reset(token)

    def configure(self, **config: ConstTypes):
        """
        Note passing configuration as function arguments limit the name you can use
        (e.g. `compiler.c.flags` is not a valid name). This is intended to work
        well with dependency injection in the rule where configuration is requested
        by using it name as function argument.
        """
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
                    missings = '/'.join(f"`{x}`" for x in extract_params_from_signature(fn) - config.keys())
                    if missings:
                        errors.append(
                            f"Lazy config `{fn.__name__}` contains unknwon config item(s) {missings}"
                        )
                raise IsengardConsistencyError(
                    f"Invalid lazy config: {', '.join(errors)}"
                )
            else:
                to_run = cannot_run_yet
                cannot_run_yet = []

        self._config = config

        # Configured rules' output targets and check config
        for rule in self._rules:
            for target in rule.outputs:
                configured = target.configure(**config)
                assigned_rule = self._configured_target_to_rule.setdefault(
                    configured, rule
                )
                if assigned_rule is not rule:
                    raise IsengardConsistencyError(
                        f"Multiple rules to produce target {target!r}: {rule.name} and {assigned_rule.name}"
                    )
            for config_name in rule.needed_config:
                if config_name not in self._config:
                    raise IsengardConsistencyError(
                        f"Rule `{rule.name}` contains unknwon config item `{config_name}`"
                    )

    def lazy_config(self, fn):
        if self._config is not None:
            raise IsengardConsistencyError(
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
        outputs: Optional[List[TargetLike]] = None,
        output: Optional[TargetLike] = None,
        inputs: Optional[List[TargetLike]] = None,
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
                    raise TypeError(
                        "Cannot define both `output` and `outputs` parameters"
                    )
                else:
                    outputs = [output]
                if "output" not in fn_params or "outputs" in fn_params:
                    raise TypeError(
                        "Function must have a `output` and no `outputs` parameter"
                    )
            elif outputs is not None:
                if "outputs" not in fn_params or "output" in fn_params:
                    raise TypeError(
                        "Function must have a `outputs` and no `output` parameter"
                    )
            else:
                raise TypeError("One of `output` or `outputs` parameters is mandatory")

            if input is not None:
                if inputs is not None:
                    raise TypeError(
                        "Cannot define both `input` and `inputs` parameters"
                    )
                else:
                    inputs = [input]
                if "input" not in fn_params or "inputs" in fn_params:
                    raise TypeError(
                        "Function must have an `input` and no `inputs` parameter"
                    )
            elif inputs is not None:
                if "inputs" not in fn_params or "input" in fn_params:
                    raise TypeError(
                        "Function must have an `inputs` and no `input` parameter"
                    )
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

            for target in rule.outputs:
                existing = self._target_to_rule.setdefault(target, rule)
                if existing is not rule:
                    raise IsengardConsistencyError(
                        f"Multiple rules to make target {target}: {rule} and {existing}"
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
                configured = StablePath(target.resolve())
            else:
                configured = StablePath((self.rootdir / target).resolve())
        else:
            target = self._parse_target_like(target)
            configured = target.configure(**self._config)

        try:
            rule = self._configured_target_to_rule[configured]
        except KeyError:
            raise IsengardConsistencyError(f"No rule has target `{target!r}` as output")

        self._run(rule, [])

    def _run(self, rule: Rule, parent_rules: List[Rule]) -> None:
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

        print(f'> {rule.name}')
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
            configured = StablePath(target.absolute().resolve())
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

    def list_configured_targets(self) -> List[Union[Path, str]]:
        if self._config is None:
            raise IsengardStateError("Must call `configure` before !")

        configureds: List[Union[Path, str]] = []
        for target in self._target_to_rule.keys():
            configured = target.configure(**self._config)
            if isinstance(configured, ConfiguredVirtualTarget):
                configureds.append(f"{configured}@")
            else:
                configureds.append(configured)
        return configureds

    def dump_graph(self):
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
        # Order rules by dependencies
        to_order = self._rules.copy()
        ordered_rules = []
        while to_order:
            to_order_rule = to_order.pop()
            if not ordered_rules:
                ordered_rules.append(to_order_rule)
            else:
                for i, ordered_rule in enumerate(ordered_rules):
                    if set(to_order_rule.outputs) & set(ordered_rule.inputs):
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
                    ordered_rules.append(ordered_rule)

        graph = ""
        already_dumped_rules = set()
        already_dumped_targets = set()

        def _dump_rule(rule: Rule) -> str:
            depends = [f"─rule:{rule.name}"]
            if rule in already_dumped_rules:
                depends.append("…")

            else:
                already_dumped_rules.add(rule)

                for config_name in sorted(rule.needed_config):
                    depends.append(f"─config:{config_name}")
                for target in rule.inputs:
                    depend_target = f"{target.label}{target.discriminant}"
                    target_rule = self._target_to_rule.get(target)
                    if target_rule:
                        already_dumped_targets.add(target)
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

        for rule in reversed(ordered_rules):
            should_dump_rule = False
            for target in rule.outputs:
                if target not in already_dumped_targets:
                    graph += f"{target.label}{target.discriminant}\n"
                    should_dump_rule = True
                already_dumped_targets.add(target)
            if should_dump_rule:
                graph += _dump_rule(rule)

        return graph

    # def main(self, argv: str) -> Any:
    #     self.run(argv[1])
