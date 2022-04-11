from typing import Optional, List, Callable, Sequence, Tuple, Any, Set, Dict, Iterable

from ._const import ConstTypes
from ._exceptions import IsengardConsistencyError
from ._rule import Rule, ResolvedRule, extract_params_from_signature, INPUT_OUTPUT_CONFIG_NAMES
from ._target import BaseTargetHandler


RuleFn = Callable[..., Any]


class Collector:
    def __init__(self, target_handlers: List[BaseTargetHandler]):
        self.target_handlers = target_handlers
        self.rules: List[Rule] = []
        # <id>: (<id>, <fn>, <fn params>)
        self.lazy_rules: Dict[str, Tuple[str, Callable, Set[str]]] = {}
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
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn)
        value = (id, fn, params)
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
        cannot_run_yet = []
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
                    setted = config.setdefault(id, value)
                    if setted is not value:
                        # Lazy config IDs are check when added, hence the only possible
                        # clash is between a lazy config and a regular config
                        raise IsengardConsistencyError(
                            f"Config `{id}` is defined multiple times: {fn} and {config[id]!r}"
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

        for lazy_rule_id, fn, params in self.lazy_rules.values():

            def register_rule(id=None, **kwargs):
                def wrapper(fn):
                    nonlocal id
                    id = id or f"{lazy_rule_id}::{fn.__name__}"
                    rules.append(Rule(fn, id=id, **kwargs))
                    return fn
                return wrapper

            lr_kwargs: Dict[str, Any] = {"register_rule": register_rule}
            if "register_rule" not in params:
                raise IsengardConsistencyError(
                    f"Lazy rule `{lazy_rule_id}` is missing mandatory `register_rule` parameter"
                )

            for k in params:
                try:
                    lr_kwargs[k] = config[k]
                except KeyError:
                    if k == "register_rule":
                        continue
                    missings = "/".join(
                        f"`{x}`" for x in params - config.keys()
                    )
                    raise IsengardConsistencyError(
                        f"Lazy rule `{lazy_rule_id}` contains unknown config item(s) {missings}"
                    )

            fn(**lr_kwargs)

        # Finally resolve inputs/outputs and check config params in each rule
        allowed_params = INPUT_OUTPUT_CONFIG_NAMES | config.keys()
        resolved_rules: Dict[str, ResolvedRule] = {}
        target_to_rule: Dict[str, str] = {}
        for rule in rules:
            resolved_inputs = []
            for target in rule.inputs:
                try:
                    resolved_inputs.append(target.format(**config))
                except KeyError as exc:
                    raise IsengardConsistencyError(
                        f"Invalid rule `{rule.id}`: input target `{target}` contains unknown configuration `{exc.args[0]}`"
                    )

            resolved_outputs = []
            for target in rule.outputs:
                try:
                    resolved_outputs.append(target.format(**config))
                except KeyError as exc:
                    raise IsengardConsistencyError(
                        f"Invalid rule `{rule.id}`: output target `{target}` contains unknown configuration `{exc.args[0]}`"
                    )
                if target in target_to_rule:
                    raise IsengardConsistencyError(
                        f"Multiple rules to produce `{target}`: `{rule.id}` and `{target_to_rule[target]}`"
                    )
                target_to_rule[target] = rule.id

            missings = "/".join(
                f"`{x}`" for x in rule.params - allowed_params
            )
            if missings:
                raise IsengardConsistencyError(
                    f"Rule `{rule.id}` contains unknown config item(s) {missings}"
                )

            resolved_rule = ResolvedRule(
                id=rule.id,
                fn=rule.fn,
                params=rule.params,
                outputs=rule.outputs,
                inputs=rule.inputs,
                resolved_outputs=resolved_outputs, resolved_inputs=resolved_inputs
            )
            setted = resolved_rules.setdefault(rule.id, resolved_rule)
            if setted is not resolved_rule:
                raise IsengardConsistencyError(f"Multiple rules have the same ID `{rule.id}`: {setted} and {resolved_rule}")

        # All set !
        return resolved_rules
