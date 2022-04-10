import pytest

from .._rule import Rule


@pytest.mark.parametrize("kwargs", [
    # Name not matching
    {"output": "foo", "fn": lambda outputs: None},
    {"outputs": ["foo", "spam"], "fn": lambda output: None},
    {"output": "foo", "input": "bar", "fn": lambda output, inputs: None},
    {"output": "foo", "inputs": ["bar", "spam"], "fn": lambda output, input: None},
    # Clashing params
    {"output": "foo", "outputs": ["foo", "bar"], "fn": lambda output, outputs: None},
    {"input": "foo", "inputs": ["foo", "bar"], "fn": lambda input,  inputs: None},
    # Output or outputs is mandatory
    {"fn": lambda: None},
    {"fn": lambda output: None},
    {"fn": lambda outputs: None},
    # defauld/args/kwargs not allowed in fn
    {"output": "foo", "fn": lambda *args, output: None},
    {"output": "foo", "fn": lambda output, **kwargs: None},
    {"output": "foo", "fn": lambda output=42: None},
])
def test_bad_init(kwargs):
    with pytest.raises(TypeError):
        Rule(**kwargs)


def test_good_init():
    rule = Rule(outputs=["foo", "bar"], input="spam", fn=lambda outputs, input, conf1, conf2: None, id="good_rule")
    assert rule.id == "good_rule"
    assert rule.needed_config == {"conf1", "conf2"}
    assert rule.outputs == ["foo", "bar"]
    assert rule.inputs == ["spam"]

    def rule_fn(output, inputs):
        pass
    rule_fn.__module__ = "foo.bar"
    rule = Rule(output="spam", inputs=["foo", "bar"], fn=rule_fn)
    assert rule.id == "foo.bar.rule_fn"
    assert rule.needed_config == set()
    assert rule.outputs == ["spam"]
    assert rule.inputs == ["foo", "bar"]
