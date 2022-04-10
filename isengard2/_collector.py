from typing import Optional, List, Callable, Tuple, Any, Set, Dict

from ._const import ConstTypes
from ._exceptions import IsengardConsistencyError
from ._rule import Rule, ResolvedRule, extract_params_from_signature, INPUT_OUTPUT_CONFIG_NAMES
from ._target import BaseTargetHandler


RuleFn = Callable[..., Any]


class Collector:
    def __init__(self, target_handlers: List[BaseTargetHandler]):
        self.target_handlers = target_handlers
        self.rules: List[Rule] = []
        self.lazy_rules: List[Tuple[str, Callable, Set[str]]] = []
        self.lazy_configs: List[Tuple[str, Callable, Set[str]]] = []

    def add_rule(
        self,
        rule: Rule,
    ):
        self.rules.append(rule)

    def add_lazy_rule(
        self,
        fn: Callable,
        id: Optional[str] = None,
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn)
        id = id or f"{fn.__module__}.{fn.__name__}"
        self.lazy_rules.append((id, fn, params))

    def add_lazy_config(
        self,
        fn: Callable,
        id: Optional[str] = None,
    ):
        # Extract params early to provide better error report
        params = extract_params_from_signature(fn)
        id = id or fn.__name__
        self.lazy_configs.append((id, fn, params))

    def configure(self, **config: ConstTypes) -> List[ResolvedRule]:
        # First, resolve lazy config
        to_run = self.lazy_configs
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
                    if id in config:
                        # Look if the name clash comes from another lazy config...
                        other: Any = next((candidate_fn for candidate_id, candidate_fn, _ in self.lazy_configs if candidate_id == id), None)
                        if not other or other is fn:
                            other = config[id] 
                        raise IsengardConsistencyError(
                            f"Config `{id}` is defined multiple times: {fn} and {other}"
                        )
                    config[id] = fn(**lc_kwargs)

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
                to_run = cannot_run_yet
                cannot_run_yet = []

        # Now we can resolve the lazy rules
        rules = self.rules.copy()

        def register_rule(**kwargs):
            def wrapper(fn):
                rules.append(Rule(fn, **kwargs))
                return fn
            return wrapper

        for id, fn, params in self.lazy_rules:
            lr_kwargs: Dict[str, Any] = {"register_rule": register_rule}
            if "register_rule" not in params:
                raise IsengardConsistencyError(
                    f"Lazy rule `{id}` is missing mandatory `register_rule` parameter"
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
                        f"Lazy rule `{id}` contains unknown config item(s) {missings}"
                    )
            fn(**lr_kwargs)

        # Finally resolve inputs/outputs and check config params in each rule
        allowed_params = INPUT_OUTPUT_CONFIG_NAMES | config.keys()
        resolved_rules = []
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

            resolved_rules.append(ResolvedRule(
                id=rule.id,
                fn=rule.fn,
                params=rule.params,
                outputs=rule.outputs,
                inputs=rule.inputs,
                resolved_outputs=resolved_outputs, resolved_inputs=resolved_inputs
            ))

        # All set !
        return resolved_rules
