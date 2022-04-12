from typing import Optional, List, Callable, Sequence, Tuple, Any, Set, Dict, Iterable
from pathlib import Path

from ._const import ConstTypes
from ._exceptions import IsengardConsistencyError
from ._rule import Rule, ResolvedRule, extract_params_from_signature, INPUT_OUTPUT_CONFIG_NAMES
from ._target import TargetHandlersBundle, ResolvedTargetID


RuleFn = Callable[..., Any]


class Collector:
    def __init__(self, target_handlers: TargetHandlersBundle):
        self.target_handlers = target_handlers
        self.rules: List[Rule] = []
        # <id>: (<id>, <fn>, <fn params>, <workdir>)
        self.lazy_rules: Dict[str, Tuple[str, Callable, Set[str], Path]] = {}
        # <id>: (<id>, <fn>, <fn params>)
        self.lazy_configs: Dict[str, Tuple[str, Callable, Set[str]]] = {}

    def add_rule(
        self,
        rule: Rule,
    ):
        # Don't check for `rule.id` unicity given lazy rules are not generated yet
        self.rules.append(rule)

    def add_lazy_rule(
        self,
        id: str,
        fn: Callable,
        workdir: Path,
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn)
        # By removing the mandatory `register_rule` param, we obtain the needed configs
        try:
            params.remove("register_rule")
        except KeyError:
            raise IsengardConsistencyError(
                f"Lazy rule `{id}` is missing mandatory `register_rule` parameter"
            )
        value = (id, fn, params, workdir)
        setted = self.lazy_rules.setdefault(id, value)
        if setted is not value:
            raise IsengardConsistencyError(f"Multiple lazy rules have the same ID `{id}`: {setted[0]} and {fn}")

    def add_lazy_config(
        self,
        id: str,
        fn: Callable,
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn)
        value = (id, fn, params)
        setted = self.lazy_configs.setdefault(id, value)
        if setted is not value:
            raise IsengardConsistencyError(f"Multiple lazy rules have the same ID `{id}`: {setted[0]} and {fn}")

    def configure(self, **config: ConstTypes) -> Dict[str, ResolvedRule]:
        # First, resolve lazy config
        to_run = self.lazy_configs.values()
        cannot_run_yet: List[Tuple[str, Callable, Set[str]]] = []
        while to_run:
            for id, fn, params in to_run:
                lc_kwargs = {}
                for k in params:
                    try:
                        lc_kwargs[k] = config[k]
                    except KeyError:
                        cannot_run_yet.append((id, fn, params))
                        break
                else:
                    value = fn(**lc_kwargs)
                    c_setted = config.setdefault(id, value)
                    if c_setted is not value:
                        # Lazy config IDs are check when added, hence the only possible
                        # clash is between a lazy config and a regular config
                        raise IsengardConsistencyError(
                            f"Config `{id}` is defined multiple times: {fn} and {c_setted!r}"
                        )

            if to_run == cannot_run_yet:
                # Unknown config or recursive dependency between two lazy configs
                errors = []
                for id, fn, params in cannot_run_yet:
                    missings = "/".join(
                        f"`{x}`" for x in params - config.keys()
                    )
                    if missings:
                        errors.append(
                            f"Lazy config `{id}` contains unknown config item(s) {missings}"
                        )
                raise IsengardConsistencyError(f"Invalid lazy configs: {', '.join(errors)}")
            else:
                to_run = cannot_run_yet  # type: ignore
                cannot_run_yet = []

        # Now we can resolve the lazy rules
        rules = self.rules.copy()

        for lr_id, lr_fn, lr_needed_config, lr_workdir in self.lazy_rules.values():

            def register_rule(**kwargs):
                def wrapper(fn):
                    kwargs.setdefault("id", f"{lr_id}::{fn.__name__}")
                    kwargs.setdefault("workdir", lr_workdir)
                    kwargs["extra_config"] = lr_needed_config
                    kwargs["fn"] = fn
                    rules.append(Rule(**kwargs))
                    return fn
                return wrapper

            lr_kwargs: Dict[str, Any] = {"register_rule": register_rule}
            for k in lr_needed_config:
                try:
                    lr_kwargs[k] = config[k]
                except KeyError:
                    missings = "/".join(
                        f"`{x}`" for x in lr_needed_config - config.keys()
                    )
                    raise IsengardConsistencyError(
                        f"Lazy rule `{lr_id}` contains unknown config item(s) {missings}"
                    )

            lr_fn(**lr_kwargs)

        # Finally resolve inputs/outputs and check config params in each rule
        allowed_params = INPUT_OUTPUT_CONFIG_NAMES | config.keys()
        resolved_rules: Dict[str, ResolvedRule] = {}
        target_to_rule: Dict[str, str] = {}
        for rule in rules:
            resolved_inputs: List[ResolvedTargetID] = []
            for ri_target in rule.inputs:
                resolved_inputs.append(self.target_handlers.resolve_target(ri_target, config, rule.workdir)[0])

            resolved_outputs: List[ResolvedTargetID] = []
            for ro_target in rule.outputs:
                resolved_outputs.append(self.target_handlers.resolve_target(ro_target, config, rule.workdir)[0])
                if ro_target in target_to_rule:
                    raise IsengardConsistencyError(
                        f"Multiple rules to produce `{ro_target}`: `{rule.id}` and `{target_to_rule[ro_target]}`"
                    )
                target_to_rule[ro_target] = rule.id

            missings = "/".join(
                f"`{x}`" for x in rule.params - allowed_params
            )
            if missings:
                raise IsengardConsistencyError(
                    f"Rule `{rule.id}` contains unknown config item(s) {missings}"
                )

            resolved_rule = ResolvedRule(
                workdir=rule.workdir,
                id=rule.id,
                fn=rule.fn,
                params=rule.params,
                outputs=rule.outputs,
                inputs=rule.inputs,
                resolved_outputs=resolved_outputs,
                resolved_inputs=resolved_inputs,
            )
            r_setted = resolved_rules.setdefault(rule.id, resolved_rule)
            if r_setted is not resolved_rule:
                raise IsengardConsistencyError(f"Multiple rules have the same ID `{rule.id}`: {r_setted!r} and {resolved_rule!r}")

        # All set !
        return resolved_rules
