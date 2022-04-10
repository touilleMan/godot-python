from typing import Callable, Set, Optional, Sequence, TypeVar, List
import inspect


INPUT_OUTPUT_CONFIG_NAMES = {"inputs", "input", "outputs", "output"}
C = TypeVar("C", bound=Callable[..., None])


def extract_params_from_signature(fn: Callable) -> Set[str]:
    params = set()
    signature = inspect.signature(fn)
    for param in signature.parameters.values():
        if param.default is not param.empty:
            raise TypeError(f"Default value to parameters not allowed")
        if param.kind == param.VAR_POSITIONAL:
            raise TypeError(f"*args parameter not allowed")
        if param.kind == param.VAR_KEYWORD:
            raise TypeError(f"**kwargs parameter not allowed")
        params.add(param.name)
    return params


class Rule:
    __slots__ = (
        "id",
        "outputs",
        "inputs",
        "fn",
        "params",
    )

    def __init__(
        self,
        fn: Callable,
        outputs: Optional[Sequence[str]] = None,
        output: Optional[str] = None,
        inputs: Optional[Sequence[str]] = None,
        input: Optional[str] = None,
        id: Optional[str] = None,
    ):
        params = extract_params_from_signature(fn)

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

        self.id = id or f"{fn.__module__}.{fn.__name__}"
        self.outputs = outputs
        self.inputs = inputs
        self.fn = fn
        self.params = params

    @property
    def needed_config(self) -> Set[str]:
        return self.params - INPUT_OUTPUT_CONFIG_NAMES

    def __repr__(self):
        return f"<{type(self).__name__} {self.id}>"


class ResolvedRule(Rule):
    __slots__ = (
        "resolved_outputs",
        "resolved_inputs",
    )

    def __init__(
        self,
        id: str,
        fn: Callable,
        params: Set[str],
        outputs: List[str],
        inputs: List[str],
        resolved_outputs: List[str],
        resolved_inputs: List[str],
    ):
        self.id = id
        self.fn = fn
        self.params = params
        self.outputs = outputs
        self.inputs = inputs
        self.resolved_outputs = resolved_outputs
        self.resolved_inputs = resolved_inputs
