import pytest
from pathlib import Path

from .._rule import Rule


@pytest.mark.parametrize(
    "kwargs",
    [
        # Name not matching
        {"output": "foo", "fn": lambda outputs: None},
        {"outputs": ["foo", "spam"], "fn": lambda output: None},
        {"output": "foo", "input": "bar", "fn": lambda output, inputs: None},
        {"output": "foo", "inputs": ["bar", "spam"], "fn": lambda output, input: None},
        # Clashing params
        {"output": "foo", "outputs": ["foo", "bar"], "fn": lambda output, outputs: None},
        {"input": "foo", "inputs": ["foo", "bar"], "fn": lambda input, inputs: None},
        # Output or outputs is mandatory
        {"fn": lambda: None},
        {"fn": lambda output: None},
        {"fn": lambda outputs: None},
        # Outputs cannot be empty
        {"outputs": [], "fn": lambda outputs: None},
        # defauld/args/kwargs not allowed in fn
        {"output": "foo", "fn": lambda *args, output: None},
        {"output": "foo", "fn": lambda output, **kwargs: None},
        {"output": "foo", "fn": lambda output=42: None},
    ],
)
def test_bad_init(kwargs):
    with pytest.raises(TypeError):
        Rule(**kwargs)


def test_good_init():
    rule = Rule(
        id="good_rule",
        fn=lambda outputs, input, conf1, conf2: None,
        outputs=["foo", "bar"],
        input="spam",
        workdir=Path("/foo/bar"),
    )
    assert rule.id == "good_rule"
    assert rule.needed_config == {"conf1", "conf2"}
    assert rule.outputs == ["foo", "bar"]
    assert rule.inputs == ["spam"]

    def rule_fn(output, inputs):
        pass

    rule = Rule(
        fn=rule_fn,
        output="spam",
        inputs=["foo", "bar"],
        workdir=Path("/foo/bar"),
    )
    assert rule.id == "rule_fn"
    assert rule.needed_config == set()
    assert rule.outputs == ["spam"]
    assert rule.inputs == ["foo", "bar"]


def test_rule_with_extra_config():
    rule = Rule(
        fn=lambda output, a: a + 1,
        workdir=Path("/foo/bar"),
        output="foo",
        extra_config={"b", "c"},
    )

    assert rule.needed_config == {"a", "b", "c"}
    assert rule.fn(output=None, a=41, b=2, c=3) == 42
