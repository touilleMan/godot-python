from typing import Optional, List, Set, Dict

from ._rule import ConfiguredRule
from ._target import ConfiguredTargetID


def dump_graph(
    rules: List[ConfiguredRule],
    target_filter: Optional[ConfiguredTargetID] = None,
    display_configured: bool = False,
) -> str:
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
    target_to_rule: Dict[ConfiguredTargetID, ConfiguredRule] = {}
    for rule in rules:
        for output in rule.configured_outputs:
            target_to_rule[output] = rule

    if target_filter and target_filter not in target_to_rule:
        raise RuntimeError(f"No rule has target `{target_filter}` as output !")

    # Order rules by dependencies
    to_order = rules.copy()
    ordered_rules: List[ConfiguredRule] = []
    while to_order:
        to_order_rule = to_order.pop()
        if not ordered_rules:
            ordered_rules.append(to_order_rule)
        else:
            to_order_rule_configured_outputs = set(to_order_rule.configured_outputs)
            for i, ordered_rule in enumerate(ordered_rules):
                if to_order_rule_configured_outputs & set(ordered_rule.configured_inputs):
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
    already_dumped_rules: Set[ConfiguredRule] = set()
    already_dumped_targets: Set[str] = set()

    def _multilines_paste(depend: str, next_line_suffix: str) -> str:
        first_line, *next_lines = depend.splitlines()
        dump = f"{first_line}\n"
        for next_line in next_lines:
            dump += next_line_suffix
            dump += next_line
            dump += "\n"
        return dump

    def _dump_rule(rule: ConfiguredRule) -> str:
        depends = [f"─rule:{rule.id}"]
        if rule in already_dumped_rules:
            depends.append("…")

        else:
            already_dumped_rules.add(rule)

            if rule.needed_config:
                depends.append("─configs:" + ", ".join(sorted(rule.needed_config)))
            for input, configured_input in zip(rule.inputs, rule.configured_inputs):
                if display_configured:
                    depend_target = configured_input
                else:
                    depend_target = input

                target_rule = target_to_rule.get(configured_input)
                if target_rule:
                    already_dumped_targets.add(configured_input)
                    depend_target += "\n"
                    depend_target += _dump_rule(target_rule)
                depends.append(depend_target)

        dump = ""
        *all_but_last_depends, last_depend = depends
        for depend in all_but_last_depends:
            dump += "├─"
            dump += _multilines_paste(depend, next_line_suffix="│ ")
        dump += "└─"
        dump += _multilines_paste(last_depend, next_line_suffix="  ")
        return dump

    # Special case if we want to dump a single target
    if target_filter:
        filtered_ordered_rules: List[ConfiguredRule] = []
        for rule in reversed(ordered_rules):
            for target in rule.configured_outputs:
                if target == target_filter:
                    already_dumped_targets |= {
                        x for x in rule.configured_outputs if x != target_filter
                    }
                    filtered_ordered_rules.append(rule)
        ordered_rules = filtered_ordered_rules

    for rule in reversed(ordered_rules):
        should_dump_rule = False
        for output, configured_output in zip(rule.outputs, rule.configured_outputs):
            if configured_output not in already_dumped_targets:
                if display_configured:
                    graph += configured_output
                else:
                    graph += output
                graph += "\n"
                should_dump_rule = True
                already_dumped_targets.add(configured_output)
        if should_dump_rule:
            graph += _dump_rule(rule)

    return graph
