import pytest

from .._target import FileTargetHandler
from .._exceptions import IsengardConsistencyError
from .._collector import Collector
from .._rule import Rule


@pytest.fixture
def collector():
    return Collector(target_handlers=[FileTargetHandler()])


@pytest.fixture
def rule():
    return Rule(
        fn=lambda output, inputs, cc, cflags: None,
        id="compile_x",
        output="x.o#",
        inputs=["x.c#", "{gen_dir}/config.h#"],
    )


@pytest.fixture
def config():
    return {"cc": "clang", "cflags": ("-O2", "-std=c99"), "gen_dir": "generated/"}



def test_ok(collector, rule, config):
    collector.add_rule(rule)
    config.pop("cflags")
    collector.add_lazy_config("cflags", lambda: None)
    collector.add_lazy_config("ldflags", lambda cflags, cc: None)

    def lazy_rule_gen(register_rule):
        @register_rule(output="foo.so", input="foo.o", id="linkstuff")
        def whatever(output, input, ldflags, cc):
            pass

    collector.add_lazy_rule("lazy_rule_gen", lazy_rule_gen)

    def lazy_rule_gen_multiple(register_rule, cc):
        assert cc == config["cc"]

        @register_rule(outputs=["foo.c", "foo_api.h"], inputs=["foo.pyx", "bar.pyi"])
        def generate_foo_c(outputs, inputs):
            pass

        @register_rule(outputs=["foo.o"], inputs=["foo.c"])
        def compile_foo_c(outputs, inputs, cc, cflags):
            pass

    collector.add_lazy_rule("lazy_rule_gen_multiple", lazy_rule_gen_multiple)

    resolved_rules = collector.configure(**config)
    assert resolved_rules.keys() == {
        'compile_x',
        'linkstuff',
        "lazy_rule_gen_multiple::generate_foo_c",
        "lazy_rule_gen_multiple::compile_foo_c",
    }


@pytest.mark.parametrize("kind", ["same_rule", "same_id"])
def test_rule_duplication(collector, rule, config, kind):
    collector.add_rule(rule)

    if kind == "same_rule":
        collector.add_rule(rule)
    else:
        assert kind == "same_id"
        rule2 = Rule(
            fn=lambda output: None,
            id=rule.id,
            output="whatever#",
        )
        collector.add_rule(rule2)

    with pytest.raises(IsengardConsistencyError):
        collector.configure(**config)


@pytest.mark.parametrize("kind", ["same_rule", "same_id"])
def test_lazy_rule_duplication(collector, kind):
    def genrule(register_rule):
        pass
    collector.add_lazy_rule("genrule", genrule)

    if kind == "same_rule":
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_rule("genrule", genrule)

    else:
        assert kind == "same_id"
        def genrule2(register_rule):
            pass
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_rule("genrule", genrule2)


def test_lazy_rule_same_fn_different_ids(collector):
    def genrule(register_rule):
        pass
    collector.add_lazy_rule("genrule", genrule)
    collector.add_lazy_rule("genrule2", genrule)
    collector.configure()


@pytest.mark.parametrize("kind", ["same_rule", "same_id", "with_non_lazy_rule"])
def test_lazy_rule_generate_rule_duplication(collector, kind):
    def genrule(register_rule):
        @register_rule(output="foo")
        def my_rule(output):
            pass
    collector.add_lazy_rule("genrule", genrule)

    if kind == "same_rule":
        collector.add_lazy_rule("genrule2", genrule)

    elif kind == "same_id":
        def genrule2(register_rule):
            @register_rule(output="foo", id="genrule::my_rule")
            def whatever(output):
                pass
        collector.add_lazy_rule("genrule2", genrule2)

    else:
        assert kind == "with_non_lazy_rule"
        rule2 = Rule(
            fn=lambda output: None,
            id="genrule::my_rule",
            output="whatever#",
        )
        collector.add_rule(rule2)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


def test_lazy_rule_missing_register_rule_param(collector):
    def genrule():
        pass

    collector.add_lazy_rule("genrule", genrule)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


@pytest.mark.parametrize("kind", ["same_fn", "same_id"])
def test_lazy_config_duplication(collector, kind):
    def genconfig():
        pass

    collector.add_lazy_config("genconfig", genconfig)

    if kind == "same_fn":
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_config("genconfig", genconfig)
    elif kind == "same_id":
        def genconfig2():
            pass
        with pytest.raises(IsengardConsistencyError):
            collector.add_lazy_config("genconfig", genconfig2)



def test_lazy_config_duplication_with_regular_config(collector):
    def foo():
        pass

    collector.add_lazy_config("foo", foo)

    with pytest.raises(IsengardConsistencyError):
        collector.configure(foo=42)


def test_missing_config(collector, rule, config):
    collector.add_rule(rule)

    config.pop("cc")

    with pytest.raises(IsengardConsistencyError):
        collector.configure(**config)
