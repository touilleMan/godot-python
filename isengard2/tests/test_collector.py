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
    collector.add_lazy_config(lambda: None, id="cflags")
    collector.add_lazy_config(lambda cflags, cc: None, id="ldflags")

    def lazy_rule_gen(register_rule):
        @register_rule(output="foo.so", input="foo.o")
        def linkstuff(output, input, ldflags, cc):
            pass

    collector.add_lazy_rule(lazy_rule_gen)

    def lazy_rule_gen_multiple(register_rule, cc):
        assert cc == config["cc"]

        @register_rule(outputs=["foo.c", "foo_api.h"], inputs=["foo.pyx", "bar.pyi"])
        def linkstuff(outputs, inputs):
            pass

        @register_rule(outputs=["foo.o"], inputs=["foo.c"])
        def linkstuff(outputs, inputs, cc, cflags):
            pass

    collector.add_lazy_rule(lazy_rule_gen_multiple)

    collector.configure(**config)


def test_rule_duplication(collector, rule, config):
    collector.add_rule(rule)
    collector.add_rule(rule)

    with pytest.raises(IsengardConsistencyError):
        collector.configure(**config)


def test_lazy_rule_duplication(collector):
    def genrule(register_rule):
        @register_rule(output="foo")
        def my_rule(output):
            pass

    collector.add_lazy_rule(genrule)
    collector.add_lazy_rule(genrule)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


def test_lazy_rule_missing_register_rule_param(collector):
    def genrule():
        pass

    collector.add_lazy_rule(genrule)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


def test_lazy_config_duplication(collector):
    def genconfig():
        pass

    collector.add_lazy_config(genconfig)
    collector.add_lazy_config(genconfig)

    with pytest.raises(IsengardConsistencyError):
        collector.configure()


def test_lazy_config_duplication_with_regular_config(collector):
    def foo():
        pass

    collector.add_lazy_config(foo)

    with pytest.raises(IsengardConsistencyError):
        collector.configure(foo=42)


def test_missing_config(collector, rule, config):
    collector.add_rule(rule)

    config.pop("cc")

    with pytest.raises(IsengardConsistencyError):
        collector.configure(**config)
