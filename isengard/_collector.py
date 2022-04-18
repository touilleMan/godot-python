from typing import Optional, List, Callable, Sequence, Tuple, Any, Set, Dict, Iterable
from pathlib import Path

from ._const import ConstTypes
from ._exceptions import IsengardConsistencyError
from ._rule import (
    Rule,
    ConfiguredRule,
    extract_params_from_signature,
    RULE_RESERVED_PARAMS,
    LAZY_RULE_RESERVED_REGISTER_PARAM,
)
from ._target import TargetHandlersBundle, ConfiguredTargetID


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

    # TODO: unique ID really needed for this ?
    def add_lazy_rule(
        self,
        id: str,
        fn: Callable,
        workdir: Path,
        kwargs_params: Set[str] = set(),
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn) | kwargs_params
        # By removing the mandatory register rule callback param, we obtain the needed configs
        try:
            params.remove(LAZY_RULE_RESERVED_REGISTER_PARAM)
        except KeyError:
            raise IsengardConsistencyError(
                f"Lazy rule `{id}` is missing mandatory `{LAZY_RULE_RESERVED_REGISTER_PARAM}` parameter"
            )
        value = (id, fn, params, workdir)
        setted = self.lazy_rules.setdefault(id, value)
        if setted is not value:
            raise IsengardConsistencyError(
                f"Multiple lazy rules have the same ID `{id}`: {setted[0]} and {fn}"
            )

    def add_lazy_config(
        self,
        id: str,
        fn: Callable,
        kwargs_params: Set[str] = set(),
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn) | kwargs_params
        value = (id, fn, params)
        setted = self.lazy_configs.setdefault(id, value)
        if setted is not value:
            raise IsengardConsistencyError(
                f"Multiple lazy rules have the same ID `{id}`: {setted[0]} and {fn}"
            )

    def configure(
        self, **config: ConstTypes
    ) -> Tuple[Dict[str, ConfiguredRule], Dict[str, ConstTypes]]:
        """
        Returns: ({<rule_id>: <rule>}, {<config_id>: <config_value>}
        """
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
                    missings = "/".join(f"`{x}`" for x in params - config.keys())
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
                    missings = "/".join(f"`{x}`" for x in lr_needed_config - config.keys())
                    raise IsengardConsistencyError(
                        f"Lazy rule `{lr_id}` contains unknown config item(s) {missings}"
                    )

            lr_fn(**lr_kwargs)

        # Finally resolve inputs/outputs and check config params in each rule
        allowed_params = RULE_RESERVED_PARAMS | config.keys()
        configured_rules: Dict[str, ConfiguredRule] = {}
        target_to_rule: Dict[str, str] = {}
        for rule in rules:
            configured_inputs: List[ConfiguredTargetID] = []
            for ri_target in rule.inputs:
                configured_inputs.append(
                    self.target_handlers.configure_target(ri_target, config, rule.workdir)[0]
                )

            configured_outputs: List[ConfiguredTargetID] = []
            for ro_target in rule.outputs:
                configured_outputs.append(
                    self.target_handlers.configure_target(ro_target, config, rule.workdir)[0]
                )
                if ro_target in target_to_rule:
                    raise IsengardConsistencyError(
                        f"Multiple rules to produce `{ro_target}`: `{rule.id}` and `{target_to_rule[ro_target]}`"
                    )
                target_to_rule[ro_target] = rule.id

            missings = "/".join(f"`{x}`" for x in rule.params - allowed_params)
            if missings:
                raise IsengardConsistencyError(
                    f"Rule `{rule.id}` contains unknown config item(s) {missings}"
                )

            configured_rule = ConfiguredRule(
                workdir=rule.workdir,
                id=rule.id,
                fn=rule.fn,
                params=rule.params,
                outputs=rule.outputs,
                inputs=rule.inputs,
                configured_outputs=configured_outputs,
                configured_inputs=configured_inputs,
            )
            r_setted = configured_rules.setdefault(rule.id, configured_rule)
            if r_setted is not configured_rule:
                raise IsengardConsistencyError(
                    f"Multiple rules have the same ID `{rule.id}`: {r_setted!r} and {configured_rule!r}"
                )

        # All set !
        return configured_rules, config
