from typing import Callable, List, Set

from ._target import Target


_INPUT_OUTPUT_CONFIG_NAMES = {"inputs", "input", "outputs", "output"}


class Rule:
    __slots__ = (
        "name",
        "fn_params",
        "outputs",
        "inputs",
        "fn",
    )

    def __init__(
        self,
        name: str,
        fn_params: Set[str],
        outputs: List[Target],
        inputs: List[Target],
        fn: Callable,
    ):
        self.name = name
        self.fn_params = fn_params
        self.outputs = outputs
        self.inputs = inputs
        self.fn = fn

    @property
    def needed_config(self) -> Set[str]:
        return set(self.fn_params) - _INPUT_OUTPUT_CONFIG_NAMES

    def __repr__(self):
        return f"<Rule {self.name}>"
