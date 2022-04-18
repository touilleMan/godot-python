from typing import Callable, Set, Optional, Sequence, TypeVar, List, Dict, Any
import inspect
from pathlib import Path
from functools import wraps

from ._const import ConstTypes
from ._target import RawTargetID, ConfiguredTargetID, ConfigID


RULE_RESERVED_PARAMS = {"inputs", "input", "outputs", "output"}
LAZY_RULE_RESERVED_REGISTER_PARAM = "register_rule"
C = TypeVar("C", bound=Callable[..., None])


def extract_params_from_signature(fn: Callable) -> Set[str]:
    params = set()
    signature = inspect.signature(fn)
    for param in signature.parameters.values():
        if param.default is not param.empty:
            raise TypeError(f"Default value to parameters not allowed")
        if param.kind == param.VAR_POSITIONAL:
            raise TypeError(f"*args parameter not allowed")
        # Unlike *args, we allow **kwargs given it's useful when the rule is too
        # dynamic to know the name of the params when the callback is defined
        if param.kind == param.VAR_KEYWORD:
            continue
        params.add(param.name)
    return params


class Rule:
    __slots__ = (
        "workdir",
        "id",
        "outputs",
        "inputs",
        "fn",
        "params",
    )

    def __init__(
        self,
        workdir: Path,
        fn: Callable,
        outputs: Optional[Sequence[RawTargetID]] = None,
        output: Optional[RawTargetID] = None,
        inputs: Optional[Sequence[RawTargetID]] = None,
        input: Optional[RawTargetID] = None,
        id: Optional[str] = None,
        extra_config: Optional[Set[str]] = None,
        kwargs_params: Optional[Set[str]] = None,
    ):
        params = extract_params_from_signature(fn)
        if kwargs_params:
            params |= kwargs_params

        if output is not None:
            if outputs is not None:
                raise TypeError("Cannot define both `output` and `outputs` parameters")
            else:
                outputs = [output]
            if "output" not in params or "outputs" in params:
                raise TypeError("Function must have a `output` and no `outputs` parameter")
        elif outputs is not None:
            outputs = list(outputs)
            if "outputs" not in params or "output" in params:
                raise TypeError("Function must have a `outputs` and no `output` parameter")
        else:
            raise TypeError("One of `output` or `outputs` parameters is mandatory")

        if not outputs:
            raise TypeError(
                "Rule must output at least one target (tip: use a virtual target if you rule has no on-disk side effect)"
            )

        if input is not None:
            if inputs is not None:
                raise TypeError("Cannot define both `input` and `inputs` parameters")
            else:
                inputs = [input]
            if "input" not in params or "inputs" in params:
                raise TypeError("Function must have an `input` and no `inputs` parameter")
        elif inputs is not None:
            if "inputs" not in params or "input" in params:
                raise TypeError("Function must have an `inputs` and no `input` parameter")
            inputs = list(inputs)
        else:
            inputs = []

        # It's easy to incorrectly provide `pathlib.Path` objects as input/output
        # so we do eager type checking here to save user some tedious debugging ^^
        for output in outputs:
            if not isinstance(output, str):
                raise TypeError(f"Output values must be str, got {output!r}")
        for input in inputs:
            if not isinstance(input, str):
                raise TypeError(f"Input values must be str, got {input!r}")

        self.workdir = workdir
        self.id = id or fn.__name__
        self.outputs = outputs
        self.inputs = inputs
        self.fn = fn
        self.params = params

        # Lazy-generated rules can rely on additonal configs that is not part of the
        # function's parameters. We solve this by wrapping the function to accept
        # the additional parameters.
        if extra_config:
            extra_config -= params
            if extra_config:

                @wraps(fn)
                def fn_with_extra_params(**kwargs):
                    for k in extra_config:
                        kwargs.pop(k)
                    return fn(**kwargs)

                self.fn = fn_with_extra_params
                self.params |= extra_config

    @property
    def needed_config(self) -> Set[str]:
        return self.params - RULE_RESERVED_PARAMS

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id} fn={self.fn}>"


class ConfiguredRule(Rule):
    __slots__ = (
        "configured_outputs",
        "configured_inputs",
    )

    def __init__(
        self,
        workdir: Path,
        id: str,
        fn: Callable,
        params: Set[str],
        outputs: List[RawTargetID],
        inputs: List[RawTargetID],
        configured_outputs: List[ConfiguredTargetID],
        configured_inputs: List[ConfiguredTargetID],
    ):
        self.workdir = workdir
        self.id = id
        self.fn = fn
        self.params = params
        self.outputs = outputs
        self.inputs = inputs
        self.configured_outputs = configured_outputs
        self.configured_inputs = configured_inputs

    def run(
        self, outputs: List[Any], inputs: List[Any], config: Dict[ConfigID, ConstTypes]
    ) -> None:
        kwargs: Dict[str, Any] = {}
        for k in self.params:
            if k == "output":
                kwargs["output"] = outputs[0]
            elif k == "outputs":
                kwargs["outputs"] = outputs
            elif k == "input":
                kwargs["input"] = inputs[0]
            elif k == "inputs":
                kwargs["inputs"] = inputs
            elif k == "ruledir":  # Additional config
                kwargs[k] = self.workdir
            else:
                kwargs[k] = config[k]

        self.fn(**kwargs)
