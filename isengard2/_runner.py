from typing import List, Dict

from ._rule import ResolvedRule
from ._const import ConstTypes
from ._exceptions import IsengardRunError


class Runner:
    def __init__(self, target_to_rule: Dict[str, str], rules: List[ResolvedRule], config: Dict[str, ConstTypes]):
        self.target_to_rule = target_to_rule
        self.rules = rules
        self.config = config

    def run(self, target: str) -> None:
        pass
